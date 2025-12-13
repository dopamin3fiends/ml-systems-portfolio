"""Test free breach detection scrapers"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.osint.modules.advanced_scraper import AdvancedScraper

print("="*70)
print("  TESTING FREE BREACH DETECTION SCRAPERS")
print("="*70)

scraper = AdvancedScraper()

# Test with your known breached emails
test_emails = [
    "kurtwarnerrop@gmail.com",
    "kurtwarner.com@gmail.com"
]

for email in test_emails:
    print(f"\n{'='*70}")
    print(f"🔍 Testing: {email}")
    print(f"{'='*70}\n")
    
    # Test each breach checker
    results = []
    results.append(scraper.check_leakcheck(email))
    results.append(scraper.check_breachdirectory(email))
    results.append(scraper.check_emailrep_breaches(email))
    results.append(scraper.check_ghostproject(email))
    
    # Display results
    print(f"\n📊 BREACH DETECTION RESULTS:")
    for result in results:
        source = result.get('source', 'Unknown')
        print(f"\n{source}:")
        if result.get('error'):
            print(f"   ❌ Error: {result['error']}")
        elif result.get('data'):
            for key, value in result['data'].items():
                print(f"   {key}: {value}")
        else:
            print(f"   ⚪ No data")

print(f"\n{'='*70}")
print("BREACH TEST COMPLETE")
print(f"{'='*70}")
