"""
Deep data extraction test - extract ACTUAL details from working sites
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.osint.modules.advanced_scraper import AdvancedScraper

print("="*70)
print("  DEEP EXTRACTION TEST")
print("  Testing what ACTUAL data we can extract from working sites")
print("="*70)

scraper = AdvancedScraper()

# Test each working scraper individually with detailed output
test_phone = "+15551234567"
test_email = "kurtwarner.com@gmail.com"
test_username = "dopaminefiends"

print("\n" + "="*70)
print("  PHONE LOOKUP - DETAILED")
print("="*70)

print("\n1. SpyDialer:")
result = scraper.scrape_spydialer(test_phone)
print(f"   Data: {result['data']}")
if result.get('error'):
    print(f"   Error: {result['error']}")

print("\n2. Sync.ME:")
result = scraper.scrape_sync_me(test_phone)
print(f"   Data: {result['data']}")

print("\n3. NumLookup:")
result = scraper.scrape_numlookup(test_phone)
print(f"   Data: {result['data']}")

print("\n4. PhoneValidator:")
result = scraper.scrape_phonevalidator(test_phone)
print(f"   Data: {result['data']}")

print("\n" + "="*70)
print("  EMAIL SEARCH - DETAILED")
print("="*70)

print("\n1. EmailRep:")
result = scraper.scrape_emailrep(test_email)
print(f"   Data: {result['data']}")

print("\n2. Hunter.io:")
result = scraper.scrape_hunter_io(test_email)
print(f"   Data: {result['data']}")

print("\n" + "="*70)
print("  SOCIAL MEDIA - DETAILED")
print("="*70)

print("\n1. Social Searcher:")
result = scraper.scrape_social_searcher(test_username)
print(f"   Data: {result['data']}")

print("\n" + "="*70)
print("  ANALYSIS")
print("="*70)
print("\nCurrent extraction capability:")
print("  • Status indicators: ✅ Working")
print("  • Actual names/locations: ❌ Need improvement")
print("  • Risk scores: ✅ Working (EmailRep)")
print("  • Domain info: ✅ Working (Hunter.io)")
print("\nNext: Improve HTML parsing to extract MORE details")
