#!/usr/bin/env bash
# Generate llms-full.txt from SIL documentation
# Concatenates all public-facing documentation into a single file for LLM consumption

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SIL_REPO="${PROJECT_ROOT}/../SIL"
OUTPUT_FILE="${PROJECT_ROOT}/static/llms-full.txt"

# Check SIL repo exists
if [ ! -d "$SIL_REPO" ]; then
  echo "Error: SIL repository not found at $SIL_REPO"
  exit 1
fi

echo "Generating llms-full.txt from SIL documentation..."
echo "SIL repo: $SIL_REPO"
echo "Output: $OUTPUT_FILE"

# Start with header
cat > "$OUTPUT_FILE" << 'EOF'
# Semantic Infrastructure Lab - Complete Documentation
# Generated for LLM consumption
# Source: https://semanticinfrastructurelab.org
# Staging: https://sil-staging.mytia.net

This file contains the complete public-facing documentation for the Semantic Infrastructure Lab.

---

EOF

# Function to add a category
add_category() {
  local category=$1
  local category_path="$SIL_REPO/docs/$category"

  if [ ! -d "$category_path" ]; then
    echo "Warning: Category $category not found, skipping"
    return
  fi

  echo "" >> "$OUTPUT_FILE"
  echo "# ========================================" >> "$OUTPUT_FILE"
  echo "# CATEGORY: ${category^^}" >> "$OUTPUT_FILE"
  echo "# ========================================" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"

  # Find all markdown files, excluding README files
  find "$category_path" -name "*.md" ! -name "README.md" -type f | sort | while read -r file; do
    local filename=$(basename "$file")
    local relative_path="${file#$SIL_REPO/docs/}"

    echo "Adding: $relative_path"

    echo "" >> "$OUTPUT_FILE"
    echo "## Document: $filename" >> "$OUTPUT_FILE"
    echo "## Path: /docs/$relative_path" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"

    cat "$file" >> "$OUTPUT_FILE"

    echo "" >> "$OUTPUT_FILE"
    echo "---" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
  done
}

# Add categories in logical order
add_category "canonical"
add_category "architecture"
add_category "semantic-os"
add_category "research"
add_category "guides"
add_category "vision"
add_category "meta"

# Add footer
cat >> "$OUTPUT_FILE" << 'EOF'

# ========================================
# END OF DOCUMENTATION
# ========================================

For the latest version of this documentation, visit:
- Production: https://semanticinfrastructurelab.org
- Staging: https://sil-staging.mytia.net
- GitHub: https://github.com/semantic-infrastructure-lab

Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
EOF

# Get file stats
file_size=$(du -h "$OUTPUT_FILE" | cut -f1)
line_count=$(wc -l < "$OUTPUT_FILE")

echo ""
echo "✅ Generated llms-full.txt"
echo "   Size: $file_size"
echo "   Lines: $line_count"
echo "   Location: $OUTPUT_FILE"
