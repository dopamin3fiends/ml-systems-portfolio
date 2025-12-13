import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.osint.modules.pivot_engine import PivotEngine

print("="*70)
print("  TESTING PIVOTING ENGINE")
print("="*70)

engine = PivotEngine()

# Start with YOUR email where APIs will find subdomains and related data
print("\nStarting with email: kurtwarner.com@gmail.com")
report = engine.pivot_search("kurtwarner.com@gmail.com", "email", max_depth=2)

# Print full intelligence profile
engine.print_full_report()

print("\n" + "="*70)
print("  PIVOT COMPLETE!")
print("="*70)
