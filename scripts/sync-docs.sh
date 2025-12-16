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

# Sync manifesto
echo "Syncing docs/manifesto/..."
rsync -av --delete \
    --exclude='.git' \
    "$SIL_REPO/docs/manifesto/" \
    "$WEBSITE_DOCS/manifesto/"
echo -e "${GREEN}✓${NC} Manifesto synced"

# Sync foundations
echo "Syncing docs/foundations/..."
rsync -av --delete \
    --exclude='.git' \
    "$SIL_REPO/docs/foundations/" \
    "$WEBSITE_DOCS/foundations/"
echo -e "${GREEN}✓${NC} Foundations synced"

# Sync architecture docs
echo "Syncing docs/architecture/..."
rsync -av --delete \
    --exclude='.git' \
    "$SIL_REPO/docs/architecture/" \
    "$WEBSITE_DOCS/architecture/"
echo -e "${GREEN}✓${NC} Architecture docs synced"

# NOTE: guides/ and vision/ directories removed from SIL repo (empty placeholders)

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

# Sync systems docs (formerly tools/ and innovations/)
echo "Syncing docs/systems/..."
rsync -av --delete \
    --exclude='.git' \
    "$SIL_REPO/docs/systems/" \
    "$WEBSITE_DOCS/systems/"
echo -e "${GREEN}✓${NC} Systems docs synced"

# Sync essays (now in public SIL repo alongside other docs)
echo "Syncing docs/essays/..."
rsync -av --delete \
    --exclude='.git' \
    "$SIL_REPO/docs/essays/" \
    "$WEBSITE_DOCS/essays/"
echo -e "${GREEN}✓${NC} Essays synced"

# Sync top-level docs
echo "Syncing top-level docs..."
# Sync all top-level docs from SIL repo
cp "$SIL_REPO/docs/FAQ.md" "$WEBSITE_DOCS/" 2>/dev/null || true
cp "$SIL_REPO/docs/PROGRESSIVE_DISCLOSURE.md" "$WEBSITE_DOCS/" 2>/dev/null || true
cp "$SIL_REPO/docs/SIL_DESIGN_PRINCIPLES.md" "$WEBSITE_DOCS/" 2>/dev/null || true
cp "$SIL_REPO/docs/SIL_SAFETY_THRESHOLDS.md" "$WEBSITE_DOCS/" 2>/dev/null || true
# NOTE: QUICKSTART.md and READING_GUIDE.md removed - consolidated into canonical/START_HERE.md
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
MANIFESTO_COUNT=$(find "$WEBSITE_DOCS/manifesto" -name "*.md" 2>/dev/null | wc -l)
FOUNDATIONS_COUNT=$(find "$WEBSITE_DOCS/foundations" -name "*.md" 2>/dev/null | wc -l)
RESEARCH_COUNT=$(find "$WEBSITE_DOCS/research" -name "*.md" 2>/dev/null | wc -l)
SYSTEMS_COUNT=$(find "$WEBSITE_DOCS/systems" -name "*.md" 2>/dev/null | wc -l)
ARCHITECTURE_COUNT=$(find "$WEBSITE_DOCS/architecture" -name "*.md" 2>/dev/null | wc -l)
META_COUNT=$(find "$WEBSITE_DOCS/meta" -name "*.md" 2>/dev/null | wc -l)
ESSAYS_COUNT=$(find "$WEBSITE_DOCS/essays" -name "*.md" 2>/dev/null | wc -l)

echo "Synced files by category:"
echo "  Manifesto:    $MANIFESTO_COUNT documents"
echo "  Foundations:  $FOUNDATIONS_COUNT documents"
echo "  Research:     $RESEARCH_COUNT documents"
echo "  Systems:      $SYSTEMS_COUNT documents"
echo "  Architecture: $ARCHITECTURE_COUNT documents"
echo "  Meta:         $META_COUNT documents"
echo "  Essays:       $ESSAYS_COUNT documents"
echo ""

TOTAL_COUNT=$((MANIFESTO_COUNT + FOUNDATIONS_COUNT + RESEARCH_COUNT + SYSTEMS_COUNT + ARCHITECTURE_COUNT + META_COUNT + ESSAYS_COUNT))
echo "Total: $TOTAL_COUNT markdown files"
echo ""

# Check for common required files
REQUIRED_FILES=(
    "manifesto/YOLO.md"
    "foundations/architectural-principles.md"
    "foundations/design-principles.md"
    "foundations/SIL_TECHNICAL_CHARTER.md"
    "foundations/FOUNDERS_LETTER.md"
    "foundations/SIL_SEMANTIC_OS_ARCHITECTURE.md"
    "architecture/UNIFIED_ARCHITECTURE_GUIDE.md"
    "research/information-architecture/PROGRESSIVE_DISCLOSURE_GUIDE.md"
    "systems/reveal.md"
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
