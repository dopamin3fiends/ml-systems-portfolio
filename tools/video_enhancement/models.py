"""
Video Enhancement Suite - Data Models
Professional video processing job management system
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime


class JobStatus(Enum):
    """Job execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Priority(Enum):
    """Job priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Backend(Enum):
    """Supported video processing backends"""
    TOPAZ = "topaz"
    FFMPEG = "ffmpeg"
    HANDBRAKE = "handbrake"
    AUTO = "auto"  # Automatic backend selection


@dataclass
class VideoJob:
    """
    Represents a video enhancement job
    
    Attributes:
        input_file: Path to input video file
        output_file: Path for output video file
        preset: Processing preset name
        backend: Video processing backend to use
        priority: Job priority level
        status: Current job status
        job_id: Unique job identifier
        created_at: Timestamp when job was created
        started_at: Timestamp when job started processing
        completed_at: Timestamp when job finished
        error_message: Error details if job failed
        retry_count: Number of retry attempts
        metadata: Additional job-specific data
    """
    input_file: str
    output_file: str
    preset: str
    backend: Backend = Backend.AUTO
    priority: Priority = Priority.MEDIUM
    status: JobStatus = JobStatus.PENDING
    job_id: Optional[str] = None
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert job to dictionary for JSON serialization"""
        return {
            "job_id": self.job_id,
            "input_file": self.input_file,
            "output_file": self.output_file,
            "preset": self.preset,
            "backend": self.backend.value,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error_message": self.error_message,
            "retry_count": self.retry_count,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'VideoJob':
        """Create job from dictionary"""
        return cls(
            job_id=data.get("job_id"),
            input_file=data["input_file"],
            output_file=data["output_file"],
            preset=data["preset"],
            backend=Backend(data.get("backend", "auto")),
            priority=Priority(data.get("priority", 2)),
            status=JobStatus(data.get("status", "pending")),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            started_at=datetime.fromisoformat(data["started_at"]) if data.get("started_at") else None,
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
            error_message=data.get("error_message"),
            retry_count=data.get("retry_count", 0),
            metadata=data.get("metadata", {})
        )


@dataclass
class ProcessingResult:
    """Result of a video processing operation"""
    success: bool
    job_id: str
    output_file: Optional[str] = None
    error_message: Optional[str] = None
    processing_time: Optional[float] = None
    backend_used: Optional[Backend] = None
    
    def to_dict(self) -> dict:
        """Convert result to dictionary"""
        return {
            "success": self.success,
            "job_id": self.job_id,
            "output_file": self.output_file,
            "error_message": self.error_message,
            "processing_time": self.processing_time,
            "backend_used": self.backend_used.value if self.backend_used else None
        }
