# ADB Automation Framework v1.0

Professional Android device automation framework for testing, debugging, and device management. Built with Android Debug Bridge (ADB) for comprehensive device control.

## Features

✅ **Device Management**: Discover and manage multiple Android devices/emulators  
✅ **App Control**: Install, uninstall, start, stop applications  
✅ **File Transfer**: Push/pull files between device and computer  
✅ **Screen Capture**: Screenshots and screen recording  
✅ **Input Simulation**: Tap, swipe, text input, key events  
✅ **Shell Commands**: Execute any shell command on device  
✅ **Automation Tasks**: Preset and custom automation workflows  
✅ **Battery Monitoring**: Track battery level and charging status  
✅ **Package Management**: List and manage installed packages  

## Prerequisites

**Android SDK Platform Tools** (includes `adb` command):

- **Windows**: [Download Platform Tools](https://developer.android.com/studio/releases/platform-tools)
- **macOS**: `brew install android-platform-tools`
- **Linux**: `sudo apt install android-tools-adb` or download from link above

Add `adb` to your PATH or use `--adb-path` flag to specify location.

## Quick Start

### Enable USB Debugging on Android Device

1. Go to **Settings → About phone**
2. Tap **Build number** 7 times to enable Developer options
3. Go to **Settings → System → Developer options**
4. Enable **USB debugging**
5. Connect device via USB and accept debugging prompt

### Run Demo Mode

```bash
python cli.py demo
```

Demo shows connected devices with model, Android version, battery, and screen resolution.

## Commands

### List Connected Devices

```bash
python cli.py devices
```

Output includes:
- Serial number
- Connection status
- Model name
- Android version (API level)
- Battery percentage
- Screen resolution
- Root status

Save as JSON:
```bash
python cli.py devices --json
```

### Capture Screenshot

```bash
# Default filename
python cli.py screenshot

# Custom filename
python cli.py screenshot --filename my_screen.png

# Specific device
python cli.py screenshot --device <serial>
```

### List Installed Apps

```bash
# All packages
python cli.py packages

# Filter by name
python cli.py packages --filter com.google

# Limit results
python cli.py packages --limit 20

# Save as JSON
python cli.py packages --json
```

### Execute Shell Command

```bash
# Get Android version
python cli.py shell "getprop ro.build.version.release"

# Get battery info
python cli.py shell "dumpsys battery"

# List running processes
python cli.py shell "ps"

# Get device uptime
python cli.py shell "uptime"
```

### Run Automation Task

**Preset tasks:**
```bash
# Device information
python cli.py task device_info

# App launch test
python cli.py task app_launch_test --context package_name=com.example.app

# Screenshot sequence
python cli.py task screenshot_sequence

# UI interaction test
python cli.py task ui_interaction

# Battery monitor
python cli.py task battery_monitor
```

**Custom task from JSON:**
```bash
python cli.py task my_task.json --save-result
```

### List Available Tasks

```bash
python cli.py list
```

## Preset Tasks

### device_info
Collect comprehensive device information including model, Android version, battery, and capture screenshot.

### app_launch_test
Launch specified app, wait 3 seconds, capture screenshot, then stop app.

**Context required:**
- `package_name` - App package (e.g., `com.android.chrome`)

### screenshot_sequence
Capture 3 screenshots with 2-second delays between each.

### ui_interaction
Test basic UI interactions: tap, swipe, back button, screenshot.

### battery_monitor
Monitor battery level every 60 seconds (repeats 5 times).

## Custom Automation Tasks

Create JSON file with task definition:

```json
{
  "name": "My Automation Task",
  "description": "Custom automation workflow",
  "actions": [
    {
      "type": "shell",
      "command": "input keyevent 3"
    },
    {
      "type": "wait",
      "duration": 2
    },
    {
      "type": "tap",
      "x": 500,
      "y": 1000
    },
    {
      "type": "screenshot",
      "filename": "result_{timestamp}.png"
    }
  ],
  "repeat_count": 1,
  "delay_between_actions": 1.0
}
```

Run custom task:
```bash
python cli.py task my_task.json
```

## Action Types

| Action Type | Description | Parameters | Example |
|-------------|-------------|------------|---------|
| `shell` | Execute shell command | `command` | `{"type": "shell", "command": "pm list packages"}` |
| `screenshot` | Capture screenshot | `filename` | `{"type": "screenshot", "filename": "screen.png"}` |
| `tap` | Tap at coordinates | `x`, `y` | `{"type": "tap", "x": 500, "y": 1000}` |
| `swipe` | Swipe gesture | `x1`, `y1`, `x2`, `y2`, `duration` | `{"type": "swipe", "x1": 500, "y1": 1500, "x2": 500, "y2": 500}` |
| `text` | Input text | `text` | `{"type": "text", "text": "Hello World"}` |
| `keyevent` | Send key code | `keycode` | `{"type": "keyevent", "keycode": 3}` |
| `wait` | Pause execution | `duration` (seconds) | `{"type": "wait", "duration": 2}` |
| `app_start` | Launch app | `package` | `{"type": "app_start", "package": "com.android.chrome"}` |
| `app_stop` | Stop app | `package` | `{"type": "app_stop", "package": "com.android.chrome"}` |

## Common Key Codes

| Key | Code | Usage |
|-----|------|-------|
| HOME | 3 | Return to home screen |
| BACK | 4 | Back button |
| MENU | 82 | Menu button |
| POWER | 26 | Power button |
| VOLUME_UP | 24 | Increase volume |
| VOLUME_DOWN | 25 | Decrease volume |
| ENTER | 66 | Enter/OK |
| DELETE | 67 | Delete/Backspace |
| APP_SWITCH | 187 | Recent apps |

Full list: [Android KeyEvent](https://developer.android.com/reference/android/view/KeyEvent)

## Python API Usage

```python
from adb_manager import ADBManager
from models import AutomationTask

# Initialize manager
manager = ADBManager(adb_path="adb")

# Get devices
devices = manager.get_devices()
for device in devices:
    print(f"{device.serial}: {device.model}")

# Capture screenshot
screenshot_path = manager.screenshot(device.serial, "screenshot.png")

# Execute shell command
output = manager.shell_command(device.serial, "getprop ro.product.model")

# Input simulation
manager.input_tap(device.serial, 500, 1000)
manager.input_swipe(device.serial, 500, 1500, 500, 500, duration=300)
manager.input_text(device.serial, "Hello World")

# App control
manager.install_apk(device.serial, "app.apk")
manager.start_app(device.serial, "com.example.app")
manager.stop_app(device.serial, "com.example.app")

# File transfer
manager.push_file(device.serial, "local.txt", "/sdcard/remote.txt")
manager.pull_file(device.serial, "/sdcard/remote.txt", "local.txt")

# Run automation task
task = AutomationTask(
    name="Test Task",
    description="Test automation",
    actions=[
        {"type": "tap", "x": 500, "y": 1000},
        {"type": "screenshot", "filename": "test.png"}
    ]
)
result = manager.run_task(task, device.serial)
print(f"Status: {result.status}, Duration: {result.duration}s")
```

## Use Cases

### ✅ Legitimate Use Cases

- **App Testing**: Automated regression testing of Android apps
- **QA Workflows**: Test app installation, launch, and basic flows
- **Device Management**: Bulk device configuration and setup
- **Screenshot Documentation**: Generate app documentation screenshots
- **Performance Testing**: Monitor battery, memory, CPU during testing
- **Debugging**: Remote device debugging and log collection
- **CI/CD Integration**: Automated testing in continuous integration
- **Development**: Quick device operations during development

### ❌ DO NOT Use For

- **Malware Distribution**: Installing malicious apps
- **Privacy Invasion**: Unauthorized access to devices or data
- **Game Cheating**: Automated gameplay or cheating
- **App Store Manipulation**: Fake reviews, ratings, or installs
- **Surveillance**: Unauthorized monitoring or spying
- **ToS Violations**: Automating actions prohibited by app terms

## Integration with Orchestrator

Register tool in `src/orchestrator/registry.json`:

```json
{
  "id": "adb_automation",
  "name": "ADB Automation Framework",
  "description": "Android device automation and management",
  "command": ["python", "tools/adb_automation/cli.py"],
  "args_template": ["task", "{task}", "--context", "package_name={package}"],
  "category": "automation",
  "trusted": true,
  "version": "1.0.0",
  "demo_mode": {
    "command": ["python", "tools/adb_automation/cli.py", "demo"],
    "safe": true
  }
}
```

## Architecture

```
tools/adb_automation/
├── models.py        # Data models (Device, Package, AutomationTask, TaskResult)
├── adb_manager.py   # ADB wrapper with device management and automation
├── cli.py           # Command-line interface
└── README.md        # Documentation
```

**Data Flow**:
1. **models.py**: Define device info, tasks, and results
2. **adb_manager.py**: ADBManager wraps ADB commands with Python
3. **cli.py**: Parse arguments, execute commands, display results

## Troubleshooting

**"ADB not found"**:
- Install Android SDK Platform Tools
- Add `adb` to PATH or use `--adb-path` flag
- Verify: `adb version`

**"No devices found"**:
- Enable USB debugging on device
- Connect via USB cable
- Accept USB debugging prompt on device
- Check connection: `adb devices`

**"device unauthorized"**:
- Disconnect and reconnect device
- Accept USB debugging authorization on device
- Check "Always allow from this computer"

**"device offline"**:
- Restart ADB: `adb kill-server` then `adb start-server`
- Restart device
- Try different USB cable or port

**Screenshot/command fails**:
- Check device is unlocked
- Verify USB debugging is enabled
- Try: `adb shell screencap -p /sdcard/test.png`

## Wireless ADB (WiFi)

Connect to device over WiFi:

```bash
# On device via USB first
adb tcpip 5555

# Find device IP (Settings → About → Status → IP address)
# Connect wirelessly
adb connect <device_ip>:5555

# Now unplug USB cable and use wireless
python cli.py devices
```

## Security & Privacy

⚠️ **This tool is for authorized testing and development only.**

**Security considerations:**
- Only connect to devices you own or have permission to access
- USB debugging allows full device access - use responsibly
- Disable USB debugging when not in development
- Never grant USB debugging to unknown computers
- Automation can modify device settings and data - test carefully
- Screenshots may capture sensitive information - handle appropriately

**Legal compliance:**
- Obtain explicit permission before automating on devices
- Respect app Terms of Service
- Do not use for unauthorized access or surveillance
- Follow applicable laws regarding device access and automation

## Educational Use Disclaimer

This tool is for **educational, testing, and development purposes only**.

Users are responsible for:
- Obtaining permission for device access
- Complying with app Terms of Service
- Following applicable laws and regulations
- Protecting captured data and screenshots
- Using automation ethically and responsibly

**Misuse may result in:**
- Device damage or data loss
- Account suspension or bans
- Legal action from app developers
- Violation of computer fraud laws

**Always use responsibly and ethically.**

## License

MIT License - See LICENSE file for details

## Version History

- **v1.0.0** (2024-01): Initial release
  - Device discovery and management
  - 9 action types (shell, screenshot, tap, swipe, text, keyevent, wait, app_start, app_stop)
  - 5 preset tasks (device_info, app_launch_test, screenshot_sequence, ui_interaction, battery_monitor)
  - File transfer (push/pull)
  - Package management
  - Task automation with repeat and context variables

---

**Part of ml-systems-portfolio** - Professional Systems Integration Orchestrator
