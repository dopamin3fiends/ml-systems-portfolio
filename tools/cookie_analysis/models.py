"""
Data models for cookie analysis.
"""

from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional


class CookieType(Enum):
    SESSION = "session"
    PERSISTENT = "persistent"
    THIRD_PARTY = "third_party"
    SECURE = "secure"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Cookie:
    """Represents a browser cookie."""
    name: str
    value: str
    domain: str
    path: str = "/"
    secure: bool = False
    http_only: bool = False
    same_site: Optional[str] = None
    expires: Optional[datetime] = None
    cookie_type: CookieType = CookieType.SESSION
    company: Optional[str] = None
    purpose: Optional[str] = None
    risk_level: RiskLevel = RiskLevel.LOW
    
    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "domain": self.domain,
            "path": self.path,
            "secure": self.secure,
            "http_only": self.http_only,
            "same_site": self.same_site,
            "expires": self.expires.isoformat() if self.expires else None,
            "cookie_type": self.cookie_type.value,
            "company": self.company,
            "purpose": self.purpose,
            "risk_level": self.risk_level.value
        }
