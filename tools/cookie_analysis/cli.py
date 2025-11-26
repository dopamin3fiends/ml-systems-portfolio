"""
Cookie Analysis Suite - Main CLI
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

try:
    from parser import parse_cookies_file
    from enricher import enrich_cookies_file
    from risk_scanner import scan_cookies_file
    from reporter import generate_summary_reports
except ImportError:
    from .parser import parse_cookies_file
    from .enricher import enrich_cookies_file
    from .risk_scanner import scan_cookies_file
    from .reporter import generate_summary_reports


def main():
    parser = argparse.ArgumentParser(description="Cookie Analysis Suite v2.0")
    parser.add_argument("--input", help="Input cookie file")
    parser.add_argument("--output-dir", default="output", help="Output directory")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode")
    
    args = parser.parse_args()
    
    # Setup output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("🍪 Cookie Analysis Suite v2.0")
    print("=" * 50)
    print()
    
    # Stage 1: Parse
    print("[1/4] Parsing cookies...")
    parsed_output = output_dir / f"cookies_parsed_{timestamp}.json"
    cookies = parse_cookies_file(args.input or "", str(parsed_output))
    print(f"      ✓ Parsed {len(cookies)} cookies")
    print()
    
    # Stage 2: Enrich
    print("[2/4] Enriching with metadata...")
    enriched_output = output_dir / f"cookies_enriched_{timestamp}.json"
    enriched = enrich_cookies_file(str(parsed_output), str(enriched_output))
    companies = set(c.get("company") for c in enriched if c.get("company") != "Unknown")
    print(f"      ✓ Identified {len(companies)} companies")
    print()
    
    # Stage 3: Risk scan
    print("[3/4] Scanning for risks...")
    risk_output = output_dir / f"cookie_risks_{timestamp}.json"
    risk_report = scan_cookies_file(str(enriched_output), str(risk_output))
    print(f"      ✓ Found {risk_report['cookies_with_risks']} privacy/security risks")
    print(f"      ✓ Overall risk level: {risk_report['overall_risk_level']}")
    print()
    
    # Stage 4: Reports
    print("[4/4] Generating summaries...")
    domain_output = output_dir / f"cookie_domain_summary_{timestamp}.json"
    company_output = output_dir / f"cookie_company_summary_{timestamp}.json"
    domain_summary, company_summary = generate_summary_reports(
        str(enriched_output), str(domain_output), str(company_output)
    )
    print(f"      ✓ {len(domain_summary)} domains analyzed")
    print(f"      ✓ {len(company_summary)} companies identified")
    print()
    
    print("=" * 50)
    print("✓ Analysis complete!")
    print()
    print(f"Output files in: {output_dir}/")
    print(f"  - Parsed cookies: {parsed_output.name}")
    print(f"  - Enriched data: {enriched_output.name}")
    print(f"  - Risk report: {risk_output.name}")
    print(f"  - Domain summary: {domain_output.name}")
    print(f"  - Company summary: {company_output.name}")


if __name__ == "__main__":
    main()
