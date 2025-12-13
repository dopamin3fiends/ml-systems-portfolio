"""
Bulk email search with pivot engine
Testing multiple email variations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.osint.modules.pivot_engine import PivotEngine

print("="*70)
print("  BULK EMAIL PIVOT SEARCH")
print("="*70)

# Your email variations
emails = [
    "kurtwarnerrop@gmail.com",
    "warnerxkurt@gmail.com", 
    "kurtwarn3r@gmail.com",
    "kurt.warner001@gmail.com"
]

engine = PivotEngine()

for email in emails:
    print(f"\n{'='*70}")
    print(f"  SEARCHING: {email}")
    print(f"{'='*70}")
    
    results = engine.pivot_search(
        initial_query=email,
        query_type="email",
        max_depth=2
    )
    
    # Show summary for this email
    print(f"\n📊 RESULTS FOR {email}:")
    print(f"   • Names found: {len(engine.discovered['names'])}")
    print(f"   • Emails found: {len(engine.discovered['emails'])}")
    print(f"   • Phones found: {len(engine.discovered['phones'])}")
    print(f"   • Usernames found: {len(engine.discovered['usernames'])}")
    print(f"   • Addresses found: {len(engine.discovered['addresses'])}")
    
    if engine.discovered['names']:
        print(f"\n   Names discovered:")
        for name in list(engine.discovered['names'])[:5]:
            print(f"      - {name}")
    
    if engine.discovered['phones']:
        print(f"\n   Phones discovered:")
        for phone in list(engine.discovered['phones'])[:5]:
            print(f"      - {phone}")
    
    if engine.discovered['usernames']:
        print(f"\n   Usernames discovered:")
        for username in list(engine.discovered['usernames'])[:5]:
            print(f"      - {username}")
    
    # Reset for next search
    engine = PivotEngine()

print(f"\n{'='*70}")
print("  BULK SEARCH COMPLETE")
print(f"{'='*70}")
