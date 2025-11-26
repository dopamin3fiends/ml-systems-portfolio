"""
Cookie enrichment - adds company/purpose metadata.
"""

import json
from pathlib import Path
from typing import Dict, List

try:
    from models import Cookie, CookieType, RiskLevel
except ImportError:
    from .models import Cookie, CookieType, RiskLevel


COOKIE_DATABASE = {
    "_ga": {"company": "Google Analytics", "purpose": "Analytics - tracks user behavior"},
    "_gid": {"company": "Google Analytics", "purpose": "Analytics - distinguishes users"},
    "_fbp": {"company": "Facebook", "purpose": "Advertising - tracks conversions"},
    "session": {"company": "Application", "purpose": "Session management"},
    "tracking": {"company": "Third-party Tracker", "purpose": "User tracking"}
}


def enrich_cookies_file(input_path: str, output_path: str) -> List[Dict]:
    """Enrich cookies with company/purpose metadata."""
    with open(input_path, "r") as f:
        cookies = json.load(f)
    
    enriched = []
    for cookie in cookies:
        name = cookie["name"]
        
        # Check database for known patterns
        for pattern, metadata in COOKIE_DATABASE.items():
            if pattern in name.lower():
                cookie["company"] = metadata["company"]
                cookie["purpose"] = metadata["purpose"]
                break
        
        if not cookie.get("company"):
            cookie["company"] = "Unknown"
            cookie["purpose"] = "Unknown"
        
        enriched.append(cookie)
    
    with open(output_path, "w") as f:
        json.dump(enriched, f, indent=2)
    
    return enriched
