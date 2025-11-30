"""
License Key Generator for OSINT Tool Pro
Generates unique license keys for Pro version customers
"""

import hashlib
import secrets
import json
from datetime import datetime
from pathlib import Path


def generate_license_key():
    """Generate a unique license key"""
    # Use secrets for cryptographically strong random values
    random_bytes = secrets.token_bytes(32)
    
    # Create readable format: OSINT-XXXX-XXXX-XXXX-XXXX
    hex_string = random_bytes.hex().upper()
    
    # Format as license key
    key = f"OSINT-{hex_string[0:4]}-{hex_string[4:8]}-{hex_string[8:12]}-{hex_string[12:16]}"
    
    return key


def generate_key_hash(license_key):
    """Generate SHA256 hash of license key for verification"""
    return hashlib.sha256(license_key.encode()).hexdigest()


def generate_keys_batch(count=100):
    """Generate a batch of license keys"""
    keys = []
    
    print(f"🔑 Generating {count} license keys...\n")
    
    for i in range(count):
        key = generate_license_key()
        key_hash = generate_key_hash(key)
        
        keys.append({
            "id": i + 1,
            "license_key": key,
            "hash": key_hash,
            "status": "available",
            "generated_at": datetime.now().isoformat(),
            "activated_at": None,
            "customer_email": None
        })
        
        if (i + 1) % 10 == 0:
            print(f"✅ Generated {i + 1}/{count} keys...")
    
    print(f"\n🎉 Successfully generated {count} license keys!")
    return keys


def save_keys_to_file(keys, output_dir="dist"):
    """Save license keys to multiple formats"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Save full database (JSON)
    json_file = output_path / "license_keys_database.json"
    with open(json_file, 'w') as f:
        json.dump(keys, f, indent=2)
    print(f"📄 Full database saved: {json_file}")
    
    # Save keys only (for Gumroad)
    keys_only_file = output_path / "license_keys_for_gumroad.txt"
    with open(keys_only_file, 'w') as f:
        f.write("# OSINT Tool Pro - License Keys\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total Keys: {len(keys)}\n")
        f.write("# Use these keys in Gumroad's license key field\n\n")
        for key_data in keys:
            f.write(f"{key_data['license_key']}\n")
    print(f"📄 Gumroad keys saved: {keys_only_file}")
    
    # Save hashes for verification system
    hashes_file = output_path / "valid_license_hashes.txt"
    with open(hashes_file, 'w') as f:
        f.write("# Valid License Key Hashes (SHA256)\n")
        f.write("# For integration with Pro verification system\n\n")
        for key_data in keys:
            f.write(f"{key_data['hash']}\n")
    print(f"📄 Hash list saved: {hashes_file}")
    
    # Save sample keys for testing
    sample_file = output_path / "sample_license_keys.txt"
    with open(sample_file, 'w') as f:
        f.write("# Sample License Keys for Testing\n\n")
        for i in range(min(5, len(keys))):
            f.write(f"Test Key {i+1}: {keys[i]['license_key']}\n")
    print(f"📄 Sample keys saved: {sample_file}")


def update_pro_license_validator(keys, pro_init_file="tools/osint/pro/__init__.py"):
    """Update the Pro __init__.py with valid hashes"""
    valid_hashes = [k['hash'] for k in keys]
    
    print(f"\n📝 To update the Pro license validator:")
    print(f"   File: {pro_init_file}")
    print(f"   Add these {len(valid_hashes)} hashes to VALID_LICENSE_HASHES set")
    print(f"\n   Or use this code snippet:")
    print(f"   ```python")
    print(f"   # Valid license key hashes (SHA256)")
    print(f"   VALID_LICENSE_HASHES = {{")
    for h in valid_hashes[:3]:  # Show first 3 as example
        print(f"       '{h}',")
    print(f"       # ... {len(valid_hashes) - 3} more hashes")
    print(f"   }}")
    print(f"   ```")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate license keys for OSINT Tool Pro")
    parser.add_argument('--count', type=int, default=100, help='Number of keys to generate (default: 100)')
    parser.add_argument('--output', type=str, default='dist', help='Output directory (default: dist)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("  OSINT Tool Pro - License Key Generator")
    print("=" * 60)
    print()
    
    # Generate keys
    keys = generate_keys_batch(args.count)
    
    # Save to files
    print()
    save_keys_to_file(keys, args.output)
    
    # Show instructions
    update_pro_license_validator(keys)
    
    print("\n" + "=" * 60)
    print("✅ Key generation complete!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("1. Upload 'license_keys_for_gumroad.txt' to Gumroad")
    print("2. Update tools/osint/pro/__init__.py with valid hashes")
    print("3. Test activation with sample keys")
    print("4. Keep 'license_keys_database.json' secure (backup!)")
    print()
