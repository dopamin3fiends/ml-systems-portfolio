"""
Test breach detection APIs specifically
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.osint.modules.api_integrations import APIIntegrations

print("="*70)
print("  TESTING BREACH DETECTION APIs")
print("="*70)

api = APIIntegrations()

# Test emails known to be in breaches
test_emails = [
    "kurtwarnerrop@gmail.com",
    "warnerxkurt@gmail.com", 
    "kurtwarn3r@gmail.com",
    "kurt.warner001@gmail.com",
    "kurtwarner.com@gmail.com"  # Original one too
]

for email in test_emails:
    print(f"\n{'='*70}")
    print(f"Testing: {email}")
    print(f"{'='*70}")
    
    # Test IntelX
    print("\n🔒 IntelX Breach Search:")
    result = api.intelx_breach_search(email)
    if result.get('error'):
        print(f"   ❌ Error: {result['error']}")
    elif result.get('data'):
        print(f"   ✅ Data: {result['data']}")
    else:
        print(f"   ⚪ No data returned")
    
    # Also test Hunter.io verification
    print("\n🔍 Hunter.io Verification:")
    result = api.hunter_io_email(email)
    if result.get('error'):
        print(f"   ❌ Error: {result['error']}")
    elif result.get('data'):
        print(f"   ✅ Valid: {result['data'].get('valid')}")
        print(f"   ✅ Score: {result['data'].get('score')}/100")
        print(f"   ✅ Status: {result['data'].get('status')}")
    else:
        print(f"   ⚪ No data returned")

print(f"\n{'='*70}")
print("BREACH TEST COMPLETE")
print(f"{'='*70}")
