"""
Web Automation Framework - Data Models
Models for browser automation and workflow management
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime


class BrowserType(Enum):
    """Supported browser types"""
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    SAFARI = "safari"


class SessionStatus(Enum):
    """Automation session status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ActionType(Enum):
    """Types of browser actions"""
    NAVIGATE = "navigate"
    CLICK = "click"
    TYPE = "type"
    SCROLL = "scroll"
    WAIT = "wait"
    SCREENSHOT = "screenshot"
    EXTRACT = "extract"
    EXECUTE_JS = "execute_js"


@dataclass
class BrowserConfig:
    """
    Browser configuration for automation
    
    Attributes:
        browser_type: Type of browser to use
        headless: Run browser in headless mode
        user_agent: Custom user agent string
        proxy: Proxy server (format: host:port or http://host:port)
        window_size: Browser window size (width, height)
        timeout: Page load timeout in seconds
        disable_images: Disable image loading for speed
        disable_javascript: Disable JavaScript execution
    """
    browser_type: BrowserType = BrowserType.CHROME
    headless: bool = False
    user_agent: Optional[str] = None
    proxy: Optional[str] = None
    window_size: tuple = (1920, 1080)
    timeout: int = 30
    disable_images: bool = False
    disable_javascript: bool = False
    
    def to_dict(self) -> dict:
        """Convert config to dictionary"""
        return {
            "browser_type": self.browser_type.value,
            "headless": self.headless,
            "user_agent": self.user_agent,
            "proxy": self.proxy,
            "window_size": list(self.window_size),
            "timeout": self.timeout,
            "disable_images": self.disable_images,
            "disable_javascript": self.disable_javascript
        }


@dataclass
class BrowserAction:
    """
    Single browser action to perform
    
    Attributes:
        action_type: Type of action
        target: Target element (CSS selector, XPath, or URL)
        value: Value for action (text to type, JS to execute, etc.)
        wait_after: Seconds to wait after action
        metadata: Additional action parameters
    """
    action_type: ActionType
    target: Optional[str] = None
    value: Optional[str] = None
    wait_after: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert action to dictionary"""
        return {
            "action_type": self.action_type.value,
            "target": self.target,
            "value": self.value,
            "wait_after": self.wait_after,
            "metadata": self.metadata
        }


@dataclass
class Workflow:
    """
    Automation workflow (sequence of actions)
    
    Attributes:
        name: Workflow name
        description: Workflow description
        actions: List of browser actions
        config: Browser configuration
        repeat_count: Number of times to repeat workflow
    """
    name: str
    description: str
    actions: List[BrowserAction]
    config: BrowserConfig = field(default_factory=BrowserConfig)
    repeat_count: int = 1
    
    def to_dict(self) -> dict:
        """Convert workflow to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "actions": [a.to_dict() for a in self.actions],
            "config": self.config.to_dict(),
            "repeat_count": self.repeat_count
        }


@dataclass
class SessionResult:
    """
    Result of an automation session
    
    Attributes:
        session_id: Unique session identifier
        workflow_name: Name of executed workflow
        status: Session status
        start_time: When session started
        end_time: When session ended
        actions_completed: Number of actions completed
        actions_failed: Number of actions that failed
        screenshots: List of screenshot file paths
        extracted_data: Data extracted during session
        error_message: Error details if failed
        metadata: Additional session data
    """
    session_id: str
    workflow_name: str
    status: SessionStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    actions_completed: int = 0
    actions_failed: int = 0
    screenshots: List[str] = field(default_factory=list)
    extracted_data: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert result to dictionary"""
        return {
            "session_id": self.session_id,
            "workflow_name": self.workflow_name,
            "status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "actions_completed": self.actions_completed,
            "actions_failed": self.actions_failed,
            "screenshots": self.screenshots,
            "extracted_data": self.extracted_data,
            "error_message": self.error_message,
            "metadata": self.metadata
        }
    
    @property
    def duration(self) -> Optional[float]:
        """Get session duration in seconds"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None


# Preset workflows for common tasks
PRESET_WORKFLOWS = {
    "health_check": Workflow(
        name="Website Health Check",
        description="Navigate to URL and verify page loads successfully",
        actions=[
            BrowserAction(ActionType.NAVIGATE, target="{url}"),
            BrowserAction(ActionType.WAIT, value="2"),
            BrowserAction(ActionType.SCREENSHOT, target="health_check_{timestamp}.png"),
            BrowserAction(ActionType.EXECUTE_JS, value="return document.title;", metadata={"extract_as": "page_title"})
        ]
    ),
    "form_test": Workflow(
        name="Form Testing",
        description="Test form submission workflow",
        actions=[
            BrowserAction(ActionType.NAVIGATE, target="{url}"),
            BrowserAction(ActionType.WAIT, value="2"),
            BrowserAction(ActionType.TYPE, target="{input_selector}", value="{input_value}"),
            BrowserAction(ActionType.CLICK, target="{submit_selector}"),
            BrowserAction(ActionType.WAIT, value="3"),
            BrowserAction(ActionType.SCREENSHOT, target="form_result_{timestamp}.png")
        ]
    ),
    "page_scrape": Workflow(
        name="Page Content Extraction",
        description="Extract text content from page elements",
        actions=[
            BrowserAction(ActionType.NAVIGATE, target="{url}"),
            BrowserAction(ActionType.WAIT, value="2"),
            BrowserAction(ActionType.SCROLL, value="bottom"),
            BrowserAction(ActionType.EXTRACT, target="{selector}", metadata={"extract_as": "content"}),
            BrowserAction(ActionType.SCREENSHOT, target="scrape_{timestamp}.png")
        ]
    ),
    "link_checker": Workflow(
        name="Link Validation",
        description="Check all links on a page",
        actions=[
            BrowserAction(ActionType.NAVIGATE, target="{url}"),
            BrowserAction(ActionType.WAIT, value="2"),
            BrowserAction(ActionType.EXECUTE_JS, 
                         value="return Array.from(document.querySelectorAll('a')).map(a => a.href);",
                         metadata={"extract_as": "links"}),
            BrowserAction(ActionType.SCREENSHOT, target="links_{timestamp}.png")
        ]
    )
}
