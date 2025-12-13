"""Test HaveIBeenPwned API for breach detection"""
import requests
import time

def check_hibp(email):
    """Check HaveIBeenPwned for breaches"""
    print(f"\n{'='*70}")
    print(f"🔍 Checking: {email}")
    print(f"{'='*70}")
    
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        'User-Agent': 'OSINT-Tool-Pro-Breach-Checker'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            breaches = response.json()
            print(f"\n🚨 BREACHED! Found in {len(breaches)} breaches:")
            for breach in breaches[:5]:  # Show first 5
                print(f"   • {breach.get('Name')} - {breach.get('BreachDate')}")
                print(f"     Data: {', '.join(breach.get('DataClasses', [])[:5])}")
            return True
        elif response.status_code == 404:
            print("✅ Not found in any breaches (or rate limited)")
            return False
        else:
            print(f"⚠️  Unexpected response: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Test your emails
emails = [
    "kurtwarnerrop@gmail.com",
    "warnerxkurt@gmail.com",
    "kurtwarn3r@gmail.com",
    "kurt.warner001@gmail.com",
    "kurtwarner.com@gmail.com"
]

print("="*70)
print("  TESTING HAVEIBEENPWNED BREACH DETECTION")
print("="*70)
print("\n⚠️  Note: HIBP rate limits to 1 request every 1.5 seconds")

for email in emails:
    check_hibp(email)
    time.sleep(2)  # Rate limit

print(f"\n{'='*70}")
print("BREACH CHECK COMPLETE")
print(f"{'='*70}")
