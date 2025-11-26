# ⚙️ Windows Feature Manager v1.0

Professional Windows optional feature management with safety checks, presets, and rollback capabilities.

## Features

### 🔍 Feature Discovery
- **Query All Features**: List all Windows optional features with DISM
- **State Filtering**: Show only enabled/disabled features
- **Category Organization**: Group by Development, Virtualization, Networking, Security, Legacy
- **Detailed Info**: View feature descriptions, dependencies, restart requirements

### 🛡️ Safety Features
- **Admin Validation**: Requires administrator privileges for changes
- **Backup/Restore**: Save and restore complete feature states
- **Dry Run Mode**: Preview changes before applying
- **No Auto-Restart**: Control when system restarts occur

### 📦 Preset Groups
Pre-configured feature sets for common scenarios:

1. **dev_tools** - Development environment (WSL, Containers, .NET)
2. **virtualization** - Hyper-V and VM platforms
3. **networking** - Network utilities (Telnet, TFTP, SMB)
4. **security** - Security features (Application Guard)
5. **legacy** - Legacy compatibility features

### ⚡ Bulk Operations
- **Enable Presets**: Activate multiple related features at once
- **Batch Processing**: Process groups with progress tracking
- **Dependency Handling**: Automatically enable required features

## Installation

**No additional dependencies required** - uses built-in Windows PowerShell commands.

## Quick Start

### List Features
```bash
# List all features
python cli.py list

# List enabled features only
python cli.py list --state enabled

# List disabled features only
python cli.py list --state disabled
```

**Output:**
```
⚙️  Windows Optional Features (145 total)
================================================================================

📂 DEVELOPMENT
--------------------------------------------------------------------------------
✅ Microsoft-Windows-Subsystem-Linux
   Windows Subsystem for Linux - Run Linux distributions on Windows 🔄
❌ Containers
   Windows Containers - Container runtime support 🔄

📂 VIRTUALIZATION
--------------------------------------------------------------------------------
✅ Microsoft-Hyper-V-All
   Hyper-V - Hardware virtualization platform 🔄
```

### Feature Details
```bash
python cli.py info Microsoft-Windows-Subsystem-Linux
```

### Enable/Disable Features
```bash
# Enable WSL (requires admin)
python cli.py enable Microsoft-Windows-Subsystem-Linux --no-restart

# Disable Telnet client
python cli.py disable TelnetClient --no-restart
```

### Use Presets
```bash
# Enable development tools (WSL, Containers, .NET, etc.)
python cli.py preset dev_tools

# Enable virtualization features
python cli.py preset virtualization

# Skip confirmation prompt
python cli.py preset dev_tools -y
```

### Backup & Restore
```bash
# Backup current state
python cli.py backup

# Preview restore (dry run)
python cli.py restore <backup_id> --dry-run

# Restore from backup
python cli.py restore <backup_id>
```

### Demo Mode
```bash
python cli.py demo
```

## Output Files

### Backup Files (`data/tmp/feature_backups/`)
```json
{
  "backup_id": "abc-123-def-456",
  "timestamp": "2025-11-26T15:30:00.000000",
  "hostname": "WORKSTATION",
  "os_version": "10.0.19045",
  "features": {
    "Microsoft-Windows-Subsystem-Linux": "enabled",
    "Containers": "disabled",
    "Microsoft-Hyper-V-All": "enabled"
  }
}
```

## Integration with Orchestrator

### Via REST API
```bash
curl -X POST http://localhost:8000/run/tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_id": "windows_features",
    "input_text": "preset|dev_tools"
  }'
```

### Via Dashboard
1. Navigate to http://localhost:8000
2. Select "Windows Feature Manager"
3. Provide: `preset|dev_tools` or `enable|Microsoft-Windows-Subsystem-Linux`
4. Click "Run Tool"

## Architecture

```
windows_features/
├── models.py          # Data classes (WindowsFeature, FeatureGroup, etc.)
├── manager.py         # PowerShell-based feature management
├── cli.py            # Command-line interface
└── README.md         # This file
```

## Use Cases

### 🧑‍💻 Development Setup
```bash
# Enable full development stack
python cli.py preset dev_tools

# Features enabled:
# - WSL 2
# - Virtual Machine Platform
# - Windows Containers
# - .NET Framework 3.5
# - .NET Framework 4.8 ASPNET
```

### 🖥️ Server Configuration
```bash
# Enable Hyper-V for virtualization
python cli.py preset virtualization

# Backup before changes
python cli.py backup

# Restore if issues occur
python cli.py restore <backup_id>
```

### 🔒 Security Hardening
```bash
# Disable legacy protocols
python cli.py disable TelnetClient
python cli.py disable SMB1Protocol

# Enable security features
python cli.py preset security
```

### 🔄 System Migration
```bash
# Backup source system
python cli.py backup

# Copy backup file to target system
# Restore on target system
python cli.py restore <backup_id>
```

## Advanced Usage

### Custom Presets
Edit `models.py` to add custom presets:
```python
FEATURE_GROUPS["my_preset"] = FeatureGroup(
    name="My Custom Preset",
    description="Custom feature set",
    features=[
        "Feature1",
        "Feature2"
    ],
    category=FeatureCategory.DEVELOPMENT
)
```

### Scripting
```python
from manager import WindowsFeatureManager

manager = WindowsFeatureManager()

# Check admin
if not manager.is_admin():
    print("Need admin!")
    exit(1)

# Enable feature
result = manager.enable_feature("Microsoft-Windows-Subsystem-Linux")
print(result.message)
```

### Batch Processing
```bash
# Enable multiple features
for feature in WSL VirtualMachinePlatform Containers; do
    python cli.py enable $feature --no-restart
done
```

## Preset Details

### Development Tools (`dev_tools`)
- **WSL (Windows Subsystem for Linux)** - Run Linux CLI tools
- **Virtual Machine Platform** - Required for WSL 2
- **Containers** - Docker Desktop support
- **Hyper-V** - Hardware virtualization
- **.NET Framework 3.5** - Legacy .NET support
- **.NET Framework 4.8 ASPNET** - Modern ASP.NET

### Virtualization (`virtualization`)
- **Hyper-V All** - Complete Hyper-V suite
- **Hyper-V Management PowerShell** - PowerShell cmdlets
- **Virtual Machine Platform** - Core VM support
- **Hypervisor Platform** - Windows Hypervisor

### Networking (`networking`)
- **Telnet Client** - Legacy network protocol
- **TFTP Client** - Trivial FTP
- **Simple TCP/IP Services** - Echo, discard, etc.
- **SMB 1.0 Protocol** - Legacy file sharing (insecure)

### Security (`security`)
- **Windows Defender Application Guard** - Sandbox for Edge
- **Hypervisor** - Hardware-based security

### Legacy (`legacy`)
- **Legacy Components** - Older Windows features
- **DirectPlay** - Legacy gaming API
- **.NET Framework 3.5** - Legacy .NET

## Requirements

### System Requirements
- **OS**: Windows 10/11 (Pro, Enterprise, or Education for Hyper-V)
- **Privileges**: Administrator for enable/disable operations
- **PowerShell**: Built-in (version 5.1+)

### Hardware Requirements (for specific features)
- **Hyper-V**: CPU virtualization support (Intel VT-x/AMD-V)
- **WSL 2**: Virtual Machine Platform
- **Containers**: Hyper-V or WSL 2

## Troubleshooting

### "Administrator privileges required"
- Right-click PowerShell/CMD
- Select "Run as Administrator"
- Navigate to project directory
- Run command again

### "Feature not found"
- Run `python cli.py list` to see available features
- Check exact feature name (case-sensitive)
- Some features only available on Pro/Enterprise editions

### "Restart required" but system won't restart
- Run: `shutdown /r /t 0` (immediate restart)
- Or: `shutdown /r /t 300` (restart in 5 minutes)
- Or restart manually via Start menu

### Backup restore fails
- Ensure running as Administrator
- Check backup file exists in `data/tmp/feature_backups/`
- Use `--dry-run` to preview changes first

### Feature enable fails
- Check Windows edition (Home vs Pro)
- Verify hardware support (CPU virtualization for Hyper-V)
- Check disk space (some features require downloads)
- Review Windows Update status

## Security Considerations

### Permissions
- Requires **Administrator privileges** for modifications
- Read-only operations (list, info) don't require admin
- Backup/restore require admin to apply changes

### Risk Management
- **Always backup** before major changes
- **Test in VM** before production systems
- **Review presets** before enabling groups
- **Understand dependencies** between features

### Legacy Protocols
- **TelnetClient**: Unencrypted, insecure
- **SMB1Protocol**: Security vulnerabilities, disable if possible
- **DirectPlay**: Deprecated gaming API

## Educational Use

This tool is designed for **authorized system administration** including:
- Corporate IT management
- Development environment setup
- System configuration standardization
- Educational/training purposes

**DO NOT use for:**
- Unauthorized system modifications
- Disabling security features maliciously
- Circumventing organizational policies

## Support

For issues, feature requests, or questions:
- GitHub: https://github.com/dopamin3fiends/ml-systems-portfolio
- Email: support@example.com

---

**Built with ❤️ by the Legacy Systems Team**

*"Professional Windows feature management made simple"*
