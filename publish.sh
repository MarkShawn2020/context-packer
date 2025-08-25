#!/bin/bash
# Publish context-packer to PyPI using UV or traditional tools

set -e

echo "🚀 Publishing context-packer to PyPI"
echo "======================================"

# Check if UV is installed
if command -v uv &> /dev/null; then
    echo "✅ Using UV for fast publishing"
    
    # Install build dependencies
    uv pip install --upgrade build twine
    
    # Clean previous builds
    rm -rf dist/ build/ *.egg-info
    
    # Build the package
    python -m build
    
    # Check the package
    twine check dist/*
    
    # Upload to Test PyPI first (optional)
    read -p "Upload to Test PyPI first? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📤 Uploading to Test PyPI..."
        twine upload --repository testpypi dist/*
        echo "✅ Test upload complete!"
        echo "Test with: uv pip install -i https://test.pypi.org/simple/ context-packer"
        read -p "Continue with production PyPI? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi
    
    # Upload to PyPI
    echo "📤 Uploading to PyPI..."
    twine upload dist/*
    
else
    echo "⚠️  UV not found, using traditional pip"
    
    # Install build dependencies
    pip install --upgrade build twine
    
    # Clean previous builds
    rm -rf dist/ build/ *.egg-info
    
    # Build the package
    python -m build
    
    # Check the package
    twine check dist/*
    
    # Upload
    echo "📤 Uploading to PyPI..."
    twine upload dist/*
fi

echo "✅ Successfully published to PyPI!"
echo "Install with: pip install context-packer"
echo "Or with UV: uv pip install context-packer"