"""
Web Automation Framework - CLI Interface
Command-line interface for browser automation workflows
"""

import argparse
import json
from pathlib import Path
from datetime import datetime

try:
    from models import Workflow, PRESET_WORKFLOWS
    from engine import AutomationEngine, demo_automation, SELENIUM_AVAILABLE
except ImportError:
    from .models import Workflow, PRESET_WORKFLOWS
    from .engine import AutomationEngine, demo_automation, SELENIUM_AVAILABLE


def run_workflow_command(args):
    """Execute workflow from JSON file"""
    print(f"🤖 Running workflow: {args.workflow}\n")
    
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium not installed. Install with: pip install selenium")
        return
    
    # Load workflow
    workflow_path = Path(args.workflow)
    if not workflow_path.exists():
        print(f"❌ Workflow file not found: {workflow_path}")
        return
    
    with open(workflow_path) as f:
        workflow_data = json.load(f)
    
    workflow = Workflow.from_dict(workflow_data)
    
    # Parse context
    context = {}
    if args.context:
        for item in args.context:
            key, value = item.split("=", 1)
            context[key] = value
    
    print(f"[1/3] Workflow: {workflow.name}")
    print(f"      Actions: {len(workflow.actions)}")
    print(f"      Browser: {workflow.config.browser_type.value}")
    
    print("\n[2/3] Executing...")
    
    # Run workflow
    engine = AutomationEngine(output_dir=args.output)
    result = engine.run_workflow(workflow, context)
    
    print(f"\n[3/3] Results")
    print(f"      Session: {result.session_id[:8]}")
    print(f"      Status: {result.status.value}")
    print(f"      Completed: {result.actions_completed}")
    print(f"      Failed: {result.actions_failed}")
    print(f"      Duration: {result.duration:.2f}s")
    
    if result.screenshots:
        print(f"\n      Screenshots:")
        for screenshot in result.screenshots:
            print(f"         {screenshot}")
    
    if result.extracted_data:
        print(f"\n      Extracted Data:")
        for key, value in result.extracted_data.items():
            print(f"         {key}: {value}")
    
    # Save result
    if args.save_result:
        result_path = Path(args.output) / f"result_{result.session_id[:8]}.json"
        with open(result_path, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"\n      Result saved: {result_path}")


def run_preset_command(args):
    """Execute preset workflow"""
    print(f"🤖 Running preset: {args.preset}\n")
    
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium not installed. Install with: pip install selenium")
        return
    
    if args.preset not in PRESET_WORKFLOWS:
        print(f"❌ Unknown preset: {args.preset}")
        print(f"   Available presets: {', '.join(PRESET_WORKFLOWS.keys())}")
        return
    
    workflow = PRESET_WORKFLOWS[args.preset]
    
    # Parse context (required for preset workflows)
    context = {}
    if args.context:
        for item in args.context:
            key, value = item.split("=", 1)
            context[key] = value
    
    # Check required context
    if "url" not in context:
        print("❌ URL required. Use --context url=https://example.com")
        return
    
    print(f"[1/3] Preset: {workflow.name}")
    print(f"      URL: {context.get('url')}")
    print(f"      Actions: {len(workflow.actions)}")
    
    print("\n[2/3] Executing...")
    
    # Run workflow
    engine = AutomationEngine(output_dir=args.output)
    result = engine.run_workflow(workflow, context)
    
    print(f"\n[3/3] Results")
    print(f"      Session: {result.session_id[:8]}")
    print(f"      Status: {result.status.value}")
    print(f"      Completed: {result.actions_completed}")
    print(f"      Duration: {result.duration:.2f}s")
    
    if result.screenshots:
        print(f"\n      Screenshots:")
        for screenshot in result.screenshots:
            print(f"         {screenshot}")
    
    if result.extracted_data:
        print(f"\n      Extracted Data:")
        for key, value in result.extracted_data.items():
            print(f"         {key}: {value}")


def list_presets_command(args):
    """List available preset workflows"""
    print("🤖 Available Preset Workflows\n")
    print("=" * 60)
    
    for name, workflow in PRESET_WORKFLOWS.items():
        print(f"\n{name}")
        print(f"   {workflow.description}")
        print(f"   Actions: {len(workflow.actions)}")


def demo_command(args):
    """Run demo mode"""
    demo_automation()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Web Automation Framework - Browser automation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run preset workflow
  python cli.py preset health_check --context url=https://example.com
  
  # Run custom workflow
  python cli.py run workflow.json --context user=test password=demo
  
  # List available presets
  python cli.py list
  
  # Run demo
  python cli.py demo
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Run workflow command
    run_parser = subparsers.add_parser("run", help="Run custom workflow from file")
    run_parser.add_argument("workflow", help="Path to workflow JSON file")
    run_parser.add_argument("--context", "-c", nargs="+", help="Context variables (key=value)")
    run_parser.add_argument("--output", "-o", default="data/tmp/automation_output", help="Output directory")
    run_parser.add_argument("--save-result", action="store_true", help="Save result to JSON")
    
    # Preset workflow command
    preset_parser = subparsers.add_parser("preset", help="Run preset workflow")
    preset_parser.add_argument("preset", help="Preset name", choices=PRESET_WORKFLOWS.keys())
    preset_parser.add_argument("--context", "-c", nargs="+", required=True, help="Context variables (url=...)")
    preset_parser.add_argument("--output", "-o", default="data/tmp/automation_output", help="Output directory")
    
    # List presets command
    list_parser = subparsers.add_parser("list", help="List available presets")
    
    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run demo mode")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "run":
        run_workflow_command(args)
    elif args.command == "preset":
        run_preset_command(args)
    elif args.command == "list":
        list_presets_command(args)
    elif args.command == "demo":
        demo_command(args)


if __name__ == "__main__":
    main()
