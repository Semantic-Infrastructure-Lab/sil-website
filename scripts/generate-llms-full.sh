#!/usr/bin/env python3
"""
Generate llms-full.txt from SIL documentation.

Manifest-driven: sources its file list from CONTENT_MANIFEST.yaml's
visibility: public entries (the same source of truth sync-docs.py uses),
instead of walking a hardcoded, drift-prone category list. A file only
appears here if it's also allowed onto the website itself.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SIL_REPO = PROJECT_ROOT.parent / "SIL"
MANIFEST_PATH = SIL_REPO / "docs" / "CONTENT_MANIFEST.yaml"
OUTPUT_FILE = PROJECT_ROOT / "static" / "llms-full.txt"

# Display order for categories; anything not listed here sorts after, alphabetically.
CATEGORY_ORDER = [
    "(root)",
    "foundations",
    "manifesto",
    "architecture",
    "systems",
    "research",
    "vision",
    "articles",
    "essays",
    "meta",
]


def load_public_files() -> dict[str, list[str]]:
    """Group public, non-removal-flagged manifest paths by top-level docs/ category."""
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())

    groups: dict[str, list[str]] = {}
    for item in manifest.get("files", []):
        path = item.get("path", "")
        if not path or item.get("visibility") != "public":
            continue
        if item.get("flagged_for_removal"):
            continue

        rel = path[len("docs/") :] if path.startswith("docs/") else path
        if Path(rel).name == "README.md":
            continue  # navigational index, not content

        parts = rel.split("/")
        category = parts[0] if len(parts) > 1 else "(root)"
        groups.setdefault(category, []).append(rel)

    for paths in groups.values():
        paths.sort()

    return groups


def ordered_categories(groups: dict[str, list[str]]) -> list[str]:
    known = [c for c in CATEGORY_ORDER if c in groups]
    unknown = sorted(c for c in groups if c not in CATEGORY_ORDER)
    return known + unknown


def main() -> int:
    if not SIL_REPO.exists():
        print(f"Error: SIL repository not found at {SIL_REPO}")
        return 1
    if not MANIFEST_PATH.exists():
        print(f"Error: CONTENT_MANIFEST.yaml not found at {MANIFEST_PATH}")
        return 1

    print("Generating llms-full.txt from SIL documentation (manifest-driven)...")
    print(f"SIL repo: {SIL_REPO}")
    print(f"Manifest: {MANIFEST_PATH}")
    print(f"Output: {OUTPUT_FILE}")

    groups = load_public_files()

    parts = [
        "# Semantic Infrastructure Lab - Complete Documentation\n"
        "# Generated for LLM consumption\n"
        "# Source: https://semanticinfrastructurelab.org\n"
        "# Staging: https://sil-staging.mytia.net\n"
        "\n"
        "This file contains the complete public-facing documentation for the "
        "Semantic Infrastructure Lab.\n"
        "\n"
        "---\n"
    ]

    total_docs = 0
    for category in ordered_categories(groups):
        rel_paths = groups[category]
        parts.append(
            f"\n# {'=' * 40}\n"
            f"# CATEGORY: {category.upper()}\n"
            f"# {'=' * 40}\n"
        )
        for rel in rel_paths:
            file_path = SIL_REPO / "docs" / rel
            if not file_path.exists():
                print(f"Warning: {rel} listed in manifest but missing on disk, skipping")
                continue

            filename = Path(rel).name
            print(f"Adding: {rel}")
            total_docs += 1

            parts.append(
                f"\n## Document: {filename}\n"
                f"## Path: /docs/{rel}\n"
                "\n"
                f"{file_path.read_text()}\n"
                "\n---\n"
            )

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    parts.append(
        f"\n# {'=' * 40}\n"
        "# END OF DOCUMENTATION\n"
        f"# {'=' * 40}\n"
        "\n"
        "For the latest version of this documentation, visit:\n"
        "- Production: https://semanticinfrastructurelab.org\n"
        "- Staging: https://sil-staging.mytia.net\n"
        "- GitHub: https://github.com/semantic-infrastructure-lab\n"
        "\n"
        f"Generated: {generated_at}\n"
    )

    OUTPUT_FILE.write_text("".join(parts))

    size_kb = OUTPUT_FILE.stat().st_size / 1024
    line_count = OUTPUT_FILE.read_text().count("\n")
    print()
    print("Generated llms-full.txt")
    print(f"   Documents: {total_docs}")
    print(f"   Size: {size_kb:.1f}K")
    print(f"   Lines: {line_count}")
    print(f"   Location: {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
