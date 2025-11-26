"""
Risk scanner - analyzes cookies for privacy/security risks.
"""

import json
from pathlib import Path
from typing import Dict, List

try:
    from models import RiskLevel
except ImportError:
    from .models import RiskLevel


def scan_cookies_file(input_path: str, output_path: str) -> Dict:
    """Scan cookies for privacy/security risks."""
    with open(input_path, "r") as f:
        cookies = json.load(f)
    
    risks = []
    risk_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    
    for cookie in cookies:
        cookie_risks = []
        
        # Check for insecure cookies
        if not cookie.get("secure"):
            cookie_risks.append({
                "type": "insecure_transmission",
                "severity": "medium",
                "description": "Cookie transmitted over unencrypted HTTP"
            })
            risk_counts["medium"] += 1
        
        # Check for missing HttpOnly
        if not cookie.get("http_only") and "session" in cookie["name"].lower():
            cookie_risks.append({
                "type": "xss_vulnerable",
                "severity": "high",
                "description": "Session cookie accessible via JavaScript (XSS risk)"
            })
            risk_counts["high"] += 1
        
        # Check for third-party tracking
        if cookie.get("cookie_type") == "third_party":
            cookie_risks.append({
                "type": "privacy_tracking",
                "severity": "medium",
                "description": "Third-party tracking cookie"
            })
            risk_counts["medium"] += 1
        
        if cookie_risks:
            risks.append({
                "cookie_name": cookie["name"],
                "domain": cookie["domain"],
                "risks": cookie_risks
            })
    
    # Overall risk level
    if risk_counts["critical"] > 0:
        overall_risk = "CRITICAL"
    elif risk_counts["high"] > 0:
        overall_risk = "HIGH"
    elif risk_counts["medium"] > 0:
        overall_risk = "MEDIUM"
    else:
        overall_risk = "LOW"
    
    report = {
        "total_cookies_scanned": len(cookies),
        "cookies_with_risks": len(risks),
        "overall_risk_level": overall_risk,
        "risk_counts": risk_counts,
        "detailed_risks": risks
    }
    
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    
    return report
