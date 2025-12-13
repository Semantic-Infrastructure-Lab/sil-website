#!/usr/bin/env python3
"""Test auto-discovery of markdown files for content service"""

import re
from pathlib import Path


def filename_to_slug(filename: str) -> str:
    """Convert filename to URL-friendly slug.

    Examples:
        RAG_AS_SEMANTIC_MANIFOLD_TRANSPORT.md -> rag-manifold-transport
        UNIFIED_ARCHITECTURE_GUIDE.md -> unified-architecture-guide
        layer-0-semantic-memory.md -> layer-0-semantic-memory
        README.md -> overview (special case for semantic-os)
    """
    # Remove .md extension
    name = filename.replace('.md', '')

    # Special case: README becomes 'overview'
    if name == 'README':
        return 'overview'

    # Remove common prefixes
    name = re.sub(r'^SIL_', '', name)

    # Convert to lowercase and replace underscores with hyphens
    slug = name.lower().replace('_', '-')

    return slug


def discover_docs(docs_path: Path, category: str) -> dict[str, str]:
    """Auto-discover all markdown files in a category.

    Returns:
        Dict mapping slug -> filename
    """
    category_path = docs_path / category

    if not category_path.exists():
        return {}

    slug_map = {}

    for md_file in category_path.glob('*.md'):
        filename = md_file.name
        slug = filename_to_slug(filename)
        slug_map[slug] = filename

    return slug_map


if __name__ == '__main__':
    # Test with actual docs
    docs_path = Path('/home/scottsen/src/projects/sil-website/docs')

    categories = ['canonical', 'architecture', 'research', 'guides', 'vision', 'meta', 'semantic-os']

    print("Auto-discovered slug mappings:\n")

    for category in categories:
        slugs = discover_docs(docs_path, category)

        if slugs:
            print(f"{category}:")
            for slug, filename in sorted(slugs.items()):
                print(f"  {slug:40} -> {filename}")
            print()
