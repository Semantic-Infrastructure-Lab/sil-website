---
title: "Reveal: A Semantic Query Layer for Code, Infrastructure, and Docs"
subtitle: "Progressive disclosure, URI-based queries, and 23 adapters — what it actually does and why it matters"
author: "Scott Senkeresty"
date: "2026-04-19"
type: "article"
status: "published"
audience: "developers"
topics: ["reveal", "progressive-disclosure", "token-efficiency", "code-exploration", "semantic-stack", "uri-adapters", "call-graph", "ai-agents", "mcp", "imports", "git-blame", "structural-analysis"]
related_projects: ["reveal", "beth", "sil"]
related_docs:
  - "PROGRESSIVE_DISCLOSURE_GUIDE.md"
  - "REVEAL_BETH_PROGRESSIVE_KNOWLEDGE_SYSTEM.md"
  - "../systems/reveal.md"
canonical_url: "https://semanticinfrastructurelab.org/articles/reveal-introduction"
reading_time: "18 minutes"
beth_topics: [reveal, progressive-disclosure, token-efficiency, uri-adapters, call-graph, pack, code-review, agent-help, mcp-server, sil, imports, semantic-blame, structural-analysis, nav-flags, boundary, sideeffects]
session_provenance: "crackling-drought-0320"
version: "v0.81.0"
linkedin_posted: true
---

# Reveal: A Semantic Query Layer for Code, Infrastructure, and Docs

**Or: one consistent syntax for asking questions about everything in your project**

---

You know the moment. Claude needs to understand your auth module, so it reads `auth.py`. Then it reads `config.py` because auth imports it. Then `models.py`, `utils.py`, and three more files because who knows what's actually needed. By the time it gets to your question, it's burned 15,000 tokens just navigating the codebase.

This is the default. It doesn't have to be.

**Reveal** solves this with progressive disclosure — a structured query layer that gives you (and AI agents) exactly what you need without reading everything. But that's just where it starts. By the time we're done here, you'll have seen call-graph analysis, architectural layer enforcement, token-budgeted codebase snapshots, automated PR review, unified health checks spanning code and infrastructure, documentation as a queryable graph, and Excel workbooks parsed like databases.

Install it now if you want to follow along:

```bash
pip install reveal-cli
```

---

## Start Here: The Three-Level Drill-Down

Most tools give you two options: a directory listing (too little) or full file contents (too much). Reveal enforces three levels:

```bash
# Level 1: What's in this directory?
$ reveal src/
📁 src/ (12 files)
├── auth.py (342 lines, Python)
├── config.py (189 lines, Python)
├── models/
│   ├── user.py (156 lines, Python)
│   └── post.py (203 lines, Python)
└── ...
```

~100 tokens. You now know what exists. You don't need to read a single file.

```bash
# Level 2: What's in this file?
$ reveal src/auth.py
auth.py (342 lines, Python)
├── Imports (6)
├── Classes (1)
│   └── AuthManager (lines 18-287)
└── Functions (8)
    ├── validate_token (lines 291-318, complexity: 7)
    ├── refresh_token (lines 320-341, complexity: 4)
    └── ...
```

~250 tokens. You now know what functions exist, roughly how complex they are, and where they live. You still haven't read the file.

```bash
# Level 3: What does this function do?
$ reveal src/auth.py validate_token
src/auth.py:291-318
def validate_token(token: str, *, require_fresh: bool = False) -> AuthClaims:
    """Validate a JWT token and return decoded claims."""
    try:
        claims = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if require_fresh and not claims.get("fresh"):
            raise TokenNotFreshError("Token is not fresh")
        return AuthClaims(**claims)
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError(f"Token expired at {claims.get('exp')}")
    except jwt.InvalidTokenError as e:
        raise InvalidTokenError(str(e))
```

~150 tokens. Exact implementation, nothing else.

**Total: ~500 tokens.** Traditional approach (read all three relevant files): ~8,500 tokens. The 10–150x token reduction claim isn't marketing — it's structurally guaranteed by the architecture. Structure output is always smaller than content output.

But this is the easy part. The three-level drill-down is just the default interaction model. Here's what actually makes Reveal interesting.

---

## The URI Architecture: Everything Is a Resource

Most tools expose features as subcommands: `git log`, `git blame`, `docker ps`. You learn each command separately. Reveal takes a different approach — it exposes *resources* as URIs with query parameters.

```bash
reveal ast://src/?complexity>10&sort=-complexity
reveal calls://src/?target=validate_token&depth=3
reveal imports://src/?circular
reveal ssl://api.example.com
reveal mysql://prod/?type=replication
reveal markdown://docs/?aggregate=type
```

Same syntax. Same query operators (`=`, `~=`, `>`, `!`, `..`, `*`). Same output format. Whether you're querying code complexity, call graphs, import cycles, SSL certificates, database replication status, or documentation metadata — the mental model is identical.

This isn't an aesthetic choice. It's what makes everything composable. The output of `nginx://` feeds `ssl://`. The output of `diff://` feeds `ast://`. Infrastructure becomes queryable data that pipes into the next analysis.

23 adapters ship today. Let's look at the ones you'll actually use.

---

## Scenario 1: "What Calls This Function — and Who Wrote It?"

You're about to refactor `validate_token`. Before you touch it, you want to know: what else in this codebase depends on it? And once you've scoped the change, who actually understands this code?

### Impact radius with calls://

Reveal's `calls://` adapter walks each function's body at the AST level and builds an inverted call index, distinguishing call expressions from comments, strings, and variable names.

```bash
# Who calls validate_token — anywhere in the project?
reveal 'calls://src/?target=validate_token'

# What does validate_token call? (dependency surface)
reveal 'calls://src/?callees=validate_token'

# Callers of callers — two levels deep
reveal 'calls://src/?target=validate_token&depth=3'

# Most architecturally load-bearing functions in the whole project
reveal 'calls://src/?rank=callers&top=20'

# Dead code candidates — functions with no callers in the index
reveal 'calls://src/?uncalled&type=function'

# Visual call graph
reveal 'calls://src/?target=validate_token&format=dot' | dot -Tsvg > callgraph.svg
```

**Honest limitations worth knowing:** This is static analysis, not a language server. It works by name — if two functions share the same name across files, their callers are merged. Method calls written as `self.validate_token()` index under `self.validate_token`. Dynamic dispatch won't appear.

Where it reliably delivers: uniquely-named utility functions, `?rank=callers` coupling metrics (name collisions don't skew relative rankings much), and impact-radius checks before touching well-named functions.

The `?rank=callers` metric is the one I find most useful. It surfaces architecturally load-bearing functions before you know to look for them — not by searching for a specific name, but by asking the whole codebase what it depends on most.

### Ownership with semantic blame

Now the other question: before you refactor, who has the most context on this function?

Standard `git blame` attributes individual lines. Semantic blame understands the *element boundary* — it attributes lines within a function or class, tells you the primary author and contributors, and links directly to the relevant commits.

```bash
# Who owns validate_token — by function, not by line?
reveal 'git://src/auth.py?type=blame&element=validate_token'
```

```
Element Blame: src/auth.py → validate_token
Lines 291-318 (1 hunks)

Contributors (by lines owned):
  Jane Smith                   18 lines (64.3%)  Last: 2026-03-18 14:22:41
  John Doe                     10 lines (35.7%)  Last: 2025-07-14 09:05:12

Key hunks (largest continuous blocks):
  Lines 291-308 (18 lines)  def5678 2026-03-18 14:22:41 Jane Smith
    feat: harden token validation with expiry check
  Lines 309-318 (10 lines)  abc1234 2025-07-14 09:05:12 John Doe
    feat: initial JWT implementation

Use: reveal git://src/auth.py?type=blame&detail=full  for line-by-line view
```

```bash
# Who owns the AuthManager class?
reveal 'git://src/auth.py?type=blame&element=AuthManager'

# Class method attribution
reveal 'git://src/models.py?type=blame&element=User.save'
```

`?rank=callers` tells you what depends on a function. Semantic blame tells you who to talk to before changing it. Together they're the full picture for safe refactoring.

---

## Scenario 2: "Where Are the Structural Cracks?"

Bad architecture doesn't fail loudly. Circular dependencies accumulate over months. Layer violations creep in when a deadline is tight. By the time you notice, there are dozens of them. Reveal's `imports://` adapter makes this visible.

```bash
# Find circular dependency chains
reveal 'imports://src/?circular'
```

```
============================================================
Circular Dependencies: 3
============================================================

  1. src/models/user.py -> src/services/auth.py -> src/models/user.py
  2. src/api/routes.py -> src/handlers/users.py -> src/api/routes.py
  3. src/db/models.py -> src/db/session.py -> src/db/base.py -> src/db/models.py
```

```bash
# Imports that are declared but never used
reveal 'imports://src/?unused'

# Full import graph overview — who imports what across the project
reveal 'imports://src/'
```

These two commands — `?circular` and `?unused` — are a fast architectural health audit. Run them before a refactor. Run them in CI. Circular dependencies make testing fragile, cause module initialization failures, and are genuinely hard to find any other way.

Architecture layer enforcement (`?violations`) is on the roadmap — it will catch cases where your domain layer imports from infrastructure or your presentation layer bypasses the service layer, enforced against `.reveal.yaml` configuration.

---

## Scenario 3: "Give the AI Exactly the Right Codebase Context"

Here's a problem that comes up constantly when working with AI agents: how do you give Claude useful codebase context without burning its entire context window on boilerplate?

The naive approach is to read every file. The thoughtful approach is `reveal pack`:

```bash
# Fit the most important code in 8000 tokens
reveal pack src/ --budget 8000 --content
```

What this does: ranks files by priority (entry points first, then key modules, then recency), fills up to the budget, then emits each file's structure. The agent gets the right code in the right order at the right size.

Without `--content`, pack outputs a prioritized file list — useful for planning what to read, but not for feeding an agent directly.

But the really useful version is the PR-aware snapshot:

```bash
# Changed files first, then fill with key dependencies
reveal pack src/ --since main --budget 8000 --content
```

`--since main` boosts every file changed in the current branch above entry points, above everything. The remaining budget fills with the most important context. When you hand this to an AI agent for a PR review, it leads with what actually changed, not what's biggest.

Replace `main` with your default branch name if it differs (`master`, `develop`, etc.).

This is built for agents, not retrofitted. The token budget is a first-class parameter. The problem it solves — agents exhausting their context on stub `__init__.py` files before reaching the actual logic — is real and constant.

---

## Scenario 4: "Did This PR Make Anything Harder to Maintain?"

Most CI checks catch bugs. Very few catch *architectural decay* — the gradual accumulation of complexity that makes a codebase harder to work with over time.

### reveal review: the full PR picture

```bash
# Full PR review: structural diff + quality violations + hotspots + complexity delta
reveal review main..HEAD   # replace 'main' with your default branch name
```

Under the hood, `reveal review` composes four things:
1. **Structural diff** — what functions and classes were added, removed, or modified
2. **Quality checks** — 69 rules across bugs, security, complexity, and more
3. **Hotspot detection** — which files got worse
4. **Complexity delta** — before/after complexity on every changed function

That last one is the novel part. Every modified function carries `complexity_before`, `complexity_after`, and `complexity_delta` in the output. You can now ask: "did this PR make anything meaningfully more complex?"

```bash
# Find functions that got more complex in this PR
reveal diff://git://main/foo.py:git://HEAD/foo.py --format json | \
  jq '.diff.functions[] | select(.complexity_delta > 5)'

# CI gate: exit 0 clean, exit 1 warnings, exit 2 errors
reveal review main..HEAD || exit 1   # replace 'main' with your default branch name
```

### reveal check: surgical quality gates

When you don't need the full PR review, `reveal check` runs the quality rule engine directly against any file or directory:

```bash
reveal check src/                          # all 69 rules, full recursive scan
reveal check src/ --select B,S            # bugs and security only — fast CI gate
reveal check src/ --select I              # imports only (circular, unused)
reveal check src/ --severity high         # high and critical issues only
reveal check src/ --only-failures         # hide passing checks
reveal check --rules                      # list all 69 rules with descriptions
reveal check --explain C901              # explain the cyclomatic complexity rule
```

The rule categories span 14 domains: **B**ugs, **C**omplexity, **D**uplicates, **E**rrors, **F**rontmatter, **I**mports, **L**inks, **M**aintainability, i**N**frastructure (nginx), **R**efactoring, **S**ecurity, **T**ypes, **U**RLs, **V**alidation. Every check is a valid CI gate with no configuration.

```bash
# Drop this in a pre-commit hook
reveal check src/ --select B,S --only-failures || exit 1
```

---

## Scenario 5: "One Command for Code, Certs, DNS, and Database"

Most teams have three or four separate tools for infrastructure health: something for code quality, `openssl s_client` for certificates, a DNS checker, a MySQL monitoring query. None of them share output formats. None of them compose.

```bash
# Check everything at once
reveal health ./src ssl://api.example.com domain://example.com mysql://prod
```

One command. Code quality violations + SSL certificate expiry and chain validation + DNS health + MySQL replication status, all under unified exit codes and JSON output.

```bash
# JSON for monitoring pipelines
reveal health ./src --format json | jq '.overall_exit'

# CI gate
reveal health ./src && deploy.sh || alert_oncall.sh
```

### ssl:// — more than just expiry

```bash
reveal ssl://api.example.com
# → Status: ✅ HEALTHY (75 days until expiry), Chain Valid, Hostname Match

reveal ssl://api.example.com/san        # all Subject Alternative Names
reveal ssl://api.example.com/chain      # full certificate chain
reveal ssl://api.example.com/dates      # expiry details only
reveal ssl://api.example.com --check    # exit 0/1/2 for CI
```

### domain:// — full domain health in one shot

`domain://` is one of the most useful single-command tools in the suite. It combines DNS records, WHOIS, SSL status, email deliverability, and HTTP behavior under one adapter:

```bash
reveal domain://example.com
# → A records, MX configured, SSL ✅, registrar, expiry

reveal domain://example.com/mail
# → Status: ❌ FAILURE
# →   ✅ mx_records: MX configured (5 records)
# →   ❌ spf_record: No SPF record — domain is open to email spoofing
# →   ❌ dmarc_record: No DMARC — spoofed emails reach inboxes undetected

reveal domain://example.com/http
# → http://example.com → 301 → https://example.com → 200

reveal domain://example.com/ns-audit
# → All 2 NS servers agree — no stale/orphaned entries

reveal domain://example.com --check    # full health gate: DNS + SSL + email + HTTP
```

The `/mail` element alone — checking SPF and DMARC — catches email deliverability problems that are easy to miss and expensive to discover after the fact.

### nginx config file analysis

The nginx file analyzer works on any `.conf` file regardless of where nginx is running:

```bash
reveal /etc/nginx/conf.d/myapp.conf     # structure: servers, locations, SSL blocks
reveal check /etc/nginx/conf.d/myapp.conf     # N rules: missing headers, rate limiting, server_tokens, etc.
```

To batch-check SSL on every domain in a config file — the output of `--extract domains` already produces `ssl://`-prefixed URIs, ready to pipe:

```bash
reveal nginx.conf --extract domains | reveal --stdin --check
# → SSL Batch Check: 3 domains, 2 passed, 1 failed
```

The output of one adapter feeds the next. This is the composability the URI architecture enables.

---

## Scenario 6: "Our Docs Are a Graph, Not a Pile of Files"

If your project has significant documentation — architecture docs, guides, references, changelogs — `markdown://` turns it into a queryable graph.

```bash
# What document types exist across the knowledge base?
reveal 'markdown://docs/?aggregate=type'
# → guide: 23, reference: 18, architecture: 7, procedure: 12 ...

# Find all docs tagged with a topic
reveal 'markdown://docs/?beth_topics~=authentication'

# Full link graph — who links to what, how many backlinks each doc has
reveal 'markdown://docs/?link-graph'
# → 50 files | 264 edges | 2 isolated
# → ADAPTER_AUTHORING_GUIDE.md  (linked by 16)
# →   → AGENT_HELP.md
# →   → QUICK_START.md ...
# → Isolated (2 files with no links):
# →   REVIEW_VALIDATION_AND_IMPROVEMENTS.md
# →   UX_ISSUES.md

# Full-text search combined with structured metadata filtering
reveal 'markdown://docs/?body-contains=retry&type=procedure'
```

Bidirectional link graphs. Taxonomy frequency tables. Full-text search combined with frontmatter filtering. This is knowledge graph functionality in a code tool. For projects where the docs are first-class (not an afterthought), this changes how you maintain them.

---

## Scenario 7: "That Spreadsheet Is a Database"

`xlsx://` and `json://` extend Reveal's query model to data files — treating them as structured resources rather than opaque blobs.

### Excel workbooks

```bash
# What sheets exist and how big are they?
reveal report.xlsx
# → Sheets (3): Sales (1,234 rows × 8 cols), Summary (25 rows × 5 cols), Raw (500 rows × 12 cols)

# Extract a specific sheet
reveal 'xlsx://report.xlsx?sheet=Sales'

# Pull a specific cell range
reveal 'xlsx://report.xlsx?sheet=Sales&range=A1:E50'

# Export a sheet to CSV
reveal 'xlsx://report.xlsx?sheet=Sales&format=csv' > sales.csv

# Search across all sheets for a value
reveal 'xlsx://report.xlsx?search=Q4 2025'
```

Power Pivot workbooks (with embedded data models) are also supported — `reveal` will detect them automatically and expose the pivot tables, Power Query M code, and external data connections.

### JSON navigation

```bash
# Navigate to a nested key — no jq syntax needed
reveal json://config.json/database/host

# Type introspection
reveal json://api-response.json/users?type
# → Array[Object] (150 items)

# Flatten to grep-able lines (gron-style)
reveal json://config.json?flatten | grep database
# → config.database.host = "localhost"
# → config.database.port = 5432
# → config.database.name = "mydb"

# Filter an array
reveal 'json://users.json/users?status=active&sort=-created_at&limit=10'

# Schema inference on unknown JSON
reveal json://api-response.json?schema
```

Both adapters follow the same progressive disclosure model: start with structure, drill to content, filter to what you need.

---

## The Architecture Behind the Composability

These aren't independent features bolted together. They share a common architecture that makes them composable:

| Design choice | What it enables |
|---|---|
| URI-as-language | Same query syntax across all resources — code, infra, data, docs |
| Universal operators (`=`, `~=`, `>`, `!`, `..`, `*`) | Filter expressions transfer across adapters without learning new syntax |
| `--stdin` piping | Output of one adapter is input to the next |
| Structured JSON output | Every query composable with `jq`, scripts, and AI agents |
| Exit code discipline (0/1/2) | Every check is a valid CI gate with no configuration |
| Token budgeting | First-class LLM context constraint, not a workaround |
| `reveal://` self-reference | The tool introspects itself using its own syntax |

The self-reference property is worth dwelling on. `reveal help://schemas/ast` gives you a machine-readable JSON schema for the AST adapter. `reveal help://adapters` lists every adapter with syntax and examples. `reveal --agent-help` generates a condensed decision tree for AI agents encountering the tool for the first time.

This means agents can safely discover what Reveal offers and how to use it without external documentation. The tool documents itself. When you're building AI workflows, adoption friction drops to near zero.

---

## The MCP Server: Agents Get All of This Natively

```bash
pip install reveal-cli
```

`reveal-mcp` (included in `reveal-cli`) exposes all of Reveal's capabilities as MCP tools for Claude Code, Cursor, and Windsurf. Six tools: `reveal_structure`, `reveal_element`, `reveal_query`, `reveal_pack`, `reveal_check`, `reveal_nav`. Agents get progressive disclosure, call-graph analysis, quality checks, and deep function-level navigation without subprocess overhead.

`reveal_nav(path, element, flag)` is the sixth tool — the one that completes the four-level drill-down. It routes all nav flags to agents: `boundary` (function contract: inputs + environment + effects), `sideeffects` (classified outbound calls: db/http/cache/log/file/sleep/hard_stop), `returns` (exit paths with gate conditions), `ifmap`, `varflow`, `deps`, `mutations`, and more. Agents can answer "what does this function touch outside itself?" without ever reading source.

This is how the architecture of progressive disclosure becomes the default behavior for AI agents working on your codebase — not something they have to be instructed to do, but something built into how they access code.

---

## What Nobody Else Does

After using Reveal daily for months, here are capabilities I haven't found elsewhere in a CLI tool:

**Semantic blame by element** — `git://src/auth.py?type=blame&element=validate_token` answers "who owns this *function*?" Not who last touched line 47, but who wrote the 28-line function that lives at lines 291–318, with attribution percentages and direct commit links. Git blame has existed for decades. Semantic blame over a named element is new.

**`reveal health` spanning code + certs + DB + DNS** — a genuine category collapse. One command, one JSON blob, one exit code, four different infrastructure domains. The cross-domain unified exit code makes this work as a real CI gate.

**`complexity_delta` on every changed function** — `diff://` carries `complexity_before`, `complexity_after`, and `complexity_delta` for every modified function. Pipe to `jq` to gate on specific thresholds. "Did this PR make anything harder to maintain?" is now a scriptable CI check.

**`reveal pack --since <branch> --budget N`** — PR-aware codebase snapshots that boost changed files to priority tier 0. Built for AI agents; the token budget is a first-class parameter.

**`?decorator=*cache*` wildcard matching** — finds all functions decorated with `@lru_cache`, `@cached_property`, `@cache`, or any pattern, without knowing exact decorator names. `reveal 'ast://src/?decorator=*retry*'` surfaces every retry-decorated function in the codebase.

**`markdown://docs/?link-graph`** — bidirectional documentation link analysis with orphan detection. Rare in any tool category.

**`claude://sessions/` session archaeology** — AI work history as queryable structured data. Find every file a session touched, search across sessions for references to a function, reconstruct the context of a decision made three weeks ago.

**`--boundary`: complete function contract in one shot** — `reveal app.py process_order --boundary` emits three sections: INPUTS (variables flowing in), ENVIRONMENT (env reads, PHP superglobals), EFFECTS (all outbound calls classified by category: db/http/cache/log/file/sleep/hard_stop). No other CLI tool answers "what does this function touch outside itself?" as a structured, classified output. `--sideeffects` gives the effects layer alone; `--returns` shows every exit path with its gate conditions. These work on Python and PHP.

**Self-describing infrastructure** — `help://schemas/<adapter>` returns machine-readable JSON schemas for every adapter. `reveal --agent-help` generates a decision-tree reference for agents. Agents can discover and use the full API without external documentation.

---

## The 23 Adapters

| Domain | Adapters |
|--------|----------|
| Code semantics | `ast://`, `calls://`, `imports://`, `diff://`, `python://` |
| Data systems | `mysql://`, `sqlite://`, `json://`, `xlsx://` |
| Infrastructure | `ssl://`, `nginx://`, `domain://`, `cpanel://`, `autossl://`, `letsencrypt://`, `env://` |
| Documents | `markdown://`, `stats://`, `git://` |
| Meta / self-referential | `help://`, `reveal://`, `claude://` |

80 languages: 64 built-in analyzers plus 16 via Tree-sitter fallback. 69 quality rules across 14 categories. Zero configuration required.

---

## The Day-to-Day Patterns You'll Actually Use

The scenarios above are the highlights. In practice, these are the patterns you'll run dozens of times a day:

```bash
# Orient on an unfamiliar codebase
reveal .                                # directory structure
reveal src/                             # drill into source
reveal src/main.py                      # file outline
reveal src/main.py create_app           # extract one function

# Find things without reading files
reveal 'ast://src/?name=*auth*'         # anything with "auth" in the name
reveal 'ast://src/?complexity>10'       # functions that need attention
reveal 'ast://src/?decorator=*cache*'   # cached functions
reveal 'ast://src/?decorator=*retry*'   # retry-decorated functions

# Understand architectural coupling
reveal 'calls://src/?rank=callers&top=20'       # what holds everything together
reveal 'calls://src/?target=fn_name'            # impact radius before refactoring
reveal 'imports://src/?circular'                # circular dependency chains
reveal 'imports://src/?unused'                  # dead imports before a cleanup
reveal 'imports://src/?violations'              # architecture layer violations (roadmap)

# Code ownership and history
reveal 'git://src/auth.py?type=blame&element=validate_token'   # who owns this function?
reveal 'git://src/auth.py?type=blame&element=AuthManager'      # who owns this class?

# Orient an AI agent
reveal overview .                       # codebase dashboard in one output
reveal deps .                           # dependency health
reveal hotspots src/                    # worst files by combined metrics
reveal pack src/ --since main --budget 8000 --content   # PR context for agent

# Infrastructure health
reveal ssl://yourdomain.com             # certificate status + expiry
reveal ssl://yourdomain.com/san         # Subject Alternative Names
reveal domain://yourdomain.com          # DNS + SSL + WHOIS combined
reveal domain://yourdomain.com/mail     # SPF + DMARC deliverability check
reveal domain://yourdomain.com/http     # HTTP→HTTPS redirect chain
reveal /etc/nginx/conf.d/app.conf       # nginx config structure
reveal /etc/nginx/conf.d/app.conf --check  # nginx rule violations
reveal nginx.conf --extract domains | reveal --stdin --check   # batch SSL from nginx
reveal health ./src ssl://api.example.com    # combined code + SSL gate
reveal env://                           # runtime environment snapshot
reveal env://DATABASE_URL               # specific env variable lookup

# Data inspection
reveal report.xlsx                      # workbook structure
reveal json://config.json?flatten       # gron-style JSON for grepping

# Before/after a PR
reveal review main..HEAD                # full review with complexity delta (replace 'main' with your branch)
reveal check src/ --select B,S         # fast: bugs + security only
reveal check src/ --select I           # import health: circular, unused
```

---

## Try It

```bash
pip install reveal-cli
cd ~/your-project
reveal .
```

Pick any file that looks interesting. Run `reveal file.py`. See the outline in ~200 tokens instead of reading 5,000.

Then extract one function: `reveal file.py function_name`.

Then ask a structural question: `reveal 'ast://src/?complexity>10'`.

Then find the architectural load-bearing functions: `reveal 'calls://src/?rank=callers&top=20'`.

Then check for structural cracks: `reveal 'imports://src/?circular'`.

Then — if you have a team — ask who owns the most critical code: `reveal 'git://src/core.py?type=blame&element=MainClass'`.

Then go one level deeper into any function: `reveal file.py function_name --boundary`.

---

## Why This Exists

Reveal is the first production system from the **Semantic Infrastructure Lab** — a research project building the foundations for AI-native tooling. The core thesis: AI agents need infrastructure that meets them where they are, not human tools retrofitted for automated use.

Progressive disclosure is one piece of that. The same pattern that makes Reveal efficient for code will extend to semantic graphs, provenance chains, and multi-agent reasoning systems. But that's the longer story. This is the part that ships today, works immediately on your codebase, and makes your AI agent workflows measurably better.

**GitHub:** [Semantic-Infrastructure-Lab/reveal](https://github.com/Semantic-Infrastructure-Lab/reveal)
**PyPI:** [reveal-cli](https://pypi.org/project/reveal-cli/)
**MCP Server:** `reveal-mcp` command included in `pip install reveal-cli`

---

*Reveal v0.81.0 — 7,913 tests, 23 URI adapters, 69 quality rules, 80 languages. MIT license.*
