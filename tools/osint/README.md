# OSINT Tool - Open Source Intelligence Gathering

🔍 **Professional-grade OSINT tool** for gathering intelligence on emails, usernames, domains, phone numbers, and data breaches. Access **104 curated OSINT resources** across 11 categories with automated searching capabilities.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> 💎 **[Get OSINT Tool Pro](https://gumroad.com/l/osint-tool-pro)** - PDF reports, bulk search, scheduled monitoring, no watermarks - **$19.99 one-time**

---

## 🆓 Free vs 💎 Pro

| Feature | Free | Pro |
|---------|------|-----|
| Email Lookup | ✅ | ✅ |
| Username Search (20+ platforms) | ✅ | ✅ |
| Breach Check | ✅ | ✅ |
| WHOIS Lookup | ✅ | ✅ |
| 104 OSINT Resources Database | ✅ | ✅ |
| Auto-Search Multiple Sites | ✅ | ✅ |
| HTML Reports | ✅ Watermarked | ✅ No Watermark |
| PDF Reports | ❌ | ✅ |
| Bulk Search (CSV/JSON) | ❌ | ✅ |
| Scheduled Monitoring | ❌ | ✅ |
| Priority Support | ❌ | ✅ |
| Commercial Use | ❌ | ✅ |

**[→ Upgrade to Pro for $19.99](https://gumroad.com/l/osint-tool-pro)**

---

## ✨ Features

### Core Intelligence Gathering
- ✅ **Email Lookup** - Validate emails, extract domains, guess social profiles
- ✅ **Username Search** - Search 20+ platforms (GitHub, Twitter, Reddit, etc.)
- ✅ **Breach Check** - Check if email/username appears in data breaches (HIBP integration)
- ✅ **WHOIS Lookup** - Domain registration information
- ✅ **Phone Lookup** - Reverse phone number searches across 10+ sites
- ✅ **Full Investigation** - Run all checks in one command with HTML reports

### OSINT Resources (104 Sites)
- 🌎 **US People Search** (24 sites) - Spokeo, Pipl, WhitePages, BeenVerified, etc.
- 🌍 **International Search** (10 sites) - 192.com (UK), Infobel (Europe), etc.
- 📱 **Phone Lookup** (10 sites) - TrueCaller, SpyDialer, ZabaSearch
- 👤 **Username Search** (4 frameworks) - Sherlock, WhatsMyName
- 🖼️ **Image Search** (4 tools) - TinEye, Google Reverse Image
- 📧 **Email Search** (7 tools) - Hunter.io, EmailRep, Clearbit
- 📱 **Social Media** (10 platforms) - Social Searcher, Social Mention
- 🔒 **Breach Databases** (7 sources) - Have I Been Pwned, DeHashed
- 🌐 **IP Tools** (16 tools) - Shodan, Censys, IPVoid
- ⚖️ **Criminal Records** (7 databases) - NSOPW, VINELink
- 🛠️ **OSINT Frameworks** (5 tools) - Maltego, Recon-ng, SpiderFoot

### Automated Search
- 🔎 **Auto-Search** - Automatically opens searches on multiple OSINT sites
- 🚀 **Parallel Execution** - Fast concurrent searches across platforms
- 📊 **Categorized Results** - Organized by platform type

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/dopamin3fiends/ml-systems-portfolio.git
cd ml-systems-portfolio

# Install dependencies
pip install requests

# Run your first investigation
python -m tools.osint.cli username your_target_username
```

### Basic Commands

```bash
# Email investigation
python -m tools.osint.cli email john.doe@example.com

# Username search across 20+ platforms
python -m tools.osint.cli username johndoe123

# Check data breaches
python -m tools.osint.cli breach john.doe@example.com

# WHOIS domain lookup
python -m tools.osint.cli whois example.com

# Phone number search
python -m tools.osint.cli phone "+1234567890"

# View all 104 OSINT resources
python -m tools.osint.cli resources

# Auto-search across multiple sites
python -m tools.osint.cli search --email test@example.com
python -m tools.osint.cli search --phone "+1234567890"
python -m tools.osint.cli search --name "John Doe"

# Full investigation with HTML report
python -m tools.osint.cli full john.doe@example.com --report html

# Save results to JSON
python -m tools.osint.cli full john.doe@example.com --output results.json
```

### 💎 Pro Commands

```bash
# Generate PDF report (Pro only)
python -m tools.osint.cli full target@email.com --report pdf

# Bulk search from CSV (Pro only)
python -m tools.osint.pro.bulk_search targets.csv --output-dir reports/

# Activate Pro license
python -m tools.osint.pro activate YOUR_LICENSE_KEY
```

## Modules

### 1. Email Lookup (`modules/email_lookup.py`)
- Validates email format
- Extracts domain
- Checks for disposable email providers
- Guesses potential social media profiles

### 2. Username Search (`modules/username_search.py`)
- Searches 20+ platforms simultaneously
- Uses parallel requests for speed
- Verifies existence where APIs available (GitHub, Reddit)
- Returns profile URLs

**Supported Platforms:**
- GitHub, Twitter, Instagram, Reddit
- LinkedIn, Facebook, YouTube, TikTok
- Twitch, Pinterest, Snapchat, Discord
- Steam, DeviantArt, Medium, Patreon
- Vimeo, SoundCloud, Spotify, Dribbble

### 3. Breach Check (`modules/breach_check.py`)
- Checks Have I Been Pwned database
- Password exposure checking (k-anonymity)
- Returns breach details (date, compromised data)

### 4. WHOIS Lookup (`modules/whois_lookup.py`)
- Queries WHOIS servers
- Returns registration details
- Name servers, registrar info
- Creation/expiration dates

## Output

Results are displayed in terminal and optionally saved to JSON:

```json
{
  "target": "john.doe@example.com",
  "timestamp": "2025-11-30T...",
  "results": {
    "email": { ... },
    "breaches": { ... },
    "whois": { ... }
  }
}
```

## Examples

### Example 1: Investigate Email
```bash
python -m tools.osint.cli email test@gmail.com
```

Output:
```
📧 Email: test@gmail.com
   Valid Format: ✅
   Domain: gmail.com

👤 Potential Social Profiles:
   • GitHub: https://github.com/test
   • Twitter: https://twitter.com/test
   • LinkedIn: https://linkedin.com/in/test
```

### Example 2: Search Username
```bash
python -m tools.osint.cli username dopaminefiend
```

Output:
```
🔍 Searching for: dopaminefiend
   Platforms checked: 20
   Found: 3

✅ Found on these platforms:
   • GitHub: https://github.com/dopaminefiend
     Status: Public repos: 5
   • Reddit: https://reddit.com/user/dopaminefiend
     Status: Karma: 150
```

### Example 3: Check Breaches
```bash
python -m tools.osint.cli breach test@example.com
```

Output:
```
🔒 Email: test@example.com
   Total Breaches: 2

⚠️  FOUND IN THESE BREACHES:
   📋 LinkedIn
      Date: 2012-06
      Compromised Data: Email addresses, Passwords
```

## API Keys (Optional)

Some features work better with API keys:

- **Have I Been Pwned**: Get API key from https://haveibeenpwned.com/API/Key
- Set as environment variable: `HIBP_API_KEY=your_key_here`

## Limitations

- Some platforms (LinkedIn, Facebook) require login for verification
- Breach data requires HIBP API key for full access
- Rate limiting applies to some services
- WHOIS data varies by registrar

## Privacy & Ethics

⚠️ **Use responsibly:**
- Only investigate information you have permission to check
- Respect privacy laws (GDPR, CCPA)
- Don't use for stalking or harassment
- Educational and security research purposes only

## 💼 Use Cases

- 🔐 **Security Research** - Investigate potential security threats
- 🕵️ **Background Checks** - Verify online identities
- 📊 **OSINT Training** - Learn intelligence gathering techniques
- 🎯 **Bug Bounty Recon** - Initial reconnaissance for security researchers
- 🏢 **Corporate Security** - Employee verification and threat detection
- 📰 **Journalism** - Fact-checking and source verification
- 🎓 **Educational** - Teaching OSINT methodologies

## 📸 Screenshots

### Username Search Results
```
🔍 Searching for: dopaminefiend
   Platforms checked: 20
   
✅ Found (3 platforms):
   • GitHub: https://github.com/dopaminefiend
     └─ Public repos: 0
   • Reddit: https://reddit.com/user/dopaminefiend
     └─ Karma: 620
   • Instagram: https://instagram.com/dopaminefiend
```

### OSINT Resources Database
```
📚 OSINT Resources (104 total)

🌎 US_PEOPLE_SEARCH (24 resources):
   1. Spokeo - https://www.spokeo.com
   2. Pipl - https://pipl.com
   3. WhitePages - https://www.whitepages.com
   [... 21 more]

🌍 INTERNATIONAL_SEARCH (10 resources):
   1. 192.com (UK) - https://www.192.com
   [... 9 more]
```

## 🛣️ Roadmap

### Free Version
- [ ] Add more platforms (Mastodon, BlueSky, Threads)
- [ ] IP address geolocation
- [ ] Company/domain intelligence
- [ ] Cryptocurrency wallet lookup
- [ ] Dark web monitoring (Tor onion links)
- [ ] API mode for integration

### Pro Version (Available Now)
- [x] PDF report generation
- [x] Bulk search from CSV/JSON
- [x] No watermarks on reports
- [ ] Scheduled monitoring with alerts
- [ ] Advanced filtering and search
- [ ] Historical tracking
- [ ] Team collaboration features
- [ ] API access with authentication

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 💎 Get Pro

**OSINT Tool Pro** includes:
- ✅ **PDF Reports** - Professional, shareable reports
- ✅ **Bulk Search** - Process CSV/JSON files with hundreds of targets
- ✅ **No Watermarks** - Clean, professional output
- ✅ **Commercial License** - Use in business/consulting
- ✅ **Priority Support** - Direct email support
- ✅ **Lifetime Updates** - All future Pro features included

**One-time payment: $19.99** (no subscription)

**[→ Buy Now on Gumroad](https://gumroad.com/l/osint-tool-pro)**

---

## 📝 License

MIT License - Free for personal and educational use.

For commercial use, please purchase the Pro version.

## 🙏 Credits

Built with ❤️ by [dopamin3fiends](https://github.com/dopamin3fiends)

**Data Sources:**
- Have I Been Pwned API
- GitHub API
- Reddit API
- 104 curated OSINT resources

**Inspired by:**
- Sherlock Project
- theHarvester
- Maltego
- SpiderFoot

---

## ⚠️ Disclaimer

This tool is for **educational and legitimate security research purposes only**. Users are responsible for complying with applicable laws and regulations. The author assumes no liability for misuse.

**Use responsibly:**
- Obtain proper authorization before investigating
- Respect privacy laws (GDPR, CCPA, etc.)
- Don't use for stalking, harassment, or illegal activities
- Follow platform Terms of Service

---

**Found this useful? ⭐ Star the repo!**

**Need more power? 💎 [Get Pro](https://gumroad.com/l/osint-tool-pro)**
