"""
PathPulse - Data Models
File system monitoring and anomaly detection models
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path


class EventType(Enum):
    """File system event types"""
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"
    MOVED = "moved"
    ACCESSED = "accessed"


class RiskLevel(Enum):
    """Event risk assessment levels"""
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FileCategory(Enum):
    """File categories for targeted monitoring"""
    SYSTEM = "system"
    EXECUTABLE = "executable"
    DOCUMENT = "document"
    DATABASE = "database"
    CONFIGURATION = "configuration"
    SENSITIVE = "sensitive"
    MEDIA = "media"
    ARCHIVE = "archive"
    UNKNOWN = "unknown"


@dataclass
class FileEvent:
    """
    Represents a file system event
    
    Attributes:
        event_type: Type of file system event
        path: Full path to the file/directory
        timestamp: When the event occurred
        event_id: Unique event identifier
        file_size: File size in bytes (if applicable)
        file_category: Category of the file
        src_path: Source path (for move operations)
        dest_path: Destination path (for move operations)
        process_name: Process that triggered the event
        user: User account that triggered the event
        risk_level: Assessed risk level
        metadata: Additional event-specific data
    """
    event_type: EventType
    path: str
    timestamp: datetime
    event_id: Optional[str] = None
    file_size: Optional[int] = None
    file_category: FileCategory = FileCategory.UNKNOWN
    src_path: Optional[str] = None
    dest_path: Optional[str] = None
    process_name: Optional[str] = None
    user: Optional[str] = None
    risk_level: RiskLevel = RiskLevel.SAFE
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert event to dictionary for JSON serialization"""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "path": self.path,
            "timestamp": self.timestamp.isoformat(),
            "file_size": self.file_size,
            "file_category": self.file_category.value,
            "src_path": self.src_path,
            "dest_path": self.dest_path,
            "process_name": self.process_name,
            "user": self.user,
            "risk_level": self.risk_level.value,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'FileEvent':
        """Create event from dictionary"""
        return cls(
            event_id=data.get("event_id"),
            event_type=EventType(data["event_type"]),
            path=data["path"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            file_size=data.get("file_size"),
            file_category=FileCategory(data.get("file_category", "unknown")),
            src_path=data.get("src_path"),
            dest_path=data.get("dest_path"),
            process_name=data.get("process_name"),
            user=data.get("user"),
            risk_level=RiskLevel(data.get("risk_level", "safe")),
            metadata=data.get("metadata", {})
        )


@dataclass
class ThreatPattern:
    """
    Detected threat pattern
    
    Attributes:
        pattern_type: Type of threat pattern
        description: Human-readable description
        events: List of events that match this pattern
        risk_level: Overall risk assessment
        confidence: Confidence score (0.0 to 1.0)
        first_seen: When pattern was first detected
        last_seen: Most recent matching event
        event_count: Number of events in pattern
        recommended_action: Suggested response
    """
    pattern_type: str
    description: str
    events: List[FileEvent]
    risk_level: RiskLevel
    confidence: float
    first_seen: datetime
    last_seen: datetime
    event_count: int
    recommended_action: str
    
    def to_dict(self) -> dict:
        """Convert threat pattern to dictionary"""
        return {
            "pattern_type": self.pattern_type,
            "description": self.description,
            "events": [e.to_dict() for e in self.events],
            "risk_level": self.risk_level.value,
            "confidence": self.confidence,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "event_count": self.event_count,
            "recommended_action": self.recommended_action
        }


@dataclass
class MonitoringSession:
    """
    File system monitoring session
    
    Attributes:
        session_id: Unique session identifier
        start_time: When monitoring started
        end_time: When monitoring ended (None if active)
        monitored_paths: List of paths being monitored
        total_events: Total events captured
        threat_patterns: Detected threat patterns
        status: Session status (active/stopped/paused)
    """
    session_id: str
    start_time: datetime
    monitored_paths: List[str]
    end_time: Optional[datetime] = None
    total_events: int = 0
    threat_patterns: List[ThreatPattern] = field(default_factory=list)
    status: str = "active"
    
    def to_dict(self) -> dict:
        """Convert session to dictionary"""
        return {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "monitored_paths": self.monitored_paths,
            "total_events": self.total_events,
            "threat_patterns": [t.to_dict() for t in self.threat_patterns],
            "status": self.status
        }


# Sensitive path patterns (for risk assessment)
SENSITIVE_PATHS = [
    r"C:\\Windows\\System32",
    r"C:\\Program Files",
    r"/etc",
    r"/usr/bin",
    r"/var/log",
    r"\.ssh",
    r"\.aws",
    r"\.kube",
    r"wallet\.dat",
    r"private.*key",
    r"credentials",
    r"password",
]

# High-risk file extensions
HIGH_RISK_EXTENSIONS = [
    ".exe", ".dll", ".sys", ".bat", ".ps1", ".vbs", ".js",
    ".encrypted", ".locked", ".crypto", ".ransom"
]

# File category mapping
CATEGORY_EXTENSIONS = {
    FileCategory.EXECUTABLE: [".exe", ".dll", ".sys", ".so", ".dylib", ".app"],
    FileCategory.DOCUMENT: [".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".txt"],
    FileCategory.DATABASE: [".db", ".sqlite", ".sql", ".mdb", ".accdb"],
    FileCategory.CONFIGURATION: [".conf", ".config", ".ini", ".yaml", ".yml", ".json", ".xml"],
    FileCategory.SENSITIVE: [".key", ".pem", ".cert", ".p12", ".pfx", ".kdb", ".wallet"],
    FileCategory.MEDIA: [".jpg", ".png", ".mp4", ".avi", ".mp3", ".wav"],
    FileCategory.ARCHIVE: [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
}


def categorize_file(file_path: str) -> FileCategory:
    """
    Categorize file based on extension
    
    Args:
        file_path: Path to file
        
    Returns:
        FileCategory
    """
    ext = Path(file_path).suffix.lower()
    
    for category, extensions in CATEGORY_EXTENSIONS.items():
        if ext in extensions:
            return category
    
    return FileCategory.UNKNOWN


def is_sensitive_path(file_path: str) -> bool:
    """
    Check if path is sensitive
    
    Args:
        file_path: Path to check
        
    Returns:
        True if path is sensitive
    """
    import re
    
    for pattern in SENSITIVE_PATHS:
        if re.search(pattern, file_path, re.IGNORECASE):
            return True
    
    return False
