#!/usr/bin/env python3
"""
Simple version bumping utility for context-packer
"""

import re
import sys
from pathlib import Path


def bump_version(version_type='patch'):
    """Bump version in pyproject.toml and setup.py"""
    
    # Read current version from pyproject.toml
    pyproject_path = Path('pyproject.toml')
    content = pyproject_path.read_text()
    
    # Find current version
    version_match = re.search(r'^version = "(\d+)\.(\d+)\.(\d+)"', content, re.MULTILINE)
    if not version_match:
        print("❌ Could not find version in pyproject.toml")
        return False
    
    major, minor, patch = map(int, version_match.groups())
    
    # Calculate new version
    if version_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif version_type == 'minor':
        minor += 1
        patch = 0
    elif version_type == 'patch':
        patch += 1
    else:
        print(f"❌ Unknown version type: {version_type}")
        return False
    
    old_version = f"{version_match.group(1)}.{version_match.group(2)}.{version_match.group(3)}"
    new_version = f"{major}.{minor}.{patch}"
    
    print(f"📦 Bumping version: {old_version} → {new_version}")
    
    # Update pyproject.toml
    content = re.sub(
        r'^version = "\d+\.\d+\.\d+"',
        f'version = "{new_version}"',
        content,
        flags=re.MULTILINE
    )
    pyproject_path.write_text(content)
    print("✅ Updated pyproject.toml")
    
    # Update setup.py if it exists
    setup_path = Path('setup.py')
    if setup_path.exists():
        setup_content = setup_path.read_text()
        setup_content = re.sub(
            r'version="\d+\.\d+\.\d+"',
            f'version="{new_version}"',
            setup_content
        )
        setup_path.write_text(setup_content)
        print("✅ Updated setup.py")
    
    print(f"\n🎉 Version bumped to {new_version}")
    print("\nNext steps:")
    print(f"1. git add -A")
    print(f"2. git commit -m 'Bump version to {new_version}'")
    print(f"3. git tag v{new_version}")
    print(f"4. git push origin main --tags")
    print(f"5. ./publish.sh")
    
    return True


if __name__ == '__main__':
    if len(sys.argv) > 1:
        version_type = sys.argv[1]
        if version_type not in ['major', 'minor', 'patch']:
            print("Usage: python bump_version.py [major|minor|patch]")
            print("Default: patch")
            sys.exit(1)
    else:
        version_type = 'patch'
    
    if bump_version(version_type):
        sys.exit(0)
    else:
        sys.exit(1)