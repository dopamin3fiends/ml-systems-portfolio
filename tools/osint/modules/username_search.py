"""
Username Search Module
Search for username across multiple platforms
"""

import requests
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed


class UsernameSearch:
    """Search for username across social media and websites"""
    
    def __init__(self):
        self.platforms = [
            {'name': 'GitHub', 'url': 'https://github.com/{}', 'check_url': 'https://api.github.com/users/{}'},
            {'name': 'Twitter', 'url': 'https://twitter.com/{}', 'check_url': 'https://twitter.com/{}'},
            {'name': 'Instagram', 'url': 'https://instagram.com/{}', 'check_url': 'https://www.instagram.com/{}'},
            {'name': 'Reddit', 'url': 'https://reddit.com/user/{}', 'check_url': 'https://www.reddit.com/user/{}/about.json'},
            {'name': 'LinkedIn', 'url': 'https://linkedin.com/in/{}', 'check_url': None},
            {'name': 'Facebook', 'url': 'https://facebook.com/{}', 'check_url': None},
            {'name': 'YouTube', 'url': 'https://youtube.com/@{}', 'check_url': None},
            {'name': 'TikTok', 'url': 'https://tiktok.com/@{}', 'check_url': None},
            {'name': 'Twitch', 'url': 'https://twitch.tv/{}', 'check_url': 'https://www.twitch.tv/{}'},
            {'name': 'Pinterest', 'url': 'https://pinterest.com/{}', 'check_url': None},
            {'name': 'Snapchat', 'url': 'https://snapchat.com/add/{}', 'check_url': None},
            {'name': 'Discord', 'url': 'discord.com/users/{}', 'check_url': None},
            {'name': 'Steam', 'url': 'https://steamcommunity.com/id/{}', 'check_url': None},
            {'name': 'DeviantArt', 'url': 'https://{}.deviantart.com', 'check_url': None},
            {'name': 'Medium', 'url': 'https://medium.com/@{}', 'check_url': None},
            {'name': 'Patreon', 'url': 'https://patreon.com/{}', 'check_url': None},
            {'name': 'Vimeo', 'url': 'https://vimeo.com/{}', 'check_url': None},
            {'name': 'SoundCloud', 'url': 'https://soundcloud.com/{}', 'check_url': None},
            {'name': 'Spotify', 'url': 'https://open.spotify.com/user/{}', 'check_url': None},
            {'name': 'Dribbble', 'url': 'https://dribbble.com/{}', 'check_url': None},
        ]
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def check_platform(self, username: str, platform: Dict) -> Dict:
        """Check if username exists on a platform"""
        result = {
            'name': platform['name'],
            'url': platform['url'].format(username),
            'exists': 'unknown',
            'status': None
        }
        
        # If no check URL, just return the profile URL
        if not platform['check_url']:
            result['exists'] = 'possible'
            return result
        
        try:
            check_url = platform['check_url'].format(username)
            response = self.session.get(check_url, timeout=5, allow_redirects=True)
            
            # GitHub API returns 404 if user doesn't exist
            if platform['name'] == 'GitHub':
                if response.status_code == 200:
                    result['exists'] = 'yes'
                    data = response.json()
                    result['status'] = f"Public repos: {data.get('public_repos', 0)}"
                else:
                    result['exists'] = 'no'
            
            # Reddit returns 404 in JSON if user doesn't exist
            elif platform['name'] == 'Reddit':
                if response.status_code == 200:
                    result['exists'] = 'yes'
                    data = response.json()
                    karma = data.get('data', {}).get('total_karma', 0)
                    result['status'] = f"Karma: {karma}"
                else:
                    result['exists'] = 'no'
            
            # For others, check status code
            elif response.status_code == 200:
                result['exists'] = 'likely'
            elif response.status_code == 404:
                result['exists'] = 'no'
            
        except Exception:
            result['exists'] = 'error'
        
        return result
    
    def search(self, username: str) -> Dict:
        """Search for username across all platforms"""
        results = {
            'username': username,
            'total_platforms': len(self.platforms),
            'found': [],
            'possible': [],
            'not_found': [],
            'errors': []
        }
        
        # Use ThreadPoolExecutor for parallel checking
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(self.check_platform, username, platform): platform
                for platform in self.platforms
            }
            
            for future in as_completed(futures):
                result = future.result()
                
                if result['exists'] == 'yes' or result['exists'] == 'likely':
                    results['found'].append(result)
                elif result['exists'] == 'possible':
                    results['possible'].append(result)
                elif result['exists'] == 'no':
                    results['not_found'].append(result)
                else:
                    results['errors'].append(result)
        
        results['found_count'] = len(results['found'])
        results['possible_count'] = len(results['possible'])
        
        return results
