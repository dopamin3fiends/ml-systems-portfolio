#!/usr/bin/env python3
"""
🔍 PathPulse v1.0
Real-time file system monitoring and threat pattern detection

Usage:
    python cli.py monitor <path> [--duration 60] [--recursive]
    python cli.py analyze <events.json>
    python cli.py demo [--duration 10]

Examples:
    # Monitor directory for 60 seconds
    python cli.py monitor C:\\Users\\Documents --duration 60 --recursive
    
    # Analyze captured events
    python cli.py analyze data/tmp/pathpulse_events.json
    
    # Run demo mode
    python cli.py demo --duration 10
"""

import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    from models import FileEvent, EventType, RiskLevel
    from monitor import FileSystemMonitor, demo_monitor, WATCHDOG_AVAILABLE
    from analyzer import PatternAnalyzer
except ImportError:
    from .models import FileEvent, EventType, RiskLevel
    from .monitor import FileSystemMonitor, demo_monitor, WATCHDOG_AVAILABLE
    from .analyzer import PatternAnalyzer


def monitor_command(args):
    """Monitor file system in real-time"""
    if not WATCHDOG_AVAILABLE:
        print("❌ Error: watchdog library not installed.")
        print("   Install with: pip install watchdog")
        return
    
    print(f"🔍 PathPulse - File System Monitor\n")
    print("=" * 60)
    print(f"\nMonitoring: {args.path}")
    print(f"Duration: {args.duration}s")
    print(f"Recursive: {args.recursive}")
    print(f"Output: {args.output}\n")
    
    # Initialize monitor
    monitor = FileSystemMonitor()
    
    # Track events for later analysis
    all_events = []
    
    def event_callback(event: FileEvent):
        """Callback for each file system event"""
        all_events.append(event)
        
        # Print event with icon
        icon = {
            EventType.CREATED: "➕",
            EventType.MODIFIED: "✏️",
            EventType.DELETED: "🗑️",
            EventType.MOVED: "🔀"
        }.get(event.event_type, "❓")
        
        risk_icon = {
            RiskLevel.SAFE: "✅",
            RiskLevel.LOW: "ℹ️",
            RiskLevel.MEDIUM: "⚠️",
            RiskLevel.HIGH: "🔴",
            RiskLevel.CRITICAL: "🚨"
        }.get(event.risk_level, "❓")
        
        file_name = Path(event.path).name
        print(f"{icon} {event.event_type.value.upper()}: {file_name} {risk_icon} [{event.file_category.value}]")
    
    monitor.add_callback(event_callback)
    
    # Start monitoring
    try:
        monitor.start_monitoring([args.path], recursive=args.recursive)
        
        print("Press Ctrl+C to stop monitoring early...\n")
        time.sleep(args.duration)
    
    except KeyboardInterrupt:
        print("\n\n⏸️  Monitoring interrupted by user.")
    
    finally:
        monitor.stop_monitoring()
    
    # Save events to file
    if all_events:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump([e.to_dict() for e in all_events], f, indent=2)
        
        print(f"\n💾 Saved {len(all_events)} events to {output_path}")
        
        # Run pattern analysis
        print("\n🔍 Analyzing for threat patterns...")
        analyzer = PatternAnalyzer()
        patterns = analyzer.analyze_events(all_events)
        
        if patterns:
            print(f"\n⚠️  WARNING: {len(patterns)} threat pattern(s) detected!\n")
            for pattern in patterns:
                risk_icon = {
                    RiskLevel.LOW: "ℹ️",
                    RiskLevel.MEDIUM: "⚠️",
                    RiskLevel.HIGH: "🔴",
                    RiskLevel.CRITICAL: "🚨"
                }.get(pattern.risk_level, "❓")
                
                print(f"{risk_icon} [{pattern.risk_level.value.upper()}] {pattern.pattern_type.upper()}")
                print(f"   {pattern.description}")
                print(f"   Events: {pattern.event_count} | Confidence: {pattern.confidence:.0%}")
                print(f"   Action: {pattern.recommended_action}\n")
            
            # Save report
            report = analyzer.generate_report(all_events, patterns)
            report_path = output_path.with_name(f"{output_path.stem}_report.json")
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"📊 Detailed report saved to {report_path}")
        else:
            print("\n✅ No suspicious patterns detected.")
        
        # Show statistics
        stats = monitor.get_stats()
        print(f"\n📊 Statistics:")
        print(f"   Total events: {stats['total_events']}")
        print(f"   Event types: {stats['event_types']}")
        print(f"   Risk levels: {stats['risk_levels']}")


def analyze_command(args):
    """Analyze previously captured events"""
    print(f"🔍 PathPulse - Event Analysis\n")
    print("=" * 60)
    
    # Load events
    try:
        with open(args.events_file, 'r') as f:
            events_data = json.load(f)
        
        events = [FileEvent.from_dict(e) for e in events_data]
        print(f"\n✅ Loaded {len(events)} events from {args.events_file}")
    
    except FileNotFoundError:
        print(f"❌ Error: File not found: {args.events_file}")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in {args.events_file}")
        return
    
    # Analyze patterns
    print("\n🔍 Analyzing for threat patterns...")
    analyzer = PatternAnalyzer()
    patterns = analyzer.analyze_events(events, window_seconds=args.window)
    
    if patterns:
        print(f"\n⚠️  WARNING: {len(patterns)} threat pattern(s) detected!\n")
        for pattern in patterns:
            risk_icon = {
                RiskLevel.LOW: "ℹ️",
                RiskLevel.MEDIUM: "⚠️",
                RiskLevel.HIGH: "🔴",
                RiskLevel.CRITICAL: "🚨"
            }.get(pattern.risk_level, "❓")
            
            print(f"{risk_icon} [{pattern.risk_level.value.upper()}] {pattern.pattern_type.upper()}")
            print(f"   {pattern.description}")
            print(f"   Events: {pattern.event_count} | Confidence: {pattern.confidence:.0%}")
            print(f"   First seen: {pattern.first_seen.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Last seen: {pattern.last_seen.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Action: {pattern.recommended_action}\n")
        
        # Generate and save report
        report = analyzer.generate_report(events, patterns)
        report_path = Path(args.events_file).with_name(f"{Path(args.events_file).stem}_analysis.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Detailed analysis report saved to {report_path}")
    else:
        print("\n✅ No suspicious patterns detected.")
    
    print("\n" + "=" * 60)


def demo_command(args):
    """Run demo mode"""
    demo_monitor(duration=args.duration)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="🔍 PathPulse - Real-time file system monitoring and threat detection",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Monitor file system in real-time')
    monitor_parser.add_argument('path', help='Directory path to monitor')
    monitor_parser.add_argument('--duration', type=int, default=60,
                               help='Monitoring duration in seconds (default: 60)')
    monitor_parser.add_argument('--recursive', action='store_true',
                               help='Monitor subdirectories recursively')
    monitor_parser.add_argument('--output', default='data/tmp/pathpulse_events.json',
                               help='Output file for captured events')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze captured events')
    analyze_parser.add_argument('events_file', help='JSON file with captured events')
    analyze_parser.add_argument('--window', type=int, default=300,
                               help='Time window for pattern detection in seconds (default: 300)')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demo mode')
    demo_parser.add_argument('--duration', type=int, default=10,
                            help='Demo duration in seconds (default: 10)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    if args.command == 'monitor':
        monitor_command(args)
    elif args.command == 'analyze':
        analyze_command(args)
    elif args.command == 'demo':
        demo_command(args)


if __name__ == "__main__":
    main()
