"""
Video Enhancement Suite - Job Queue Manager
Priority-based job queue with concurrent processing and retry logic
"""

import json
import uuid
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime
from queue import PriorityQueue
from threading import Thread, Lock
import time

try:
    from models import VideoJob, JobStatus, Priority, ProcessingResult
    from processor import VideoProcessor
except ImportError:
    from .models import VideoJob, JobStatus, Priority, ProcessingResult
    from .processor import VideoProcessor


class JobQueue:
    """
    Priority-based video processing job queue
    
    Features:
    - Priority scheduling (CRITICAL > HIGH > MEDIUM > LOW)
    - Concurrent job processing
    - Automatic retry on failure
    - Persistent queue storage
    - Real-time status tracking
    """
    
    def __init__(self, queue_file: str = "data/tmp/video_queue.json", max_workers: int = 2):
        """
        Initialize job queue
        
        Args:
            queue_file: Path to persistent queue storage
            max_workers: Maximum concurrent processing jobs
        """
        self.queue_file = Path(queue_file)
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.jobs: Dict[str, VideoJob] = {}
        self.priority_queue = PriorityQueue()
        self.max_workers = max_workers
        self.active_jobs = 0
        self.lock = Lock()
        self.processor = VideoProcessor()
        self.workers_running = False
        
        # Load existing queue
        self._load_queue()
    
    def add_job(
        self,
        input_file: str,
        output_file: str,
        preset: str,
        backend: str = "auto",
        priority: str = "medium"
    ) -> str:
        """
        Add job to queue
        
        Args:
            input_file: Input video path
            output_file: Output video path
            preset: Processing preset
            backend: Backend to use (auto/topaz/ffmpeg/handbrake)
            priority: Job priority (low/medium/high/critical)
            
        Returns:
            Job ID
        """
        from models import Backend
        
        job = VideoJob(
            job_id=str(uuid.uuid4()),
            input_file=input_file,
            output_file=output_file,
            preset=preset,
            backend=Backend(backend.lower()),
            priority=Priority[priority.upper()],
            status=JobStatus.PENDING,
            created_at=datetime.now()
        )
        
        with self.lock:
            self.jobs[job.job_id] = job
            # PriorityQueue uses (priority, item) - lower number = higher priority
            # Invert priority value so higher priority comes first
            self.priority_queue.put((-job.priority.value, job.job_id))
            self._save_queue()
        
        return job.job_id
    
    def remove_job(self, job_id: str) -> bool:
        """
        Remove job from queue (only if pending)
        
        Args:
            job_id: Job identifier
            
        Returns:
            True if removed, False if not found or already running
        """
        with self.lock:
            job = self.jobs.get(job_id)
            if not job:
                return False
            
            if job.status in [JobStatus.RUNNING]:
                return False
            
            if job.status == JobStatus.PENDING:
                job.status = JobStatus.CANCELLED
            
            self._save_queue()
            return True
    
    def get_job(self, job_id: str) -> Optional[VideoJob]:
        """Get job by ID"""
        return self.jobs.get(job_id)
    
    def list_jobs(self, status: Optional[JobStatus] = None) -> List[VideoJob]:
        """
        List jobs, optionally filtered by status
        
        Args:
            status: Filter by job status (None = all jobs)
            
        Returns:
            List of jobs
        """
        jobs = list(self.jobs.values())
        
        if status:
            jobs = [j for j in jobs if j.status == status]
        
        # Sort by priority (high to low), then created_at
        jobs.sort(key=lambda j: (-j.priority.value, j.created_at or datetime.now()))
        
        return jobs
    
    def get_queue_stats(self) -> dict:
        """Get queue statistics"""
        status_counts = {}
        for status in JobStatus:
            status_counts[status.value] = len([j for j in self.jobs.values() if j.status == status])
        
        return {
            "total_jobs": len(self.jobs),
            "status_breakdown": status_counts,
            "active_workers": self.active_jobs,
            "max_workers": self.max_workers,
            "available_backends": self.processor.get_available_backends_info()
        }
    
    def start_workers(self):
        """Start background worker threads"""
        if self.workers_running:
            return
        
        self.workers_running = True
        
        for i in range(self.max_workers):
            worker = Thread(target=self._worker, args=(i,), daemon=True)
            worker.start()
    
    def stop_workers(self):
        """Stop background workers"""
        self.workers_running = False
    
    def _worker(self, worker_id: int):
        """
        Background worker thread
        
        Args:
            worker_id: Worker identifier
        """
        while self.workers_running:
            try:
                # Get next job from priority queue (with timeout)
                try:
                    priority, job_id = self.priority_queue.get(timeout=1)
                except:
                    continue
                
                job = self.jobs.get(job_id)
                
                if not job or job.status != JobStatus.PENDING:
                    continue
                
                # Mark job as running
                with self.lock:
                    job.status = JobStatus.RUNNING
                    job.started_at = datetime.now()
                    self.active_jobs += 1
                    self._save_queue()
                
                print(f"[Worker {worker_id}] Processing job {job_id[:8]}... ({job.input_file})")
                
                # Process video
                result = self.processor.process_video(
                    job_id=job.job_id,
                    input_file=job.input_file,
                    output_file=job.output_file,
                    preset=job.preset,
                    backend=job.backend
                )
                
                # Update job status
                with self.lock:
                    if result.success:
                        job.status = JobStatus.COMPLETED
                        job.completed_at = datetime.now()
                        print(f"[Worker {worker_id}] ✅ Job {job_id[:8]} completed in {result.processing_time:.1f}s")
                    else:
                        job.retry_count += 1
                        
                        # Retry up to 3 times
                        if job.retry_count < 3:
                            job.status = JobStatus.PENDING
                            # Re-queue with same priority
                            self.priority_queue.put((-job.priority.value, job_id))
                            print(f"[Worker {worker_id}] ⚠️ Job {job_id[:8]} failed, retry {job.retry_count}/3")
                        else:
                            job.status = JobStatus.FAILED
                            job.error_message = result.error_message
                            job.completed_at = datetime.now()
                            print(f"[Worker {worker_id}] ❌ Job {job_id[:8]} failed after 3 retries: {result.error_message}")
                    
                    self.active_jobs -= 1
                    self._save_queue()
            
            except Exception as e:
                print(f"[Worker {worker_id}] Error: {e}")
                with self.lock:
                    self.active_jobs -= 1
    
    def _save_queue(self):
        """Persist queue to disk"""
        data = {
            "jobs": {job_id: job.to_dict() for job_id, job in self.jobs.items()},
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.queue_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_queue(self):
        """Load queue from disk"""
        if not self.queue_file.exists():
            return
        
        try:
            with open(self.queue_file, 'r') as f:
                data = json.load(f)
            
            self.jobs = {
                job_id: VideoJob.from_dict(job_data)
                for job_id, job_data in data.get("jobs", {}).items()
            }
            
            # Rebuild priority queue with pending jobs
            for job in self.jobs.values():
                if job.status == JobStatus.PENDING:
                    self.priority_queue.put((-job.priority.value, job.job_id))
                
                # Reset running jobs to pending (crashed/restarted)
                if job.status == JobStatus.RUNNING:
                    job.status = JobStatus.PENDING
                    self.priority_queue.put((-job.priority.value, job.job_id))
        
        except Exception as e:
            print(f"Warning: Could not load queue: {e}")
