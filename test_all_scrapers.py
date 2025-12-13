"""
Comprehensive test of all scraper functions
Tests each site individually to see which ones work
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.osint.modules.advanced_scraper import AdvancedScraper

print("="*70)
print("  TESTING INDIVIDUAL SCRAPERS")
print("="*70)

scraper = AdvancedScraper()

# Test data
test_email = "kurtwarner.com@gmail.com"
test_phone = "+15551234567"
test_name = "Kurt Warner"
test_username = "dopaminefiends"

print("\n" + "="*70)
print("  US PEOPLE SEARCH SITES")
print("="*70)

# Test each scraper individually
scrapers_to_test = [
    ("Spokeo", lambda: scraper.scrape_spokeo(name=test_name, email=test_email)),
    ("Pipl", lambda: scraper.scrape_pipl(name=test_name, email=test_email)),
    ("WhitePages", lambda: scraper.scrape_whitepages(name=test_name, phone=test_phone)),
    ("BeenVerified", lambda: scraper.scrape_beenverified(name=test_name, phone=test_phone)),
    ("TruthFinder", lambda: scraper.scrape_truthfinder(name=test_name)),
    ("Intelius", lambda: scraper.scrape_intelius(name=test_name, phone=test_phone)),
    ("ZabaSearch", lambda: scraper.scrape_zabasearch(name=test_name, phone=test_phone)),
]

print("\n" + "="*70)
print("  PHONE LOOKUP SITES")
print("="*70)

phone_scrapers = [
    ("TrueCaller", lambda: scraper.scrape_truecaller(test_phone)),
    ("SpyDialer", lambda: scraper.scrape_spydialer(test_phone)),
    ("Sync.ME", lambda: scraper.scrape_sync_me(test_phone)),
]

print("\n" + "="*70)
print("  EMAIL SEARCH SITES")
print("="*70)

email_scrapers = [
    ("Hunter.io", lambda: scraper.scrape_hunter_io(test_email)),
    ("EmailRep", lambda: scraper.scrape_emailrep(test_email)),
    ("Clearbit", lambda: scraper.scrape_clearbit(test_email)),
    ("DeHashed", lambda: scraper.check_dehashed_preview(test_email)),
]

print("\n" + "="*70)
print("  INTERNATIONAL SITES")
print("="*70)

intl_scrapers = [
    ("192.com (UK)", lambda: scraper.scrape_192_uk(test_name)),
    ("Infobel", lambda: scraper.scrape_infobel(test_phone)),
]

print("\n" + "="*70)
print("  SOCIAL MEDIA")
print("="*70)

social_scrapers = [
    ("Social Searcher", lambda: scraper.scrape_social_searcher(test_username)),
]

# Test all scrapers
all_scrapers = scrapers_to_test + phone_scrapers + email_scrapers + intl_scrapers + social_scrapers

working = []
blocked = []
errors = []

for name, func in all_scrapers:
    print(f"\nTesting {name}...")
    try:
        result = func()
        
        if 'error' in result and '403' in result.get('error', ''):
            blocked.append(name)
            print(f"   ❌ BLOCKED (403)")
        elif 'error' in result:
            errors.append(name)
            print(f"   ⚠️  ERROR: {result['error'][:50]}")
        elif result['data']:
            working.append(name)
            print(f"   ✅ WORKING - Data: {result['data']}")
        else:
            print(f"   ⚪ No data found (might be working)")
    except Exception as e:
        errors.append(name)
        print(f"   💥 EXCEPTION: {str(e)[:50]}")

# Summary
print("\n" + "="*70)
print("  SUMMARY")
print("="*70)
print(f"\n✅ Working: {len(working)} sites")
for site in working:
    print(f"   • {site}")

print(f"\n❌ Blocked (403): {len(blocked)} sites")
for site in blocked:
    print(f"   • {site}")

print(f"\n⚠️  Errors: {len(errors)} sites")
for site in errors:
    print(f"   • {site}")

print(f"\n📊 Success Rate: {len(working)}/{len(all_scrapers)} ({100*len(working)//len(all_scrapers)}%)")
