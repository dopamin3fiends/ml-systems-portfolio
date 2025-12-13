"""Direct test of EmailRep API"""
import requests

email = "kurtwarnerrop@gmail.com"
url = f"https://emailrep.io/{email}"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',
    'Accept': 'application/json'
}

print(f"Testing: {email}")
print(f"URL: {url}\n")

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}\n")
    
    if response.status_code == 200:
        data = response.json()
        print("Raw JSON Response:")
        import json
        print(json.dumps(data, indent=2))
        
        print("\n" + "="*70)
        print("BREACH ANALYSIS:")
        print("="*70)
        
        details = data.get('details', {})
        print(f"\nCredentials Leaked: {details.get('credentials_leaked', 'N/A')}")
        print(f"Data Breach: {details.get('data_breach', 'N/A')}")
        print(f"Malicious Activity: {details.get('malicious_activity', 'N/A')}")
        print(f"Suspicious: {data.get('suspicious', 'N/A')}")
        print(f"Reputation: {data.get('reputation', 'N/A')}")
        print(f"First Seen: {details.get('first_seen', 'N/A')}")
        print(f"Last Seen: {details.get('last_seen', 'N/A')}")
        
    else:
        print(f"Error response: {response.text[:500]}")
        
except Exception as e:
    print(f"Exception: {e}")
