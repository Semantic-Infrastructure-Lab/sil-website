#!/usr/bin/env bash
# Auto-deploy documentation updates
# Single script that does EVERYTHING needed when SIL docs change

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 SIL Auto-Deploy Documentation"
echo "=================================="
echo ""

# Step 1: Sync docs from SIL repo
echo "📋 Step 1: Syncing documentation from SIL repo..."
"$SCRIPT_DIR/sync-docs.sh"
echo ""

# Step 2: Regenerate llms-full.txt
echo "🤖 Step 2: Regenerating llms-full.txt for LLMs..."
"$SCRIPT_DIR/generate-llms-full.sh"
echo ""

# Step 3: Git status check
echo "📊 Step 3: Checking what changed..."
cd "$PROJECT_ROOT"
if git diff --quiet docs/ static/llms-full.txt 2>/dev/null; then
  echo "✅ No documentation changes detected"
  echo ""
  echo "Nothing to deploy!"
  exit 0
fi

echo ""
echo "📝 Changes detected:"
git status --short docs/ static/llms-full.txt 2>/dev/null || true
echo ""

# Step 4: Ask if user wants to commit
read -p "Commit and deploy these changes? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Aborted by user"
  exit 1
fi

# Step 5: Commit changes
echo "💾 Step 4: Committing changes..."
git add docs/ static/llms-full.txt

# Generate commit message
COMMIT_MSG="docs: sync from SIL repo + regenerate llms-full.txt

Auto-synced documentation changes from SIL repository.

$(git diff --cached --stat docs/ static/llms-full.txt 2>/dev/null || echo 'Changes detected')"

git commit -m "$COMMIT_MSG"
echo ""

# Step 6: Deploy to staging
echo "🚢 Step 5: Deploying to staging..."
read -p "Deploy to staging now? (Y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Nn]$ ]]; then
  echo "✅ Changes committed but not deployed"
  echo ""
  echo "To deploy later, run:"
  echo "  ./deploy/deploy-container.sh staging"
  exit 0
fi

"$PROJECT_ROOT/deploy/deploy-container.sh" staging

echo ""
echo "✅ Complete!"
echo ""
echo "Staging site: https://sil-staging.mytia.net"
echo "Verify llms.txt: https://sil-staging.mytia.net/llms.txt"
