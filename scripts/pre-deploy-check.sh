#!/bin/bash
# SIL Website - Pre-Deployment Checklist
# Run this before deploying to staging or production to ensure everything is ready
#
# Usage:
#   ./scripts/pre-deploy-check.sh [staging|production]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Counters
PASS=0
FAIL=0
WARN=0

# Environment
ENV="${1:-staging}"

echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║       SIL Website - Pre-Deployment Checklist            ║${NC}"
echo -e "${CYAN}║                                                          ║${NC}"
echo -e "${CYAN}║  Ensures you know what's deployed and links work        ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Target Environment: ${ENV}${NC}"
echo ""

# Helper functions
pass() {
    echo -e "${GREEN}  ✓${NC} $1"
    ((PASS++))
}

fail() {
    echo -e "${RED}  ✗${NC} $1"
    ((FAIL++))
}

warn() {
    echo -e "${YELLOW}  ⚠${NC} $1"
    ((WARN++))
}

info() {
    echo -e "    ${BLUE}→${NC} $1"
}

section() {
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEBSITE_ROOT="$(dirname "$SCRIPT_DIR")"
SIL_REPO="$WEBSITE_ROOT/../SIL"
MANIFEST="$SIL_REPO/docs/CONTENT_MANIFEST.yaml"

# ============================================================================
section "📋 Step 1: Know What's Public vs Internal"
# ============================================================================

if [[ -f "$MANIFEST" ]]; then
    pass "Content manifest found"

    # Show stats
    PUBLIC_COUNT=$(grep -c "visibility: public" "$MANIFEST")
    INTERNAL_COUNT=$(grep -c "visibility: internal" "$MANIFEST")

    info "📊 Content inventory:"
    info "   • $PUBLIC_COUNT files marked PUBLIC (will be on website)"
    info "   • $INTERNAL_COUNT files marked INTERNAL (will NOT be on website)"

    # Check if manifest is up to date
    LAST_AUDIT=$(grep "date:" "$MANIFEST" | grep -A1 "last_audit:" | tail -1 | awk '{print $2}')
    info "   • Last audit: $LAST_AUDIT"

else
    fail "Content manifest NOT found at: $MANIFEST"
    info "This tells you which files are public vs internal"
fi

# List some key public files
echo ""
info "📄 Key public files (sample):"
grep -A1 "visibility: public" "$MANIFEST" | grep "path:" | sed 's/.*path: //' | head -5 | while read -r file; do
    info "   • $file"
done
info "   ... and $(($PUBLIC_COUNT - 5)) more"

# List internal files
echo ""
info "🔒 Internal files (NOT on website):"
grep -A1 "visibility: internal" "$MANIFEST" | grep "path:" | sed 's/.*path: //' | head -5 | while read -r file; do
    info "   • $file"
done
if [[ $INTERNAL_COUNT -gt 5 ]]; then
    info "   ... and $(($INTERNAL_COUNT - 5)) more"
fi

# ============================================================================
section "🔄 Step 2: Verify Sync Status"
# ============================================================================

cd "$WEBSITE_ROOT"

# Run sync validation
if ./scripts/sync-docs.py --validate > /tmp/sync-check.log 2>&1; then
    pass "Sync validation passed"
    info "All public files synced, no internal files in website"
else
    fail "Sync validation FAILED"
    cat /tmp/sync-check.log
    info "Fix: cd $WEBSITE_ROOT && ./scripts/sync-docs.py"
fi

# Check for files not in manifest
UNTRACKED=$(cd "$SIL_REPO" && comm -13 \
    <(grep "path: docs/" "$MANIFEST" | sed 's/.*path: //' | sort) \
    <(find docs -name "*.md" -type f | sort) 2>/dev/null | head -5)

if [[ -z "$UNTRACKED" ]]; then
    pass "All SIL docs tracked in manifest"
else
    warn "Some docs not in manifest (may be intentional):"
    echo "$UNTRACKED" | while read -r file; do
        info "   • $file"
    done
fi

# ============================================================================
section "🔗 Step 3: Validate Links"
# ============================================================================

info "Checking for common link problems..."

# Check for broken internal links (simple check)
BROKEN_COUNT=0

# Check for links with unencoded spaces
SPACE_LINKS=$(grep -r "\[.*\](.*[[:space:]].*)" "$WEBSITE_ROOT/docs" --include="*.md" 2>/dev/null | wc -l || echo 0)
if [[ $SPACE_LINKS -eq 0 ]]; then
    pass "No links with unencoded spaces"
else
    warn "Found $SPACE_LINKS links with spaces (may need encoding)"
fi

# Check for common broken patterns
HASH_ONLY=$(grep -r "\[.*\](#)" "$WEBSITE_ROOT/docs" --include="*.md" 2>/dev/null | wc -l || echo 0)
if [[ $HASH_ONLY -eq 0 ]]; then
    pass "No empty anchor links"
else
    warn "Found $HASH_ONLY empty anchor links (#)"
fi

# Sample relative link check
info "Sampling relative links..."
SAMPLE_BROKEN=0
cd "$WEBSITE_ROOT/docs"
for file in $(find . -name "*.md" | head -10); do
    grep -o "\[.*\](\.\.*/[^)]*)" "$file" 2>/dev/null | while IFS= read -r match; do
        link=$(echo "$match" | sed 's/.*(\([^)]*\)).*/\1/')
        dir=$(dirname "$file")
        target="$dir/$link"
        if [[ ! -f "$target" && ! -d "$target" ]]; then
            ((SAMPLE_BROKEN++)) || true
        fi
    done
done

if [[ $SAMPLE_BROKEN -eq 0 ]]; then
    pass "Sample link check passed (10 files)"
else
    warn "Sample found $SAMPLE_BROKEN broken links"
    info "Run full validation if needed"
fi

# ============================================================================
section "📦 Step 4: Git Status"
# ============================================================================

cd "$WEBSITE_ROOT"

# Check for uncommitted changes
if [[ -z $(git status --porcelain) ]]; then
    pass "No uncommitted changes"
else
    warn "Uncommitted changes:"
    git status --short | head -5
    info "Consider committing before deploy"
fi

# Show current commit
CURRENT_COMMIT=$(git rev-parse --short HEAD)
CURRENT_BRANCH=$(git branch --show-current)
info "Current state:"
info "   • Branch: $CURRENT_BRANCH"
info "   • Commit: $CURRENT_COMMIT"
info "   • Message: $(git log -1 --pretty=%B | head -1)"

# ============================================================================
section "🌐 Step 5: Check Target Environment"
# ============================================================================

if [[ "$ENV" == "staging" ]]; then
    URL="https://sil-staging.mytia.net"
    CONTAINER="sil-website-staging"
    HOST="tia-staging"
elif [[ "$ENV" == "production" ]]; then
    URL="https://semanticinfrastructurelab.org"
    CONTAINER="sil-website"
    HOST="tia-apps"
else
    fail "Unknown environment: $ENV"
    exit 1
fi

info "Target: $URL"

# Check if reachable
if curl -s -f "$URL/health" > /dev/null 2>&1; then
    HEALTH=$(curl -s "$URL/health")
    SERVICE=$(echo "$HEALTH" | jq -r '.service' 2>/dev/null || echo "unknown")
    VERSION=$(echo "$HEALTH" | jq -r '.version' 2>/dev/null || echo "unknown")

    if [[ "$SERVICE" == "sil-website" ]]; then
        pass "Environment reachable and healthy"
        info "   • Service: $SERVICE"
        info "   • Version: $VERSION"
    else
        warn "Health check returned wrong service: $SERVICE"
    fi
else
    warn "Environment not reachable (may be in maintenance)"
fi

# Check container status
if ssh "$HOST" "podman ps --filter name=$CONTAINER --format '{{.Status}}'" 2>/dev/null | grep -q "Up"; then
    pass "Container running on $HOST"
else
    warn "Container not running on $HOST"
fi

# ============================================================================
section "🚦 Step 6: Check Nginx Maintenance Mode"
# ============================================================================

info "Checking if nginx on tia-proxy is in maintenance mode..."

# Determine domain based on environment
if [[ "$ENV" == "staging" ]]; then
    NGINX_DOMAIN="sil-staging.mytia.net"
elif [[ "$ENV" == "production" ]]; then
    NGINX_DOMAIN="semanticinfrastructurelab.org"
fi

# Check if nginx config serves maintenance page
if ssh tia-proxy "grep -q 'root /var/www/maintenance' /etc/nginx/sites-available/${NGINX_DOMAIN}" 2>/dev/null; then
    fail "Nginx is in MAINTENANCE MODE!"
    info "Nginx is serving static HTML instead of proxying to container"
    info "This will cause deployment to appear successful but site won't update"
    echo ""
    echo "Fix:"
    echo "  1. Find latest backup:"
    echo "     ssh tia-proxy 'ls -lt /etc/nginx/sites-available/${NGINX_DOMAIN}.backup-* | head -1'"
    echo ""
    echo "  2. Restore config:"
    echo "     ssh tia-proxy 'sudo cp /etc/nginx/sites-available/${NGINX_DOMAIN}.backup-TIMESTAMP /etc/nginx/sites-available/${NGINX_DOMAIN}'"
    echo ""
    echo "  3. Reload nginx:"
    echo "     ssh tia-proxy 'sudo nginx -t && sudo systemctl reload nginx'"
    echo ""
    echo "See DEPLOYMENT.md 'Maintenance Mode' section for details"
else
    pass "Nginx is in normal proxy mode (not maintenance)"
    info "Nginx will proxy to container on deployment"
fi

# ============================================================================
section "✅ Step 7: Deployment Checklist"
# ============================================================================

echo ""
echo -e "${BLUE}Before you deploy, confirm:${NC}"
echo ""
echo "  □ I know which files are public vs internal (Step 1)"
echo "  □ Sync validation passed (Step 2)"
echo "  □ Links look good (Step 3)"
echo "  □ Changes are committed (Step 4)"
echo "  □ Target environment is accessible (Step 5)"
echo "  □ Nginx is NOT in maintenance mode (Step 6)"
echo ""

# ============================================================================
section "📊 Summary"
# ============================================================================

echo ""
echo -e "Results:"
echo -e "  ${GREEN}✓ Passed:   $PASS${NC}"
echo -e "  ${RED}✗ Failed:   $FAIL${NC}"
echo -e "  ${YELLOW}⚠ Warnings: $WARN${NC}"
echo ""

if [[ $FAIL -eq 0 && $WARN -eq 0 ]]; then
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✓ READY TO DEPLOY                                       ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "Deploy command:"
    echo -e "${CYAN}  ./deploy/deploy-container.sh $ENV --fresh${NC}"
    echo ""
    exit 0
elif [[ $FAIL -eq 0 ]]; then
    echo -e "${YELLOW}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║  ⚠ READY WITH WARNINGS                                   ║${NC}"
    echo -e "${YELLOW}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Review warnings above. Deployment should be safe."
    echo ""
    echo -e "Deploy command:"
    echo -e "${CYAN}  ./deploy/deploy-container.sh $ENV --fresh${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ✗ NOT READY - FIX ISSUES FIRST                          ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Common fixes:"
    echo "  ./scripts/sync-docs.py              # Sync from SIL repo"
    echo "  ./scripts/sync-docs.py --validate   # Check sync status"
    echo "  git add . && git commit -m 'msg'    # Commit changes"
    echo ""
    exit 1
fi
