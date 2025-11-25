# Orchestrator: Systems Integration Platform

**Automate. Chain. Audit. Scale.**

A production-ready systems integration platform that discovers, catalogs, chains, and audits legacy tools and automation scripts. Generate comprehensive audit trails. Expose via REST API. Publish workflows on Gumroad.

---

## 🎯 What It Does

**Orchestrator** is a meta-system that:

1. **Discovers & catalogs** your existing tools (Python scripts, .exe binaries, shell commands)
2. **Chains them together** (output of Tool A → input of Tool B)
3. **Logs everything** to an immutable audit trail (`Legacy_Journal/`)
4. **Exposes via REST API** so tools can be called programmatically
5. **Provides a dashboard** for human-friendly interaction

**Use cases:**
- Forensic analysis pipelines (extract cookies → parse processes → correlate artifacts)
- Security threat intelligence workflows
- Compliance automation & audit reporting
- Batch automation with full traceability
- SaaS microservice orchestration

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│      Orchestrator Dashboard (HTML/JS)       │ ← User Interface
├─────────────────────────────────────────────┤
│      FastAPI REST Server (orchestrator_api) │ ← API Layer
├─────────────────────────────────────────────┤
│ Pipeline Runner  │ Executor  │ Monitoring   │ ← Business Logic
├─────────────────────────────────────────────┤
│        Tool Registry (registry.json)         │ ← Configuration
├─────────────────────────────────────────────┤
│  Tool 1  │  Tool 2  │ Tool 3  │  Tool N     │ ← Actual Tools
└─────────────────────────────────────────────┘

Legacy_Journal/
├── run_12345_tool1_plan.json      # what we planned to run
├── run_12345_tool1_meta.json      # execution metadata
├── run_12345_tool1.out.txt        # stdout
├── run_12345_tool1.err.txt        # stderr
└── pipeline_67890.json            # full pipeline trace
```

### Key Components

- **`src/orchestrator/registry.json`** — Tool manifest (id, name, command, args, metadata)
- **`src/orchestrator/executor.py`** — Runs individual tools, captures output, writes to journal
- **`src/orchestrator/pipeline.py`** — Chains tools; passes output of one as input to next
- **`src/orchestrator/monitoring.py`** — Query journal; get stats, historical runs, audit trail
- **`src/backend/orchestrator_api.py`** — FastAPI server; REST endpoints for discovery, execution, audit
- **`static/index.html`** — Interactive web dashboard
- **`Legacy_Journal/`** — Immutable audit trail (git-safe, no secrets by default)

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1           # Windows PowerShell
source .venv/bin/activate              # Mac/Linux

python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Start the API Server

```bash
cd c:\Users\Dopaminefiend\OneDrive\Projects\LegacySystems\ml-systems-portfolio
uvicorn src.backend.orchestrator_api:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 3. Open Dashboard

Visit **http://localhost:8000** in your browser.

You should see:
- ✅ List of available tools (from registry.json)
- ✅ Form to run individual tools
- ✅ Recent execution runs
- ✅ Recent pipelines

### 4. Run Your First Tool

In the dashboard:
1. Select a tool (e.g., "Echo Demo")
2. Optionally enter input
3. Click "Execute Tool"
4. View results in "Recent Runs"

### 5. Run Your First Pipeline

In the dashboard:
1. Under "Build & Run Pipeline", enter tool names: `cookie_parser, procexp, cmd_unlock`
2. Click "Run Pipeline"
3. View in "Recent Pipelines"

Check `Legacy_Journal/` folder — you'll see execution logs and audit trail.

---

## 📡 REST API

### Available Endpoints

```
GET  /                          # Dashboard (HTML)
GET  /health                    # Health check
GET  /tools                     # List all tools
POST /run/tool                  # Execute single tool
POST /run/pipeline              # Execute pipeline (chained tools)
GET  /runs                      # Recent tool runs (limit=50)
GET  /run/{run_id}              # Get specific run metadata
GET  /pipelines                 # Recent pipelines
GET  /pipeline/{pipeline_id}    # Get full pipeline log
GET  /stats                     # Journal statistics
```

### Example: Run a Tool

```bash
curl -X POST http://localhost:8000/run/tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_id": "cookie_parser",
    "input_text": "browser_artifacts.json",
    "timeout": 120
  }'
```

**Response:**
```json
{
  "status": "success",
  "run_id": "a1b2c3d4e5f6...",
  "tool_id": "cookie_parser",
  "exit_code": 0,
  "output_file": "/path/to/data/tmp/a1b2c3d4_cookie_parser.out.txt",
  "stderr_file": "/path/to/data/tmp/a1b2c3d4_cookie_parser.err.txt"
}
```

### Example: Run a Pipeline

```bash
curl -X POST http://localhost:8000/run/pipeline \
  -H "Content-Type: application/json" \
  -d '{
    "tools": ["cookie_parser", "procexp", "cmd_unlock"],
    "initial_input": "forensic_data.zip",
    "pipeline_name": "threat_analysis_v1"
  }'
```

**Response:**
```json
{
  "status": "success",
  "pipeline_id": "xyz789...",
  "pipeline_name": "threat_analysis_v1",
  "tools": ["cookie_parser", "procexp", "cmd_unlock"],
  "num_steps": 3,
  "steps_summary": [
    {"tool_id": "cookie_parser", "exit_code": 0},
    {"tool_id": "procexp", "exit_code": 0},
    {"tool_id": "cmd_unlock", "exit_code": 0}
  ]
}
```

### Example: List Tools

```bash
curl http://localhost:8000/tools
```

**Response:**
```json
{
  "tools": [
    {
      "id": "cookie_parser",
      "name": "Cookie Parser & Audit",
      "description": "Extracts and audits browser cookies for forensic analysis",
      "category": "forensics",
      "trusted": true
    },
    {
      "id": "procexp",
      "name": "Process Explorer (procexp.exe)",
      "description": "Captures running processes and system state",
      "category": "forensics",
      "trusted": true
    }
    ...
  ],
  "total": 15
}
```

### Example: Get Journal Stats

```bash
curl http://localhost:8000/stats
```

**Response:**
```json
{
  "total_runs": 42,
  "total_pipelines": 8,
  "tool_counts": {
    "cookie_parser": 10,
    "procexp": 15,
    "cmd_unlock": 12,
    ...
  },
  "journal_path": "/path/to/Legacy_Journal"
}
```

---

## 🔧 How to Add a Tool

### 1. Edit `src/orchestrator/registry.json`

Add an entry to the `"tools"` object:

```json
{
  "tools": {
    "my_new_tool": {
      "id": "my_new_tool",
      "name": "My New Tool",
      "description": "Does something awesome",
      "command": ["python", "path/to/script.py"],
      "args_template": ["{input}", "--output", "{output}"],
      "category": "analysis",
      "trusted": true,
      "version": "1.0.0"
    }
  }
}
```

### 2. Understand Fields

- **`id`** — unique identifier (used in API calls)
- **`name`** — human-readable name (shown in dashboard)
- **`description`** — what it does
- **`command`** — list of command + args (e.g., `["python", "script.py"]`)
- **`args_template`** — template for tool arguments
  - `{input}` = path to input file
  - `{output}` = path to output file
- **`category`** — tag for grouping (forensics, analysis, automation, etc.)
- **`trusted`** — boolean; if false, dashboard marks as untrusted
- **`version`** — semantic version

### 3. Test in Dashboard

Restart API:
```bash
# Ctrl+C to stop
uvicorn src.backend.orchestrator_api:app --reload --port 8000
```

Your tool should appear in the dashboard's "Available Tools" list.

### 4. Example: Wrapping an .exe

```json
{
  "procexp": {
    "id": "procexp",
    "name": "Process Explorer",
    "description": "System process inspection",
    "command": ["procexp.exe"],
    "args_template": ["/s", "/accepteula"],
    "category": "forensics",
    "trusted": true,
    "version": "16.0"
  }
}
```

**Note:** If the .exe needs to write output, use:
```json
"args_template": ["/s", "/accepteula", "-c", "{output}"]
```

---

## 📋 Audit Trail / Legacy_Journal

Every execution is logged:

```
Legacy_Journal/
├── run_a1b2c3d4e5f6_cookie_parser_plan.json
│   └── {"run_id": "...", "tool_id": "...", "cmd": [...], "start": "..."}
│
├── run_a1b2c3d4e5f6_cookie_parser_meta.json
│   └── {"run_id": "...", "exit_code": 0, "start": "...", "end": "...", ...}
│
├── pipeline_xyz789_plan.json
│   └── [same structure]
│
└── pipeline_xyz789.json
    └── {"pipeline_id": "...", "tools": [...], "steps": [...]}
```

**Why it matters:**
- ✅ Immutable record of who ran what when
- ✅ Compliance & audit trail (commit to Git for history)
- ✅ Debugging (read stderr, stdout, metadata)
- ✅ Traceability (link to data leaks, forensic investigations)

---

## 🔐 Security Considerations

1. **No PII in registry** — registry.json is committed to Git. Don't hardcode secrets.
2. **Tool trust levels** — use `"trusted": false` for untrusted tools; dashboard warns.
3. **Timeout protection** — default 120s timeout; override per request.
4. **Subprocess sandboxing** — consider running under unprivileged account or container.
5. **Input validation** — registry prevents path traversal (templates only allow specific substitutions).
6. **Audit logging** — all runs logged to Legacy_Journal; never delete logs.

---

## 🎛️ Configuration

### Environment Variables

```bash
# Optional: override API port
export ORCHESTRATOR_PORT=9000

# Optional: override journal path
export ORCHESTRATOR_JOURNAL=/custom/path/Legacy_Journal
```

### registry.json Fields (Advanced)

```json
{
  "tool": {
    "timeout_override": 300,          # max seconds for this tool
    "env_vars": {"KEY": "value"},     # environment variables to inject
    "cwd": "/optional/working/dir",   # custom working directory
    "requires_auth": false,           # require API auth (future)
    "cost_per_run": 0.01              # for billing (future)
  }
}
```

---

## 📊 Dashboard Features

- **Tool Discovery** — search/filter tools by name or category
- **Single Tool Execution** — select tool, enter input, execute
- **Pipeline Builder** — drag/drop or text-based tool chaining
- **Live Status** — auto-refresh runs every 5 seconds
- **Audit Trail Viewer** — browse all historical runs
- **Statistics** — total runs, tools, execution trends

---

## 🚢 Deployment

### Local Development

```bash
uvicorn src.backend.orchestrator_api:app --reload --port 8000
```

### Production (Docker)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "src.backend.orchestrator_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t orchestrator:latest .
docker run -p 8000:8000 -v $(pwd)/Legacy_Journal:/app/Legacy_Journal orchestrator:latest
```

### Production (Systemd)

Create `/etc/systemd/system/orchestrator.service`:

```ini
[Unit]
Description=Orchestrator API
After=network.target

[Service]
Type=notify
User=orchestrator
WorkingDirectory=/opt/orchestrator
ExecStart=/opt/orchestrator/venv/bin/uvicorn src.backend.orchestrator_api:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable orchestrator
sudo systemctl start orchestrator
sudo systemctl status orchestrator
```

---

## 📦 Publishing to Gumroad

### Package Your Workflows

Create a `workflows/` directory with example pipelines:

```
workflows/
├── threat_analysis.json          # pipeline definition
├── forensic_extraction.json
├── compliance_audit.json
└── README.md                     # how to use
```

Example `threat_analysis.json`:
```json
{
  "name": "Threat Intelligence Analysis Pipeline",
  "description": "Extract browser artifacts → capture processes → identify threats",
  "pipeline": ["cookie_parser", "procexp", "cmd_unlock"],
  "estimated_duration_minutes": 5,
  "requirements": ["Windows 10+", "Admin access"],
  "license": "Commercial"
}
```

### Create Gumroad Product

1. Go to [gumroad.com](https://gumroad.com)
2. Create product: "Systems Orchestrator - [Theme]"
3. Description:
   ```
   Automate your security workflows.

   Pre-built pipelines for threat intelligence, forensics, and compliance.
   
   Includes:
   - 30+ integrated tools
   - Pipeline templates (threat analysis, audit extraction, etc.)
   - Dashboard + REST API
   - Full audit trail

   For security professionals, incident response teams, compliance analysts.
   ```
4. Attach as downloadable:
   - `orchestrator-v1.0.zip` (source code)
   - `workflows/` (example pipelines)
   - `README.md` + `API_DOCS.md`
5. Price: $29 - $199 (tiered by features)
6. Promote via GitHub, LinkedIn, Medium

---

## 📈 Roadmap

- [ ] Web UI for pipeline builder (drag/drop)
- [ ] API authentication & rate limiting
- [ ] Workflow marketplace (share/discover pipelines)
- [ ] Scheduling & background jobs (Celery/APScheduler)
- [ ] Notifications (Slack, email on completion)
- [ ] Analytics dashboard (run trends, performance)
- [ ] Data lineage tracking (who consumed what output)
- [ ] Container support (run tools in isolated environments)

---

## 🤝 Contributing

1. Add tool to `registry.json`
2. Test via dashboard
3. Commit with description
4. Submit PR

---

## 📚 Documentation

- [API Reference](./docs/API.md)
- [Tool Development Guide](./docs/TOOLS.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Deployment](./docs/DEPLOYMENT.md)

---

## 📄 License

MIT License. See `LICENSE` for details.

---

## 🙋 Support

- **Issues**: [GitHub Issues](https://github.com/dopamin3fiends/ml-systems-portfolio/issues)
- **Discussions**: [GitHub Discussions](https://github.com/dopamin3fiends/ml-systems-portfolio/discussions)
- **Email**: contact@example.com

---

**Built with ❤️ for security professionals, forensic analysts, and automation enthusiasts.**
