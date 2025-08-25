#!/bin/bash
# Quick release script for context-packer (assumes PyPI token is configured)

set -e

# Color codes for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default to patch version
VERSION_TYPE=${1:-patch}

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    Context Packer - Quick Release Script${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

# Run tests first
echo -e "\n${YELLOW}📋 Running tests...${NC}"
if python tests/test_context_packer.py > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Tests passed${NC}"
else
    echo -e "${RED}❌ Tests failed! Fix them before releasing.${NC}"
    exit 1
fi

# Format code
echo -e "\n${YELLOW}🎨 Formatting code...${NC}"
if command -v black &> /dev/null; then
    black context_packer.py --quiet
    echo -e "${GREEN}✅ Code formatted${NC}"
fi

# Bump version
echo -e "\n${YELLOW}📝 Bumping version (${VERSION_TYPE})...${NC}"
python bump_version.py $VERSION_TYPE

# Extract new version
NEW_VERSION=$(grep 'version = ' pyproject.toml | cut -d'"' -f2)
echo -e "${GREEN}✅ Version bumped to ${NEW_VERSION}${NC}"

# Git operations
echo -e "\n${YELLOW}📌 Committing changes...${NC}"
git add -A
git commit -m "Release v${NEW_VERSION}" || true

echo -e "\n${YELLOW}🏷️  Creating git tag...${NC}"
git tag -a "v${NEW_VERSION}" -m "Release version ${NEW_VERSION}"

echo -e "\n${YELLOW}🚀 Pushing to GitHub...${NC}"
git push origin main --follow-tags

# Build and publish
echo -e "\n${YELLOW}📦 Building package...${NC}"
rm -rf dist/ build/ *.egg-info
python -m build

echo -e "\n${YELLOW}🌍 Publishing to PyPI...${NC}"
twine upload dist/* --skip-existing

# Success message
echo -e "\n${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🎉 Release v${NEW_VERSION} completed successfully!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "\n📦 Install with: ${BLUE}pip install context-packer==${NEW_VERSION}${NC}"
echo -e "🔗 View release: ${BLUE}https://github.com/MarkShawn2020/context-packer/releases/tag/v${NEW_VERSION}${NC}"
echo -e "📈 PyPI page: ${BLUE}https://pypi.org/project/context-packer/${NEW_VERSION}/${NC}"