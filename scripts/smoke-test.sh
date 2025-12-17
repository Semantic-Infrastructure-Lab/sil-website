#!/bin/bash
# SIL Website - Smoke Test Suite
# Tests critical pages after deployment to ensure site is working
#
# Usage:
#   ./smoke-test.sh [staging|production]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Parse environment
ENVIRONMENT="${1:-staging}"

# Determine base URL
if [[ "$ENVIRONMENT" == "production" ]]; then
    BASE_URL="https://semanticinfrastructurelab.org"
elif [[ "$ENVIRONMENT" == "staging" ]]; then
    BASE_URL="https://sil-staging.mytia.net"
else
    echo -e "${RED}ERROR: Invalid environment: $ENVIRONMENT${NC}"
    echo "Usage: $0 [staging|production]"
    exit 1
fi

echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║       SIL Website - Smoke Test Suite                    ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Environment: $ENVIRONMENT${NC}"
echo -e "${BLUE}Base URL: $BASE_URL${NC}"
echo ""

# Test counters
PASS=0
FAIL=0
TOTAL=0

# Critical pages to test
declare -A CRITICAL_PAGES=(
    ["/health"]="Health Check Endpoint"
    ["/"]="Homepage"
    ["/manifesto/YOLO"]="YOLO Manifesto"
    ["/foundations/FOUNDERS_LETTER"]="Founders Letter"
    ["/foundations/design-principles"]="Design Principles"
    ["/systems/beth"]="Beth System Documentation"
    ["/systems/reveal"]="Reveal System Documentation"
    ["/systems/tia"]="TIA System Documentation"
    ["/research"]="Research Index"
)

# Test a single page
test_page() {
    local path=$1
    local description=$2
    local url="${BASE_URL}${path}"

    ((TOTAL++))

    # Test HTTP status code
    local http_code=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
    local response_time=$(curl -s -o /dev/null -w "%{time_total}" "$url" 2>/dev/null)

    if [[ "$http_code" == "200" ]]; then
        echo -e "${GREEN}✓${NC} $description"
        echo -e "    ${BLUE}→${NC} $path (${http_code}, ${response_time}s)"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} $description"
        echo -e "    ${RED}→${NC} $path (HTTP $http_code)"
        ((FAIL++))
    fi
}

# Run tests
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}Running Smoke Tests${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

for path in "${!CRITICAL_PAGES[@]}"; do
    test_page "$path" "${CRITICAL_PAGES[$path]}"
done

# Summary
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}Test Results${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "Total Tests: $TOTAL"
echo -e "${GREEN}Passed: $PASS${NC}"
echo -e "${RED}Failed: $FAIL${NC}"
echo ""

# Exit status
if [[ $FAIL -eq 0 ]]; then
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✓ ALL SMOKE TESTS PASSED                               ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Deployment verified - all critical pages accessible${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ✗ SMOKE TESTS FAILED                                    ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${RED}Deployment verification failed - $FAIL critical page(s) not accessible${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check container logs: ssh $HOST 'podman logs sil-website'"
    echo "  2. Check health endpoint: curl $BASE_URL/health"
    echo "  3. Verify nginx config: ssh tia-proxy 'sudo nginx -t'"
    echo "  4. Check if in maintenance mode"
    echo ""
    exit 1
fi
