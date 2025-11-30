#!/usr/bin/env python3
"""
OSINT Tool - CLI Interface
Gather intelligence on emails, usernames, domains
"""

import sys
import argparse
from pathlib import Path
import json
from datetime import datetime
import os

# Fix imports for both module and standalone execution
if __name__ == '__main__' and __package__ is None:
    # Running as standalone script
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from tools.osint.modules.email_lookup import EmailLookup
    from tools.osint.modules.username_search import UsernameSearch
    from tools.osint.modules.breach_check import BreachCheck
    from tools.osint.modules.whois_lookup import WhoisLookup
    from tools.osint.modules.resources import OSINTResources
    from tools.osint.modules.auto_search import AutoSearch
else:
    # Running as module
    from .modules.email_lookup import EmailLookup
    from .modules.username_search import UsernameSearch
    from .modules.breach_check import BreachCheck
    from .modules.whois_lookup import WhoisLookup
    from .modules.resources import OSINTResources
    from .modules.auto_search import AutoSearch


def print_banner():
    print("""
╔═══════════════════════════════════════════════════════════╗
║                    OSINT Intelligence Tool                ║
║              Open Source Intelligence Gathering           ║
╚═══════════════════════════════════════════════════════════╝
    """)


def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def email_command(args):
    """Lookup email information"""
    print_section(f"Email Lookup: {args.email}")
    
    lookup = EmailLookup()
    results = lookup.investigate(args.email)
    
    print(f"📧 Email: {results['email']}")
    print(f"   Valid Format: {'✅' if results['valid_format'] else '❌'}")
    print(f"   Domain: {results['domain']}")
    
    if results.get('breach_data'):
        print(f"\n⚠️  BREACH ALERT:")
        for breach in results['breach_data']['breaches'][:5]:
            print(f"   • {breach}")
        if results['breach_data']['total'] > 5:
            print(f"   ... and {results['breach_data']['total'] - 5} more")
    
    if results.get('social_profiles'):
        print(f"\n👤 Potential Social Profiles:")
        for platform, url in results['social_profiles'].items():
            print(f"   • {platform}: {url}")
    
    if args.output:
        save_results(results, args.output)
        print(f"\n💾 Results saved to: {args.output}")


def username_command(args):
    """Search for username across platforms"""
    print_section(f"Username Search: {args.username}")
    
    search = UsernameSearch()
    results = search.search(args.username)
    
    print(f"🔍 Searching for: {results['username']}")
    print(f"   Platforms checked: {results['total_platforms']}")
    print(f"   Found: {results['found_count']}")
    
    if results['found']:
        print(f"\n✅ Found on these platforms:")
        for platform in results['found']:
            print(f"   • {platform['name']}: {platform['url']}")
            if platform.get('status'):
                print(f"     Status: {platform['status']}")
    
    if results['possible']:
        print(f"\n❓ Possible matches (need verification):")
        for platform in results['possible'][:5]:
            print(f"   • {platform['name']}: {platform['url']}")
    
    if args.output:
        save_results(results, args.output)
        print(f"\n💾 Results saved to: {args.output}")


def breach_command(args):
    """Check for data breaches"""
    print_section(f"Breach Check: {args.identifier}")
    
    checker = BreachCheck()
    
    if '@' in args.identifier:
        results = checker.check_email(args.identifier)
        identifier_type = "Email"
    else:
        results = checker.check_username(args.identifier)
        identifier_type = "Username"
    
    print(f"🔒 {identifier_type}: {results['identifier']}")
    print(f"   Total Breaches: {results['breach_count']}")
    
    if results['breaches']:
        print(f"\n⚠️  FOUND IN THESE BREACHES:")
        for breach in results['breaches']:
            print(f"\n   📋 {breach['name']}")
            print(f"      Date: {breach['date']}")
            print(f"      Compromised Data: {', '.join(breach['data_types'])}")
            if breach.get('description'):
                print(f"      Info: {breach['description'][:100]}...")
    else:
        print(f"\n✅ No breaches found (good news!)")
    
    if args.output:
        save_results(results, args.output)
        print(f"\n💾 Results saved to: {args.output}")


def whois_command(args):
    """WHOIS domain lookup"""
    print_section(f"WHOIS Lookup: {args.domain}")
    
    lookup = WhoisLookup()
    results = lookup.query(args.domain)
    
    print(f"🌐 Domain: {results['domain']}")
    print(f"   Registered: {'✅ Yes' if results['registered'] else '❌ No'}")
    
    if results['registered']:
        print(f"\n📝 Registration Details:")
        if results.get('registrar'):
            print(f"   Registrar: {results['registrar']}")
        if results.get('creation_date'):
            print(f"   Created: {results['creation_date']}")
        if results.get('expiration_date'):
            print(f"   Expires: {results['expiration_date']}")
        if results.get('name_servers'):
            print(f"   Name Servers:")
            for ns in results['name_servers'][:3]:
                print(f"      • {ns}")
    
    if args.output:
        save_results(results, args.output)
        print(f"\n💾 Results saved to: {args.output}")


def full_command(args):
    """Run full OSINT investigation"""
    print_section(f"Full OSINT Investigation: {args.target}")
    
    all_results = {
        'target': args.target,
        'timestamp': datetime.now().isoformat(),
        'results': {}
    }
    
    # Email lookup if it's an email
    if '@' in args.target:
        print("\n[1/3] Running email lookup...")
        lookup = EmailLookup()
        all_results['results']['email'] = lookup.investigate(args.target)
        
        domain = args.target.split('@')[1]
        print("\n[2/3] Running WHOIS on domain...")
        whois = WhoisLookup()
        all_results['results']['whois'] = whois.query(domain)
    else:
        # Username search
        print("\n[1/2] Searching username across platforms...")
        search = UsernameSearch()
        all_results['results']['username'] = search.search(args.target)
    
    # Always check breaches
    print("\n[3/3] Checking for data breaches...")
    checker = BreachCheck()
    if '@' in args.target:
        all_results['results']['breaches'] = checker.check_email(args.target)
    else:
        all_results['results']['breaches'] = checker.check_username(args.target)
    
    print_section("Investigation Complete")
    print(f"📊 Results summary:")
    for key, data in all_results['results'].items():
        print(f"   • {key.title()}: ✅ Complete")
    
    # Generate report if requested
    if hasattr(args, 'report') and args.report:
        print(f"\n📄 Generating {args.report.upper()} report...")
        from .pro.report_generator import PDFReportGenerator
        generator = PDFReportGenerator()
        report_path = generator.generate_report(all_results, args.output or 'report')
        print(f"✅ Report saved: {report_path}")
        print(f"\n💎 Upgrade to Pro for PDF reports without watermarks!")
        print(f"   Get Pro: https://gumroad.com/your-product")
    else:
        output_file = args.output or f"osint_{args.target.replace('@', '_at_').replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        save_results(all_results, output_file)
        print(f"\n💾 Full results saved to: {output_file}")
        print(f"\n💡 Tip: Add --report html to generate a report!")


def search_command(args):
    """Auto-search multiple OSINT sites"""
    print_section(f"Auto-Search: {args.target}")
    
    searcher = AutoSearch()
    results = searcher.search_all(args.target, args.type)
    
    print(f"📊 Searched {len(results)} sites\n")
    
    for result in results:
        print(f"{'='*60}")
        print(f"  {result['site']}")
        print(f"{'='*60}\n")
        
        if result.get('found') == True:
            print(f"  ✅ FOUND!")
            if result.get('data'):
                for key, value in result['data'].items():
                    print(f"     {key}: {value}")
            if result.get('breaches'):
                print(f"     Breaches: {', '.join(result['breaches'])}")
                if result.get('breach_count'):
                    print(f"     Total: {result['breach_count']}")
        elif result.get('found') == False:
            print(f"  ❌ Not found")
        else:
            print(f"  ❓ Manual verification required")
        
        if result.get('search_url'):
            print(f"\n  🔗 {result['search_url']}")
        
        if result.get('note'):
            print(f"  ℹ️  {result['note']}")
        
        if result.get('error'):
            print(f"  ⚠️  Error: {result['error']}")
        
        print()
    
    summary = {
        'target': args.target,
        'type': args.type,
        'timestamp': datetime.now().isoformat(),
        'sites_searched': len(results),
        'results': results
    }
    
    if args.output:
        save_results(summary, args.output)
        print(f"\n💾 Results saved to: {args.output}")


def resources_command(args):
    """Display OSINT resources database"""
    print_section("OSINT Resources Database")
    
    all_resources = OSINTResources.get_all_resources()
    total_count = OSINTResources.get_resource_count()
    
    print(f"📚 Total Resources: {total_count}")
    print(f"🗂️  Categories: {len(all_resources)}\n")
    
    if args.category == 'all':
        for category, resources in all_resources.items():
            print(f"\n{'='*60}")
            print(f"  {category.replace('_', ' ').title()} ({len(resources)})")
            print(f"{'='*60}\n")
            
            for resource in resources[:10]:  # Show first 10 per category
                print(f"  • {resource['name']}")
                print(f"    {resource['url']}")
                if 'type' in resource:
                    print(f"    Type: {resource['type']}")
                elif 'region' in resource:
                    print(f"    Region: {resource['region']}")
                elif 'platform' in resource:
                    print(f"    Platform: {resource['platform']}")
                print()
            
            if len(resources) > 10:
                print(f"  ... and {len(resources) - 10} more\n")
    else:
        resources = OSINTResources.search_by_type(args.category)
        print(f"\n{args.category.replace('_', ' ').title()} ({len(resources)})\n")
        
        for resource in resources:
            print(f"  • {resource['name']}")
            print(f"    {resource['url']}")
            if 'type' in resource:
                print(f"    Type: {resource['type']}")
            elif 'region' in resource:
                print(f"    Region: {resource['region']}")
            elif 'platform' in resource:
                print(f"    Platform: {resource['platform']}")
            print()


def save_results(results, output_path):
    """Save results to JSON file"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)


def main():
    parser = argparse.ArgumentParser(
        description="OSINT Tool - Open Source Intelligence Gathering",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Email lookup
  python -m tools.osint.cli email john.doe@example.com
  
  # Username search
  python -m tools.osint.cli username johndoe123
  
  # Breach check
  python -m tools.osint.cli breach john.doe@example.com
  
  # WHOIS lookup
  python -m tools.osint.cli whois example.com
  
  # Full investigation
  python -m tools.osint.cli full john.doe@example.com --output results.json
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Email command
    email_parser = subparsers.add_parser('email', help='Lookup email information')
    email_parser.add_argument('email', help='Email address to investigate')
    email_parser.add_argument('-o', '--output', help='Output JSON file')
    
    # Username command
    username_parser = subparsers.add_parser('username', help='Search username across platforms')
    username_parser.add_argument('username', help='Username to search')
    username_parser.add_argument('-o', '--output', help='Output JSON file')
    
    # Breach command
    breach_parser = subparsers.add_parser('breach', help='Check for data breaches')
    breach_parser.add_argument('identifier', help='Email or username to check')
    breach_parser.add_argument('-o', '--output', help='Output JSON file')
    
    # WHOIS command
    whois_parser = subparsers.add_parser('whois', help='WHOIS domain lookup')
    whois_parser.add_argument('domain', help='Domain to lookup')
    whois_parser.add_argument('-o', '--output', help='Output JSON file')
    
    # Full investigation command
    full_parser = subparsers.add_parser('full', help='Run full OSINT investigation')
    full_parser.add_argument('target', help='Email or username to investigate')
    full_parser.add_argument('-o', '--output', help='Output JSON file')
    full_parser.add_argument('--report', choices=['html', 'pdf'], help='Generate report (html=free, pdf=Pro)')
    
    # Resources command
    resources_parser = subparsers.add_parser('resources', help='List all OSINT resources')
    resources_parser.add_argument('--category', choices=[
        'us_people_search', 'international_search', 'phone_lookup', 
        'username_search', 'image_search', 'email_search', 
        'social_search', 'breach_databases', 'ip_tools', 
        'criminal_records', 'osint_frameworks', 'all'
    ], default='all', help='Filter by category')
    
    # Auto-search command
    search_parser = subparsers.add_parser('search', help='Auto-search multiple OSINT sites')
    search_parser.add_argument('target', help='Target to search (email, phone, name, or image URL)')
    search_parser.add_argument('--type', choices=['email', 'phone', 'name', 'image'], 
                               required=True, help='Type of target')
    search_parser.add_argument('-o', '--output', help='Output JSON file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    print_banner()
    
    try:
        if args.command == 'email':
            email_command(args)
        elif args.command == 'username':
            username_command(args)
        elif args.command == 'breach':
            breach_command(args)
        elif args.command == 'whois':
            whois_command(args)
        elif args.command == 'full':
            full_command(args)
        elif args.command == 'resources':
            resources_command(args)
        elif args.command == 'search':
            search_command(args)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
