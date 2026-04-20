---
title: "Reveal - Universal Resource Explorer"
type: reference
beth_topics:
  - reveal
  - progressive-disclosure
  - uri-adapters
  - agent-help
  - code-analysis
  - sil-production
---

# Reveal - Universal Resource Explorer

**Status:** ✅ Production v0.81.0 | Available on [PyPI](https://pypi.org/project/reveal-cli/)

**Tagline:** A semantic query layer — one consistent syntax for asking questions about code, infrastructure, documentation, and data.

---

## Quick Start

**Install:**
```bash
pip install reveal-cli
```

**Use:**
```bash
reveal src/                    # Directory → tree view
reveal app.py                  # File → structure (imports, functions, classes)
reveal app.py load_config      # Element → exact function extraction
```

Zero configuration. Works immediately on any codebase, 190+ languages.

---

## The Problem

Developers and AI agents waste tokens reading entire files when they only need structure or a single function. Traditional tools force you to choose between "nothing" and "everything."

**The deeper problem:** There's no consistent way to query code, infrastructure, databases, and documentation. You learn `git blame`, `openssl s_client`, `mysql SHOW STATUS`, and `grep` as separate mental models that don't compose.

---

## The Solution: Progressive Disclosure + URI Architecture

### Progressive Disclosure

Three levels of detail — start broad, drill down as needed:

```bash
reveal src/              # ~100 tokens — directory tree
reveal app.py            # ~200-500 tokens — outline: imports, functions, classes
reveal app.py load_config  # ~50-300 tokens — exact code
```

**The key property:** This is architecturally enforced, not suggested. Reveal defaults you into efficient behavior. You cannot accidentally dump 7,000 tokens of raw code.

**Token reduction:** 10–150x vs reading files directly. The 10-150x claim is structurally guaranteed — structure output is always smaller than content output.

### URI Architecture: Everything Is a Resource

Most tools expose features as subcommands (`git log`, `git blame`). Reveal exposes *resources* as URIs:

```bash
reveal ast://src/?complexity>10&sort=-complexity
reveal calls://src/?target=validate_token&depth=3
reveal ssl://api.example.com
reveal mysql://prod/?type=replication
reveal markdown://docs/?aggregate=type
```

Same syntax. Same operators. Same output format. Whether querying code, certificates, databases, or docs — the mental model doesn't change. New capabilities drop in as new adapters without touching core code.

---

## Core Capabilities

### 1. Progressive Code Exploration (the day-to-day core)

```bash
reveal src/                              # What's in this directory?
reveal src/auth.py                       # What's in this file?
reveal src/auth.py validate_token        # What does this function do?
reveal 'ast://src/?complexity>10'        # Find complex functions
reveal 'ast://src/?decorator=*cache*'   # Find cached functions (wildcard)
reveal 'git://src/auth.py?type=blame&element=validate_token'  # Semantic blame
```

### 2. Cross-File Call Graph Analysis (`calls://`)

```bash
reveal 'calls://src/?target=validate_token'          # Who calls this function?
reveal 'calls://src/?target=validate_token&depth=3'  # Callers-of-callers (impact radius)
reveal 'calls://src/?callees=process_payment'        # What does this call?
reveal 'calls://src/?rank=callers&top=20'            # Most-coupled functions
reveal 'calls://src/?uncalled&type=function'         # Dead code candidates
reveal 'calls://src/?format=dot' | dot -Tsvg > callgraph.svg  # Visual graph
```

No IDE. No language server. No configuration. Call-graph analysis from the CLI.

### 3. Token-Budgeted Context Snapshots (`reveal pack`)

```bash
reveal pack src/ --budget 8000                        # Snapshot within token budget
reveal pack src/ --focus "authentication" --budget 6000  # Focus-matched snapshot
reveal pack src/ --since main --budget 8000           # PR review: changed files first
```

Gives AI agents the right code in the right order at the right size. Changed files are boosted to priority tier 0 (above entry points). Solves agents burning context on stub `__init__.py` files before reaching actual logic.

### 4. Automated PR Review (`reveal review`)

```bash
reveal review main..HEAD                  # Full review: diff + checks + hotspots + complexity delta
reveal review main..HEAD --select B,S     # Security and bugs only (fast)
reveal review main..HEAD --format json    # CI/automated processing
reveal review main..HEAD || exit 1        # CI gate
```

Composes structural diff, quality checks, hotspot detection, and complexity analysis under consistent exit codes. Every changed function carries `complexity_before`, `complexity_after`, and `complexity_delta`.

### 5. Unified Health Checks (`reveal health`)

```bash
reveal health                                                # Full: code + infra + certs
reveal health ./src ssl://api.example.com domain://example.com  # Mix and match
reveal health ./src --format json | jq '.overall_exit'       # Monitoring
```

Code quality + SSL certificates + MySQL replication + domain DNS — all in one invocation, all under unified exit codes and JSON output.

### 6. Codebase Dashboard

```bash
reveal overview .    # File count, language breakdown, quality score, git activity
reveal deps .        # Circular import chains, unused imports, top importers
reveal hotspots src/ # Worst files by combined complexity + violations
```

### 7. Composable Pipelines

```bash
# nginx config → extract all domains → check each SSL cert
reveal nginx.conf --extract domains | sed 's/^/ssl:\/\//' | reveal --stdin --check

# Structural diff between branches
reveal diff://git://main/.:git://HEAD/.

# Find circular imports
reveal 'imports://src/?circular'
```

### 8. Documentation as a Queryable Graph (`markdown://`)

```bash
reveal 'markdown://docs/?aggregate=type'             # Document type taxonomy
reveal 'markdown://docs/?beth_topics~=authentication'  # Find by topic
reveal 'markdown://docs/?link-graph'                 # Bidirectional link graph
reveal 'markdown://docs/?body-contains=retry&type=procedure'  # Full-text + metadata
```

### 9. Session Archaeology (`claude://`)

```bash
reveal claude://sessions/                          # List sessions
reveal claude://session/my-session-0316/files      # Files touched in a session
reveal 'claude://sessions/?search=validate_token'  # Search across sessions
```

AI work history as queryable structured data. Useful for auditing what a session actually changed.

---

## 23 URI Adapters

| Domain | Adapters |
|--------|----------|
| Code semantics | `ast://`, `calls://`, `imports://`, `diff://`, `python://` |
| Data systems | `mysql://`, `sqlite://`, `json://`, `xlsx://` |
| Infrastructure | `ssl://`, `nginx://`, `domain://`, `cpanel://`, `autossl://`, `letsencrypt://`, `env://` |
| Documents | `markdown://`, `stats://`, `git://` |
| Meta / self-referential | `help://`, `reveal://`, `claude://`, `demo://` |

Same query operators (`=`, `~=`, `>`, `!`, `..`, `*`) across all adapters. Filter expressions learned once, applied everywhere.

---

## Quality Rules (69 rules, 14 categories)

| Category | Code | What it finds |
|----------|------|---------------|
| Bugs | B | Bare excepts, invalid decorators, broken imports |
| Complexity | C | Cyclomatic complexity, function length, nesting depth |
| Duplicates | D | Duplicate code blocks |
| Errors | E | Line length, style violations |
| Frontmatter | F | Missing/invalid YAML front matter in markdown |
| Imports | I | Unused imports, circular dependencies, layer violations |
| Links | L | Broken markdown links, anchor mismatches |
| Maintainability | M | Long parameter lists, deep inheritance |
| Infrastructure | N | nginx config issues, SSL misconfig, security headers |
| Refactoring | R | Refactor candidates |
| Security | S | Insecure protocols, Docker :latest tags |
| Types | T | Type annotation issues |
| URLs | U | Insecure URL patterns |
| Validation | V | Adapter contract validation (reveal's own rules) |

```bash
reveal src/ --check              # All rules
reveal src/ --check --select B,S # Bugs + security only
reveal --rules                   # Full list with descriptions
reveal --explain B001            # Explain one rule
```

---

## Language Support

**190+ languages total:**
- 37 built-in analyzers (Python, JavaScript, TypeScript, Rust, Go, Ruby, Elixir, Bash, YAML, JSON, TOML, Markdown, Nginx, Dockerfile, GDScript, Jupyter, and more)
- 165 additional languages via Tree-sitter fallback (AST-accurate, not regex)

---

## MCP Server (`reveal-mcp`)

```bash
pip install reveal-mcp
```

Exposes all reveal capabilities as MCP tools for Claude Code, Cursor, and Windsurf. Five tools: `reveal_structure`, `reveal_element`, `reveal_query`, `reveal_pack`, `reveal_check`. Agents get progressive disclosure and call-graph analysis without subprocess overhead.

---

## Agent-Help System

Three-tier discovery designed for AI agents:

```bash
reveal --agent-help       # Tier 1: Strategic guide — decision trees, when to use what (~1,500 tokens)
reveal help://            # Tier 2: Dynamic self-documentation — never goes stale, auto-discovers adapters
reveal --agent-help-full  # Tier 3: Comprehensive offline reference (~12,000 tokens)
```

Also: `help://schemas/<adapter>` gives agents machine-readable JSON schemas for every adapter — enabling safe exploration without external documentation. This **self-describing infrastructure** property drops adoption friction to near zero.

---

## SIL Principles in Action

Reveal demonstrates SIL's core research pillar — **Progressive Disclosure**:

✅ **Clarity** — Structure is visible, not hidden
✅ **Simplicity** — Zero configuration; just works
✅ **Composability** — URI output pipes to the next query
✅ **Correctness** — Tree-sitter AST parsing, not regex
✅ **Verifiability** — Precise `filename:line` output (vim/git/grep compatible)
✅ **Self-describing** — `help://schemas/<adapter>` makes the tool introspectable without docs

**Layer in Semantic OS:** Layer 5 (Human Interfaces / SIM) — makes all semantic structure visible and navigable.

The same progressive disclosure pattern Reveal proves for code will extend to: Semantic graphs (Pantheon IR), Provenance chains (GenesisGraph), Multi-agent reasoning (Agent Ether), Domain schemas (Morphogen).

---

## Production Stats (v0.81.0)

| Metric | Value |
|--------|-------|
| Tests | 7,913 passing |
| Quality score | 99.8/100 |
| Coverage | 68% overall |
| CI platforms | Linux / macOS / Windows |
| Downloads/month | 3.1K (100% organic) |
| URI adapters | 23 |
| Quality rules | 69 across 14 categories |
| Languages | 80 (64 built-in + 16 Tree-sitter) |
| MCP tools | 6 (structure, element, query, pack, check, nav) |
| Subcommands | check, review, pack, health, hotspots, overview, deps |

---

## Related SIL Projects

- [**morphogen**](https://github.com/semantic-infrastructure-lab/morphogen) — Cross-domain deterministic computation
- [**tiacad**](https://github.com/semantic-infrastructure-lab/tiacad) — Declarative parametric CAD in YAML
- [**genesisgraph**](https://github.com/semantic-infrastructure-lab/genesisgraph) — Cryptographic provenance verification
- [**agent-help standard**](/research/agent-help-standard) — The standard Reveal validates

---

**GitHub:** https://github.com/Semantic-Infrastructure-Lab/reveal
**PyPI:** https://pypi.org/project/reveal-cli/
**Last Updated:** 2026-04-19 (v0.81.0)
