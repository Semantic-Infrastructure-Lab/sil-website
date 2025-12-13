#!/usr/bin/env bash
# Validate Website Deployment Readiness
# Checks that source files are synced, generated files are current, etc.

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SIL_REPO="${PROJECT_ROOT}/../SIL"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Website Deployment Validation${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

ERRORS=0
WARNINGS=0

# Check 1: SIL repo exists
echo -n "Checking SIL source repo... "
if [ -d "$SIL_REPO" ]; then
  echo -e "${GREEN}✓${NC}"
else
  echo -e "${RED}✗ NOT FOUND${NC}"
  echo "  Expected: $SIL_REPO"
  ((ERRORS++))
fi

# Check 2: Docs directory exists
echo -n "Checking docs directory... "
if [ -d "${PROJECT_ROOT}/docs" ]; then
  echo -e "${GREEN}✓${NC}"
else
  echo -e "${RED}✗ NOT FOUND${NC}"
  echo "  Run: ./scripts/sync-docs.sh"
  ((ERRORS++))
fi

# Check 3: Compare source vs synced (sample files)
echo ""
echo "Checking source vs synced files..."

SAMPLE_FILES=(
  "meta/FOUNDER_BACKGROUND.md"
  "canonical/SIL_MANIFESTO.md"
  "canonical/SIL_PRINCIPLES.md"
)

for file in "${SAMPLE_FILES[@]}"; do
  echo -n "  $file... "

  SRC="${SIL_REPO}/docs/${file}"
  DST="${PROJECT_ROOT}/docs/${file}"

  if [ ! -f "$SRC" ]; then
    echo -e "${YELLOW}⚠ Source missing${NC}"
    ((WARNINGS++))
    continue
  fi

  if [ ! -f "$DST" ]; then
    echo -e "${RED}✗ Not synced${NC}"
    echo "    Run: ./scripts/sync-docs.sh"
    ((ERRORS++))
    continue
  fi

  if diff -q "$SRC" "$DST" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Synced${NC}"
  else
    echo -e "${RED}✗ OUT OF SYNC${NC}"
    echo "    Source: $SRC"
    echo "    Synced: $DST"
    echo "    Run: ./scripts/sync-docs.sh"
    ((ERRORS++))
  fi
done

# Check 4: llms-full.txt exists
echo ""
echo -n "Checking llms-full.txt exists... "
if [ -f "${PROJECT_ROOT}/static/llms-full.txt" ]; then
  echo -e "${GREEN}✓${NC}"

  # Check file age
  FILE_AGE=$(($(date +%s) - $(stat -c %Y "${PROJECT_ROOT}/static/llms-full.txt")))
  FILE_AGE_HOURS=$((FILE_AGE / 3600))

  echo -n "  Age: ${FILE_AGE_HOURS} hours... "
  if [ $FILE_AGE_HOURS -gt 24 ]; then
    echo -e "${YELLOW}⚠ Old (>24h)${NC}"
    echo "    Consider regenerating: ./scripts/generate-llms-full.sh"
    ((WARNINGS++))
  else
    echo -e "${GREEN}✓ Recent${NC}"
  fi
else
  echo -e "${RED}✗ NOT FOUND${NC}"
  echo "  Run: ./scripts/generate-llms-full.sh"
  ((ERRORS++))
fi

# Check 5: Git status
echo ""
echo -n "Checking git status... "
cd "$PROJECT_ROOT"

if git diff --quiet && git diff --cached --quiet; then
  echo -e "${GREEN}✓ Clean${NC}"
else
  echo -e "${YELLOW}⚠ Uncommitted changes${NC}"
  echo ""
  git status --short
  echo ""
  echo "  Consider committing changes before deployment"
  ((WARNINGS++))
fi

# Check 6: Known factual errors
echo ""
echo "Checking for known incorrect facts..."

INCORRECT_FACTS=(
  "Colorado Boulder:University of Colorado"
  "1994-2010:Microsoft start year"
  "16 years at Microsoft:Should be 13 years"
)

cd "$PROJECT_ROOT"
for fact_check in "${INCORRECT_FACTS[@]}"; do
  SEARCH="${fact_check%%:*}"
  DESCRIPTION="${fact_check##*:}"

  echo -n "  $DESCRIPTION... "

  # Check in docs
  if grep -r "$SEARCH" docs/ 2>/dev/null | grep -v README > /dev/null; then
    echo -e "${RED}✗ FOUND IN DOCS${NC}"
    grep -r "$SEARCH" docs/ 2>/dev/null | grep -v README | head -3
    ((ERRORS++))
  # Check in llms-full.txt
  elif grep "$SEARCH" static/llms-full.txt > /dev/null 2>&1; then
    echo -e "${RED}✗ FOUND IN llms-full.txt${NC}"
    echo "    Regenerate: ./scripts/generate-llms-full.sh"
    ((ERRORS++))
  else
    echo -e "${GREEN}✓ Not found${NC}"
  fi
done

# Check 7: Required correct facts
echo ""
echo "Checking for required correct facts..."

REQUIRED_FACTS=(
  "Cal Poly:Correct education"
  "California Polytechnic:Correct education (full)"
  "1997-2010:Correct Microsoft dates"
  "13 years:Correct Microsoft tenure"
)

for fact_check in "${REQUIRED_FACTS[@]}"; do
  SEARCH="${fact_check%%:*}"
  DESCRIPTION="${fact_check##*:}"

  echo -n "  $DESCRIPTION... "

  if grep -r "$SEARCH" docs/ 2>/dev/null | grep -v README > /dev/null; then
    echo -e "${GREEN}✓ Found${NC}"
  else
    echo -e "${YELLOW}⚠ Not found in docs${NC}"
    echo "    Check if sync completed: ./scripts/sync-docs.sh"
    ((WARNINGS++))
  fi
done

# Summary
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Validation Summary${NC}"
echo -e "${BLUE}========================================${NC}"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
  echo -e "${GREEN}✓ All checks passed${NC}"
  echo ""
  echo "Ready to deploy:"
  echo "  ./deploy/deploy-container.sh staging --fresh"
  exit 0
elif [ $ERRORS -eq 0 ]; then
  echo -e "${YELLOW}⚠ Passed with $WARNINGS warning(s)${NC}"
  echo ""
  echo "Review warnings above. Deployment should be safe but review recommended."
  exit 0
else
  echo -e "${RED}✗ Failed with $ERRORS error(s) and $WARNINGS warning(s)${NC}"
  echo ""
  echo "Fix errors before deploying. Common fixes:"
  echo "  ./scripts/sync-docs.sh              # Sync from SIL repo"
  echo "  ./scripts/generate-llms-full.sh     # Regenerate llms-full.txt"
  echo "  git add . && git commit -m 'msg'    # Commit changes"
  exit 1
fi
