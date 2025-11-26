# Web Automation Framework v1.0

Professional browser automation framework for testing, QA workflows, and web scraping. Built with Selenium WebDriver for reliable cross-browser automation.

## Features

✅ **Multi-Browser Support**: Chrome, Firefox, Edge  
✅ **Headless Execution**: Background automation without GUI  
✅ **Flexible Actions**: Navigate, click, type, scroll, screenshot, extract data, execute JavaScript  
✅ **Preset Workflows**: Pre-built workflows for common tasks  
✅ **Context Variables**: Dynamic workflows with variable interpolation  
✅ **Session Tracking**: Detailed execution logs with timestamps and results  
✅ **Screenshot Capture**: Automatic screenshots on errors or explicit actions  
✅ **Data Extraction**: Extract text, attributes, or execute custom JavaScript  

## Prerequisites

```bash
pip install selenium
```

**WebDriver Setup**: Selenium requires browser drivers. Install for your browser:

- **Chrome**: [ChromeDriver](https://chromedriver.chromium.org/)
- **Firefox**: [geckodriver](https://github.com/mozilla/geckodriver/releases)
- **Edge**: [EdgeDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

Or use `webdriver-manager` for automatic driver management:

```bash
pip install webdriver-manager
```

## Quick Start

### Run Demo Mode

```bash
python cli.py demo
```

Demo navigates to example.com, captures screenshot, and extracts page title.

### Run Preset Workflows

**Health Check** - Verify website is accessible:
```bash
python cli.py preset health_check --context url=https://example.com
```

**Form Test** - Test form submission:
```bash
python cli.py preset form_test --context url=https://example.com/form username=test password=demo
```

**Page Scrape** - Extract all links from page:
```bash
python cli.py preset page_scrape --context url=https://example.com
```

**Link Checker** - Validate all links on page:
```bash
python cli.py preset link_checker --context url=https://example.com
```

### Custom Workflows

Create a workflow JSON file:

```json
{
  "name": "My Workflow",
  "description": "Custom automation workflow",
  "actions": [
    {
      "action_type": "NAVIGATE",
      "target": "https://example.com"
    },
    {
      "action_type": "SCREENSHOT",
      "target": "screenshot_{timestamp}.png",
      "wait_after": 2.0
    },
    {
      "action_type": "EXECUTE_JS",
      "value": "return document.title;",
      "metadata": {"extract_as": "title"}
    }
  ],
  "config": {
    "browser_type": "CHROME",
    "headless": true,
    "timeout": 30
  }
}
```

Run custom workflow:
```bash
python cli.py run my_workflow.json --context url=https://example.com
```

## Action Types

| Action Type | Description | Target | Value | Example |
|-------------|-------------|--------|-------|---------|
| `NAVIGATE` | Navigate to URL | URL | - | `target: "https://example.com"` |
| `CLICK` | Click element | CSS selector or XPath | - | `target: "button.submit"` |
| `TYPE` | Type into input | CSS selector or XPath | Text to type | `target: "input#username"`, `value: "test"` |
| `SCROLL` | Scroll page | - | "top", "bottom", or pixels | `value: "bottom"` |
| `WAIT` | Wait/pause | - | Seconds | `value: "2.5"` |
| `SCREENSHOT` | Capture screenshot | Filename | - | `target: "screenshot.png"` |
| `EXTRACT` | Extract text from elements | CSS selector | - | `target: "h1"`, `metadata: {"extract_as": "headings"}` |
| `EXECUTE_JS` | Execute JavaScript | - | JS code | `value: "return document.title;"` |

## Configuration Options

```python
BrowserConfig(
    browser_type=BrowserType.CHROME,  # CHROME, FIREFOX, EDGE
    headless=False,                   # Run without GUI
    user_agent="Custom Agent",        # Custom user agent
    proxy="http://proxy:8080",        # Proxy server
    window_size=(1920, 1080),         # Window dimensions
    timeout=30,                        # Page load timeout
    disable_images=False,             # Disable image loading
    disable_javascript=False          # Disable JavaScript
)
```

## Use Cases

### ✅ Legitimate Use Cases

- **QA Testing**: Automated regression testing of web applications
- **Website Monitoring**: Health checks and uptime monitoring
- **Web Scraping**: Extract public data (with respect for robots.txt and ToS)
- **Form Testing**: Validate form submissions and error handling
- **Link Validation**: Check for broken links and dead pages
- **Screenshot Capture**: Generate visual documentation
- **Performance Testing**: Measure page load times and responsiveness

### ❌ DO NOT Use For

- **Spam/Fraud**: Creating fake accounts, reviews, or engagement
- **ToS Violations**: Automating actions prohibited by website terms
- **DDoS/Attack**: Overwhelming servers with requests
- **Credential Stuffing**: Testing stolen credentials
- **Content Manipulation**: Automated voting, liking, or commenting
- **Scraping Private Data**: Accessing data requiring authentication without permission

## Integration with Orchestrator

Register tool in `src/orchestrator/registry.json`:

```json
{
  "id": "web_automation",
  "name": "Web Automation Framework",
  "description": "Browser automation for testing and QA workflows",
  "command": ["python", "tools/web_automation/cli.py"],
  "args_template": ["preset", "{preset}", "--context", "url={url}"],
  "category": "automation",
  "trusted": true,
  "version": "1.0.0",
  "demo_mode": {
    "command": ["python", "tools/web_automation/cli.py", "demo"],
    "safe": true
  }
}
```

Run via orchestrator:
```bash
python src/orchestrator/executor.py web_automation --url https://example.com --preset health_check
```

## Architecture

```
tools/web_automation/
├── models.py       # Data models (BrowserConfig, BrowserAction, Workflow, SessionResult)
├── engine.py       # Selenium automation engine
├── cli.py          # Command-line interface
└── README.md       # Documentation
```

**Data Flow**:
1. **models.py**: Define workflow structure and configuration
2. **engine.py**: AutomationEngine executes actions with Selenium WebDriver
3. **cli.py**: Parse arguments, load workflow, display results

## Session Results

Every execution produces a `SessionResult`:

```json
{
  "session_id": "abc123",
  "workflow_name": "Health Check",
  "status": "COMPLETED",
  "start_time": "2024-01-15T10:30:00",
  "end_time": "2024-01-15T10:30:15",
  "actions_completed": 5,
  "actions_failed": 0,
  "screenshots": ["screenshot_20240115_103015.png"],
  "extracted_data": {
    "title": "Example Domain",
    "status_code": 200
  }
}
```

## Advanced Examples

### Dynamic Workflows with Context

```bash
# Pass multiple context variables
python cli.py preset form_test \
  --context url=https://example.com/login \
           username=test_user \
           password=test_pass
```

Workflow actions use `{variable}` interpolation:
```json
{
  "action_type": "TYPE",
  "target": "input#username",
  "value": "{username}"
}
```

### Headless Scraping

```json
{
  "config": {
    "browser_type": "CHROME",
    "headless": true,
    "disable_images": true,
    "timeout": 60
  }
}
```

### Proxy Configuration

```json
{
  "config": {
    "proxy": "http://proxy.example.com:8080",
    "user_agent": "Mozilla/5.0 Custom Bot"
  }
}
```

## Error Handling

- **Element Not Found**: Actions retry with multiple selector strategies (CSS, XPath)
- **Timeout**: Page load timeout triggers automatic error capture
- **Screenshot on Error**: Failed sessions automatically capture error screenshots
- **Graceful Shutdown**: Browser cleanup guaranteed via `try/finally` blocks

## Troubleshooting

**"selenium not installed"**:
```bash
pip install selenium
```

**"WebDriver not found"**:
- Ensure ChromeDriver/geckodriver is in PATH
- Or use `webdriver-manager` for automatic management

**"Element not found"**:
- Verify CSS selector or XPath is correct
- Add `WAIT` action before element interaction
- Check if element is in iframe (requires frame switching)

**"Timeout"**:
- Increase `timeout` in BrowserConfig
- Check internet connection and website availability

## Educational Use Disclaimer

⚠️ **This tool is for educational, testing, and QA purposes only.**

Users are responsible for:
- Complying with website Terms of Service
- Respecting robots.txt and rate limits
- Obtaining permission for data extraction
- Following applicable laws and regulations

Misuse may result in:
- IP blocking or account suspension
- Legal action from website owners
- Violation of computer fraud laws

**Always use responsibly and ethically.**

## License

MIT License - See LICENSE file for details

## Version History

- **v1.0.0** (2024-01): Initial release
  - Multi-browser support (Chrome, Firefox, Edge)
  - 8 action types (Navigate, Click, Type, Scroll, Wait, Screenshot, Extract, Execute JS)
  - 4 preset workflows (Health Check, Form Test, Page Scrape, Link Checker)
  - Session tracking and result export
  - Headless mode and proxy support

---

**Part of ml-systems-portfolio** - Professional Systems Integration Orchestrator
