#!/usr/bin/env python3
"""
One-command release script for context-packer.
Usage: python release.py [patch|minor|major]
"""

import subprocess
import sys
import re
from pathlib import Path


def run_command(cmd, capture=False, check=True):
    """Run a shell command."""
    print(f"  → {cmd}")
    if capture:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip()
    else:
        return subprocess.run(cmd, shell=True, check=check)


def main():
    version_type = sys.argv[1] if len(sys.argv) > 1 else 'patch'
    
    if version_type not in ['patch', 'minor', 'major']:
        print("❌ Invalid version type. Use: patch, minor, or major")
        sys.exit(1)
    
    print(f"\n🚀 Starting release ({version_type} version bump)...\n")
    
    # 1. Run tests
    print("📋 Running tests...")
    try:
        run_command("python tests/test_context_packer.py", capture=True)
        print("✅ Tests passed\n")
    except subprocess.CalledProcessError:
        print("❌ Tests failed! Fix them before releasing.")
        sys.exit(1)
    
    # 2. Format code
    print("🎨 Formatting code...")
    try:
        run_command("black context_packer.py --quiet", check=False)
        run_command("ruff check --fix context_packer.py --quiet", check=False)
        print("✅ Code formatted\n")
    except:
        print("⚠️  Formatting tools not found, skipping...\n")
    
    # 3. Bump version
    print(f"📝 Bumping version ({version_type})...")
    run_command(f"python bump_version.py {version_type}")
    
    # Get new version
    pyproject = Path("pyproject.toml").read_text()
    version_match = re.search(r'version = "([^"]+)"', pyproject)
    if not version_match:
        print("❌ Could not find version in pyproject.toml")
        sys.exit(1)
    
    new_version = version_match.group(1)
    print(f"✅ Version bumped to {new_version}\n")
    
    # 4. Git commit and tag
    print("📌 Creating git commit...")
    run_command("git add -A")
    try:
        run_command(f'git commit -m "Release v{new_version}"')
    except:
        print("  → No changes to commit")
    
    print(f"\n🏷️  Creating tag v{new_version}...")
    run_command(f'git tag -a v{new_version} -m "Release version {new_version}"')
    
    # 5. Push to GitHub
    print("\n🌍 Pushing to GitHub...")
    run_command("git push origin main --follow-tags")
    
    # 6. Build and publish to PyPI
    print("\n📦 Building package...")
    run_command("rm -rf dist/ build/ *.egg-info")
    run_command("python -m build")
    
    print("\n📤 Publishing to PyPI...")
    try:
        run_command("twine upload dist/* --skip-existing")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  PyPI upload failed: {e}")
        print("Make sure TWINE_USERNAME and TWINE_PASSWORD environment variables are set")
        print("Or configure ~/.pypirc with your PyPI token")
        sys.exit(1)
    
    # Success!
    print("\n" + "="*50)
    print(f"🎉 Release v{new_version} completed successfully!")
    print("="*50)
    print(f"\n📦 Install: pip install context-packer=={new_version}")
    print(f"🔗 GitHub: https://github.com/MarkShawn2020/context-packer/releases/tag/v{new_version}")
    print(f"📈 PyPI: https://pypi.org/project/context-packer/{new_version}/")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Release cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Release failed: {e}")
        sys.exit(1)