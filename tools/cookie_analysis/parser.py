"""
Cookie parser - extracts and cleans cookie data.
"""

import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime, timedelta

try:
    from models import Cookie, CookieType
except ImportError:
    from .models import Cookie, CookieType


def parse_cookies_file(input_path: str, output_path: str) -> List[Cookie]:
    """Parse cookies from various formats."""
    cookies = []
    
    # Demo mode - generate fake cookies
    demo_cookies = [
        {
            "name": "_ga",
            "value": "GA1.2.1234567890.1234567890",
            "domain": ".example.com",
            "path": "/",
            "secure": True,
            "http_only": False
        },
        {
            "name": "session_token",
            "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.demo",
            "domain": "app.example.com",
            "path": "/",
            "secure": True,
            "http_only": True
        },
        {
            "name": "_fbp",
            "value": "fb.1.1234567890123.1234567890",
            "domain": ".example.com",
            "path": "/",
            "secure": False,
            "http_only": False
        },
        {
            "name": "tracking_id",
            "value": "xyz789tracking",
            "domain": ".tracker.com",
            "path": "/",
            "secure": False,
            "http_only": False
        },
        {
            "name": "user_prefs",
            "value": "theme=dark;lang=en",
            "domain": "example.com",
            "path": "/",
            "secure": True,
            "http_only": False
        }
    ]
    
    for c_data in demo_cookies:
        cookie = Cookie(
            name=c_data["name"],
            value=c_data["value"],
            domain=c_data["domain"],
            path=c_data.get("path", "/"),
            secure=c_data.get("secure", False),
            http_only=c_data.get("http_only", False),
            cookie_type=CookieType.THIRD_PARTY if c_data["domain"].startswith(".") else CookieType.SESSION
        )
        cookies.append(cookie)
    
    # Write output
    with open(output_path, "w") as f:
        json.dump([c.to_dict() for c in cookies], f, indent=2)
    
    return cookies
