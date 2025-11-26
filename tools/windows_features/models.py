"""
Windows Feature Manager - Data Models
Models for Windows optional feature management
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime


class FeatureState(Enum):
    """Windows feature installation state"""
    ENABLED = "enabled"
    DISABLED = "disabled"
    ENABLE_PENDING = "enable_pending"
    DISABLE_PENDING = "disable_pending"
    UNKNOWN = "unknown"


class OperationType(Enum):
    """Feature operation types"""
    ENABLE = "enable"
    DISABLE = "disable"
    QUERY = "query"
    BACKUP = "backup"
    RESTORE = "restore"


class FeatureCategory(Enum):
    """Feature categories for organization"""
    DEVELOPMENT = "development"
    VIRTUALIZATION = "virtualization"
    NETWORKING = "networking"
    SECURITY = "security"
    LEGACY = "legacy"
    SYSTEM = "system"
    MEDIA = "media"
    UNKNOWN = "unknown"


@dataclass
class WindowsFeature:
    """
    Represents a Windows optional feature
    
    Attributes:
        name: Feature name (e.g., "Microsoft-Windows-Subsystem-Linux")
        display_name: Human-readable name
        state: Current installation state
        category: Feature category
        description: Feature description
        restart_required: Whether restart is needed after change
        dependencies: List of dependent feature names
        metadata: Additional feature information
    """
    name: str
    display_name: str
    state: FeatureState
    category: FeatureCategory = FeatureCategory.UNKNOWN
    description: Optional[str] = None
    restart_required: bool = False
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert feature to dictionary"""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "state": self.state.value,
            "category": self.category.value,
            "description": self.description,
            "restart_required": self.restart_required,
            "dependencies": self.dependencies,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'WindowsFeature':
        """Create feature from dictionary"""
        return cls(
            name=data["name"],
            display_name=data["display_name"],
            state=FeatureState(data.get("state", "unknown")),
            category=FeatureCategory(data.get("category", "unknown")),
            description=data.get("description"),
            restart_required=data.get("restart_required", False),
            dependencies=data.get("dependencies", []),
            metadata=data.get("metadata", {})
        )


@dataclass
class FeatureGroup:
    """
    Predefined group of related features
    
    Attributes:
        name: Group name
        description: Group description
        features: List of feature names in group
        category: Primary category
    """
    name: str
    description: str
    features: List[str]
    category: FeatureCategory
    
    def to_dict(self) -> dict:
        """Convert group to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "features": self.features,
            "category": self.category.value
        }


@dataclass
class OperationResult:
    """
    Result of a feature operation
    
    Attributes:
        success: Whether operation succeeded
        operation: Type of operation performed
        feature_name: Name of affected feature
        message: Result message
        restart_required: Whether restart is needed
        error: Error details if failed
        timestamp: When operation was performed
    """
    success: bool
    operation: OperationType
    feature_name: str
    message: str
    restart_required: bool = False
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Convert result to dictionary"""
        return {
            "success": self.success,
            "operation": self.operation.value,
            "feature_name": self.feature_name,
            "message": self.message,
            "restart_required": self.restart_required,
            "error": self.error,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class SystemBackup:
    """
    Backup of Windows feature states
    
    Attributes:
        backup_id: Unique backup identifier
        timestamp: When backup was created
        features: Dictionary of feature states
        hostname: Computer name
        os_version: Windows version
    """
    backup_id: str
    timestamp: datetime
    features: Dict[str, FeatureState]
    hostname: str
    os_version: str
    
    def to_dict(self) -> dict:
        """Convert backup to dictionary"""
        return {
            "backup_id": self.backup_id,
            "timestamp": self.timestamp.isoformat(),
            "features": {name: state.value for name, state in self.features.items()},
            "hostname": self.hostname,
            "os_version": self.os_version
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SystemBackup':
        """Create backup from dictionary"""
        return cls(
            backup_id=data["backup_id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            features={name: FeatureState(state) for name, state in data["features"].items()},
            hostname=data["hostname"],
            os_version=data["os_version"]
        )


# Predefined feature groups
FEATURE_GROUPS = {
    "dev_tools": FeatureGroup(
        name="Development Tools",
        description="Features for software development (WSL, Containers, etc.)",
        features=[
            "Microsoft-Windows-Subsystem-Linux",
            "VirtualMachinePlatform",
            "Containers",
            "Microsoft-Hyper-V-All",
            "NetFx3",
            "NetFx4Extended-ASPNET45"
        ],
        category=FeatureCategory.DEVELOPMENT
    ),
    "virtualization": FeatureGroup(
        name="Virtualization",
        description="Hyper-V and virtualization features",
        features=[
            "Microsoft-Hyper-V-All",
            "Microsoft-Hyper-V",
            "Microsoft-Hyper-V-Management-PowerShell",
            "VirtualMachinePlatform",
            "HypervisorPlatform"
        ],
        category=FeatureCategory.VIRTUALIZATION
    ),
    "networking": FeatureGroup(
        name="Network Tools",
        description="Network utilities and protocols",
        features=[
            "TelnetClient",
            "TFTP",
            "SimpleTCP",
            "SMB1Protocol"
        ],
        category=FeatureCategory.NETWORKING
    ),
    "security": FeatureGroup(
        name="Security Features",
        description="Security and authentication features",
        features=[
            "Windows-Defender-ApplicationGuard",
            "Microsoft-Hyper-V-Hypervisor"
        ],
        category=FeatureCategory.SECURITY
    ),
    "legacy": FeatureGroup(
        name="Legacy Support",
        description="Older Windows features for compatibility",
        features=[
            "LegacyComponents",
            "DirectPlay",
            "NetFx3"
        ],
        category=FeatureCategory.LEGACY
    )
}


# Feature metadata (descriptions, categories, warnings)
FEATURE_METADATA = {
    "Microsoft-Windows-Subsystem-Linux": {
        "category": FeatureCategory.DEVELOPMENT,
        "description": "Windows Subsystem for Linux - Run Linux distributions on Windows",
        "restart_required": True
    },
    "VirtualMachinePlatform": {
        "category": FeatureCategory.VIRTUALIZATION,
        "description": "Virtual Machine Platform - Required for WSL 2",
        "restart_required": True
    },
    "Microsoft-Hyper-V-All": {
        "category": FeatureCategory.VIRTUALIZATION,
        "description": "Hyper-V - Hardware virtualization platform",
        "restart_required": True
    },
    "Containers": {
        "category": FeatureCategory.DEVELOPMENT,
        "description": "Windows Containers - Container runtime support",
        "restart_required": True
    },
    "TelnetClient": {
        "category": FeatureCategory.NETWORKING,
        "description": "Telnet Client - Legacy network protocol (insecure)",
        "restart_required": False
    },
    "NetFx3": {
        "category": FeatureCategory.DEVELOPMENT,
        "description": ".NET Framework 3.5 - Legacy .NET runtime",
        "restart_required": False
    }
}
