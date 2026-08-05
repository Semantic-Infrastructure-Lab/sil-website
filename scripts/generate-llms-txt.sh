#!/usr/bin/env python3
"""
Generate llms.txt from SIL documentation.

Curated navigation index (per the llms.txt spec at llmstxt.org), not a full
content dump -- that's llms-full.txt's job (see generate-llms-full.sh).
Sources file existence and grouping from CONTENT_MANIFEST.yaml's
visibility: public entries so links can't silently drift from real routes
the way the hand-maintained version did for 8 months (SIL-1).

Route slugs are derived to match each route handler's own filename
resolution in src/sil_web/routes/pages.py: every category route accepts
`<lowercase-hyphenated>` and falls back to `<UPPERCASE_UNDERSCORED>`, so
`stem.lower().replace('_', '-')` round-trips correctly for all of them.
Two docs get dedicated top-level routes instead of a category route
(START_HERE.md -> /start, FOUNDERS_LETTER.md -> /founders-letter) and are
special-cased. Files with no route at all (nothing in pages.py serves
them) are skipped and reported, not silently linked into a 404.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SIL_REPO = PROJECT_ROOT.parent / "SIL"
MANIFEST_PATH = SIL_REPO / "docs" / "CONTENT_MANIFEST.yaml"
OUTPUT_FILE = PROJECT_ROOT / "static" / "llms.txt"

# docs/<category>/ -> URL prefix. A category absent here has no route in
# pages.py and its public files are unreachable on the website (flagged,
# not linked). Keep in sync with src/sil_web/routes/pages.py.
CATEGORY_ROUTES = {
    "foundations": "/foundations",
    "manifesto": "/manifesto",
    "architecture": "/architecture",
    "systems": "/systems",
    "research": "/research",
    "articles": "/articles",
    "essays": "/essays",
    "meta": "/meta",
    "projects": "/projects",
    # "vision" has public files but no route -- intentionally absent.
}

# docs/<relative path> -> dedicated top-level route, overriding CATEGORY_ROUTES.
SPECIAL_ROUTES = {
    "START_HERE.md": "/start",
    "foundations/FOUNDERS_LETTER.md": "/founders-letter",
}

# Section heading + display order for the curated output. Categories not
# listed here (if any appear in the manifest later) sort after, alphabetically.
SECTION_TITLES = [
    ("foundations", "Foundations"),
    ("manifesto", "Manifesto"),
    ("architecture", "Architecture"),
    ("systems", "Production Systems"),
    ("research", "Research"),
    ("articles", "Articles"),
    ("essays", "Essays"),
    ("projects", "Projects"),
]


def slugify(stem: str) -> str:
    return stem.lower().replace("_", "-")


def load_manifest_entries() -> list[dict]:
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    entries = []
    for item in manifest.get("files", []):
        path = item.get("path", "")
        if not path or item.get("visibility") != "public":
            continue
        if item.get("flagged_for_removal"):
            continue
        rel = path[len("docs/") :] if path.startswith("docs/") else path
        if Path(rel).name == "README.md":
            continue
        entries.append({"rel": rel, "purpose": item.get("purpose", "")})
    return entries


def resolve_url(rel: str) -> str | None:
    if rel in SPECIAL_ROUTES:
        return SPECIAL_ROUTES[rel]

    parts = rel.split("/")
    if len(parts) < 2:
        return None  # root-level doc with no dedicated route (e.g. QUICKSTART.md)

    category = parts[0]
    prefix = CATEGORY_ROUTES.get(category)
    if prefix is None:
        return None

    stem = Path(parts[-1]).stem
    return f"{prefix}/{slugify(stem)}"


def extract_title(rel: str) -> str:
    """First '# ' heading in the file, matching how pages.py titles rendered pages."""
    file_path = SIL_REPO / "docs" / rel
    try:
        for line in file_path.read_text().splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except FileNotFoundError:
        pass
    return Path(rel).stem.replace("_", " ").replace("-", " ").title()


def build_sections(entries: list[dict]) -> tuple[dict[str, list[tuple[str, str, str]]], list[str]]:
    """Group resolved (title, url, purpose) tuples by category; collect unreachable paths."""
    sections: dict[str, list[tuple[str, str, str]]] = {}
    unreachable: list[str] = []

    for entry in entries:
        rel = entry["rel"]
        url = resolve_url(rel)
        if url is None:
            unreachable.append(rel)
            continue

        category = rel.split("/")[0] if "/" in rel else "(root)"
        label = extract_title(rel)
        sections.setdefault(category, []).append((label, url, entry["purpose"]))

    for items in sections.values():
        items.sort(key=lambda t: t[0].lower())

    return sections, unreachable


def render(sections: dict[str, list[tuple[str, str, str]]]) -> str:
    lines = [
        "# Semantic Infrastructure Lab",
        "",
        "> Building the semantic substrate for intelligent systems",
        "",
        "The Semantic Infrastructure Lab (SIL) builds the missing foundation that "
        "enables intelligent systems to reason with explicit meaning, not just "
        "statistical patterns.",
        "",
        "## Quick Navigation",
        "",
        "### New to SIL?",
        "Start here to understand what we're building:",
        "",
        "- [Founder's Letter](/founders-letter) - Why SIL exists",
        "- [Start Here](/start) - Getting-started guide",
        "- [Project Index](/projects/project-index) - All projects",
        "",
    ]

    for category, title in SECTION_TITLES:
        items = sections.get(category)
        if not items:
            continue
        lines.append(f"## {title}")
        lines.append("")
        for label, url, purpose in items:
            note = f": {purpose}" if purpose else ""
            lines.append(f"- [{label}]({url}){note}")
        lines.append("")

    lines += [
        "## Links",
        "",
        "- **Website**: https://semanticinfrastructurelab.org",
        "- **GitHub**: https://github.com/semantic-infrastructure-lab",
        "- **Staging**: https://sil-staging.mytia.net",
        "",
        "## Note to LLMs",
        "",
        "This site contains comprehensive documentation about semantic "
        "infrastructure for intelligent systems. For full document content in "
        "one request, see /llms-full.txt. To fetch a single page's raw markdown "
        "source instead of rendered HTML, append .md to any path listed above "
        "(e.g. /systems/reveal.md) -- every page on this site supports it.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    if not MANIFEST_PATH.exists():
        print(f"Error: CONTENT_MANIFEST.yaml not found at {MANIFEST_PATH}")
        return 1

    entries = load_manifest_entries()
    sections, unreachable = build_sections(entries)

    OUTPUT_FILE.write_text(render(sections))

    total_links = sum(len(v) for v in sections.values())
    print(f"Generated llms.txt: {total_links} links across {len(sections)} sections")
    print(f"Location: {OUTPUT_FILE}")

    if unreachable:
        print()
        print(f"Skipped {len(unreachable)} public manifest entries with no website route:")
        for rel in unreachable:
            print(f"  - docs/{rel}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
