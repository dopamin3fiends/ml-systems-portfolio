#!/usr/bin/env python3
"""
🎬 Video Enhancement Suite v1.0
Professional video processing queue manager with multi-backend support

Usage:
    python cli.py add <input> <output> --preset <preset> [--priority medium] [--backend auto]
    python cli.py list [--status pending]
    python cli.py stats
    python cli.py process [--workers 2]
    python cli.py demo

Examples:
    # Add job to queue
    python cli.py add input.mp4 output_4k.mp4 --preset upscale_4x --priority high
    
    # Start processing
    python cli.py process --workers 2
    
    # Check queue status
    python cli.py list --status pending
    python cli.py stats
    
    # Run demo (no real processing)
    python cli.py demo
"""

import argparse
import sys
import time
from pathlib import Path

try:
    from models import JobStatus, Priority, Backend
    from queue_manager import JobQueue
    from processor import VideoProcessor
except ImportError:
    from .models import JobStatus, Priority, Backend
    from .queue_manager import JobQueue
    from .processor import VideoProcessor


def add_job_command(args, queue: JobQueue):
    """Add job to queue"""
    job_id = queue.add_job(
        input_file=args.input,
        output_file=args.output,
        preset=args.preset,
        backend=args.backend,
        priority=args.priority
    )
    
    print(f"✅ Job added to queue: {job_id}")
    print(f"   Input: {args.input}")
    print(f"   Output: {args.output}")
    print(f"   Preset: {args.preset}")
    print(f"   Priority: {args.priority.upper()}")
    print(f"   Backend: {args.backend.upper()}")


def list_jobs_command(args, queue: JobQueue):
    """List jobs in queue"""
    status_filter = JobStatus(args.status) if args.status else None
    jobs = queue.list_jobs(status=status_filter)
    
    if not jobs:
        print("No jobs in queue.")
        return
    
    print(f"\n{'='*80}")
    print(f"📋 Job Queue ({len(jobs)} jobs)")
    print(f"{'='*80}\n")
    
    for job in jobs:
        status_icon = {
            JobStatus.PENDING: "⏳",
            JobStatus.RUNNING: "▶️",
            JobStatus.COMPLETED: "✅",
            JobStatus.FAILED: "❌",
            JobStatus.CANCELLED: "🚫"
        }.get(job.status, "❓")
        
        print(f"{status_icon} [{job.status.value.upper()}] {job.job_id[:8]}")
        print(f"   {job.input_file} → {job.output_file}")
        print(f"   Preset: {job.preset} | Priority: {job.priority.name} | Backend: {job.backend.value}")
        
        if job.error_message:
            print(f"   Error: {job.error_message}")
        
        if job.completed_at:
            duration = (job.completed_at - job.started_at).total_seconds() if job.started_at else 0
            print(f"   Duration: {duration:.1f}s")
        
        print()


def stats_command(args, queue: JobQueue):
    """Show queue statistics"""
    stats = queue.get_queue_stats()
    
    print(f"\n{'='*80}")
    print(f"📊 Video Enhancement Queue Statistics")
    print(f"{'='*80}\n")
    
    print(f"Total Jobs: {stats['total_jobs']}")
    print(f"Active Workers: {stats['active_workers']} / {stats['max_workers']}\n")
    
    print("Status Breakdown:")
    for status, count in stats['status_breakdown'].items():
        print(f"  {status.capitalize()}: {count}")
    
    print("\nAvailable Backends:")
    backends = stats['available_backends']
    for backend, available in backends.items():
        if backend != 'count':
            icon = "✅" if available else "❌"
            print(f"  {icon} {backend.upper()}")
    
    print(f"\nTotal Backends Available: {backends['count']}")
    
    if backends['count'] == 0:
        print("\n⚠️  WARNING: No video processing backends detected!")
        print("   Install FFmpeg, Topaz Video AI, or HandBrake to process videos.")


def process_command(args, queue: JobQueue):
    """Start processing queue"""
    stats = queue.get_queue_stats()
    
    if stats['available_backends']['count'] == 0:
        print("❌ Error: No video processing backends available.")
        print("   Install FFmpeg, Topaz Video AI, or HandBrake to continue.")
        return
    
    pending = stats['status_breakdown'].get('pending', 0)
    
    if pending == 0:
        print("ℹ️  No pending jobs in queue.")
        return
    
    print(f"🎬 Starting video processing with {args.workers} workers...")
    print(f"   Pending jobs: {pending}")
    print(f"   Press Ctrl+C to stop\n")
    
    queue.max_workers = args.workers
    queue.start_workers()
    
    try:
        # Monitor queue until all jobs complete or user interrupts
        while True:
            stats = queue.get_queue_stats()
            pending = stats['status_breakdown'].get('pending', 0)
            running = stats['status_breakdown'].get('running', 0)
            
            if pending == 0 and running == 0:
                print("\n✅ All jobs completed!")
                break
            
            print(f"⏳ Pending: {pending} | ▶️  Running: {running}", end='\r')
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n⏸️  Stopping workers...")
        queue.stop_workers()
        print("Queue saved. Run 'python cli.py process' to resume.")


def demo_command(args, queue: JobQueue):
    """Run demo mode"""
    print("🎬 Video Enhancement Suite v1.0 - Demo Mode\n")
    print("=" * 60)
    
    # Show available backends
    processor = VideoProcessor()
    backends = processor.get_available_backends_info()
    
    print("\n[1/4] Detecting video processing backends...")
    for backend, available in backends.items():
        if backend != 'count':
            icon = "✅" if available else "❌"
            print(f"   {icon} {backend.upper()}")
    
    # Create demo jobs
    print("\n[2/4] Creating demo jobs...")
    demo_jobs = [
        {"input_file": "demo_video_1080p.mp4", "output_file": "demo_video_4k.mp4", "preset": "upscale_4x", "priority": "high"},
        {"input_file": "demo_noisy.mp4", "output_file": "demo_clean.mp4", "preset": "denoise", "priority": "medium"},
        {"input_file": "demo_large.mp4", "output_file": "demo_compressed.mp4", "preset": "compress", "priority": "low"}
    ]
    
    job_ids = []
    for demo in demo_jobs:
        job_id = queue.add_job(**demo, backend="auto")
        job_ids.append(job_id)
        print(f"   ✅ Added: {demo['input_file']} → {demo['output_file']} (Priority: {demo['priority']})")
    
    # Show queue stats
    print("\n[3/4] Queue statistics...")
    stats = queue.get_queue_stats()
    print(f"   Total jobs: {stats['total_jobs']}")
    print(f"   Pending: {stats['status_breakdown'].get('pending', 0)}")
    print(f"   Available workers: {stats['max_workers']}")
    
    # Show job list
    print("\n[4/4] Job queue:")
    for job_id in job_ids:
        job = queue.get_job(job_id)
        print(f"   ⏳ [{job.priority.name}] {job.job_id[:8]} - {job.preset}")
    
    print("\n" + "=" * 60)
    print("✅ Demo complete! 3 jobs added to queue.")
    print("\nTo process these jobs:")
    print("  python cli.py process --workers 2")
    print("\nTo view queue:")
    print("  python cli.py list")
    print("\nNote: Demo jobs use placeholder files. Replace with real files to process.")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="🎬 Video Enhancement Suite - Professional video processing queue manager",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add job command
    add_parser = subparsers.add_parser('add', help='Add job to queue')
    add_parser.add_argument('input', help='Input video file path')
    add_parser.add_argument('output', help='Output video file path')
    add_parser.add_argument('--preset', required=True, 
                           help='Processing preset (upscale_2x, upscale_4x, denoise, sharpen, compress)')
    add_parser.add_argument('--priority', default='medium', 
                           choices=['low', 'medium', 'high', 'critical'],
                           help='Job priority (default: medium)')
    add_parser.add_argument('--backend', default='auto',
                           choices=['auto', 'topaz', 'ffmpeg', 'handbrake'],
                           help='Video processing backend (default: auto)')
    
    # List jobs command
    list_parser = subparsers.add_parser('list', help='List jobs in queue')
    list_parser.add_argument('--status', choices=[s.value for s in JobStatus],
                            help='Filter by job status')
    
    # Stats command
    subparsers.add_parser('stats', help='Show queue statistics')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Start processing queue')
    process_parser.add_argument('--workers', type=int, default=2,
                               help='Number of concurrent workers (default: 2)')
    
    # Demo command
    subparsers.add_parser('demo', help='Run demo mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize queue
    queue = JobQueue()
    
    # Execute command
    if args.command == 'add':
        add_job_command(args, queue)
    elif args.command == 'list':
        list_jobs_command(args, queue)
    elif args.command == 'stats':
        stats_command(args, queue)
    elif args.command == 'process':
        process_command(args, queue)
    elif args.command == 'demo':
        demo_command(args, queue)


if __name__ == "__main__":
    main()
