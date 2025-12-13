"""
Test API integrations with real data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.osint.modules.api_integrations import APIIntegrations

print("="*70)
print("  TESTING PREMIUM OSINT APIs")
print("="*70)

api = APIIntegrations()

# Test with your real data
email = "kurtwarner.com@gmail.com"
username = "dopaminefiends"
domain = "gmail.com"

results = api.search_all_apis(
    email=email,
    username=username,
    domain=domain
)

print("\n" + "="*70)
print("  DETAILED RESULTS")
print("="*70)

for source in results['sources']:
    print(f"\n{'='*70}")
    print(f"  {source['source']}")
    print(f"{'='*70}")
    
    if source.get('error'):
        print(f"  ❌ Error: {source['error']}")
    elif source.get('data'):
        for key, value in source['data'].items():
            if isinstance(value, list):
                print(f"  • {key}: {len(value)} items")
                for item in value[:3]:  # Show first 3
                    print(f"      - {item}")
            else:
                print(f"  • {key}: {value}")
    else:
        print(f"  ⚪ No data returned")

print("\n" + "="*70)
print("  SUMMARY")
print("="*70)
print(f"Total APIs: {results['summary']['total_apis_called']}")
print(f"✅ Successful: {results['summary']['successful_calls']}")
print(f"❌ Failed: {results['summary']['failed_calls']}")
print(f"Success Rate: {100 * results['summary']['successful_calls'] // results['summary']['total_apis_called']}%")
