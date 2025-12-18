#!/usr/bin/env python3
"""
Add frontmatter to SIL website documents.

This script adds standardized YAML frontmatter to markdown files
that are missing it, using data from DOCUMENT_TIERS for tier/order.

Usage:
    python scripts/add-frontmatter.py --dry-run   # Preview changes
    python scripts/add-frontmatter.py --apply     # Apply changes
    python scripts/add-frontmatter.py --file docs/foo.md --apply  # Single file
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional, Tuple


# DOCUMENT_TIERS mapping (tier, order)
# Copied from src/sil_web/services/content.py
DOCUMENT_TIERS = {
    # Tier 1: Essential Documents (5 docs - the "1 hour" reading list)
    "start-here": (1, 1),
    "manifesto": (1, 2),
    "founders-letter": (1, 3),
    "principles": (1, 4),
    "glossary": (1, 5),
    "research-agenda-year1": (1, 6),

    # Tier 3: Deep Reference (only top 5 shown in sidebar)
    # Architecture & Governance
    "semantic-os-architecture": (3, 1),
    "stewardship-manifesto": (3, 2),
    "technical-charter": (3, 3),
    "design-principles": (3, 4),

    # Trust & Agency
    "trust-assertion-protocol": (3, 5),
    "authorization-protocol": (3, 6),
    "hierarchical-agency-framework": (3, 7),
    "safety-thresholds": (3, 8),

    # Research Papers
    "semantic-feedback-loops": (3, 9),
    "semantic-observability": (3, 10),
    "multi-agent-protocol-principles": (3, 11),
    "founders-note-multishot-agent-learning": (3, 12),

    # Implementation Guides
    "progressive-disclosure-guide": (3, 13),
    "reveal-beth-progressive-knowledge-system": (3, 14),
    "tool-quality-monitoring": (3, 15),
}


def filename_to_slug(filename: str) -> str:
    """Convert filename to slug (matches content.py logic)."""
    # Remove extension
    slug = filename.replace('.md', '')

    # Handle various filename patterns
    # SIL_TECHNICAL_CHARTER.md -> technical-charter
    # FOUNDERS_LETTER.md -> founders-letter
    # semantic-os-architecture.md -> semantic-os-architecture

    # Remove SIL_ prefix if present
    if slug.startswith('SIL_'):
        slug = slug[4:]

    # Convert to lowercase
    slug = slug.lower()

    # Replace underscores with hyphens
    slug = slug.replace('_', '-')

    return slug


def extract_title_from_content(content: str) -> Optional[str]:
    """Extract title from first H1 heading."""
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    return None


def get_tier_and_order(slug: str) -> Tuple[int, int]:
    """Get tier and order for a slug, with defaults."""
    return DOCUMENT_TIERS.get(slug, (3, 999))


def has_frontmatter(content: str) -> bool:
    """Check if content already has frontmatter."""
    return content.startswith('---')


def add_frontmatter_to_file(
    file_path: Path,
    dry_run: bool = True
) -> Tuple[bool, str]:
    """
    Add frontmatter to a markdown file.

    Returns:
        (changed, message): Whether file would be/was changed, and status message
    """
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return False, f"Error reading file: {e}"

    # Skip if already has frontmatter
    if has_frontmatter(content):
        return False, "Already has frontmatter"

    # Determine slug from filename
    slug = filename_to_slug(file_path.name)

    # Get tier and order
    tier, order = get_tier_and_order(slug)

    # Extract title from content or generate from filename
    title = extract_title_from_content(content)
    if not title:
        # Generate title from filename
        title = file_path.stem.replace('_', ' ').replace('-', ' ').title()

    # Determine category from directory
    # docs/foundations/foo.md -> category: foundations
    # docs/research/standards/bar.md -> category: research
    category_parts = file_path.parts
    if 'docs' in category_parts:
        docs_idx = category_parts.index('docs')
        if len(category_parts) > docs_idx + 1:
            category = category_parts[docs_idx + 1]
        else:
            category = 'root'
    else:
        category = 'unknown'

    # Build frontmatter
    frontmatter_lines = [
        '---',
        f'title: "{title}"',
        f'tier: {tier}',
        f'order: {order}',
        'private: false',
    ]

    # Add description placeholder for tier 1 docs
    if tier == 1:
        frontmatter_lines.append('description: "TODO: Add description"')

    frontmatter_lines.append('---')

    # Combine frontmatter with original content
    new_content = '\n'.join(frontmatter_lines) + '\n\n' + content

    # Apply or preview
    if not dry_run:
        try:
            file_path.write_text(new_content, encoding='utf-8')
            return True, f"✓ Added frontmatter (tier {tier}, order {order})"
        except Exception as e:
            return False, f"✗ Error writing file: {e}"
    else:
        return True, f"Would add frontmatter (tier {tier}, order {order}, title: {title})"


def process_directory(
    docs_path: Path,
    dry_run: bool = True,
    verbose: bool = True
) -> Tuple[int, int]:
    """
    Process all markdown files in docs directory.

    Returns:
        (changed_count, skipped_count)
    """
    changed = 0
    skipped = 0

    # Find all markdown files
    md_files = sorted(docs_path.rglob('*.md'))

    print(f"Found {len(md_files)} markdown files")
    print()

    for md_file in md_files:
        rel_path = md_file.relative_to(docs_path.parent)

        was_changed, message = add_frontmatter_to_file(md_file, dry_run=dry_run)

        if was_changed:
            changed += 1
            if verbose:
                print(f"{rel_path}: {message}")
        else:
            skipped += 1
            if verbose and not message.startswith("Already"):
                print(f"{rel_path}: {message}")

    return changed, skipped


def main():
    parser = argparse.ArgumentParser(
        description='Add frontmatter to SIL website markdown files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Apply changes to files'
    )
    parser.add_argument(
        '--file',
        type=Path,
        help='Process single file instead of all docs'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Only show summary, not individual files'
    )

    args = parser.parse_args()

    # Require --dry-run or --apply
    if not args.dry_run and not args.apply:
        parser.error("Must specify either --dry-run or --apply")

    dry_run = not args.apply
    verbose = not args.quiet

    # Determine docs path
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_path = project_root / 'docs'

    if not docs_path.exists():
        print(f"Error: docs directory not found at {docs_path}")
        sys.exit(1)

    # Process single file or all files
    if args.file:
        if not args.file.exists():
            print(f"Error: File not found: {args.file}")
            sys.exit(1)

        was_changed, message = add_frontmatter_to_file(args.file, dry_run=dry_run)
        print(f"{args.file}: {message}")
        sys.exit(0 if was_changed else 1)

    # Process all files
    print(f"{'DRY RUN' if dry_run else 'APPLYING CHANGES'}")
    print(f"Processing {docs_path}")
    print()

    changed, skipped = process_directory(docs_path, dry_run=dry_run, verbose=verbose)

    print()
    print("=" * 60)
    print(f"Summary:")
    print(f"  Files that would be/were changed: {changed}")
    print(f"  Files skipped (already have frontmatter): {skipped}")
    print(f"  Total files: {changed + skipped}")

    if dry_run and changed > 0:
        print()
        print("Run with --apply to make changes")


if __name__ == '__main__':
    main()
