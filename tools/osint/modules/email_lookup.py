"""
Email Lookup Module
Validates emails and searches for associated information
"""

import re
import requests
from typing import Dict, List, Optional


class EmailLookup:
    """Lookup email information from various sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OSINT-Tool/1.0'
        })
    
    def validate_format(self, email: str) -> bool:
        """Check if email format is valid"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def extract_domain(self, email: str) -> str:
        """Extract domain from email"""
        return email.split('@')[1] if '@' in email else ''
    
    def check_disposable(self, domain: str) -> bool:
        """Check if domain is a disposable email provider"""
        disposable_domains = [
            'tempmail.com', 'guerrillamail.com', '10minutemail.com',
            'mailinator.com', 'throwaway.email', 'temp-mail.org'
        ]
        return domain.lower() in disposable_domains
    
    def guess_social_profiles(self, email: str) -> Dict[str, str]:
        """Guess potential social media profiles based on email"""
        username = email.split('@')[0]
        profiles = {
            'GitHub': f'https://github.com/{username}',
            'Twitter': f'https://twitter.com/{username}',
            'LinkedIn': f'https://linkedin.com/in/{username}',
            'Instagram': f'https://instagram.com/{username}',
            'Reddit': f'https://reddit.com/user/{username}'
        }
        return profiles
    
    def investigate(self, email: str) -> Dict:
        """Run full email investigation"""
        domain = self.extract_domain(email)
        
        results = {
            'email': email,
            'valid_format': self.validate_format(email),
            'domain': domain,
            'disposable': self.check_disposable(domain),
            'social_profiles': self.guess_social_profiles(email),
            'recommendations': []
        }
        
        # Add recommendations
        if not results['valid_format']:
            results['recommendations'].append('Invalid email format')
        if results['disposable']:
            results['recommendations'].append('Disposable email detected - likely temporary')
        
        return results
