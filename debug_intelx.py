"""Debug IntelX API to see actual response"""
import requests
import os
import sys

# Load .env manually
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()

api_key = os.getenv('INTELX_API_KEY', '')

print(f"API Key loaded: {'YES' if api_key else 'NO'}")
print(f"API Key (first 10 chars): {api_key[:10]}...")

email = "kurtwarnerrop@gmail.com"
url = "https://2.intelx.io/phonebook/search"
headers = {'x-key': api_key}
payload = {
    'term': email,
    'maxresults': 10,
    'media': 0,
    'target': 1
}

print(f"\nSending request to: {url}")
print(f"Headers: {headers}")
print(f"Payload: {payload}")

try:
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    print(f"\n✅ Response Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"\nRaw Response Text:")
    print(response.text[:500])
    
    if response.text:
        try:
            data = response.json()
            print(f"\nParsed JSON:")
            print(data)
        except:
            print("\n❌ Could not parse as JSON")
    else:
        print("\n❌ Empty response body")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
