"""
ADB Automation Framework - Data Models
Models for Android device automation and management
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any


class DeviceStatus(Enum):
    """Device connection status"""
    ONLINE = "device"
    OFFLINE = "offline"
    UNAUTHORIZED = "unauthorized"
    BOOTLOADER = "bootloader"
    RECOVERY = "recovery"
    SIDELOAD = "sideload"
    UNKNOWN = "unknown"


class InputMethod(Enum):
    """Input simulation methods"""
    TAP = "tap"
    SWIPE = "swipe"
    TEXT = "text"
    KEYEVENT = "keyevent"
    LONG_PRESS = "longpress"


class KeyCode(Enum):
    """Common Android key codes"""
    HOME = 3
    BACK = 4
    MENU = 82
    POWER = 26
    VOLUME_UP = 24
    VOLUME_DOWN = 25
    CAMERA = 27
    ENTER = 66
    DELETE = 67
    APP_SWITCH = 187
    BRIGHTNESS_UP = 221
    BRIGHTNESS_DOWN = 220


@dataclass
class Device:
    """
    Android device information
    
    Attributes:
        serial: Device serial number
        status: Connection status
        model: Device model name
        android_version: Android OS version
        sdk_version: Android SDK API level
        battery_level: Battery percentage (0-100)
        screen_resolution: Screen dimensions (width, height)
        is_rooted: Whether device has root access
    """
    serial: str
    status: DeviceStatus
    model: Optional[str] = None
    android_version: Optional[str] = None
    sdk_version: Optional[int] = None
    battery_level: Optional[int] = None
    screen_resolution: Optional[tuple] = None
    is_rooted: bool = False
    
    def to_dict(self) -> dict:
        """Convert device to dictionary"""
        return {
            "serial": self.serial,
            "status": self.status.value,
            "model": self.model,
            "android_version": self.android_version,
            "sdk_version": self.sdk_version,
            "battery_level": self.battery_level,
            "screen_resolution": list(self.screen_resolution) if self.screen_resolution else None,
            "is_rooted": self.is_rooted
        }


@dataclass
class Package:
    """
    Android application package information
    
    Attributes:
        package_name: Package identifier (com.example.app)
        version_name: Version string (1.0.0)
        version_code: Version code integer
        install_time: Installation timestamp
        update_time: Last update timestamp
        is_system: Whether package is system app
        is_enabled: Whether package is enabled
    """
    package_name: str
    version_name: Optional[str] = None
    version_code: Optional[int] = None
    install_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    is_system: bool = False
    is_enabled: bool = True
    
    def to_dict(self) -> dict:
        """Convert package to dictionary"""
        return {
            "package_name": self.package_name,
            "version_name": self.version_name,
            "version_code": self.version_code,
            "install_time": self.install_time.isoformat() if self.install_time else None,
            "update_time": self.update_time.isoformat() if self.update_time else None,
            "is_system": self.is_system,
            "is_enabled": self.is_enabled
        }


@dataclass
class AutomationTask:
    """
    Automation task to execute on device
    
    Attributes:
        name: Task name
        description: Task description
        device_serial: Target device (None = any device)
        actions: List of actions to perform
        repeat_count: Number of times to repeat
        delay_between_actions: Seconds to wait between actions
    """
    name: str
    description: str
    device_serial: Optional[str] = None
    actions: List[Dict[str, Any]] = field(default_factory=list)
    repeat_count: int = 1
    delay_between_actions: float = 1.0
    
    def to_dict(self) -> dict:
        """Convert task to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "device_serial": self.device_serial,
            "actions": self.actions,
            "repeat_count": self.repeat_count,
            "delay_between_actions": self.delay_between_actions
        }


@dataclass
class TaskResult:
    """
    Result of automation task execution
    
    Attributes:
        task_name: Name of executed task
        device_serial: Device serial number
        status: Success or failure
        start_time: Execution start time
        end_time: Execution end time
        actions_completed: Number of actions completed
        actions_failed: Number of actions failed
        screenshots: List of screenshot paths
        error_message: Error message if failed
    """
    task_name: str
    device_serial: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    actions_completed: int = 0
    actions_failed: int = 0
    screenshots: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
    
    @property
    def duration(self) -> float:
        """Calculate execution duration in seconds"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    def to_dict(self) -> dict:
        """Convert result to dictionary"""
        return {
            "task_name": self.task_name,
            "device_serial": self.device_serial,
            "status": self.status,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "actions_completed": self.actions_completed,
            "actions_failed": self.actions_failed,
            "screenshots": self.screenshots,
            "error_message": self.error_message
        }


# Preset automation tasks
PRESET_TASKS = {
    "device_info": AutomationTask(
        name="Device Information",
        description="Collect comprehensive device information",
        actions=[
            {"type": "shell", "command": "getprop ro.product.model"},
            {"type": "shell", "command": "getprop ro.build.version.release"},
            {"type": "shell", "command": "dumpsys battery | grep level"},
            {"type": "screenshot", "filename": "device_screen_{timestamp}.png"}
        ]
    ),
    
    "app_launch_test": AutomationTask(
        name="App Launch Test",
        description="Launch app and capture screenshot",
        actions=[
            {"type": "app_start", "package": "{package_name}"},
            {"type": "wait", "duration": 3},
            {"type": "screenshot", "filename": "app_launch_{timestamp}.png"},
            {"type": "app_stop", "package": "{package_name}"}
        ]
    ),
    
    "screenshot_sequence": AutomationTask(
        name="Screenshot Sequence",
        description="Capture multiple screenshots with delays",
        actions=[
            {"type": "screenshot", "filename": "screenshot_1_{timestamp}.png"},
            {"type": "wait", "duration": 2},
            {"type": "screenshot", "filename": "screenshot_2_{timestamp}.png"},
            {"type": "wait", "duration": 2},
            {"type": "screenshot", "filename": "screenshot_3_{timestamp}.png"}
        ]
    ),
    
    "ui_interaction": AutomationTask(
        name="UI Interaction Test",
        description="Test basic UI interactions",
        actions=[
            {"type": "tap", "x": 500, "y": 1000},
            {"type": "wait", "duration": 1},
            {"type": "swipe", "x1": 500, "y1": 1500, "x2": 500, "y2": 500, "duration": 300},
            {"type": "wait", "duration": 1},
            {"type": "keyevent", "keycode": KeyCode.BACK.value},
            {"type": "screenshot", "filename": "ui_test_{timestamp}.png"}
        ]
    ),
    
    "battery_monitor": AutomationTask(
        name="Battery Monitor",
        description="Monitor battery level over time",
        actions=[
            {"type": "shell", "command": "dumpsys battery"},
            {"type": "wait", "duration": 60},
            {"type": "shell", "command": "dumpsys battery"}
        ],
        repeat_count=5
    )
}
