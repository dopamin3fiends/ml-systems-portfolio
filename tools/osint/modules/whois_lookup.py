"""
WHOIS Lookup Module
Query domain registration information
"""

import socket
from typing import Dict, Optional
from datetime import datetime


class WhoisLookup:
    """Perform WHOIS queries on domains"""
    
    def __init__(self):
        self.whois_servers = {
            'com': 'whois.verisign-grs.com',
            'net': 'whois.verisign-grs.com',
            'org': 'whois.pir.org',
            'io': 'whois.nic.io',
            'ai': 'whois.nic.ai',
            'default': 'whois.iana.org'
        }
    
    def get_whois_server(self, domain: str) -> str:
        """Get appropriate WHOIS server for domain TLD"""
        tld = domain.split('.')[-1].lower()
        return self.whois_servers.get(tld, self.whois_servers['default'])
    
    def query_whois(self, domain: str, server: str, port: int = 43) -> Optional[str]:
        """Query WHOIS server"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                s.connect((server, port))
                s.send(f"{domain}\r\n".encode())
                
                response = b''
                while True:
                    data = s.recv(4096)
                    if not data:
                        break
                    response += data
                
                return response.decode('utf-8', errors='ignore')
        
        except Exception as e:
            return None
    
    def parse_whois_response(self, response: str) -> Dict:
        """Parse WHOIS response into structured data"""
        data = {
            'registrar': None,
            'creation_date': None,
            'expiration_date': None,
            'updated_date': None,
            'name_servers': [],
            'status': []
        }
        
        if not response:
            return data
        
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if ':' not in line:
                continue
            
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            
            if not value:
                continue
            
            if 'registrar' in key and not data['registrar']:
                data['registrar'] = value
            elif 'creation date' in key or 'created' in key:
                data['creation_date'] = value
            elif 'expir' in key:
                data['expiration_date'] = value
            elif 'updated' in key or 'modified' in key:
                data['updated_date'] = value
            elif 'name server' in key or 'nserver' in key:
                if value and value not in data['name_servers']:
                    data['name_servers'].append(value)
            elif 'status' in key:
                if value and value not in data['status']:
                    data['status'].append(value)
        
        return data
    
    def query(self, domain: str) -> Dict:
        """Perform full WHOIS lookup"""
        # Clean domain
        domain = domain.lower().strip()
        if domain.startswith('http://') or domain.startswith('https://'):
            domain = domain.split('://')[1]
        if '/' in domain:
            domain = domain.split('/')[0]
        
        results = {
            'domain': domain,
            'registered': False,
            'whois_server': None,
            'raw_response': None
        }
        
        # Get WHOIS server
        whois_server = self.get_whois_server(domain)
        results['whois_server'] = whois_server
        
        # Query WHOIS
        response = self.query_whois(domain, whois_server)
        
        if response:
            results['raw_response'] = response
            results['registered'] = 'no match' not in response.lower()
            
            # Parse response
            parsed = self.parse_whois_response(response)
            results.update(parsed)
        
        return results
