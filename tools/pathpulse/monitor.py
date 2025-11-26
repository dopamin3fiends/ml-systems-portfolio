"""
PathPulse - File System Monitor
Real-time file system event monitoring with cross-platform support
"""

import uuid
import time
from pathlib import Path
from datetime import datetime
from typing import List, Callable, Optional
from collections import deque
import threading

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    # Create dummy base class if watchdog not available
    class FileSystemEventHandler:
        pass
    Observer = None
    FileSystemEvent = None

try:
    from models import FileEvent, EventType, FileCategory, RiskLevel, categorize_file, is_sensitive_path
except ImportError:
    from .models import FileEvent, EventType, FileCategory, RiskLevel, categorize_file, is_sensitive_path


class PathPulseEventHandler(FileSystemEventHandler):
    """
    Watchdog event handler for PathPulse
    """
    
    def __init__(self, callback: Callable[[FileEvent], None]):
        """
        Initialize event handler
        
        Args:
            callback: Function to call with each FileEvent
        """
        super().__init__()
        self.callback = callback
    
    def _create_event(self, event: FileSystemEvent, event_type: EventType) -> FileEvent:
        """Create FileEvent from watchdog event"""
        path = event.src_path
        
        # Get file size (if file exists and is not directory)
        file_size = None
        try:
            if not event.is_directory and Path(path).exists():
                file_size = Path(path).stat().st_size
        except:
            pass
        
        # Categorize file
        file_category = categorize_file(path) if not event.is_directory else FileCategory.UNKNOWN
        
        # Assess risk
        risk_level = RiskLevel.SAFE
        if is_sensitive_path(path):
            risk_level = RiskLevel.HIGH
        elif file_category == FileCategory.SENSITIVE:
            risk_level = RiskLevel.HIGH
        elif file_category == FileCategory.EXECUTABLE and event_type in [EventType.CREATED, EventType.MODIFIED]:
            risk_level = RiskLevel.MEDIUM
        
        file_event = FileEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            path=path,
            timestamp=datetime.now(),
            file_size=file_size,
            file_category=file_category,
            risk_level=risk_level,
            metadata={"is_directory": event.is_directory}
        )
        
        return file_event
    
    def on_created(self, event):
        """Handle file/directory creation"""
        file_event = self._create_event(event, EventType.CREATED)
        self.callback(file_event)
    
    def on_modified(self, event):
        """Handle file/directory modification"""
        if not event.is_directory:  # Ignore directory modifications (noisy)
            file_event = self._create_event(event, EventType.MODIFIED)
            self.callback(file_event)
    
    def on_deleted(self, event):
        """Handle file/directory deletion"""
        file_event = self._create_event(event, EventType.DELETED)
        self.callback(file_event)
    
    def on_moved(self, event):
        """Handle file/directory move"""
        file_event = self._create_event(event, EventType.MOVED)
        file_event.src_path = event.src_path
        file_event.dest_path = event.dest_path
        file_event.path = event.dest_path  # Use destination as primary path
        self.callback(file_event)


class FileSystemMonitor:
    """
    Real-time file system monitor
    
    Features:
    - Cross-platform monitoring (Windows/Linux/macOS)
    - Event buffering and rate limiting
    - Multiple path monitoring
    - Custom event callbacks
    - Automatic risk assessment
    """
    
    def __init__(self, max_buffer_size: int = 10000):
        """
        Initialize file system monitor
        
        Args:
            max_buffer_size: Maximum events to buffer in memory
        """
        if not WATCHDOG_AVAILABLE:
            raise ImportError("watchdog library required. Install with: pip install watchdog")
        
        self.observers: List[Observer] = []
        self.monitored_paths: List[str] = []
        self.event_buffer = deque(maxlen=max_buffer_size)
        self.callbacks: List[Callable[[FileEvent], None]] = []
        self.is_monitoring = False
        self.lock = threading.Lock()
        self.total_events = 0
    
    def add_callback(self, callback: Callable[[FileEvent], None]):
        """
        Add callback function to be called for each event
        
        Args:
            callback: Function accepting FileEvent
        """
        self.callbacks.append(callback)
    
    def start_monitoring(self, paths: List[str], recursive: bool = True):
        """
        Start monitoring specified paths
        
        Args:
            paths: List of directory paths to monitor
            recursive: Monitor subdirectories recursively
        """
        if self.is_monitoring:
            raise RuntimeError("Monitor already running. Stop first.")
        
        self.monitored_paths = paths
        self.is_monitoring = True
        
        # Create observer for each path
        for path in paths:
            observer = Observer()
            event_handler = PathPulseEventHandler(callback=self._handle_event)
            observer.schedule(event_handler, path, recursive=recursive)
            observer.start()
            self.observers.append(observer)
        
        print(f"🔍 Monitoring started: {len(paths)} path(s)")
    
    def stop_monitoring(self):
        """Stop monitoring all paths"""
        if not self.is_monitoring:
            return
        
        for observer in self.observers:
            observer.stop()
            observer.join()
        
        self.observers.clear()
        self.is_monitoring = False
        
        print(f"⏹️  Monitoring stopped. Captured {self.total_events} events.")
    
    def _handle_event(self, event: FileEvent):
        """
        Internal event handler
        
        Args:
            event: FileEvent to process
        """
        with self.lock:
            # Add to buffer
            self.event_buffer.append(event)
            self.total_events += 1
            
            # Call registered callbacks
            for callback in self.callbacks:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Error in callback: {e}")
    
    def get_events(self, limit: Optional[int] = None) -> List[FileEvent]:
        """
        Get buffered events
        
        Args:
            limit: Maximum number of events to return (None = all)
            
        Returns:
            List of FileEvent objects
        """
        with self.lock:
            events = list(self.event_buffer)
            
            if limit:
                events = events[-limit:]
            
            return events
    
    def clear_buffer(self):
        """Clear event buffer"""
        with self.lock:
            self.event_buffer.clear()
    
    def get_stats(self) -> dict:
        """Get monitoring statistics"""
        with self.lock:
            event_types = {}
            risk_levels = {}
            
            for event in self.event_buffer:
                event_types[event.event_type.value] = event_types.get(event.event_type.value, 0) + 1
                risk_levels[event.risk_level.value] = risk_levels.get(event.risk_level.value, 0) + 1
            
            return {
                "is_monitoring": self.is_monitoring,
                "monitored_paths": self.monitored_paths,
                "total_events": self.total_events,
                "buffered_events": len(self.event_buffer),
                "event_types": event_types,
                "risk_levels": risk_levels
            }


def demo_monitor(duration: int = 10):
    """
    Demo mode: Monitor current directory for specified duration
    
    Args:
        duration: Monitoring duration in seconds
    """
    import tempfile
    import os
    
    print("🎬 PathPulse Monitor Demo\n")
    print("=" * 60)
    
    # Create temp directory for demo
    temp_dir = tempfile.mkdtemp(prefix="pathpulse_demo_")
    print(f"\n[1/3] Created demo directory: {temp_dir}")
    
    # Initialize monitor
    monitor = FileSystemMonitor()
    
    # Add callback to print events
    def print_event(event: FileEvent):
        icon = {
            EventType.CREATED: "➕",
            EventType.MODIFIED: "✏️",
            EventType.DELETED: "🗑️",
            EventType.MOVED: "🔀"
        }.get(event.event_type, "❓")
        
        risk_icon = {
            RiskLevel.SAFE: "✅",
            RiskLevel.LOW: "ℹ️",
            RiskLevel.MEDIUM: "⚠️",
            RiskLevel.HIGH: "🔴",
            RiskLevel.CRITICAL: "🚨"
        }.get(event.risk_level, "❓")
        
        print(f"{icon} {event.event_type.value.upper()}: {Path(event.path).name} {risk_icon}")
    
    monitor.add_callback(print_event)
    
    # Start monitoring
    print(f"\n[2/3] Monitoring {temp_dir} for {duration} seconds...")
    print("Creating demo file events...\n")
    
    monitor.start_monitoring([temp_dir], recursive=True)
    
    # Simulate file operations
    try:
        time.sleep(1)
        
        # Create files
        test_file = os.path.join(temp_dir, "test_document.txt")
        with open(test_file, "w") as f:
            f.write("Demo content")
        
        time.sleep(1)
        
        # Modify file
        with open(test_file, "a") as f:
            f.write("\nMore content")
        
        time.sleep(1)
        
        # Create executable (high risk)
        exe_file = os.path.join(temp_dir, "suspicious.exe")
        with open(exe_file, "wb") as f:
            f.write(b"DEMO")
        
        time.sleep(1)
        
        # Delete file
        os.remove(test_file)
        
        # Wait remaining time
        remaining = max(0, duration - 4)
        if remaining > 0:
            time.sleep(remaining)
    
    finally:
        monitor.stop_monitoring()
    
    # Show statistics
    print("\n[3/3] Monitoring statistics:")
    stats = monitor.get_stats()
    print(f"   Total events captured: {stats['total_events']}")
    print(f"   Event types: {stats['event_types']}")
    print(f"   Risk levels: {stats['risk_levels']}")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    print("\n" + "=" * 60)
    print("✅ Demo complete!")
