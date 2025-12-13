from tools.osint.modules.advanced_scraper import AdvancedScraper

print("="*70)
print("  TESTING ADVANCED OSINT SCRAPER")
print("="*70)

scraper = AdvancedScraper()

# Test with YOUR REAL data
results = scraper.search_all(
    name="Kurt Warner",
    email="kurtwarner.com@gmail.com", 
    phone="+15551234567",
    location="California"
)

print("\n" + "="*70)
print("  FINAL RESULTS")
print("="*70)
print(f"\nSources checked: {results['summary']['total_sources_checked']}")
print(f"Sources with data: {results['summary']['sources_with_data']}")
print(f"Total data points: {results['summary']['data_points_found']}")
print(f"Errors: {results['summary']['sources_with_errors']}")

print("\n" + "="*70)
print("  DATA BY SOURCE")
print("="*70)

for source in results['sources']:
    if source.get('data') and len(source['data']) > 0:
        print(f"\n{source['source']}:")
        for key, value in source['data'].items():
            print(f"  • {key}: {value}")
