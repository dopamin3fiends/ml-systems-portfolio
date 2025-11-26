"""
ADB Automation Framework - ADB Manager
Android Debug Bridge wrapper for device management and automation
"""

import subprocess
import time
import re
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any

try:
    from models import (
        Device, DeviceStatus, Package, AutomationTask, TaskResult,
        InputMethod, KeyCode
    )
except ImportError:
    from .models import (
        Device, DeviceStatus, Package, AutomationTask, TaskResult,
        InputMethod, KeyCode
    )


class ADBManager:
    """
    Android Debug Bridge manager for device automation
    
    Features:
    - Device discovery and management
    - App installation and control
    - File transfer (push/pull)
    - Screen capture and recording
    - Input simulation (tap, swipe, text)
    - Shell command execution
    - Automation task execution
    """
    
    def __init__(self, adb_path: str = "adb", output_dir: str = "data/tmp/adb_output"):
        """
        Initialize ADB manager
        
        Args:
            adb_path: Path to adb executable
            output_dir: Directory for screenshots and output files
        """
        self.adb_path = adb_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Verify ADB is available
        try:
            self._run_adb_command(["version"])
        except Exception as e:
            raise RuntimeError(f"ADB not found at '{adb_path}'. Install Android SDK Platform Tools.") from e
    
    def _run_adb_command(self, args: List[str], device_serial: Optional[str] = None, 
                         timeout: int = 30) -> str:
        """
        Run ADB command and return output
        
        Args:
            args: ADB command arguments
            device_serial: Target device serial (None = first device)
            timeout: Command timeout in seconds
            
        Returns:
            Command output as string
        """
        cmd = [self.adb_path]
        
        if device_serial:
            cmd.extend(["-s", device_serial])
        
        cmd.extend(args)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"ADB command failed: {result.stderr}")
        
        return result.stdout.strip()
    
    def get_devices(self) -> List[Device]:
        """
        Get list of connected devices
        
        Returns:
            List of Device objects
        """
        output = self._run_adb_command(["devices", "-l"])
        lines = output.split("\n")[1:]  # Skip "List of devices attached"
        
        devices = []
        for line in lines:
            if not line.strip():
                continue
            
            parts = line.split()
            if len(parts) < 2:
                continue
            
            serial = parts[0]
            status_str = parts[1]
            
            # Parse status
            status = DeviceStatus.UNKNOWN
            for ds in DeviceStatus:
                if ds.value == status_str:
                    status = ds
                    break
            
            # Parse model from device info
            model = None
            for part in parts[2:]:
                if part.startswith("model:"):
                    model = part.split(":")[1]
                    break
            
            device = Device(serial=serial, status=status, model=model)
            
            # Get additional device info if online
            if status == DeviceStatus.ONLINE:
                try:
                    device.model = self._get_device_property(serial, "ro.product.model")
                    device.android_version = self._get_device_property(serial, "ro.build.version.release")
                    
                    sdk_str = self._get_device_property(serial, "ro.build.version.sdk")
                    device.sdk_version = int(sdk_str) if sdk_str else None
                    
                    # Get battery level
                    battery_output = self._run_adb_command(["shell", "dumpsys", "battery"], serial)
                    battery_match = re.search(r"level: (\d+)", battery_output)
                    if battery_match:
                        device.battery_level = int(battery_match.group(1))
                    
                    # Get screen resolution
                    screen_output = self._run_adb_command(["shell", "wm", "size"], serial)
                    screen_match = re.search(r"(\d+)x(\d+)", screen_output)
                    if screen_match:
                        device.screen_resolution = (int(screen_match.group(1)), int(screen_match.group(2)))
                    
                    # Check root
                    try:
                        root_check = self._run_adb_command(["shell", "su", "-c", "id"], serial)
                        device.is_rooted = "uid=0" in root_check
                    except:
                        device.is_rooted = False
                
                except Exception as e:
                    print(f"Warning: Could not get full device info for {serial}: {e}")
            
            devices.append(device)
        
        return devices
    
    def _get_device_property(self, device_serial: str, prop_name: str) -> Optional[str]:
        """Get device property value"""
        try:
            output = self._run_adb_command(["shell", "getprop", prop_name], device_serial)
            return output if output else None
        except:
            return None
    
    def install_apk(self, device_serial: str, apk_path: str, reinstall: bool = False) -> bool:
        """
        Install APK on device
        
        Args:
            device_serial: Target device serial
            apk_path: Path to APK file
            reinstall: Allow downgrade/reinstall
            
        Returns:
            True if successful
        """
        args = ["install"]
        if reinstall:
            args.append("-r")
        args.append(apk_path)
        
        try:
            output = self._run_adb_command(args, device_serial, timeout=120)
            return "Success" in output
        except Exception as e:
            print(f"Install failed: {e}")
            return False
    
    def uninstall_app(self, device_serial: str, package_name: str) -> bool:
        """Uninstall app from device"""
        try:
            output = self._run_adb_command(["uninstall", package_name], device_serial)
            return "Success" in output
        except Exception as e:
            print(f"Uninstall failed: {e}")
            return False
    
    def list_packages(self, device_serial: str, filter_text: Optional[str] = None) -> List[Package]:
        """
        List installed packages
        
        Args:
            device_serial: Target device serial
            filter_text: Filter packages by name
            
        Returns:
            List of Package objects
        """
        args = ["shell", "pm", "list", "packages"]
        if filter_text:
            args.append(filter_text)
        
        output = self._run_adb_command(args, device_serial)
        lines = output.split("\n")
        
        packages = []
        for line in lines:
            if line.startswith("package:"):
                package_name = line[8:].strip()
                packages.append(Package(package_name=package_name))
        
        return packages
    
    def start_app(self, device_serial: str, package_name: str, activity: Optional[str] = None) -> bool:
        """
        Start app on device
        
        Args:
            device_serial: Target device serial
            package_name: App package name
            activity: Activity to launch (optional)
            
        Returns:
            True if successful
        """
        try:
            if activity:
                component = f"{package_name}/{activity}"
            else:
                component = package_name
            
            self._run_adb_command(
                ["shell", "monkey", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1"],
                device_serial
            )
            return True
        except Exception as e:
            print(f"Start app failed: {e}")
            return False
    
    def stop_app(self, device_serial: str, package_name: str) -> bool:
        """Force stop app on device"""
        try:
            self._run_adb_command(["shell", "am", "force-stop", package_name], device_serial)
            return True
        except Exception as e:
            print(f"Stop app failed: {e}")
            return False
    
    def screenshot(self, device_serial: str, filename: str) -> Optional[str]:
        """
        Capture screenshot from device
        
        Args:
            device_serial: Target device serial
            filename: Output filename
            
        Returns:
            Path to saved screenshot
        """
        try:
            device_path = "/sdcard/screenshot_temp.png"
            
            # Capture on device
            self._run_adb_command(["shell", "screencap", "-p", device_path], device_serial)
            
            # Pull to local
            output_path = self.output_dir / filename
            self._run_adb_command(["pull", device_path, str(output_path)], device_serial)
            
            # Clean up device
            self._run_adb_command(["shell", "rm", device_path], device_serial)
            
            return str(output_path)
        except Exception as e:
            print(f"Screenshot failed: {e}")
            return None
    
    def input_tap(self, device_serial: str, x: int, y: int) -> bool:
        """Simulate tap at coordinates"""
        try:
            self._run_adb_command(["shell", "input", "tap", str(x), str(y)], device_serial)
            return True
        except:
            return False
    
    def input_swipe(self, device_serial: str, x1: int, y1: int, x2: int, y2: int, 
                    duration: int = 300) -> bool:
        """Simulate swipe gesture"""
        try:
            self._run_adb_command(
                ["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)],
                device_serial
            )
            return True
        except:
            return False
    
    def input_text(self, device_serial: str, text: str) -> bool:
        """Input text (spaces must be escaped with %s)"""
        try:
            escaped_text = text.replace(" ", "%s")
            self._run_adb_command(["shell", "input", "text", escaped_text], device_serial)
            return True
        except:
            return False
    
    def input_keyevent(self, device_serial: str, keycode: int) -> bool:
        """Send key event"""
        try:
            self._run_adb_command(["shell", "input", "keyevent", str(keycode)], device_serial)
            return True
        except:
            return False
    
    def shell_command(self, device_serial: str, command: str) -> Optional[str]:
        """Execute shell command on device"""
        try:
            return self._run_adb_command(["shell", command], device_serial)
        except Exception as e:
            print(f"Shell command failed: {e}")
            return None
    
    def push_file(self, device_serial: str, local_path: str, remote_path: str) -> bool:
        """Push file to device"""
        try:
            self._run_adb_command(["push", local_path, remote_path], device_serial)
            return True
        except Exception as e:
            print(f"Push failed: {e}")
            return False
    
    def pull_file(self, device_serial: str, remote_path: str, local_path: str) -> bool:
        """Pull file from device"""
        try:
            self._run_adb_command(["pull", remote_path, local_path], device_serial)
            return True
        except Exception as e:
            print(f"Pull failed: {e}")
            return False
    
    def run_task(self, task: AutomationTask, device_serial: Optional[str] = None) -> TaskResult:
        """
        Execute automation task
        
        Args:
            task: Task to execute
            device_serial: Target device (or task.device_serial)
            
        Returns:
            TaskResult with execution details
        """
        if device_serial is None:
            device_serial = task.device_serial
        
        if device_serial is None:
            devices = self.get_devices()
            if not devices:
                raise RuntimeError("No devices connected")
            device_serial = devices[0].serial
        
        start_time = datetime.now()
        result = TaskResult(
            task_name=task.name,
            device_serial=device_serial,
            status="running",
            start_time=start_time
        )
        
        try:
            # Repeat task
            for repeat in range(task.repeat_count):
                # Execute actions
                for action in task.actions:
                    try:
                        # Replace variables
                        context = {
                            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
                            "device_serial": device_serial,
                            "repeat": repeat
                        }
                        
                        action_type = action.get("type")
                        
                        if action_type == "shell":
                            command = action["command"].format(**context)
                            self.shell_command(device_serial, command)
                        
                        elif action_type == "screenshot":
                            filename = action["filename"].format(**context)
                            screenshot_path = self.screenshot(device_serial, filename)
                            if screenshot_path:
                                result.screenshots.append(screenshot_path)
                        
                        elif action_type == "tap":
                            self.input_tap(device_serial, action["x"], action["y"])
                        
                        elif action_type == "swipe":
                            self.input_swipe(
                                device_serial, 
                                action["x1"], action["y1"],
                                action["x2"], action["y2"],
                                action.get("duration", 300)
                            )
                        
                        elif action_type == "text":
                            text = action["text"].format(**context)
                            self.input_text(device_serial, text)
                        
                        elif action_type == "keyevent":
                            self.input_keyevent(device_serial, action["keycode"])
                        
                        elif action_type == "wait":
                            time.sleep(action.get("duration", 1))
                        
                        elif action_type == "app_start":
                            package = action["package"].format(**context)
                            self.start_app(device_serial, package)
                        
                        elif action_type == "app_stop":
                            package = action["package"].format(**context)
                            self.stop_app(device_serial, package)
                        
                        result.actions_completed += 1
                        
                        # Delay between actions
                        if task.delay_between_actions > 0:
                            time.sleep(task.delay_between_actions)
                    
                    except Exception as e:
                        result.actions_failed += 1
                        print(f"Action failed: {action_type} - {e}")
            
            result.status = "completed" if result.actions_failed == 0 else "partial"
        
        except Exception as e:
            result.status = "failed"
            result.error_message = str(e)
        
        finally:
            result.end_time = datetime.now()
        
        return result


def demo_adb():
    """Demo mode: Show device information"""
    print("🤖 ADB Automation Framework Demo\n")
    print("=" * 60)
    
    try:
        manager = ADBManager()
        
        print("\n[1/3] Discovering devices...")
        devices = manager.get_devices()
        
        if not devices:
            print("   ⚠️  No devices found")
            print("   Connect an Android device or start an emulator")
            print("\n   Troubleshooting:")
            print("   1. Enable USB debugging on device")
            print("   2. Accept USB debugging prompt on device")
            print("   3. Run: adb devices")
            return
        
        print(f"   ✅ Found {len(devices)} device(s)")
        
        print("\n[2/3] Device Information")
        for i, device in enumerate(devices, 1):
            print(f"\n   Device {i}:")
            print(f"      Serial: {device.serial}")
            print(f"      Status: {device.status.value}")
            
            if device.model:
                print(f"      Model: {device.model}")
            if device.android_version:
                print(f"      Android: {device.android_version} (API {device.sdk_version})")
            if device.battery_level is not None:
                print(f"      Battery: {device.battery_level}%")
            if device.screen_resolution:
                print(f"      Screen: {device.screen_resolution[0]}x{device.screen_resolution[1]}")
            print(f"      Rooted: {'Yes' if device.is_rooted else 'No'}")
        
        print("\n[3/3] Demo complete!")
        print("\n   Try these commands:")
        print("   • python cli.py devices - List all devices")
        print("   • python cli.py screenshot - Capture screenshot")
        print("   • python cli.py packages - List installed apps")
        print("   • python cli.py task device_info - Run preset task")
    
    except RuntimeError as e:
        print(f"\n   ❌ Error: {e}")
        print("\n   Install Android SDK Platform Tools:")
        print("   https://developer.android.com/studio/releases/platform-tools")
    except Exception as e:
        print(f"\n   ❌ Unexpected error: {e}")
    
    print("\n" + "=" * 60)
