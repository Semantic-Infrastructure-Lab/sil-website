#!/bin/bash
#
# Validate that all SIL website markdown files have proper frontmatter.
#
# Usage:
#   ./scripts/validate-frontmatter.sh
#
# Exit codes:
#   0 - All files have valid frontmatter
#   1 - Some files are missing frontmatter or have invalid frontmatter
#

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_DIR="$PROJECT_ROOT/docs"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Validating frontmatter in $DOCS_DIR"
echo ""

missing_frontmatter=()
missing_title=()
missing_tier=()
missing_order=()
valid_count=0

# Find all markdown files
while IFS= read -r -d '' file; do
    rel_path="${file#$PROJECT_ROOT/}"

    # Check if file starts with ---
    if ! head -n 1 "$file" | grep -q "^---$"; then
        missing_frontmatter+=("$rel_path")
        continue
    fi

    # Extract frontmatter (between first two --- lines)
    frontmatter=$(awk '/^---$/{i++}i==1{print;next}i==2{exit}' "$file")

    # Check for required fields
    if ! echo "$frontmatter" | grep -q "^title:"; then
        missing_title+=("$rel_path")
    fi

    if ! echo "$frontmatter" | grep -q "^tier:"; then
        missing_tier+=("$rel_path")
    fi

    if ! echo "$frontmatter" | grep -q "^order:"; then
        missing_order+=("$rel_path")
    fi

    # If all required fields present, count as valid
    if echo "$frontmatter" | grep -q "^title:" && \
       echo "$frontmatter" | grep -q "^tier:" && \
       echo "$frontmatter" | grep -q "^order:"; then
        ((valid_count++))
    fi

done < <(find "$DOCS_DIR" -name "*.md" -type f -print0)

# Report results
total_files=$(find "$DOCS_DIR" -name "*.md" -type f | wc -l)

echo "================================================================"
echo "Validation Results"
echo "================================================================"
echo ""
echo "Total markdown files: $total_files"
echo "Valid files: $valid_count"
echo ""

has_errors=0

if [ ${#missing_frontmatter[@]} -gt 0 ]; then
    has_errors=1
    echo -e "${RED}✗ Files missing frontmatter: ${#missing_frontmatter[@]}${NC}"
    for file in "${missing_frontmatter[@]}"; do
        echo "    $file"
    done
    echo ""
fi

if [ ${#missing_title[@]} -gt 0 ]; then
    has_errors=1
    echo -e "${YELLOW}⚠ Files missing 'title' field: ${#missing_title[@]}${NC}"
    for file in "${missing_title[@]}"; do
        echo "    $file"
    done
    echo ""
fi

if [ ${#missing_tier[@]} -gt 0 ]; then
    has_errors=1
    echo -e "${YELLOW}⚠ Files missing 'tier' field: ${#missing_tier[@]}${NC}"
    for file in "${missing_tier[@]}"; do
        echo "    $file"
    done
    echo ""
fi

if [ ${#missing_order[@]} -gt 0 ]; then
    has_errors=1
    echo -e "${YELLOW}⚠ Files missing 'order' field: ${#missing_order[@]}${NC}"
    for file in "${missing_order[@]}"; do
        echo "    $file"
    done
    echo ""
fi

if [ $has_errors -eq 0 ]; then
    echo -e "${GREEN}✓ All files have valid frontmatter!${NC}"
    echo ""
    echo "Ready for deployment."
    exit 0
else
    echo -e "${RED}✗ Validation failed${NC}"
    echo ""
    echo "Fix missing frontmatter before deployment."
    echo "Run: python scripts/add-frontmatter.py --apply"
    exit 1
fi
