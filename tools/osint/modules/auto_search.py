"""
Auto-Search Module
Automatically searches OSINT resources for a target
"""

import requests
import re
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote, urlencode
import time


class AutoSearch:
    """Automatically search multiple OSINT resources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.timeout = 10
    
    def search_whitepages(self, name: str = None, phone: str = None, address: str = None) -> Dict:
        """Search WhitePages"""
        results = {
            'site': 'WhitePages',
            'url': 'https://www.whitepages.com',
            'found': False,
            'data': {}
        }
        
        try:
            if phone:
                # Phone lookup
                clean_phone = re.sub(r'\D', '', phone)
                url = f"https://www.whitepages.com/phone/{clean_phone}"
                results['search_url'] = url
                
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 200 and 'no results' not in response.text.lower():
                    results['found'] = True
                    results['data']['status'] = 'Phone number found'
            
            elif name:
                # Name search
                url = f"https://www.whitepages.com/name/{quote(name)}"
                results['search_url'] = url
                
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    # Simple check - if page loads, there might be results
                    if 'people' in response.text.lower():
                        results['found'] = True
                        results['data']['status'] = 'Potential matches found'
        
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def search_spokeo(self, email: str = None, phone: str = None, name: str = None) -> Dict:
        """Search Spokeo (premium, returns search URL)"""
        results = {
            'site': 'Spokeo',
            'url': 'https://www.spokeo.com',
            'found': 'unknown',
            'note': 'Premium service - manual verification required'
        }
        
        if email:
            results['search_url'] = f"https://www.spokeo.com/email-search?q={quote(email)}"
        elif phone:
            clean_phone = re.sub(r'\D', '', phone)
            results['search_url'] = f"https://www.spokeo.com/reverse-phone-lookup?q={clean_phone}"
        elif name:
            results['search_url'] = f"https://www.spokeo.com/people-search?q={quote(name)}"
        
        return results
    
    def search_pipl(self, name: str = None, email: str = None, username: str = None) -> Dict:
        """Search Pipl"""
        results = {
            'site': 'Pipl',
            'url': 'https://pipl.com',
            'found': 'unknown',
            'note': 'Premium service - manual verification required'
        }
        
        params = {}
        if name:
            params['q'] = name
        elif email:
            params['q'] = email
        elif username:
            params['q'] = username
        
        if params:
            results['search_url'] = f"https://pipl.com/search/?{urlencode(params)}"
        
        return results
    
    def search_haveibeenpwned(self, email: str) -> Dict:
        """Check Have I Been Pwned"""
        results = {
            'site': 'Have I Been Pwned',
            'url': 'https://haveibeenpwned.com',
            'found': False,
            'breaches': []
        }
        
        try:
            # Use HIBP API v3
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{quote(email)}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                breaches = response.json()
                results['found'] = True
                results['breach_count'] = len(breaches)
                results['breaches'] = [b.get('Name', 'Unknown') for b in breaches[:5]]
            elif response.status_code == 404:
                results['found'] = False
                results['breach_count'] = 0
        
        except Exception as e:
            results['error'] = str(e)
            results['search_url'] = f"https://haveibeenpwned.com/account/{quote(email)}"
        
        return results
    
    def search_tineye(self, image_url: str) -> Dict:
        """Search TinEye for image"""
        results = {
            'site': 'TinEye',
            'url': 'https://tineye.com',
            'search_url': f"https://tineye.com/search?url={quote(image_url)}",
            'note': 'Reverse image search - click URL to view results'
        }
        return results
    
    def search_google_images(self, query: str) -> Dict:
        """Search Google Images"""
        results = {
            'site': 'Google Images',
            'url': 'https://images.google.com',
            'search_url': f"https://images.google.com/search?q={quote(query)}",
            'note': 'Manual verification required'
        }
        return results
    
    def search_radaris(self, name: str = None, phone: str = None, address: str = None) -> Dict:
        """Search Radaris"""
        results = {
            'site': 'Radaris',
            'url': 'https://radaris.com',
            'found': 'unknown'
        }
        
        if phone:
            clean_phone = re.sub(r'\D', '', phone)
            results['search_url'] = f"https://radaris.com/phone/{clean_phone}"
        elif name:
            results['search_url'] = f"https://radaris.com/p/{quote(name)}/"
        elif address:
            results['search_url'] = f"https://radaris.com/address/{quote(address)}"
        
        return results
    
    def search_zabasearch(self, name: str = None, phone: str = None) -> Dict:
        """Search ZabaSearch"""
        results = {
            'site': 'ZabaSearch',
            'url': 'https://www.zabasearch.com',
            'found': 'unknown'
        }
        
        if name:
            results['search_url'] = f"https://www.zabasearch.com/people/{quote(name)}/"
        elif phone:
            clean_phone = re.sub(r'\D', '', phone)
            results['search_url'] = f"https://www.zabasearch.com/phone/{clean_phone}/"
        
        return results
    
    def search_facebook_directory(self, name: str) -> Dict:
        """Search Facebook People Directory"""
        results = {
            'site': 'Facebook Directory',
            'url': 'https://www.facebook.com/directory/people/',
            'search_url': f"https://www.facebook.com/search/people/?q={quote(name)}",
            'note': 'Login may be required for full results'
        }
        return results
    
    def auto_search_email(self, email: str) -> List[Dict]:
        """Auto-search multiple sites for email"""
        searches = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(self.search_haveibeenpwned, email): 'hibp',
                executor.submit(self.search_spokeo, email=email): 'spokeo',
                executor.submit(self.search_pipl, email=email): 'pipl',
            }
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    searches.append(result)
                except Exception as e:
                    pass
        
        return searches
    
    def auto_search_phone(self, phone: str) -> List[Dict]:
        """Auto-search multiple sites for phone number"""
        searches = []
        
        search_funcs = [
            lambda: self.search_whitepages(phone=phone),
            lambda: self.search_spokeo(phone=phone),
            lambda: self.search_radaris(phone=phone),
            lambda: self.search_zabasearch(phone=phone),
        ]
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(func) for func in search_funcs]
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    searches.append(result)
                except Exception as e:
                    pass
        
        return searches
    
    def auto_search_name(self, name: str) -> List[Dict]:
        """Auto-search multiple sites for name"""
        searches = []
        
        search_funcs = [
            lambda: self.search_whitepages(name=name),
            lambda: self.search_spokeo(name=name),
            lambda: self.search_pipl(name=name),
            lambda: self.search_radaris(name=name),
            lambda: self.search_zabasearch(name=name),
            lambda: self.search_facebook_directory(name),
        ]
        
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(func) for func in search_funcs]
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    searches.append(result)
                except Exception as e:
                    pass
        
        return searches
    
    def auto_search_image(self, image_url: str) -> List[Dict]:
        """Auto-search for image across services"""
        return [
            self.search_tineye(image_url),
            self.search_google_images(image_url),
        ]
    
    def search_all(self, target: str, target_type: str) -> List[Dict]:
        """
        Search all available resources for target
        
        Args:
            target: Email, phone, name, or image URL
            target_type: 'email', 'phone', 'name', or 'image'
        """
        print(f"\n🔍 Auto-searching {target_type}: {target}")
        print("⏳ This may take 10-30 seconds...\n")
        
        if target_type == 'email':
            results = self.auto_search_email(target)
        elif target_type == 'phone':
            results = self.auto_search_phone(target)
        elif target_type == 'name':
            results = self.auto_search_name(target)
        elif target_type == 'image':
            results = self.auto_search_image(target)
        else:
            return []
        
        return results
