"""
Bulk Search (Pro Feature)
Search multiple targets simultaneously
"""

import json
from pathlib import Path
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


class BulkSearch:
    """Bulk search multiple targets (Pro feature)"""
    
    def __init__(self, osint_cli):
        """
        Args:
            osint_cli: Instance of OSINT CLI with all modules
        """
        self.cli = osint_cli
        self.results = []
    
    def load_targets(self, file_path: str) -> List[Dict]:
        """
        Load targets from CSV or JSON file
        
        CSV format:
        type,target
        email,test@example.com
        username,johndoe
        phone,555-123-4567
        
        JSON format:
        [
            {"type": "email", "target": "test@example.com"},
            {"type": "username", "target": "johndoe"}
        ]
        """
        file_path = Path(file_path)
        
        if file_path.suffix == '.json':
            with open(file_path, 'r') as f:
                return json.load(f)
        
        elif file_path.suffix == '.csv':
            targets = []
            with open(file_path, 'r') as f:
                lines = f.readlines()[1:]  # Skip header
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        targets.append({
                            'type': parts[0].strip(),
                            'target': parts[1].strip()
                        })
            return targets
        
        else:
            raise ValueError("File must be .json or .csv")
    
    def search_target(self, target_info: Dict) -> Dict:
        """Search a single target"""
        target_type = target_info['type']
        target = target_info['target']
        
        print(f"🔍 Searching {target_type}: {target}")
        
        result = {
            'type': target_type,
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'data': {}
        }
        
        try:
            if target_type == 'email':
                from ..modules.email_lookup import EmailLookup
                lookup = EmailLookup()
                result['data'] = lookup.investigate(target)
            
            elif target_type == 'username':
                from ..modules.username_search import UsernameSearch
                search = UsernameSearch()
                result['data'] = search.search(target)
            
            elif target_type == 'phone':
                from ..modules.auto_search import AutoSearch
                search = AutoSearch()
                result['data'] = search.auto_search_phone(target)
            
            result['status'] = 'success'
        
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        return result
    
    def bulk_search(self, targets: List[Dict], max_workers: int = 5) -> List[Dict]:
        """
        Search multiple targets in parallel
        
        Args:
            targets: List of {type, target} dicts
            max_workers: Max parallel searches
        
        Returns:
            List of results
        """
        print(f"\n🚀 Starting bulk search for {len(targets)} targets")
        print(f"⚡ Using {max_workers} parallel workers\n")
        
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.search_target, target): target
                for target in targets
            }
            
            completed = 0
            for future in as_completed(futures):
                completed += 1
                result = future.result()
                results.append(result)
                
                status_icon = '✅' if result['status'] == 'success' else '❌'
                print(f"[{completed}/{len(targets)}] {status_icon} {result['target']}")
        
        print(f"\n✨ Bulk search complete! {len(results)} results")
        return results
    
    def save_results(self, results: List[Dict], output_path: str):
        """Save bulk search results"""
        output_path = Path(output_path)
        
        summary = {
            'total_targets': len(results),
            'successful': sum(1 for r in results if r['status'] == 'success'),
            'failed': sum(1 for r in results if r['status'] == 'error'),
            'timestamp': datetime.now().isoformat(),
            'results': results
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {output_path}")
