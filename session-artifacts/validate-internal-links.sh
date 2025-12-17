#!/bin/bash
# Validate SIL website internal links using Reveal
# Usage: ./validate-internal-links.sh

cd $(dirname $0)

echo "🔍 Validating internal links with Reveal..."
echo ""

# Use Reveal with stdin for efficient multi-file processing
BROKEN_LINKS=$(find docs/ -name "*.md" | reveal --stdin --links --link-type internal 2>/dev/null | grep "BROKEN")

if [ -z "$BROKEN_LINKS" ]; then
  echo "✅ No broken internal links found!"
  exit 0
else
  echo "❌ Broken internal links detected:"
  echo "$BROKEN_LINKS"
  echo ""
  echo "Count: $(echo "$BROKEN_LINKS" | wc -l) broken links"
  exit 1
fi
