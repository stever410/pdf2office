#!/usr/bin/env bash
# Release helper script for PDF2Office
# Usage: ./scripts/release.sh [version]
# Example: ./scripts/release.sh 1.1.0

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if version is provided
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: Version number required${NC}"
    echo "Usage: $0 [version]"
    echo "Example: $0 1.1.0"
    exit 1
fi

NEW_VERSION="$1"

# Validate version format (semantic versioning)
if ! [[ "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}Error: Invalid version format${NC}"
    echo "Version must be in format: MAJOR.MINOR.PATCH (e.g., 1.0.0)"
    exit 1
fi

# Get current version from metadata
CURRENT_VERSION=$(python3 -c 'from pdf2office.metadata import APP_VERSION; print(APP_VERSION)')

echo -e "${BLUE}PDF2Office Release Helper${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "Current version: ${YELLOW}${CURRENT_VERSION}${NC}"
echo -e "New version:     ${GREEN}${NEW_VERSION}${NC}"
echo ""

# Check if there are uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}⚠  Warning: You have uncommitted changes${NC}"
    git status --short
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Check if tag already exists
if git rev-parse "v${NEW_VERSION}" >/dev/null 2>&1; then
    echo -e "${RED}Error: Tag v${NEW_VERSION} already exists${NC}"
    exit 1
fi

# Confirm before proceeding
echo "This will:"
echo "  1. Update APP_VERSION in metadata.py"
echo "  2. Commit the change"
echo "  3. Create and push tag v${NEW_VERSION}"
echo "  4. Trigger GitHub Actions to build and release"
echo ""
read -p "Proceed? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Update version in metadata.py
echo -e "${BLUE}[1/4]${NC} Updating version in metadata.py..."
sed -i.bak "s/APP_VERSION = \".*\"/APP_VERSION = \"${NEW_VERSION}\"/" pdf2office/metadata.py
rm pdf2office/metadata.py.bak 2>/dev/null || true

# Verify the change
UPDATED_VERSION=$(python3 -c 'from pdf2office.metadata import APP_VERSION; print(APP_VERSION)')
if [ "$UPDATED_VERSION" != "$NEW_VERSION" ]; then
    echo -e "${RED}Error: Version update failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Version updated to ${NEW_VERSION}"

# Commit the change
echo -e "${BLUE}[2/4]${NC} Committing version bump..."
git add pdf2office/metadata.py
git commit -m "Bump version to v${NEW_VERSION}"
echo -e "${GREEN}✓${NC} Committed"

# Create tag
echo -e "${BLUE}[3/4]${NC} Creating tag v${NEW_VERSION}..."
git tag -a "v${NEW_VERSION}" -m "Release v${NEW_VERSION}"
echo -e "${GREEN}✓${NC} Tag created"

# Push to GitHub
echo -e "${BLUE}[4/4]${NC} Pushing to GitHub..."
git push origin main
git push origin "v${NEW_VERSION}"
echo -e "${GREEN}✓${NC} Pushed to GitHub"

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Release process initiated!${NC}"
echo ""
echo "GitHub Actions is now building the release."
echo "Monitor progress at:"
echo -e "${BLUE}https://github.com/stever410/pdf2office/actions${NC}"
echo ""
echo "Release will be available at:"
echo -e "${BLUE}https://github.com/stever410/pdf2office/releases/tag/v${NEW_VERSION}${NC}"
echo ""
echo "This typically takes 5-15 minutes."
