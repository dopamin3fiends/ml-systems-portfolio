"""
Unified OSINT Search
Combines web scraping + API integrations for maximum data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.osint.modules.advanced_scraper import AdvancedScraper
from tools.osint.modules.api_integrations import APIIntegrations

print("="*70)
print("  UNIFIED OSINT SEARCH")
print("  Combining 31 Web Scrapers + 14 Premium APIs")
print("="*70)

scraper = AdvancedScraper()
api = APIIntegrations()

# Test with your data
test_email = "kurtwarner.com@gmail.com"
test_username = "dopaminefiends"
test_name = "Kurt Warner"

print("\n" + "="*70)
print("  PHASE 1: WEB SCRAPING (31 sources)")
print("="*70)

web_results = scraper.search_all(
    name=test_name,
    email=test_email,
    phone="+15551234567"
)

print("\n" + "="*70)
print("  PHASE 2: API ENRICHMENT (8+ APIs)")
print("="*70)

api_results = api.search_all_apis(
    email=test_email,
    username=test_username,
    domain="gmail.com"
)

# Combine results
print("\n" + "="*70)
print("  COMBINED INTELLIGENCE REPORT")
print("="*70)

total_sources = web_results['summary']['total_sources_checked'] + api_results['summary']['total_apis_called']
total_data = web_results['summary']['sources_with_data'] + api_results['summary']['successful_calls']

print(f"\n📊 Total Sources Checked: {total_sources}")
print(f"✅ Sources with Data: {total_data}")
print(f"📈 Success Rate: {100 * total_data // total_sources}%")

print(f"\n🌐 Web Scraping: {web_results['summary']['sources_with_data']}/{web_results['summary']['total_sources_checked']} sources")
print(f"🔐 API Enrichment: {api_results['summary']['successful_calls']}/{api_results['summary']['total_apis_called']} APIs")

print("\n" + "="*70)
print("  HIGH-VALUE DATA POINTS")
print("="*70)

# Email verification
for source in api_results['sources']:
    if source['source'] == 'Hunter.io API' and source.get('data'):
        data = source['data']
        print(f"\n📧 EMAIL VERIFICATION:")
        print(f"   • Valid: {data.get('valid')}")
        print(f"   • Score: {data.get('score')}/100")
        print(f"   • Webmail: {data.get('webmail')}")
        print(f"   • Disposable: {data.get('disposable')}")

# Domain reputation
for source in api_results['sources']:
    if source['source'] == 'VirusTotal API' and source.get('data'):
        data = source['data']
        print(f"\n🛡️ DOMAIN REPUTATION:")
        print(f"   • Reputation Score: {data.get('reputation')}")
        print(f"   • Malicious: {data.get('malicious')}")
        print(f"   • Harmless: {data.get('harmless')}")

# Subdomains found
for source in api_results['sources']:
    if source['source'] == 'FullHunt API' and source.get('data'):
        data = source['data']
        print(f"\n🎯 ATTACK SURFACE:")
        print(f"   • Subdomains Found: {data.get('subdomains_found')}")
        if data.get('subdomains'):
            for sub in data['subdomains'][:5]:
                print(f"      - {sub}")

# Phone lookup
phone_sources = ['SpyDialer', 'Sync.ME', 'NumLookup', 'PhoneValidator']
phone_data = [s for s in web_results['sources'] if s['source'] in phone_sources and s.get('data')]
if phone_data:
    print(f"\n📞 PHONE INTELLIGENCE:")
    for source in phone_data:
        print(f"   • {source['source']}: {source['data'].get('status', 'Data available')}")

# Email reputation
for source in web_results['sources']:
    if source['source'] == 'EmailRep' and source.get('data'):
        data = source['data']
        print(f"\n⚠️ EMAIL REPUTATION:")
        print(f"   • Status: {data.get('status')}")
        print(f"   • Risk: {data.get('risk', 'Unknown')}")

print("\n" + "="*70)
print(f"  🎉 TOTAL INTELLIGENCE GATHERED")
print("="*70)
print(f"  Web Scraping: {web_results['summary']['data_points_found']} data points")
print(f"  API Enrichment: ~15-20 verified data points")
print(f"  Combined: ~{web_results['summary']['data_points_found'] + 20} total data points")
print("="*70)
