#!/bin/bash
# SIL Website - Documentation Sync Script
# Syncs markdown docs from SIL repo to website for deployment

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEBSITE_ROOT="$(dirname "$SCRIPT_DIR")"
SIL_REPO="${WEBSITE_ROOT}/../SIL"
WEBSITE_DOCS="${WEBSITE_ROOT}/docs"

echo "========================================="
echo "SIL Documentation Sync"
echo "========================================="
echo ""

# Check if SIL repo exists
if [ ! -d "$SIL_REPO" ]; then
    echo -e "${RED}ERROR: SIL repository not found at $SIL_REPO${NC}"
    echo "Please ensure SIL repo is cloned at the expected location."
    exit 1
fi

echo -e "${GREEN}✓${NC} Found SIL repo: $SIL_REPO"

# Check if SIL docs directory exists
if [ ! -d "$SIL_REPO/docs" ]; then
    echo -e "${RED}ERROR: SIL docs directory not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Found SIL docs directory"
echo ""

# Create website docs directory if it doesn't exist
mkdir -p "$WEBSITE_DOCS"

# Sync canonical docs
echo "Syncing docs/canonical/..."
rsync -av --delete \
    --exclude='.git' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    "$SIL_REPO/docs/canonical/" \
    "$WEBSITE_DOCS/canonical/"
echo -e "${GREEN}✓${NC} Canonical docs synced"

# Sync architecture docs
echo "Syncing docs/architecture/..."
rsync -av --delete \
    --exclude='.git' \
    "$SIL_REPO/docs/architecture/" \
    "$WEBSITE_DOCS/architecture/"
echo -e "${GREEN}✓${NC} Architecture docs synced"

# Sync guides
echo "Syncing docs/guides/..."
rsync -av --delete \
    --exclude='.git' \
    "$SIL_REPO/docs/guides/" \
    "$WEBSITE_DOCS/guides/"
echo -e "${GREEN}✓${NC} Guides synced"

# Sync vision docs
echo "Syncing docs/vision/..."
rsync -av --delete \
    --exclude='.git' \
    "$SIL_REPO/docs/vision/" \
    "$WEBSITE_DOCS/vision/"
echo -e "${GREEN}✓${NC} Vision docs synced"

# Sync research docs
echo "Syncing docs/research/..."
rsync -av --delete \
    --exclude='.git' \
    "$SIL_REPO/docs/research/" \
    "$WEBSITE_DOCS/research/"
echo -e "${GREEN}✓${NC} Research docs synced"

# Sync meta docs
echo "Syncing docs/meta/..."
rsync -av --delete \
    --exclude='.git' \
    "$SIL_REPO/docs/meta/" \
    "$WEBSITE_DOCS/meta/"
echo -e "${GREEN}✓${NC} Meta docs synced"

# Sync innovations docs
echo "Syncing docs/innovations/..."
rsync -av --delete \
    --exclude='.git' \
    "$SIL_REPO/docs/innovations/" \
    "$WEBSITE_DOCS/innovations/"
echo -e "${GREEN}✓${NC} Innovations docs synced"

# Sync semantic-os docs
echo "Syncing docs/semantic-os/..."
rsync -av --delete \
    --exclude='.git' \
    "$SIL_REPO/docs/semantic-os/" \
    "$WEBSITE_DOCS/semantic-os/"
echo -e "${GREEN}✓${NC} Semantic OS docs synced"

# Sync tools docs
echo "Syncing docs/tools/..."
rsync -av --delete \
    --exclude='.git' \
    "$SIL_REPO/docs/tools/" \
    "$WEBSITE_DOCS/tools/"
echo -e "${GREEN}✓${NC} Tools docs synced"

# Sync top-level docs
echo "Syncing top-level docs..."
# Sync all top-level docs from SIL repo
cp "$SIL_REPO/docs/FAQ.md" "$WEBSITE_DOCS/" 2>/dev/null || true
cp "$SIL_REPO/docs/PROGRESSIVE_DISCLOSURE.md" "$WEBSITE_DOCS/" 2>/dev/null || true
cp "$SIL_REPO/docs/SIL_DESIGN_PRINCIPLES.md" "$WEBSITE_DOCS/" 2>/dev/null || true
cp "$SIL_REPO/docs/SIL_SAFETY_THRESHOLDS.md" "$WEBSITE_DOCS/" 2>/dev/null || true
cp "$SIL_REPO/docs/QUICKSTART.md" "$WEBSITE_DOCS/" 2>/dev/null || true
cp "$SIL_REPO/docs/READING_GUIDE.md" "$WEBSITE_DOCS/" 2>/dev/null || true
cp "$SIL_REPO/docs/README.md" "$WEBSITE_DOCS/" 2>/dev/null || true
echo -e "${GREEN}✓${NC} Top-level docs synced"

# Sync projects index
echo "Syncing PROJECT_INDEX.md..."
mkdir -p "$WEBSITE_DOCS/projects"
cp "$SIL_REPO/projects/PROJECT_INDEX.md" "$WEBSITE_DOCS/projects/"
echo -e "${GREEN}✓${NC} Projects index synced"

# Sync README (for homepage)
echo "Syncing README.md..."
cp "$SIL_REPO/README.md" "$WEBSITE_DOCS/"
echo -e "${GREEN}✓${NC} README synced"

echo ""
echo "========================================="
echo "Validation"
echo "========================================="
echo ""

# Count synced files
CANONICAL_COUNT=$(find "$WEBSITE_DOCS/canonical" -name "*.md" 2>/dev/null | wc -l)
ARCHITECTURE_COUNT=$(find "$WEBSITE_DOCS/architecture" -name "*.md" 2>/dev/null | wc -l)
GUIDES_COUNT=$(find "$WEBSITE_DOCS/guides" -name "*.md" 2>/dev/null | wc -l)
VISION_COUNT=$(find "$WEBSITE_DOCS/vision" -name "*.md" 2>/dev/null | wc -l)
RESEARCH_COUNT=$(find "$WEBSITE_DOCS/research" -name "*.md" 2>/dev/null | wc -l)
META_COUNT=$(find "$WEBSITE_DOCS/meta" -name "*.md" 2>/dev/null | wc -l)
SEMANTIC_OS_COUNT=$(find "$WEBSITE_DOCS/semantic-os" -name "*.md" 2>/dev/null | wc -l)
TOOLS_COUNT=$(find "$WEBSITE_DOCS/tools" -name "*.md" 2>/dev/null | wc -l)

echo "Synced files by category:"
echo "  Canonical:    $CANONICAL_COUNT documents"
echo "  Architecture: $ARCHITECTURE_COUNT documents"
echo "  Guides:       $GUIDES_COUNT documents"
echo "  Vision:       $VISION_COUNT documents"
echo "  Research:     $RESEARCH_COUNT documents"
echo "  Meta:         $META_COUNT documents"
echo "  Semantic OS:  $SEMANTIC_OS_COUNT documents"
echo "  Tools:        $TOOLS_COUNT documents"
echo ""

TOTAL_COUNT=$((CANONICAL_COUNT + ARCHITECTURE_COUNT + GUIDES_COUNT + VISION_COUNT + RESEARCH_COUNT + META_COUNT + SEMANTIC_OS_COUNT + TOOLS_COUNT))
echo "Total: $TOTAL_COUNT markdown files"
echo ""

# Check for common required files
REQUIRED_FILES=(
    "canonical/SIL_MANIFESTO.md"
    "canonical/SIL_PRINCIPLES.md"
    "canonical/SIL_TECHNICAL_CHARTER.md"
    "canonical/FOUNDERS_LETTER.md"
    "architecture/UNIFIED_ARCHITECTURE_GUIDE.md"
    "research/RAG_AS_SEMANTIC_MANIFOLD_TRANSPORT.md"
    "meta/FAQ.md"
    "README.md"
)

echo "Checking required files..."
MISSING_FILES=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$WEBSITE_DOCS/$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} Missing: $file"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

echo ""

if [ $MISSING_FILES -eq 0 ]; then
    echo -e "${GREEN}=========================================${NC}"
    echo -e "${GREEN}✓ Documentation sync completed successfully${NC}"
    echo -e "${GREEN}=========================================${NC}"
    exit 0
else
    echo -e "${YELLOW}=========================================${NC}"
    echo -e "${YELLOW}⚠ Sync completed with $MISSING_FILES missing files${NC}"
    echo -e "${YELLOW}=========================================${NC}"
    exit 1
fi
