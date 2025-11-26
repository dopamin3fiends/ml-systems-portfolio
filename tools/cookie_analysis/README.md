# Cookie Analysis Suite v2.0

Professional browser cookie forensics toolkit for security analysis, privacy auditing, and threat intelligence.

## Features

- **Parse**: Extract cookies from multiple formats (Netscape, JSON, Chrome)
- **Enrich**: Add company/purpose metadata using known cookie database
- **Scan**: Identify privacy and security risks
- **Report**: Generate domain and company summaries

## Quick Start

```bash
# Demo mode (generates sample data)
python cli.py --demo

# Analyze real cookie file
python cli.py --input cookies.txt --output-dir results/
```

## Output

Creates 5 JSON reports per run:
- `cookies_parsed_*.json` - Cleaned cookie data
- `cookies_enriched_*.json` - With company/purpose metadata
- `cookie_risks_*.json` - Security/privacy risk analysis
- `cookie_domain_summary_*.json` - Per-domain statistics
- `cookie_company_summary_*.json` - Per-company statistics

## Integration with Orchestrator

Added to `registry.json` as:
- `cookie_parser` - Full analysis pipeline
- `cookie_parser_demo` - Demo mode

## Architecture

```
cli.py          → Main orchestrator
models.py       → Data classes (Cookie, RiskLevel, etc.)
parser.py       → Stage 1: Parse & clean
enricher.py     → Stage 2: Add metadata
risk_scanner.py → Stage 3: Identify risks
reporter.py     → Stage 4: Generate summaries
```

## Educational Use

This tool uses **demo/sanitized data** by default. For production use with real cookies, ensure compliance with privacy laws (GDPR, CCPA, etc.).

## License

Part of the Systems Integration Orchestrator portfolio project.
