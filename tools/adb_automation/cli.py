"""
ADB Automation Framework - CLI Interface
Command-line interface for Android device automation
"""

import argparse
import json
from pathlib import Path
from datetime import datetime

try:
    from models import AutomationTask, PRESET_TASKS
    from adb_manager import ADBManager, demo_adb
except ImportError:
    from .models import AutomationTask, PRESET_TASKS
    from .adb_manager import ADBManager, demo_adb


def devices_command(args):
    """List connected devices"""
    print("🤖 Connected Devices\n")
    
    try:
        manager = ADBManager(adb_path=args.adb_path)
        devices = manager.get_devices()
        
        if not devices:
            print("No devices found. Connect device and enable USB debugging.")
            return
        
        for i, device in enumerate(devices, 1):
            print(f"\nDevice {i}:")
            print(f"   Serial: {device.serial}")
            print(f"   Status: {device.status.value}")
            
            if device.model:
                print(f"   Model: {device.model}")
            if device.android_version:
                print(f"   Android: {device.android_version} (API {device.sdk_version})")
            if device.battery_level is not None:
                print(f"   Battery: {device.battery_level}%")
            if device.screen_resolution:
                print(f"   Resolution: {device.screen_resolution[0]}x{device.screen_resolution[1]}")
            print(f"   Rooted: {'Yes' if device.is_rooted else 'No'}")
        
        if args.json:
            output_path = Path(args.output) / f"devices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_path, 'w') as f:
                json.dump([d.to_dict() for d in devices], f, indent=2)
            print(f"\n✅ Saved to: {output_path}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def packages_command(args):
    """List installed packages"""
    print("🤖 Installed Packages\n")
    
    try:
        manager = ADBManager(adb_path=args.adb_path)
        devices = manager.get_devices()
        
        if not devices:
            print("No devices found.")
            return
        
        device_serial = args.device or devices[0].serial
        print(f"Device: {device_serial}\n")
        
        packages = manager.list_packages(device_serial, args.filter)
        print(f"Found {len(packages)} packages")
        
        if args.limit:
            packages = packages[:args.limit]
        
        for pkg in packages:
            print(f"   • {pkg.package_name}")
        
        if args.json:
            output_path = Path(args.output) / f"packages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_path, 'w') as f:
                json.dump([p.to_dict() for p in packages], f, indent=2)
            print(f"\n✅ Saved to: {output_path}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def screenshot_command(args):
    """Capture screenshot"""
    print("🤖 Screenshot Capture\n")
    
    try:
        manager = ADBManager(adb_path=args.adb_path, output_dir=args.output)
        devices = manager.get_devices()
        
        if not devices:
            print("No devices found.")
            return
        
        device_serial = args.device or devices[0].serial
        print(f"Device: {device_serial}")
        
        filename = args.filename or f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        print(f"Capturing...")
        screenshot_path = manager.screenshot(device_serial, filename)
        
        if screenshot_path:
            print(f"✅ Saved: {screenshot_path}")
        else:
            print("❌ Screenshot failed")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def shell_command(args):
    """Execute shell command"""
    print("🤖 Shell Command\n")
    
    try:
        manager = ADBManager(adb_path=args.adb_path)
        devices = manager.get_devices()
        
        if not devices:
            print("No devices found.")
            return
        
        device_serial = args.device or devices[0].serial
        print(f"Device: {device_serial}")
        print(f"Command: {args.command}\n")
        
        output = manager.shell_command(device_serial, args.command)
        
        if output:
            print("Output:")
            print(output)
        else:
            print("❌ Command failed")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def task_command(args):
    """Execute automation task"""
    print(f"🤖 Running Task: {args.task}\n")
    
    try:
        manager = ADBManager(adb_path=args.adb_path, output_dir=args.output)
        devices = manager.get_devices()
        
        if not devices:
            print("No devices found.")
            return
        
        device_serial = args.device or devices[0].serial
        
        # Load task
        if args.task in PRESET_TASKS:
            task = PRESET_TASKS[args.task]
            print(f"Preset: {task.name}")
            print(f"Description: {task.description}")
        else:
            task_path = Path(args.task)
            if not task_path.exists():
                print(f"❌ Task not found: {args.task}")
                return
            
            with open(task_path) as f:
                task_data = json.load(f)
            task = AutomationTask(**task_data)
            print(f"Custom: {task.name}")
        
        print(f"Device: {device_serial}")
        print(f"Actions: {len(task.actions)}\n")
        
        # Parse context
        context = {}
        if args.context:
            for item in args.context:
                key, value = item.split("=", 1)
                context[key] = value
        
        # Apply context to task actions
        if context:
            for action in task.actions:
                for key, value in action.items():
                    if isinstance(value, str):
                        action[key] = value.format(**context)
        
        print("Executing...")
        result = manager.run_task(task, device_serial)
        
        print(f"\n✅ Task Complete")
        print(f"   Status: {result.status}")
        print(f"   Duration: {result.duration:.2f}s")
        print(f"   Completed: {result.actions_completed}")
        print(f"   Failed: {result.actions_failed}")
        
        if result.screenshots:
            print(f"   Screenshots: {len(result.screenshots)}")
            for screenshot in result.screenshots:
                print(f"      • {screenshot}")
        
        if result.error_message:
            print(f"   Error: {result.error_message}")
        
        if args.save_result:
            result_path = Path(args.output) / f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(result_path, 'w') as f:
                json.dump(result.to_dict(), f, indent=2)
            print(f"\n   Result saved: {result_path}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def list_tasks_command(args):
    """List available preset tasks"""
    print("🤖 Available Preset Tasks\n")
    print("=" * 60)
    
    for name, task in PRESET_TASKS.items():
        print(f"\n{name}")
        print(f"   {task.description}")
        print(f"   Actions: {len(task.actions)}")


def demo_command(args):
    """Run demo mode"""
    demo_adb()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="ADB Automation Framework - Android device automation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List connected devices
  python cli.py devices
  
  # Capture screenshot
  python cli.py screenshot
  
  # List installed apps
  python cli.py packages --filter com.google
  
  # Run shell command
  python cli.py shell "pm list packages"
  
  # Run preset task
  python cli.py task device_info
  
  # Run custom task
  python cli.py task my_task.json --context package_name=com.example.app
  
  # List available tasks
  python cli.py list
  
  # Run demo
  python cli.py demo
        """
    )
    
    parser.add_argument("--adb-path", default="adb", help="Path to adb executable")
    parser.add_argument("--output", "-o", default="data/tmp/adb_output", help="Output directory")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Devices command
    devices_parser = subparsers.add_parser("devices", help="List connected devices")
    devices_parser.add_argument("--json", action="store_true", help="Save output as JSON")
    
    # Packages command
    packages_parser = subparsers.add_parser("packages", help="List installed packages")
    packages_parser.add_argument("--device", "-d", help="Device serial")
    packages_parser.add_argument("--filter", "-f", help="Filter packages by name")
    packages_parser.add_argument("--limit", "-l", type=int, help="Limit number of results")
    packages_parser.add_argument("--json", action="store_true", help="Save output as JSON")
    
    # Screenshot command
    screenshot_parser = subparsers.add_parser("screenshot", help="Capture screenshot")
    screenshot_parser.add_argument("--device", "-d", help="Device serial")
    screenshot_parser.add_argument("--filename", "-f", help="Output filename")
    
    # Shell command
    shell_parser = subparsers.add_parser("shell", help="Execute shell command")
    shell_parser.add_argument("command", help="Shell command to execute")
    shell_parser.add_argument("--device", "-d", help="Device serial")
    
    # Task command
    task_parser = subparsers.add_parser("task", help="Run automation task")
    task_parser.add_argument("task", help="Task name or JSON file path")
    task_parser.add_argument("--device", "-d", help="Device serial")
    task_parser.add_argument("--context", "-c", nargs="+", help="Context variables (key=value)")
    task_parser.add_argument("--save-result", action="store_true", help="Save result to JSON")
    
    # List tasks command
    list_parser = subparsers.add_parser("list", help="List available preset tasks")
    
    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run demo mode")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "devices":
        devices_command(args)
    elif args.command == "packages":
        packages_command(args)
    elif args.command == "screenshot":
        screenshot_command(args)
    elif args.command == "shell":
        shell_command(args)
    elif args.command == "task":
        task_command(args)
    elif args.command == "list":
        list_tasks_command(args)
    elif args.command == "demo":
        demo_command(args)


if __name__ == "__main__":
    main()
