"""
Build script for creating OSINT Tool Pro Windows executable
"""
import PyInstaller.__main__
import os

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.abspath(__file__))
cli_path = os.path.join(project_root, 'tools', 'osint', 'cli.py')

# PyInstaller arguments
PyInstaller.__main__.run([
    cli_path,
    '--onefile',                          # Single executable file
    '--name=osint-tool-pro',              # Output name
    '--console',                          # Keep console window
    '--clean',                            # Clean build cache
    '--noconfirm',                        # Don't ask for confirmation
    f'--distpath={os.path.join(project_root, "dist")}',
    f'--workpath={os.path.join(project_root, "build")}',
    f'--specpath={os.path.join(project_root, "build")}',
    '--add-data', f'{os.path.join(project_root, "tools", "osint", "modules")}{os.pathsep}tools/osint/modules',
    '--add-data', f'{os.path.join(project_root, "tools", "osint", "pro")}{os.pathsep}tools/osint/pro',
    '--hidden-import=tools.osint.modules.email_lookup',
    '--hidden-import=tools.osint.modules.username_search',
    '--hidden-import=tools.osint.modules.breach_check',
    '--hidden-import=tools.osint.modules.whois_lookup',
    '--hidden-import=tools.osint.modules.resources',
    '--hidden-import=tools.osint.modules.auto_search',
    '--hidden-import=tools.osint.pro',
    '--hidden-import=tools.osint.pro.report_generator',
    '--hidden-import=tools.osint.pro.bulk_search',
])

print("\n✅ Build complete!")
print(f"📦 Executable location: {os.path.join(project_root, 'dist', 'osint-tool-pro.exe')}")
print("\nTest it with:")
print("  .\\dist\\osint-tool-pro.exe --help")
