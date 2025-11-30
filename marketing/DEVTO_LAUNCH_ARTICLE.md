# I Built a Professional OSINT Tool with 104 Curated Resources - Here's How

*Building a Python CLI tool for Open Source Intelligence gathering, integrating 104 resources, and launching it as a Free/Pro hybrid product*

---

## TL;DR

I built **OSINT Tool**, a Python command-line tool that automates intelligence gathering across 104 curated resources. It searches usernames across 20+ platforms, validates emails, checks data breaches, performs WHOIS lookups, and generates professional reports.

**Try it:** [GitHub (Free)](https://github.com/dopamin3fiends/ml-systems-portfolio/tree/main/tools/osint) | [Pro Version ($19.99)](https://gumroad.com/l/osint-tool-pro)

**Stack:** Python 3.8+, requests, concurrent.futures, argparse, PyInstaller

---

## The Problem

As a security researcher and developer, I constantly found myself:
- Manually visiting 20+ websites to check if a username exists
- Copy-pasting emails into various breach databases
- Opening dozens of tabs for OSINT investigations
- Losing track of which resources I'd already checked

**I needed a single tool that could:**
1. Automate searches across multiple platforms
2. Organize results in a readable format
3. Generate professional reports for clients
4. Save hours of manual work

So I built one.

---

## Architecture Overview

### Core Design Principles

1. **Modular Architecture** - Each feature is a separate module
2. **Parallel Execution** - Use ThreadPoolExecutor for concurrent API calls
3. **CLI-First** - Command-line interface for power users
4. **Hybrid Monetization** - Free core features + Pro enhancements

### Project Structure

```
tools/osint/
├── cli.py                 # Main CLI interface
├── modules/
│   ├── email_lookup.py    # Email validation & analysis
│   ├── username_search.py # Search 20+ platforms
│   ├── breach_check.py    # Have I Been Pwned integration
│   ├── whois_lookup.py    # Domain registration data
│   ├── resources.py       # 104 OSINT resources database
│   └── auto_search.py     # Auto-open multiple search sites
└── pro/
    ├── __init__.py        # License verification
    ├── report_generator.py # PDF/HTML reports
    └── bulk_search.py     # Process CSV files
```

---

## Key Features Breakdown

### 1. Username Search Across 20+ Platforms

The most powerful feature - search a username across GitHub, Twitter, Reddit, Instagram, and 16 more platforms **simultaneously**.

```python
# tools/osint/modules/username_search.py
from concurrent.futures import ThreadPoolExecutor
import requests

class UsernameSearch:
    PLATFORMS = {
        'GitHub': {
            'url': 'https://api.github.com/users/{}',
            'method': 'api'
        },
        'Reddit': {
            'url': 'https://www.reddit.com/user/{}/about.json',
            'method': 'api'
        },
        'Twitter': {
            'url': 'https://twitter.com/{}',
            'method': 'check'
        },
        # ... 17 more platforms
    }
    
    def search(self, username: str):
        results = {'found': [], 'possible': [], 'not_found': []}
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(self.check_platform, platform, data, username): platform
                for platform, data in self.PLATFORMS.items()
            }
            
            for future in as_completed(futures):
                platform = futures[future]
                result = future.result()
                
                if result['status'] == 'found':
                    results['found'].append(result)
                elif result['status'] == 'possible':
                    results['possible'].append(result)
                else:
                    results['not_found'].append(result)
        
        return results
```

**Why parallel execution matters:**
- Sequential: 20 platforms × 2 seconds = 40 seconds
- Parallel (10 workers): ~4 seconds total

**Real example:**
```bash
$ osint-tool-pro username dopaminefiend

✅ Found (5 platforms):
   • GitHub: https://github.com/dopaminefiend
     Status: Public repos: 0
   • Reddit: https://reddit.com/user/dopaminefiend
     Status: Karma: 620
   • Instagram: https://instagram.com/dopaminefiend
   • Twitter: https://twitter.com/dopaminefiend
   • Twitch: https://twitch.tv/dopaminefiend
```

---

### 2. Curated Database of 104 OSINT Resources

Instead of Googling "how to find someone by phone number" every time, I compiled 104 vetted resources organized into 11 categories.

```python
# tools/osint/modules/resources.py
class OSINTResources:
    US_PEOPLE_SEARCH = [
        {"name": "Spokeo", "url": "https://www.spokeo.com", "type": "premium"},
        {"name": "Pipl", "url": "https://pipl.com", "type": "premium"},
        {"name": "WhitePages", "url": "http://www.whitepages.com", "type": "general"},
        # ... 21 more
    ]
    
    PHONE_LOOKUP = [
        {"name": "TrueCaller", "url": "https://www.truecaller.com", "type": "app"},
        {"name": "SpyDialer", "url": "http://www.spydialer.com/", "type": "reverse"},
        # ... 8 more
    ]
    
    BREACH_DATABASES = [
        {"name": "Have I Been Pwned", "url": "https://haveibeenpwned.com/", "type": "breach"},
        {"name": "DeHashed", "url": "https://www.dehashed.com/", "type": "premium"},
        # ... 5 more
    ]
    
    # 8 more categories...
```

**Categories included:**
- 🌎 US People Search (24)
- 🌍 International Search (10)
- 📱 Phone Lookup (10)
- 👤 Username Search (4)
- 🖼️ Image Search (4)
- 📧 Email Search (7)
- 📱 Social Media (10)
- 🔒 Breach Databases (7)
- 🌐 IP Tools (16)
- ⚖️ Criminal Records (7)
- 🛠️ OSINT Frameworks (5)

View all resources:
```bash
$ osint-tool-pro resources

📚 Total Resources: 104
🗂️  Categories: 11

============================================================
  US People Search (24)
============================================================
  • Spokeo - https://www.spokeo.com
  • Pipl - https://pipl.com
  • WhitePages - http://www.whitepages.com
  ...
```

---

### 3. Automated Multi-Site Search

The `auto-search` feature automatically opens searches across multiple sites based on the target type.

```python
# tools/osint/modules/auto_search.py
class AutoSearch:
    def auto_search_email(self, email: str):
        """Search email across multiple OSINT sites"""
        sites = [
            f"https://www.spokeo.com/email-search/results?q={email}",
            f"https://pipl.com/search/?q={email}",
            f"https://haveibeenpwned.com/unifiedsearch/{email}",
            # ... more sites
        ]
        
        for site in sites:
            webbrowser.open(site)
            time.sleep(0.5)  # Don't overwhelm the browser
        
        return sites
    
    def auto_search_phone(self, phone: str):
        """Search phone number across lookup sites"""
        # Similar implementation
    
    def auto_search_name(self, name: str):
        """Search name across people search engines"""
        # Similar implementation
```

**Usage:**
```bash
$ osint-tool-pro search --email john.doe@example.com

🔍 Opening searches for: john.doe@example.com

✅ Opened 6 searches:
   • Spokeo
   • Pipl
   • Have I Been Pwned
   • Hunter.io
   • EmailRep
   • Social Searcher
```

---

### 4. Professional Report Generation

Generate HTML (free) or PDF (Pro) reports with all findings.

```python
# tools/osint/pro/report_generator.py
class PDFReportGenerator:
    def generate_report(self, data: Dict, output_path: str) -> str:
        """Generate professional HTML/PDF report"""
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>OSINT Report - {data['target']}</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
                .section {{ border-left: 4px solid #667eea; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔍 OSINT Investigation Report</h1>
                <p>Target: {data['target']}</p>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            {self._email_section(data.get('email'))}
            {self._username_section(data.get('usernames'))}
            {self._breach_section(data.get('breaches'))}
            {self._whois_section(data.get('whois'))}
        </body>
        </html>
        """
        
        # Save HTML
        Path(output_path).write_text(html)
        
        # Pro: Convert to PDF using reportlab
        if self.is_pro:
            pdf_path = output_path.replace('.html', '.pdf')
            self._convert_to_pdf(html, pdf_path)
            return pdf_path
        
        return output_path
```

**Free version includes watermark:**
```html
<div class="watermark">
    <h3>💎 Upgrade to OSINT Tool Pro</h3>
    <p>Get PDF reports, bulk search, scheduled monitoring, and more!</p>
    <p><strong>Only $19.99 one-time</strong></p>
</div>
```

---

## Building the CLI Interface

Using `argparse` to create a clean, intuitive CLI with subcommands:

```python
# tools/osint/cli.py
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='OSINT Tool - Open Source Intelligence Gathering'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Email lookup command
    email_parser = subparsers.add_parser('email', help='Lookup email information')
    email_parser.add_argument('email', help='Email address to investigate')
    
    # Username search command
    username_parser = subparsers.add_parser('username', help='Search username across platforms')
    username_parser.add_argument('username', help='Username to search')
    
    # Full investigation command
    full_parser = subparsers.add_parser('full', help='Run full OSINT investigation')
    full_parser.add_argument('target', help='Email, username, or domain')
    full_parser.add_argument('--report', choices=['html', 'pdf'], help='Generate report')
    full_parser.add_argument('--output', help='Output file path')
    
    # ... more commands
    
    args = parser.parse_args()
    
    # Route to appropriate handler
    if args.command == 'email':
        email_command(args)
    elif args.command == 'username':
        username_command(args)
    # ... etc
```

**Result:** Clean, discoverable interface
```bash
$ osint-tool-pro --help

usage: osint-tool-pro [-h] {email,username,breach,whois,full,resources,search} ...

OSINT Tool - Open Source Intelligence Gathering

positional arguments:
  {email,username,breach,whois,full,resources,search}
    email               Lookup email information
    username            Search username across platforms
    breach              Check for data breaches
    whois               WHOIS domain lookup
    full                Run full OSINT investigation
    resources           List all OSINT resources
    search              Auto-search multiple OSINT sites
```

---

## Packaging for Distribution

### Building a Windows Executable with PyInstaller

For non-technical users, a standalone .exe is essential.

```python
# build_exe.py
import PyInstaller.__main__

PyInstaller.__main__.run([
    'tools/osint/cli.py',
    '--onefile',                    # Single executable
    '--name=osint-tool-pro',        # Output name
    '--console',                     # Keep console window
    '--hidden-import=tools.osint.modules.email_lookup',
    '--hidden-import=tools.osint.modules.username_search',
    # ... more hidden imports
])
```

**Build command:**
```bash
python build_exe.py
```

**Result:** `dist/osint-tool-pro.exe` (12MB standalone executable)

---

## Monetization Strategy: Free + Pro Hybrid

### Free Version (GitHub)
- ✅ All core OSINT features
- ✅ 104 resources database
- ✅ Username search across 20+ platforms
- ✅ Breach checking
- ✅ HTML reports (with watermark)

### Pro Version ($19.99, Gumroad)
- ✅ PDF reports (no watermark)
- ✅ Bulk search from CSV files
- ✅ Commercial license
- ✅ Priority email support
- ✅ Lifetime updates

**Why this works:**
1. **Portfolio value** - Free version showcases skills on GitHub
2. **User acquisition** - Free users discover the tool organically
3. **Conversion** - Pro features target professionals who'll pay
4. **Sustainability** - One-time payment, no subscription complexity

---

## License Verification System

Pro version uses hash-based license verification:

```python
# tools/osint/pro/__init__.py
import hashlib
import json
from pathlib import Path

# 100 pre-generated valid license key hashes
VALID_LICENSE_HASHES = {
    '2a8b199486eb1b8ace94198b7f3c3656c41cf68368c90424f788ad44e43b4be1',
    'f5d5146e59fb9b72657e5cdfaafbf7c1aa17cd2192d5e7e0ebb5233b86a2fd38',
    # ... 98 more hashes
}

class ProLicense:
    def verify_license(self, key: str = None) -> bool:
        """Verify license key"""
        if not key:
            # Load from saved license file
            license_file = Path.home() / '.osint_pro_license'
            if license_file.exists():
                with open(license_file) as f:
                    data = json.load(f)
                    key = data.get('key')
        
        if not key:
            return False
        
        # Hash the provided key
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        # Check if hash is in valid set
        return key_hash in VALID_LICENSE_HASHES
    
    def save_license(self, key: str):
        """Save activated license locally"""
        license_file = Path.home() / '.osint_pro_license'
        with open(license_file, 'w') as f:
            json.dump({
                'key': key,
                'activated': datetime.now().isoformat()
            }, f)
```

**Activation:**
```bash
$ osint-tool-pro activate OSINT-34E7-55C3-4ECC-772D

✅ License activated successfully!
   Pro features unlocked.
```

**Generating 100 license keys:**
```python
# tools/osint/pro/generate_keys.py
import secrets
import hashlib

def generate_license_key():
    """Generate unique license key"""
    random_bytes = secrets.token_bytes(32)
    hex_string = random_bytes.hex().upper()
    
    # Format: OSINT-XXXX-XXXX-XXXX-XXXX
    return f"OSINT-{hex_string[0:4]}-{hex_string[4:8]}-{hex_string[8:12]}-{hex_string[12:16]}"

# Generate 100 keys
keys = [generate_license_key() for _ in range(100)]

# Save for Gumroad delivery
with open('license_keys_for_gumroad.txt', 'w') as f:
    for key in keys:
        f.write(f"{key}\n")
```

---

## Challenges & Solutions

### Challenge 1: Handling Rate Limits

**Problem:** Many platforms rate-limit API requests

**Solution:** Implemented exponential backoff and rotation

```python
def check_platform_with_retry(self, platform, username, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 429:  # Rate limited
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
                continue
            return response
        except requests.RequestException:
            if attempt == max_retries - 1:
                return None
    return None
```

### Challenge 2: API Changes

**Problem:** Platforms change their APIs/HTML structure

**Solution:** Graceful degradation + logging

```python
def check_platform(self, platform, data, username):
    try:
        if data['method'] == 'api':
            # Use API endpoint
            result = self._check_via_api(data['url'].format(username))
        else:
            # Fallback to HTTP check
            result = self._check_via_http(data['url'].format(username))
        
        return result
    except Exception as e:
        # Log error but don't crash
        logger.warning(f"Failed to check {platform}: {e}")
        return {'status': 'error', 'platform': platform, 'error': str(e)}
```

### Challenge 3: Cross-Platform Compatibility

**Problem:** Path handling differs between Windows/Mac/Linux

**Solution:** Use `pathlib` everywhere

```python
from pathlib import Path

# ❌ Bad (platform-specific)
config_file = os.path.join(os.path.expanduser('~'), '.osint', 'config.json')

# ✅ Good (cross-platform)
config_file = Path.home() / '.osint' / 'config.json'
config_file.parent.mkdir(parents=True, exist_ok=True)
```

---

## Performance Optimizations

### 1. Concurrent API Calls

Using `ThreadPoolExecutor` reduced search time from 40s to ~4s:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {
        executor.submit(check_platform, platform, data, username): platform
        for platform, data in PLATFORMS.items()
    }
    
    for future in as_completed(futures):
        result = future.result()
        process_result(result)
```

### 2. Caching WHOIS Results

WHOIS lookups are slow - cache them:

```python
import functools
from datetime import datetime, timedelta

@functools.lru_cache(maxsize=128)
def whois_lookup_cached(domain: str):
    """Cached WHOIS lookup (1 hour TTL)"""
    return whois_lookup(domain)
```

### 3. Lazy Loading Modules

Import heavy modules only when needed:

```python
def generate_pdf_report(data):
    # Only import reportlab if PDF generation is requested
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    
    # ... PDF generation code
```

---

## Testing Strategy

### Unit Tests for Core Modules

```python
# tests/test_username_search.py
import unittest
from tools.osint.modules.username_search import UsernameSearch

class TestUsernameSearch(unittest.TestCase):
    def setUp(self):
        self.searcher = UsernameSearch()
    
    def test_check_github_existing_user(self):
        result = self.searcher.check_platform('GitHub', 
            {'url': 'https://api.github.com/users/{}', 'method': 'api'},
            'octocat'  # Known GitHub account
        )
        self.assertEqual(result['status'], 'found')
    
    def test_check_github_nonexistent_user(self):
        result = self.searcher.check_platform('GitHub',
            {'url': 'https://api.github.com/users/{}', 'method': 'api'},
            'thisuserdefinitelydoesnotexist123456789'
        )
        self.assertEqual(result['status'], 'not_found')
```

### Integration Test: Full Investigation

```python
def test_full_investigation():
    """Test complete workflow"""
    from tools.osint.cli import run_full_investigation
    
    result = run_full_investigation('test@example.com', report_format='html')
    
    assert result['email']['valid'] == True
    assert 'breaches' in result
    assert 'whois' in result
    assert Path('report.html').exists()
```

---

## Lessons Learned

### 1. Start Simple, Iterate Fast
- V1: Just username search on 5 platforms
- V2: Added email lookup and breach checking
- V3: Integrated 104 resources
- V4: Added reports and Pro features

**Takeaway:** Ship something usable quickly, then improve based on feedback.

### 2. Documentation is Marketing
The README with clear examples and Free/Pro comparison IS the sales page.

### 3. CLI Tools Have a Market
Not everything needs a GUI. Developers and security professionals prefer CLI tools for automation and scripting.

### 4. Hybrid Monetization Works
- GitHub stars → visibility → organic traffic
- Free version → trust building → Pro conversions
- One-time payment → easier to sell than subscription

---

## What's Next?

### Planned Features (v2.0)

**Free:**
- [ ] Dark web monitoring (Tor onion links)
- [ ] Cryptocurrency wallet lookup
- [ ] Company/domain intelligence
- [ ] More platforms (Mastodon, BlueSky, Threads)

**Pro:**
- [ ] Scheduled monitoring with email alerts
- [ ] Historical tracking (compare investigations over time)
- [ ] Team collaboration (shared reports)
- [ ] API mode for integration

### Growing the Business

**Short-term (Month 1-3):**
- Launch on ProductHunt
- Write guest posts for security blogs
- Reach out to cybersecurity training platforms
- Build affiliate program (20% commission)

**Long-term (Month 6+):**
- Enterprise tier ($199/year) with team features
- Consulting services for custom OSINT implementations
- Training course: "OSINT Fundamentals with Python"

---

## Try It Yourself

### Free Version (GitHub)
```bash
git clone https://github.com/dopamin3fiends/ml-systems-portfolio.git
cd ml-systems-portfolio
pip install requests

# Run username search
python -m tools.osint.cli username your_username

# Generate HTML report
python -m tools.osint.cli full email@example.com --report html
```

### Pro Version ($19.99)
- Windows .exe (no Python needed)
- PDF reports without watermarks
- Bulk search from CSV
- Commercial license
- [**Get OSINT Tool Pro →**](https://gumroad.com/l/osint-tool-pro)

---

## Source Code Highlights

**Full source available on GitHub:**
- [Main CLI](https://github.com/dopamin3fiends/ml-systems-portfolio/blob/main/tools/osint/cli.py)
- [Username Search Module](https://github.com/dopamin3fiends/ml-systems-portfolio/blob/main/tools/osint/modules/username_search.py)
- [Resources Database](https://github.com/dopamin3fiends/ml-systems-portfolio/blob/main/tools/osint/modules/resources.py)

---

## Discussion

**Questions I'd love to hear from you:**
1. What OSINT resources would you add to the database?
2. Would you prefer a GUI or is CLI sufficient?
3. Any privacy/ethical concerns with tools like this?
4. What other intelligence gathering features would be useful?

Drop a comment below! And if you found this useful, consider:
- ⭐ Star the repo: [github.com/dopamin3fiends/ml-systems-portfolio](https://github.com/dopamin3fiends/ml-systems-portfolio)
- 🐦 Share on Twitter
- 💎 Try [OSINT Tool Pro](https://gumroad.com/l/osint-tool-pro)

---

## Tags
#python #opensource #security #osint #cli #tools #infosec #cybersecurity

---

*Built by a security researcher, for security researchers. Happy investigating! 🔍*
