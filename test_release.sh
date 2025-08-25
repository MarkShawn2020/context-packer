#!/bin/bash
# Test release process without actually publishing

set -e

echo "🧪 Testing release process..."

# Test version extraction
VERSION=$(grep '^version = ' pyproject.toml | cut -d'"' -f2)
echo "✅ Version extraction works: $VERSION"

# Test that tests pass
echo "📋 Running tests..."
if python tests/test_context_packer.py > /dev/null 2>&1; then
    echo "✅ Tests pass"
else
    echo "❌ Tests failed!"
    exit 1
fi

# Test building
echo "📦 Testing build..."
rm -rf dist/ build/
if python -m build > /dev/null 2>&1; then
    echo "✅ Build succeeds"
    ls -la dist/
else
    echo "❌ Build failed!"
    exit 1
fi

# Test that PyPI credentials are configured
echo "🔑 Checking PyPI configuration..."
if [ -n "$TWINE_PASSWORD" ]; then
    echo "✅ TWINE_PASSWORD is set"
elif [ -f ~/.pypirc ]; then
    echo "✅ ~/.pypirc exists"
else
    echo "⚠️  No PyPI credentials found. You need to either:"
    echo "   - Set TWINE_USERNAME=__token__ and TWINE_PASSWORD=pypi-..."
    echo "   - Create ~/.pypirc with your token"
fi

echo ""
echo "🎉 Release process test complete!"
echo ""
echo "To do actual release, run one of:"
echo "  make release"
echo "  python release.py"
echo "  ./quick-release.sh"