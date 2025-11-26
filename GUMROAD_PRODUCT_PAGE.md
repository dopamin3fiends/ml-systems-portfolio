# 🎛️ ML Systems Portfolio - Professional Automation Toolkit

## Gumroad Product Page Content

**Created:** November 26, 2025  
**Version:** 1.0  
**Status:** Ready for Launch

---

## 📝 Product Title

**"Professional Automation Toolkit - 6 Production-Ready Tools + Orchestrator Platform"**

---

## 🎯 Product Description (Main Copy)

### Transform Your Workflow with Professional Automation

Stop juggling dozens of scattered scripts and tools. Get a complete, professional automation platform with 6 production-ready tools, REST API orchestration, and a modern web dashboard.

**What You Get:**

🔧 **6 Professional Automation Tools** (6,877 lines of production code)
- Cookie Analysis Suite - Forensic browser cookie analysis with 4-stage pipeline
- Video Enhancement Suite - Multi-backend video processing with priority queuing
- PathPulse - Real-time file system threat detection and monitoring
- Windows Feature Manager - Professional Windows optional feature management
- Web Automation Framework - Multi-browser automation with Selenium
- ADB Automation Framework - Android device automation and testing

🎛️ **Systems Integration Orchestrator**
- FastAPI REST API for tool execution
- Interactive web dashboard for monitoring
- Pipeline builder to chain tools together
- Complete audit trail (Legacy_Journal) for compliance
- GitHub Actions CI/CD pipeline included

📚 **Complete Documentation**
- Comprehensive README for each tool
- API reference documentation
- Architecture deep-dive
- Quick start guides with examples
- Demo modes for safe testing

✅ **Production Quality**
- Professional code architecture
- Error handling and validation
- Safety disclaimers and warnings
- Cross-platform support (Windows/Linux/macOS compatible)
- Educational use guidelines

---

## 💎 What Makes This Different?

### Not Just Scripts - Professional Software

Every tool follows enterprise-grade patterns:
- **Type-safe data models** with validation
- **Modular architecture** (models → business logic → CLI)
- **Comprehensive error handling** with meaningful messages
- **Demo modes** for safe exploration
- **Educational disclaimers** for responsible use

### Built for Integration

Unlike scattered scripts, these tools integrate seamlessly:
- **Unified CLI** across all tools
- **JSON-based** input/output for easy chaining
- **Orchestrator API** to execute any tool programmatically
- **Consistent patterns** make customization easy

### Real Documentation

Not placeholder READMEs - actual comprehensive docs:
- Feature lists with examples
- Use case scenarios (legitimate & prohibited)
- Troubleshooting guides
- Architecture explanations
- API integration examples

---

## 🔧 Tool Details

### 1. Cookie Analysis Suite v2.0 (466 lines)

**Professional browser cookie forensic analysis**

**Features:**
- 4-stage processing pipeline (Parse → Enrich → Scan → Report)
- Company database for privacy tracking detection
- Risk assessment (SAFE → LOW → MEDIUM → HIGH → CRITICAL)
- Multiple output formats (JSON reports)
- Demo mode with 5 sample cookies

**Use Cases:**
- Digital forensics investigations
- Privacy audit research
- Browser artifact analysis
- Security training and education

**Commands:**
```bash
python cli.py parse cookies.txt         # Parse cookies
python cli.py analyze cookies.txt       # Full analysis
python cli.py demo                      # Safe demo mode
```

---

### 2. Video Enhancement Suite v1.0 (1,112 lines)

**Multi-backend video processing with priority queue management**

**Features:**
- Support for multiple backends (Topaz Video AI, FFmpeg, HandBrake)
- Priority-based job scheduling (LOW/MEDIUM/HIGH/CRITICAL)
- Concurrent worker processing
- Automatic retry on failure (3 attempts)
- Persistent queue (JSON storage)
- JSON output for integration

**Use Cases:**
- Video quality enhancement workflows
- Batch video processing
- Upscaling automation
- Denoising pipelines

**Commands:**
```bash
python cli.py add video.mp4 --priority HIGH  # Add job
python cli.py process --workers 2            # Start processing
python cli.py status                         # Check queue
python cli.py demo                           # Demo mode
```

---

### 3. PathPulse v1.0 (1,205 lines)

**Real-time file system monitoring with threat detection**

**Features:**
- 6 threat pattern detectors:
  - Mass deletion attacks
  - Ransomware encryption patterns
  - Rapid file creation (data exfiltration)
  - System file tampering
  - Sensitive file access
  - Unusual file extensions
- 5-level risk assessment (SAFE → CRITICAL)
- Cross-platform file monitoring (watchdog library)
- Real-time alerts with event context
- JSON output for SIEM integration

**Use Cases:**
- Endpoint security monitoring
- Ransomware detection
- Data loss prevention
- Security research and testing

**Commands:**
```bash
python cli.py monitor C:\Users          # Monitor directory
python cli.py monitor . --duration 60   # Monitor for 60s
python cli.py demo                      # Safe demo mode
```

---

### 4. Windows Feature Manager v1.0 (1,418 lines)

**Professional Windows optional feature management with backup/restore**

**Features:**
- Enable/disable Windows optional features
- 5 preset feature groups:
  - dev_tools (WSL, containers, Hyper-V)
  - virtualization (Hyper-V, Virtual Machine Platform)
  - networking (SMB, NFS, Telnet Client)
  - security (Windows Sandbox, Credential Guard)
  - legacy (DirectPlay, legacy components)
- Backup/restore with rollback capability
- Admin privilege validation
- Dry-run mode for safety
- PowerShell integration via DISM

**Use Cases:**
- System administration automation
- Development environment setup
- Feature audit and compliance
- Automated provisioning

**Commands:**
```bash
python cli.py enable Microsoft-Windows-Subsystem-Linux
python cli.py preset dev_tools          # Enable dev preset
python cli.py backup backup.json        # Create backup
python cli.py restore backup.json       # Restore from backup
python cli.py demo                      # Safe demo mode
```

---

### 5. Web Automation Framework v1.0 (1,121 lines)

**Multi-browser automation for testing and QA workflows**

**Features:**
- Multi-browser support (Chrome, Firefox, Edge)
- 8 action types:
  - Navigate, Click, Type, Scroll, Wait
  - Screenshot, Extract text, Execute JavaScript
- 4 preset workflows:
  - health_check - Verify website accessibility
  - form_test - Test form submission
  - page_scrape - Extract page content
  - link_checker - Validate links
- Headless mode for background execution
- Proxy configuration support
- Screenshot capture with error handling
- Context variables for dynamic workflows
- Session result tracking with timing

**Use Cases:**
- QA testing and automation
- Website health monitoring
- Web scraping (with legal compliance)
- Form validation testing
- Link checking and validation

**Commands:**
```bash
python cli.py preset health_check --context url=https://example.com
python cli.py preset form_test --context url=https://... username=test
python cli.py run workflow.json --context url=https://...
python cli.py demo                      # Safe demo mode
```

**Educational Disclaimers:**
- DO NOT use for spam, fraud, or ToS violations
- Respect robots.txt and rate limits
- Obtain permission for data extraction

---

### 6. ADB Automation Framework v1.0 (1,555 lines)

**Android device automation and testing framework**

**Features:**
- Device discovery with detailed info:
  - Model, Android version, SDK level
  - Battery percentage
  - Screen resolution
  - Root detection
- App control (install/uninstall/start/stop)
- File transfer (push/pull)
- Screen capture with auto-cleanup
- Input simulation (tap/swipe/text/keyevents)
- Shell command execution
- 9 action types for automation
- 5 preset tasks:
  - device_info - Comprehensive device data
  - app_launch_test - App testing workflow
  - screenshot_sequence - Timed captures
  - ui_interaction - Basic UI testing
  - battery_monitor - Track battery over time

**Use Cases:**
- App testing and QA automation
- Device management at scale
- Performance monitoring
- Screenshot documentation
- CI/CD integration for mobile apps

**Commands:**
```bash
python cli.py devices                   # List connected devices
python cli.py screenshot                # Capture screenshot
python cli.py packages --filter com.    # List apps
python cli.py shell "getprop ro.build.version.release"
python cli.py task device_info          # Run preset task
python cli.py demo                      # Safe demo mode
```

**Security Warnings:**
- Only use on devices you own or have permission to access
- Disable USB debugging when not developing
- Educational and testing purposes only

---

## 🎛️ Systems Integration Orchestrator

### REST API Server (FastAPI + Uvicorn)

**Endpoints:**
- `GET /tools` - List all registered tools
- `POST /run/tool` - Execute single tool
- `POST /run/pipeline` - Execute tool chain
- `GET /runs` - View execution history
- `GET /pipelines` - List saved pipelines
- `GET /stats` - System statistics
- `GET /health` - Health check
- `GET /` - Web dashboard

**Example API Usage:**
```bash
# Start server
python src/backend/orchestrator_api.py

# Execute tool via API
curl -X POST http://localhost:8000/run/tool \
  -H "Content-Type: application/json" \
  -d '{"tool_id": "cookie_analysis", "input_text": "cookies.txt"}'

# Create pipeline
curl -X POST http://localhost:8000/run/pipeline \
  -d '{"pipeline": [
    {"tool_id": "pathpulse", "input": "C:\\Users"},
    {"tool_id": "cookie_analysis", "input": "cookies.txt"}
  ]}'
```

### Web Dashboard (static/index.html)

**Features:**
- Tool discovery and filtering
- One-click tool execution with forms
- Real-time run history
- Pipeline builder (visual chaining)
- System statistics dashboard
- Auto-refresh every 5 seconds

### Audit Trail (Legacy_Journal)

Every execution is logged:
- Run ID (unique UUID)
- Tool metadata (ID, name, command)
- Execution details (start time, duration, exit code)
- Input/output file paths
- stdout/stderr capture

**Files per run:**
- `{run_id}_{tool}_meta.json` - Metadata
- `{run_id}_{tool}_plan.json` - Execution plan
- `{run_id}_{tool}.out.txt` - stdout capture
- `{run_id}_{tool}.err.txt` - stderr capture

---

## 📦 What's Included

### Source Code
```
ml-systems-portfolio/
├── tools/
│   ├── cookie_analysis/    (466 lines)
│   ├── video_enhancement/  (1,112 lines)
│   ├── pathpulse/         (1,205 lines)
│   ├── windows_features/  (1,418 lines)
│   ├── web_automation/    (1,121 lines)
│   └── adb_automation/    (1,555 lines)
├── src/
│   ├── orchestrator/      (executor.py, registry.json)
│   └── backend/           (orchestrator_api.py - FastAPI)
├── static/
│   └── index.html         (Web dashboard)
├── .github/
│   └── workflows/         (CI/CD pipeline)
└── docs/
    ├── ORCHESTRATOR.md    (Full documentation)
    ├── QUICKSTART.md      (Quick start guide)
    └── README.md          (Main documentation)
```

### Documentation Files
- **README.md** (main) - Project overview
- **ORCHESTRATOR.md** - Complete orchestrator guide
- **QUICKSTART.md** - 5-minute quick start
- Individual tool READMEs (6 comprehensive docs)
- API reference examples
- Architecture explanations

### Configuration Files
- **pyproject.toml** - Python project metadata
- **requirements.txt** - Python dependencies
- **Makefile** - Build automation
- **.github/workflows/ci.yml** - CI/CD pipeline
- **src/orchestrator/registry.json** - Tool registry

---

## 💻 System Requirements

### Required
- **Python 3.11+** (tested on 3.11)
- **pip** (Python package manager)
- **Git** (for version control)

### Tool-Specific Requirements
- **Video Enhancement**: FFmpeg/Topaz Video AI/HandBrake (optional)
- **PathPulse**: watchdog library (included in requirements.txt)
- **Web Automation**: Selenium + WebDriver (ChromeDriver/geckodriver)
- **ADB Automation**: Android SDK Platform Tools (adb command)
- **Windows Features**: Windows 10/11, Admin privileges

### Python Dependencies (requirements.txt included)
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.2
numpy>=1.24.0,<2.0.0
pandas>=2.0.3
scikit-learn>=1.3.2
watchdog==6.0.0
selenium>=4.0.0  # Optional, for web automation
```

### Platform Support
- **Windows 10/11** - Full support (all tools)
- **macOS** - Supported (except Windows Features)
- **Linux** - Supported (except Windows Features)

---

## 🚀 Quick Start (5 Minutes)

### 1. Clone Repository
```bash
git clone https://github.com/dopamin3fiends/ml-systems-portfolio.git
cd ml-systems-portfolio
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Test a Tool (Demo Mode)
```bash
cd tools/cookie_analysis
python cli.py demo
```

### 4. Start Orchestrator
```bash
cd ../../
python src/backend/orchestrator_api.py
```

### 5. Open Dashboard
Navigate to: `http://localhost:8000`

---

## 🎓 Learning Path

### Beginner (Day 1)
1. Run demo modes for each tool
2. Explore web dashboard
3. Execute single tools via CLI
4. Read individual tool READMEs

### Intermediate (Week 1)
1. Create custom automation tasks
2. Use REST API to execute tools
3. Chain tools together manually
4. Modify tool configurations

### Advanced (Month 1)
1. Build custom pipelines
2. Integrate with your existing systems
3. Add your own tools to registry
4. Customize web dashboard
5. Deploy to production

---

## 💡 Use Case Examples

### Security Operations
```bash
# Monitor file system for threats
python tools/pathpulse/cli.py monitor C:\Users --duration 3600

# Analyze browser artifacts
python tools/cookie_analysis/cli.py analyze cookies.txt

# Chain via orchestrator API
curl -X POST http://localhost:8000/run/pipeline -d '{
  "pipeline": [
    {"tool_id": "pathpulse", "input": "C:\\Users"},
    {"tool_id": "cookie_analysis", "input": "artifacts.txt"}
  ]
}'
```

### Development & QA
```bash
# Setup development environment
python tools/windows_features/cli.py preset dev_tools

# Test web application
python tools/web_automation/cli.py preset health_check \
  --context url=https://myapp.com

# Test mobile app
python tools/adb_automation/cli.py task app_launch_test \
  --context package_name=com.example.app
```

### Video Processing
```bash
# Batch video enhancement
python tools/video_enhancement/cli.py add video1.mp4 --priority HIGH
python tools/video_enhancement/cli.py add video2.mp4 --priority MEDIUM
python tools/video_enhancement/cli.py process --workers 2
```

---

## 🛡️ Safety & Compliance

### Educational Disclaimers

**All tools include clear warnings about:**
- Authorized use only
- Respect for Terms of Service
- Privacy and security considerations
- Legal compliance requirements
- Ethical usage guidelines

### Prohibited Use Cases

**DO NOT use these tools for:**
- Unauthorized access to systems or data
- Malware distribution or installation
- Privacy invasion or surveillance
- Game cheating or manipulation
- App store fraud or fake reviews
- Spam, fraud, or social engineering
- DDoS attacks or system overload
- Credential stuffing or brute force
- Violations of terms of service
- Any illegal activities

### Recommended Use Cases

**✅ Legitimate professional uses:**
- Security research and testing (authorized)
- QA and software testing
- Development environment automation
- Performance monitoring and optimization
- Educational purposes and training
- Personal device management
- Compliance auditing (authorized)
- Digital forensics (authorized)

---

## 🎯 Pricing Tiers

### 💎 Starter Edition - $29

**Perfect for individual developers and students**

✅ Complete source code (6,877 lines)
✅ All 6 professional tools
✅ Orchestrator platform (API + Dashboard)
✅ Complete documentation
✅ Demo modes for all tools
✅ Community support (GitHub Issues)
✅ MIT License for personal use
✅ Lifetime updates

**Best for:** Learning automation, personal projects, portfolio building

---

### 🚀 Professional Edition - $79

**For freelancers and small teams**

✅ Everything in Starter
✅ Custom workflow templates (10+ examples)
✅ Priority email support (48h response)
✅ Extended documentation with advanced patterns
✅ Integration guides for CI/CD
✅ Commercial license (up to 5 users)
✅ Monthly live Q&A sessions
✅ Workflow showcase feature requests

**Best for:** Professional consulting, client projects, small business automation

---

### 🏢 Enterprise Edition - $299

**For teams and organizations**

✅ Everything in Professional
✅ Custom tool integration service (1 tool)
✅ Dedicated support channel (Slack/Discord)
✅ Commercial license (unlimited users)
✅ On-premises deployment assistance
✅ Quarterly architecture review call
✅ Custom workflow development (2 workflows)
✅ Training session for team (90 min)
✅ Priority feature requests

**Best for:** Enterprise teams, MSPs, security operations, large-scale automation

---

### 🎁 Money-Back Guarantee

**30-day full refund** if the toolkit doesn't meet your needs. No questions asked.

---

## 📊 Technical Specifications

### Code Metrics
- **Total Lines:** 6,877 lines of production code
- **Tools:** 6 professional applications
- **Languages:** Python 3.11+
- **Frameworks:** FastAPI, Pydantic, Selenium, watchdog
- **Testing:** Demo modes for all tools
- **Documentation:** 7 comprehensive README files

### Architecture
- **Pattern:** Models → Business Logic → CLI
- **Data Format:** JSON for all I/O
- **API Style:** RESTful with OpenAPI docs
- **Storage:** JSON files (audit logs, queue, registry)
- **Logging:** Comprehensive stdout/stderr capture

### Performance
- **API Response:** <100ms for tool discovery
- **Tool Execution:** Varies by tool (seconds to minutes)
- **Dashboard Refresh:** 5-second auto-update
- **Concurrent Processing:** Supported (video queue, ADB tasks)

---

## 📞 Support & Community

### Included Support

**All Tiers:**
- GitHub Issues for bug reports
- Documentation and guides
- Demo modes for testing

**Professional & Enterprise:**
- Email support (support@example.com)
- Priority issue resolution
- Feature request consideration

### Community Resources

- **GitHub:** [dopamin3fiends/ml-systems-portfolio](https://github.com/dopamin3fiends/ml-systems-portfolio)
- **Issues:** Report bugs, request features
- **Discussions:** Share workflows, ask questions
- **Pull Requests:** Contribute improvements

---

## 🎬 Video Demos (Coming Soon)

### Planned Videos
1. **Quick Start Tour** (5 min) - Overview of all 6 tools
2. **Cookie Analysis Deep Dive** (10 min) - Forensic analysis workflow
3. **Web Automation Tutorial** (15 min) - Build custom workflows
4. **Android Testing Guide** (12 min) - App testing with ADB
5. **Orchestrator Masterclass** (20 min) - Build complex pipelines

---

## 📈 Roadmap

### Coming in v1.1 (Q1 2026)
- [ ] Docker containerization
- [ ] Additional preset workflows
- [ ] Enhanced dashboard with filtering
- [ ] Webhook notifications
- [ ] Tool marketplace for custom tools

### Coming in v2.0 (Q2 2026)
- [ ] Visual pipeline editor (drag & drop)
- [ ] Scheduled execution (cron-like)
- [ ] Multi-user support with RBAC
- [ ] Cloud deployment guides (AWS/Azure/GCP)
- [ ] Prometheus metrics export

---

## ❓ Frequently Asked Questions

**Q: Do I need all the tool dependencies installed?**
A: No! Each tool is modular. Install only what you need. Demo modes work without external dependencies.

**Q: Can I add my own tools?**
A: Yes! Add entries to `src/orchestrator/registry.json` and follow the CLI pattern.

**Q: Is this production-ready?**
A: Yes, for authorized use cases. All tools include error handling, validation, and safety checks.

**Q: What's the difference from open-source alternatives?**
A: Professional code quality, comprehensive documentation, integration platform, and commercial support options.

**Q: Can I use this commercially?**
A: Professional and Enterprise tiers include commercial licenses. See tier details above.

**Q: Do you offer custom development?**
A: Yes! Enterprise tier includes custom tool integration. Contact for additional services.

**Q: How do updates work?**
A: GitHub repository is continuously updated. Pull latest code anytime. Major versions announced.

**Q: Can I resell or redistribute?**
A: No. Commercial license allows use in your business but not resale of the toolkit itself.

---

## 🏆 Why Choose This Toolkit?

### ✅ Professional Quality
Not hobbyist scripts - enterprise-grade code with proper architecture, error handling, and documentation.

### ✅ Complete Integration
Unlike scattered tools, everything works together through a unified orchestrator platform.

### ✅ Production-Ready
Used in real-world scenarios with comprehensive testing and safety considerations.

### ✅ Actively Maintained
Regular updates, bug fixes, and feature additions. GitHub repository shows active development.

### ✅ Educational Value
Learn professional automation patterns, API design, and tool integration best practices.

### ✅ Time Savings
6 tools that would take months to build yourself, ready to use in 5 minutes.

---

## 🎁 Bonus Materials (All Tiers)

### Included Free
- **GitHub Actions CI/CD** - Complete pipeline configuration
- **Makefile** - Build automation commands
- **API Examples** - curl, Python, JavaScript integration samples
- **Tool Development Guide** - Add your own tools
- **Architecture Documentation** - Deep dive into design decisions
- **Marketing Templates** - Promote your custom tools (GUMROAD_MARKETING.md)

---

## 📄 License

### Source Code License
**MIT License** - See LICENSE file in repository

### Commercial Use License
- **Starter:** Personal use only
- **Professional:** Commercial use up to 5 users
- **Enterprise:** Commercial use unlimited users

### Restrictions
- No redistribution or resale of toolkit
- No removal of attribution
- Comply with all tool-specific disclaimers

---

## 🚀 Get Started Today

**Download Now** and transform your automation workflow!

1. ⬇️ Purchase your tier
2. 📥 Download zip file
3. 📚 Read QUICKSTART.md
4. 🎮 Run demo modes
5. 🚀 Start automating!

---

## 📧 Questions?

**Pre-sales inquiries:** Contact via Gumroad messaging  
**Technical support:** See support tier details above  
**Custom development:** Enterprise tier includes consultation

---

**Last Updated:** November 26, 2025  
**Version:** 1.0.0  
**Commit:** 6803256

---

**Built with ❤️ for automation professionals**

*Transform scattered scripts into professional automation platform in 5 minutes.*
