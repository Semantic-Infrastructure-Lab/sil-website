#!/bin/bash
# Link validation using Reveal - optimized for FastHTML routing

echo "#!/bin/bash" > validate-internal-links.sh
echo "# Validate SIL website internal links using Reveal" >> validate-internal-links.sh
echo "" >> validate-internal-links.sh
echo "cd \$(dirname \$0)" >> validate-internal-links.sh  
echo "find docs/ -name '*.md' -type f | while read file; do" >> validate-internal-links.sh
echo "  reveal \"\$file\" --links --link-type internal 2>/dev/null | grep 'BROKEN' && echo \"File: \$file\"" >> validate-internal-links.sh
echo "done" >> validate-internal-links.sh

chmod +x validate-internal-links.sh
echo "✅ Created validate-internal-links.sh script"
