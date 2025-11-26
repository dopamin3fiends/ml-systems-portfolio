#!/usr/bin/env python3
"""
⚙️ Windows Feature Manager v1.0
Professional Windows optional feature management with safety checks

Usage:
    python cli.py list [--state enabled]
    python cli.py info <feature_name>
    python cli.py enable <feature_name> [--no-restart]
    python cli.py disable <feature_name> [--no-restart]
    python cli.py preset <preset_name>
    python cli.py backup
    python cli.py restore <backup_id> [--dry-run]
    python cli.py demo

Examples:
    # List all features
    python cli.py list
    
    # List enabled features only
    python cli.py list --state enabled
    
    # Get feature details
    python cli.py info Microsoft-Windows-Subsystem-Linux
    
    # Enable WSL
    python cli.py enable Microsoft-Windows-Subsystem-Linux --no-restart
    
    # Enable development tools preset
    python cli.py preset dev_tools
    
    # Backup current state
    python cli.py backup
    
    # Demo mode (safe, no changes)
    python cli.py demo
"""

import argparse
import sys
from pathlib import Path

try:
    from models import FeatureState, FEATURE_GROUPS
    from manager import WindowsFeatureManager
except ImportError:
    from .models import FeatureState, FEATURE_GROUPS
    from .manager import WindowsFeatureManager


def list_command(args, manager: WindowsFeatureManager):
    """List Windows optional features"""
    state_filter = FeatureState(args.state) if args.state else None
    features = manager.list_features(state_filter=state_filter)
    
    if not features:
        print("No features found (requires Windows with DISM support)")
        return
    
    print(f"\n{'='*80}")
    print(f"⚙️  Windows Optional Features ({len(features)} total)")
    print(f"{'='*80}\n")
    
    # Group by category
    from collections import defaultdict
    by_category = defaultdict(list)
    
    for feature in features:
        by_category[feature.category].append(feature)
    
    for category, cat_features in sorted(by_category.items(), key=lambda x: x[0].value):
        print(f"\n📂 {category.value.upper()}")
        print("-" * 80)
        
        for feature in sorted(cat_features, key=lambda f: f.name):
            state_icon = "✅" if feature.state == FeatureState.ENABLED else "❌"
            restart_icon = " 🔄" if feature.restart_required else ""
            
            print(f"{state_icon} {feature.name}")
            if feature.description:
                print(f"   {feature.description}{restart_icon}")


def info_command(args, manager: WindowsFeatureManager):
    """Show detailed feature information"""
    feature = manager.get_feature(args.feature_name)
    
    if not feature:
        print(f"❌ Feature not found: {args.feature_name}")
        return
    
    print(f"\n{'='*80}")
    print(f"⚙️  Feature Details")
    print(f"{'='*80}\n")
    
    state_icon = "✅ ENABLED" if feature.state == FeatureState.ENABLED else "❌ DISABLED"
    
    print(f"Name: {feature.name}")
    print(f"Display Name: {feature.display_name}")
    print(f"State: {state_icon}")
    print(f"Category: {feature.category.value}")
    
    if feature.description:
        print(f"Description: {feature.description}")
    
    if feature.restart_required:
        print(f"Restart Required: Yes 🔄")
    
    if feature.dependencies:
        print(f"Dependencies: {', '.join(feature.dependencies)}")


def enable_command(args, manager: WindowsFeatureManager):
    """Enable Windows optional feature"""
    if not manager.is_admin():
        print("❌ Administrator privileges required!")
        print("   Run PowerShell/CMD as Administrator and try again.")
        return
    
    print(f"\n⏳ Enabling feature: {args.feature_name}...")
    
    result = manager.enable_feature(args.feature_name, no_restart=args.no_restart)
    
    if result.success:
        print(f"✅ {result.message}")
        
        if result.restart_required:
            print("\n⚠️  RESTART REQUIRED to complete activation.")
            print("   Run 'shutdown /r /t 0' to restart now, or restart manually.")
    else:
        print(f"❌ {result.message}")
        if result.error:
            print(f"   Error: {result.error}")


def disable_command(args, manager: WindowsFeatureManager):
    """Disable Windows optional feature"""
    if not manager.is_admin():
        print("❌ Administrator privileges required!")
        print("   Run PowerShell/CMD as Administrator and try again.")
        return
    
    print(f"\n⏳ Disabling feature: {args.feature_name}...")
    
    result = manager.disable_feature(args.feature_name, no_restart=args.no_restart)
    
    if result.success:
        print(f"✅ {result.message}")
        
        if result.restart_required:
            print("\n⚠️  RESTART REQUIRED to complete deactivation.")
    else:
        print(f"❌ {result.message}")
        if result.error:
            print(f"   Error: {result.error}")


def preset_command(args, manager: WindowsFeatureManager):
    """Enable preset group of features"""
    if not manager.is_admin():
        print("❌ Administrator privileges required!")
        print("   Run PowerShell/CMD as Administrator and try again.")
        return
    
    preset = FEATURE_GROUPS.get(args.preset_name)
    
    if not preset:
        print(f"❌ Unknown preset: {args.preset_name}")
        print(f"\nAvailable presets: {', '.join(FEATURE_GROUPS.keys())}")
        return
    
    print(f"\n{'='*80}")
    print(f"📦 Preset: {preset.name}")
    print(f"{'='*80}\n")
    print(f"{preset.description}\n")
    print(f"Features to enable ({len(preset.features)}):")
    for feature_name in preset.features:
        print(f"  - {feature_name}")
    
    if not args.yes:
        confirm = input("\nProceed? (y/n): ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return
    
    print("\n⏳ Enabling features...")
    
    results = []
    for feature_name in preset.features:
        result = manager.enable_feature(feature_name, no_restart=True)
        results.append(result)
        
        if result.success:
            print(f"✅ {feature_name}")
        else:
            print(f"❌ {feature_name}: {result.error}")
    
    # Summary
    success_count = sum(1 for r in results if r.success)
    restart_needed = any(r.restart_required for r in results)
    
    print(f"\n📊 Summary: {success_count}/{len(results)} features enabled")
    
    if restart_needed:
        print("\n⚠️  RESTART REQUIRED to complete activation.")


def backup_command(args, manager: WindowsFeatureManager):
    """Backup current feature states"""
    print("\n💾 Creating backup of Windows feature states...")
    
    backup = manager.backup_features()
    
    print(f"✅ Backup created successfully!")
    print(f"   Backup ID: {backup.backup_id}")
    print(f"   Hostname: {backup.hostname}")
    print(f"   Features: {len(backup.features)}")
    print(f"   Timestamp: {backup.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nTo restore: python cli.py restore {backup.backup_id}")


def restore_command(args, manager: WindowsFeatureManager):
    """Restore features from backup"""
    if not args.dry_run and not manager.is_admin():
        print("❌ Administrator privileges required!")
        print("   Run PowerShell/CMD as Administrator and try again.")
        return
    
    mode = "DRY RUN" if args.dry_run else "RESTORE"
    print(f"\n🔄 {mode}: Restoring from backup {args.backup_id}...")
    
    results = manager.restore_features(args.backup_id, dry_run=args.dry_run)
    
    if not results:
        print("✅ No changes needed - all features match backup state.")
        return
    
    for result in results:
        if result.success:
            print(f"✅ {result.message}")
        else:
            print(f"❌ {result.message}")
            if result.error:
                print(f"   Error: {result.error}")
    
    if args.dry_run:
        print(f"\n📊 {len(results)} changes would be made.")
        print("   Remove --dry-run to apply changes.")


def demo_command(args, manager: WindowsFeatureManager):
    """Run demo mode (safe, no changes)"""
    print("⚙️  Windows Feature Manager v1.0 - Demo Mode\n")
    print("=" * 60)
    
    # System info
    print("\n[1/4] System Information")
    info = manager.get_system_info()
    print(f"   Platform: {info['platform']}")
    print(f"   Version: {info['version']}")
    print(f"   Hostname: {info['hostname']}")
    print(f"   Administrator: {'Yes ✅' if info['is_admin'] else 'No ❌'}")
    
    # List features
    print("\n[2/4] Querying Windows features...")
    features = manager.list_features()
    
    if features:
        enabled = [f for f in features if f.state == FeatureState.ENABLED]
        disabled = [f for f in features if f.state == FeatureState.DISABLED]
        
        print(f"   Total features: {len(features)}")
        print(f"   Enabled: {len(enabled)}")
        print(f"   Disabled: {len(disabled)}")
        
        # Show sample features
        print("\n   Sample enabled features:")
        for feature in enabled[:5]:
            print(f"   ✅ {feature.name}")
        
        if len(enabled) > 5:
            print(f"   ... and {len(enabled) - 5} more")
    else:
        print("   ⚠️  Could not query features (requires Windows)")
    
    # Show presets
    print("\n[3/4] Available Presets")
    for preset_name, preset in FEATURE_GROUPS.items():
        print(f"   📦 {preset_name}: {preset.name}")
        print(f"      {preset.description}")
        print(f"      Features: {len(preset.features)}")
    
    # Backup demo
    print("\n[4/4] Backup System")
    backup = manager.backup_features()
    print(f"   ✅ Demo backup created: {backup.backup_id}")
    print(f"   Captured {len(backup.features)} feature states")
    
    print("\n" + "=" * 60)
    print("✅ Demo complete! No changes were made to your system.")
    print("\nTo actually manage features:")
    print("  python cli.py list")
    print("  python cli.py enable <feature_name>")
    print("  python cli.py preset dev_tools")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="⚙️  Windows Feature Manager - Professional Windows optional feature management",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List Windows optional features')
    list_parser.add_argument('--state', choices=['enabled', 'disabled'],
                            help='Filter by feature state')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show feature details')
    info_parser.add_argument('feature_name', help='Feature name to query')
    
    # Enable command
    enable_parser = subparsers.add_parser('enable', help='Enable feature')
    enable_parser.add_argument('feature_name', help='Feature name to enable')
    enable_parser.add_argument('--no-restart', action='store_true',
                               help='Suppress automatic restart')
    
    # Disable command
    disable_parser = subparsers.add_parser('disable', help='Disable feature')
    disable_parser.add_argument('feature_name', help='Feature name to disable')
    disable_parser.add_argument('--no-restart', action='store_true',
                                help='Suppress automatic restart')
    
    # Preset command
    preset_parser = subparsers.add_parser('preset', help='Enable preset group')
    preset_parser.add_argument('preset_name', choices=list(FEATURE_GROUPS.keys()),
                              help='Preset name')
    preset_parser.add_argument('-y', '--yes', action='store_true',
                              help='Skip confirmation prompt')
    
    # Backup command
    subparsers.add_parser('backup', help='Backup current feature states')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore from backup')
    restore_parser.add_argument('backup_id', help='Backup ID to restore')
    restore_parser.add_argument('--dry-run', action='store_true',
                               help='Show changes without applying')
    
    # Demo command
    subparsers.add_parser('demo', help='Run demo mode (safe)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize manager
    manager = WindowsFeatureManager()
    
    # Execute command
    if args.command == 'list':
        list_command(args, manager)
    elif args.command == 'info':
        info_command(args, manager)
    elif args.command == 'enable':
        enable_command(args, manager)
    elif args.command == 'disable':
        disable_command(args, manager)
    elif args.command == 'preset':
        preset_command(args, manager)
    elif args.command == 'backup':
        backup_command(args, manager)
    elif args.command == 'restore':
        restore_command(args, manager)
    elif args.command == 'demo':
        demo_command(args, manager)


if __name__ == "__main__":
    main()
