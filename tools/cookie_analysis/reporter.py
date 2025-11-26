"""
Report generator - creates summary reports.
"""

import json
from pathlib import Path
from typing import Dict, List
from collections import defaultdict


def generate_summary_reports(input_path: str, domain_output: str, company_output: str):
    """Generate domain and company summary reports."""
    with open(input_path, "r") as f:
        cookies = json.load(f)
    
    # Domain summary
    domain_stats = defaultdict(lambda: {"count": 0, "companies": set(), "cookies": []})
    
    for cookie in cookies:
        domain = cookie["domain"]
        domain_stats[domain]["count"] += 1
        if cookie.get("company"):
            domain_stats[domain]["companies"].add(cookie["company"])
        domain_stats[domain]["cookies"].append(cookie["name"])
    
    domain_summary = [
        {
            "domain": domain,
            "cookie_count": stats["count"],
            "companies": list(stats["companies"]),
            "cookies": stats["cookies"]
        }
        for domain, stats in domain_stats.items()
    ]
    
    with open(domain_output, "w") as f:
        json.dump(domain_summary, f, indent=2)
    
    # Company summary
    company_stats = defaultdict(lambda: {"count": 0, "cookies": [], "domains": set()})
    
    for cookie in cookies:
        company = cookie.get("company", "Unknown")
        company_stats[company]["count"] += 1
        company_stats[company]["cookies"].append(cookie["name"])
        company_stats[company]["domains"].add(cookie["domain"])
    
    company_summary = [
        {
            "company": company,
            "cookie_count": stats["count"],
            "domains": list(stats["domains"]),
            "cookies": stats["cookies"]
        }
        for company, stats in company_stats.items()
    ]
    
    with open(company_output, "w") as f:
        json.dump(company_summary, f, indent=2)
    
    return domain_summary, company_summary
