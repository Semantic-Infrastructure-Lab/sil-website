---
title: "Reveal - Semantic Code Explorer"
type: reference
status: current
version: "0.64.0"
last_updated: "2026-03-18"
beth_topics:
  - reveal
  - progressive-disclosure
  - code-analysis
  - token-efficiency
  - ai-agent
  - ast-adapter
  - calls-adapter
  - infrastructure
  - semantic-infrastructure
---

# Reveal — Semantic Code Explorer

**Tagline:** Progressive disclosure for codebases, databases, and infrastructure.

**Status:** ✅ Production v0.64.0 | [PyPI](https://pypi.org/project/reveal-cli/) | 8.8K total downloads, 3.1K/month

Point Reveal at a directory, file, function, or URI — get exactly what you need, nothing more.

---

## Quick Start

```bash
pip install reveal-cli

reveal src/                    # Directory → tree view
reveal app.py                  # File → structure
reveal app.py load_config      # Element → extraction
```

That's it. No flags, no configuration, just works.

---

## The Problem

AI agents and developers waste tokens reading entire files to understand structure or find specific functions.

**The trap:**
```bash
# Instead of reading 7,500 tokens to find one function:
cat auth.py

# Reveal shows structure in ~100 tokens:
reveal auth.py
# → Functions (8), where each one is, complexity hints, breadcrumbs for next step

# Then extract only what you need (~50 tokens):
reveal auth.py validate_token
```

**Total: 150 tokens instead of 7,500. Same understanding.**

---

## Progressive Disclosure: Three Tiers

Reveal is built on one principle: start broad, drill down, never read more than you need.

### Tier 1: Directory Structure
```bash
$ reveal src/
📁 src/
├── app.py (247 lines, Python)
├── database.py (189 lines, Python)
└── models/
    ├── user.py (156 lines, Python)
    └── post.py (203 lines, Python)
```

### Tier 2: File Structure
```bash
$ reveal app.py
app.py (247 lines, Python)
├── Imports (5)
├── Classes (2)
│   ├── Config (lines 15–34)
│   └── Application (lines 36–198)
└── Functions (6)
    ├── load_config (lines 201–215)
    └── ...

Next: reveal app.py <element>   # Extract specific function
      reveal app.py --check     # Quality check
```

### Tier 3: Element Extraction
```bash
$ reveal app.py load_config
app.py:201-215
def load_config(config_path: str) -> Config:
    """Load configuration from YAML file."""
    with open(config_path) as f:
        data = yaml.safe_load(f)
    return Config(**data)
```

**Every output includes breadcrumbs** — suggested next commands. Agents learn the workflow naturally.

---

## Language Support

**37 built-in analyzers** (full AST-based support):

Python, JavaScript, TypeScript, TSX, Ruby, Go, Rust, Elixir, Bash/Shell, Dockerfile, Nginx, YAML, JSON, TOML, JSONL, Markdown, CSV, XML, Jupyter notebooks (.ipynb), GDScript, SQL, PHP, Java, C, C++, Kotlin

**80+ additional languages** via Tree-sitter fallback (structure extraction without full analysis).

---

## URI Adapters

Reveal's URI protocol extends progressive disclosure beyond source files. Every adapter follows the same query syntax and breadcrumb conventions.

### Code Analysis

| Adapter | Purpose | Example |
|---------|---------|---------|
| `ast://` | Query code structure — functions, classes, complexity | `reveal 'ast://src?complexity>10'` |
| `calls://` | Cross-file call graph — who calls what across the project | `reveal 'calls://src?target=validate_item'` |
| `imports://` | Circular dependency detection, layer violations | `reveal 'imports://src?violations'` |
| `diff://` | Structural diff between commits, branches, or files | `reveal 'diff://main..feature'` |

### Data & Documents

| Adapter | Purpose | Example |
|---------|---------|---------|
| `json://` | Navigate JSON like a URL path | `reveal json://config.json/database/host` |
| `markdown://` | Query docs by frontmatter, find links, aggregate fields | `reveal 'markdown://docs?type=guide'` |
| `xlsx://` | Spreadsheet inspection | `reveal data.xlsx` |

### Infrastructure

| Adapter | Purpose | Example |
|---------|---------|---------|
| `ssl://` | Certificate inspection and expiry monitoring | `reveal ssl://example.com` |
| `domain://` | DNS, registration, HTTP health — all in one | `reveal domain://example.com` |
| `nginx://` | Vhost routing, ACLs, ACME chains, security audit | `reveal nginx://example.com` |
| `cpanel://` | Full cPanel user environment audit (SSL, ACLs, nginx) | `reveal cpanel://USERNAME/full-audit` |
| `autossl://` | cPanel AutoSSL run logs — per-domain TLS outcomes, DCV failures | `reveal autossl://` |

### Runtime & Storage

| Adapter | Purpose | Example |
|---------|---------|---------|
| `python://` | Python environment — packages, venv, bytecode, shadows | `reveal python://debug/bytecode` |
| `env://` | Environment variable inspection | `reveal env://PATH` |
| `mysql://` | Schema inspection, table structure, health | `reveal mysql://localhost/mydb` |
| `sqlite://` | Schema inspection | `reveal mydb.sqlite` |
| `stats://` | Codebase metrics — LOC, complexity, coverage | `reveal stats://src` |

### Meta & History

| Adapter | Purpose | Example |
|---------|---------|---------|
| `git://` | Commit history, blame, file history | `reveal 'git://src?type=history'` |
| `claude://` | Search and navigate Claude Code sessions | `reveal 'claude://?search=auth bug'` |

---

## Subcommands

Reveal's subcommands are high-level workflow tools built on top of the adapter system.

### `reveal check` — Quality Checks

Run the full quality rules system against any path:

```bash
reveal check src/             # All rules
reveal check src/ --select B,S  # Bugs + security only
reveal check src/ --format json | jq '.violations'
```

### `reveal review` — PR Review Workflow

One command replaces: `git diff + quality check + hotspot scan`. CI-ready.

```bash
reveal review .                    # Review working directory
reveal review main..feature        # Review branch vs main
reveal review HEAD~3..HEAD         # Last 3 commits
reveal review . --format json      # Machine-readable for CI gating
```

Exit codes: `0` = clean, `1` = warnings, `2` = errors. Pipe to CI:
```bash
# Gate PR merge on no errors
reveal review main..HEAD --format json \
  | jq '.overall_status == "pass"'
```

### `reveal health` — Unified Health Check

Health monitoring with consistent exit codes for any target type:

```bash
reveal health ssl://example.com    # Certificate health
reveal health domain://example.com # DNS + HTTP + SSL
reveal health mysql://localhost    # Database connectivity + schema
reveal health .                    # Project quality health
```

Exit codes: `0` = healthy, `1` = warnings, `2` = failures. Works in monitoring scripts.

### `reveal pack` — Token-Budgeted Context Snapshot

Curates the right files to fit within a token budget — designed for giving AI agents context without overloading their window.

```bash
reveal pack .                              # Default 4000-token budget
reveal pack . --budget 10000              # Larger budget
reveal pack . --focus authentication      # Boost auth-related files
reveal pack ./src --budget 8000 --verbose # Show per-file token counts
reveal pack . --format json | jq '.selected[].relative'  # For agents
```

Priority algorithm: entry points → focus-matching files → key directories (`core/`, `api/`, `models/`) → recently modified files.

### `reveal hotspots` — Complexity Analysis

Find the highest-complexity files and functions in one pass:

```bash
reveal hotspots src/               # File-level quality scores + complex functions
reveal hotspots src/ --top 20      # Top 20 hotspots
reveal hotspots src/ --functions-only  # Complex functions only
reveal hotspots src/ --format json # CI integration (exit 1 on quality < 70)
```

### `reveal dev` — Scaffolding

Extend Reveal with custom adapters, analyzers, and rules:

```bash
reveal dev new-adapter mydb --uri mydb        # Scaffold a new URI adapter
reveal dev new-analyzer toml --ext .toml      # Scaffold a new file analyzer
reveal dev new-rule M999 "Too Long" --cat maintainability
reveal dev inspect-config                     # See effective .reveal.yaml
```

---

## Quality Rules System

69 rules across 14 categories, run via `reveal check` or `reveal review`:

| Category | Code | Examples |
|----------|------|---------|
| Bugs | B | Bare `except`, silent exception swallowing, stale bytecode |
| Complexity | C | Cyclomatic complexity thresholds, deep nesting |
| Duplicates | D | Copy-paste detection across files |
| Error Handling | E | Missing error context, swallowed exceptions |
| Frontmatter | F | Missing required fields, invalid values in YAML front matter |
| Imports | I | Circular deps, unused imports, inline imports (I006), layer violations |
| Links | L | Broken links, missing anchors, relative path issues |
| Maintainability | M | Long files, complex modules, readability issues |
| Nginx | N | Duplicate upstreams, missing headers, TLS issues |
| Refactoring | R | Long functions, too many parameters |
| Security | S | Hardcoded secrets, insecure protocols, Docker `:latest` |
| Types | T | Missing type annotations, incorrect type usage |
| URLs | U | Broken links in docs and code |
| Validation | V | Config schema violations, adapter contract conformance |

```bash
reveal check src/ --select B,S,I     # Bugs, security, import issues
reveal --rules                         # List all available rules
reveal --explain B006                  # Explain specific rule with examples
```

---

## Configuration: `.reveal.yaml`

Reveal supports project-level configuration for architecture rules, custom patterns, and team standards. Zero config needed to start — the file is optional.

```yaml
# .reveal.yaml — version-controlled, team-shared
architecture:
  layers:
    - name: routes
      path: app/routes/**
      cannot_import: [repositories/**]   # Enforce clean architecture

semantic:
  custom_patterns:
    - name: uses_stripe_api
      description: "Track payment code"
      patterns: ["stripe\\..*\\("]

quality:
  complexity_threshold: 15              # Override default (10)
  select: [B, S, C, I]                 # Only run these categories
```

Inspect the effective config: `reveal dev inspect-config`

**Configuration as semantic contract:** Architecture rules in `.reveal.yaml` don't just lint — they declare what your code *means* in your system. Layer rules encode architectural decisions. Custom patterns codify domain knowledge.

---

## Agent-Help System

Reveal is its own best documentation. Every adapter and subcommand documents itself:

```bash
reveal help://                 # What can I do? (~50 tokens)
reveal help://ast              # AST adapter reference (~200 tokens)
reveal help://calls            # Call graph reference
reveal help://quick-start      # Getting started (~300 tokens)
reveal help://recipes          # Common workflows (~500 tokens)
reveal --agent-help            # Strategic guide for AI agents (~1,500 tokens)
```

**The three-tier progressive discovery model:**
- `--agent-help` — teaches strategy and discovery once (~1,500 tokens)
- `help://` — per-topic docs on demand (50–500 tokens each)
- `AGENT_HELP.md` (via `--agent-help-full`) — complete reference (~12K tokens, offline)

Help content auto-discovers from the adapter registry — never goes stale when adapters are added.

---

## SIL Principles in Action

Reveal demonstrates core SIL design principles:

✅ **Progressive Disclosure** — structure before content, always
✅ **Clarity** — structure visible without reading it
✅ **Composability** — pipes naturally with grep, jq, git, CI tools
✅ **Correctness** — AST-based parsing, not regex
✅ **Verifiability** — `filename:line` format works with vim, git, grep
✅ **Self-Documentation** — tools teach agents how to use them via `help://`

**Layer in Semantic OS:** Layers 1–3 (Semantics, Types, Composition) — extracts semantic meaning from code without executing it.

---

## Economic Impact

**Token efficiency at scale (full structural scan of 50-file codebase):**

| Approach | Tokens | Cost (Claude Opus) |
|----------|--------|-------------------|
| Traditional (`cat` all files) | 375,000 | ~$0.75 |
| With Reveal | 7,500 | ~$0.015 |
| **Savings** | **50x reduction** | **$0.74 per review** |

Measured on reveal's own codebase (v0.64.x): **3.9–33x** depending on task.
Typical for file inspection and call graph queries: **3.9–15x**.
Peak for targeted queries (dead code scan, caller lookup): **15–33x**.
See [BENCHMARKS.md](https://github.com/Semantic-Infrastructure-Lab/reveal/blob/main/docs/BENCHMARKS.md) for reproducible measurements.

---

## Get Started

```bash
pip install reveal-cli

reveal --version               # Verify install
reveal .                       # Explore current directory
reveal help://                 # Self-guided tour
reveal --agent-help            # If you're an AI agent
```

Full documentation:
- `reveal help://` — built-in, always current
- [AGENT_HELP.md](https://github.com/Semantic-Infrastructure-Lab/reveal/blob/main/docs/AGENT_HELP.md) — complete agent reference
- [RECIPES.md](https://github.com/Semantic-Infrastructure-Lab/reveal/blob/main/docs/RECIPES.md) — workflows and patterns

---

## Related SIL Projects

- [**Beth**](/systems/beth) — Semantic search and knowledge graphs; pairs with Reveal for full progressive knowledge disclosure
- [**TIA**](/systems/tia) — The Intelligent Agent; uses Reveal as its primary code exploration tool
- [**Pantheon**](/systems/pantheon) — Unified semantic IR connecting all SIL tools

---

*Last updated: 2026-03-18 (v0.64.0)*
