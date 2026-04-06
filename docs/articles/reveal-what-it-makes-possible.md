---
title: "From 15 Files to 500: What Reveal Makes Possible for AI Agents"
subtitle: "Progressive disclosure isn't an efficiency trick. It's a capability unlock."
author: "Scott Senkeresty"
date: "2026-03-18"
type: "article"
status: "published"
linkedin_posted: false
audience: "developers, ai-agent-builders"
beth_topics:
  - reveal
  - progressive-disclosure
  - token-efficiency
  - ai-agent
  - calls-adapter
  - mcp
  - agentic-ai
related_docs:
  - "reveal-call-graphs.md"
  - "reveal-pack-and-review.md"
  - "reveal-surprising-recipes.md"
  - "systems/reveal.md"
---

# From 15 Files to 500: What Reveal Makes Possible for AI Agents

---

There's a ceiling on what AI agents can do with your codebase. It's not the model. It's the context window — and how fast you burn through it.

A 100K-token context window sounds enormous. But if your agent reads files with `cat`, it's gone in 15 files. A moderately large Python module is 5,000–8,000 tokens of raw text. A full auth stack? Burned before the agent even starts reasoning.

**Reveal removes that ceiling.**

With progressive disclosure, an agent holds structural understanding of 500+ files in the same context window it used to fit 15. Not by compressing or summarizing — by only reading what the task actually requires.

That's the difference between an agent that can help with isolated bugs and one that can reason about your entire authentication system.

---

## The Problem Is Architectural

AI agents are trained to read. When you ask "fix the auth bug," the agent reaches for the files:

```
auth.py          → 3,200 tokens
config.py        → 1,800 tokens (auth imports it)
utils.py         → 2,100 tokens (why not)
middleware.py    → 1,900 tokens (imported transitively)
```

9,000 tokens. To fix a one-line typo. Before the agent wrote a single character.

The agent isn't doing anything wrong — it has no other tool. `cat` is how you read code. Grep is how you search it. Neither one understands structure.

**Reveal does.**

---

## What Progressive Disclosure Actually Is

Reveal enforces a three-tier drill-down. You cannot skip tiers. You cannot accidentally dump 7,000 tokens of raw code.

```bash
reveal src/auth/              # Tier 1: What files exist? (~50 tokens)
reveal src/auth/handler.py    # Tier 2: What's in this file? (~200 tokens)
reveal src/auth/handler.py validate_token  # Tier 3: Exact code (~100 tokens)
```

Each tier tells you whether to go deeper. Tier 2 shows every function — names, locations, complexity scores — without showing any implementation. You choose what to read. The rest stays invisible.

**Total for the auth example: ~350 tokens. Instead of 9,000.**

That's not a rounding error. That's the difference between burning your context window and having room to reason.

---

## Measured, Not Estimated

We ran these on reveal's own codebase (357 Python files, v0.64.x). Token counts use the 1 token ≈ 4 characters approximation.

| Task | Old approach | Reveal | Reduction |
|------|-------------|--------|-----------|
| Understand a large file (637 lines) | `cat`: 5,883 tokens | structure + element: 1,499 tokens | **3.9x** |
| Understand a focused module | `cat`: 4,128 tokens | structure: 275 tokens | **15x** |
| Find callers of a function | `grep`: 560 tokens (noisy) | `calls://`: 84 tokens (exact) | **6.7x** |
| Uncalled function scan (2,542 fns) | manual cross-ref: 7,196 tokens | `calls://?uncalled`: 220 tokens | **33x** |

**Typical range: 3.9–15x** on file inspection and call graph queries. The gap widens for large files and questions with direct answers. It narrows for small files where structure ≈ content.

The 15 files → 500 files claim follows directly: if typical inspection costs 15x less, a 100K context window reaches 15x more of your codebase.

---

## Everything Is a URI

Reveal's design decision that compounds everything else: all resources are URIs with the same query syntax.

```bash
reveal 'ast://src/?complexity>10'              # Code: complex functions
reveal 'calls://src/?target=validate_token'    # Code: who calls this?
reveal 'ssl://api.example.com'                 # Infra: cert expiry
reveal 'mysql://prod/?type=replication'        # DB: replication lag
reveal 'markdown://docs/?link-graph'           # Docs: orphaned pages
reveal 'claude://sessions/?search=auth'        # History: past work on auth
```

Same operators (`=`, `~=`, `>`, `!`, `..`, `*`). Same output format. Same piping model. Whether you're querying code, certificates, databases, or documentation — the mental model doesn't change.

New capabilities don't require new syntax. They drop in as new adapters. There are 22 today. The interface stays stable.

---

## The Capabilities That Matter Most

### Cross-File Call Graphs — From the CLI

No IDE. No language server. No configuration.

```bash
reveal 'calls://src/?target=validate_token'          # Who calls this? (anywhere)
reveal 'calls://src/?target=validate_token&depth=3'  # Callers-of-callers — full impact radius
reveal 'calls://src/?rank=callers&top=20'            # Most architecturally coupled functions
```

`?rank=callers` is the one that surprises people. It's not "who calls X" — it's "what functions are load-bearing across the whole project." Graph analysis from a single CLI command. Run it before a refactor and you'll find the functions you didn't know mattered.

---

### PR-Aware Context Snapshots

Giving an AI agent PR context is usually "read everything" or "let the agent figure it out." `reveal pack` makes an opinionated decision:

```bash
reveal pack src/ --since main --budget 8000
```

Changed files go to priority tier 0 — above entry points, above everything. Remaining budget fills with key dependencies. The agent gets the right files in the right order, sized to fit.

The problem it solves is real: agents burn context on stub `__init__.py` files before reaching the code that actually changed.

---

### One Health Check to Rule Them All

```bash
reveal health ./src ssl://api.example.com domain://example.com mysql://prod
```

Code quality + certificate expiry + DNS health + database replication. One command. One exit code. One JSON blob. No tool-switching.

The value isn't any individual check. It's that you stop switching tools.

---

### Native MCP Server

```bash
pip install reveal-cli
reveal-mcp    # starts the MCP server
```

Five tools for any MCP-compatible agent (Claude Code, Cursor, Windsurf): `reveal_structure`, `reveal_element`, `reveal_query`, `reveal_pack`, `reveal_check`. Agents get progressive disclosure and call-graph analysis without subprocess overhead. One install — works everywhere.

---

### Codebase Dashboard

```bash
reveal overview .    # file count, language breakdown, quality score, git activity
reveal deps .        # circular import chains, unused imports, package coupling
```

Before you read a single file. `reveal overview` replaces the multi-command orientation sequence that agents and developers both run manually. `reveal deps` surfaces structural debt that accumulates quietly — circular imports, unused dependencies — that `reveal check` doesn't catch.

---

### 69 Quality Rules, No Config Required

```bash
reveal check src/              # All rules
reveal check src/ --select B,S # Bugs + security only
reveal review main..HEAD        # Full PR review: diff + quality + hotspots
```

14 categories: bugs, complexity, duplicates, error handling, frontmatter, imports, links, maintainability, nginx, refactoring, security, types, URLs, validation. Every changed function in `reveal review` carries `complexity_before`, `complexity_after`, and `complexity_delta` — making "did this PR make anything harder to maintain?" a scriptable CI gate.

---

## Things That Surprise People

The features above are the core. These are the ones people forward to each other.

**Your nginx config is a source of SSL targets:**
```bash
reveal /etc/nginx/conf.d/app.conf --extract domains | reveal --stdin --check
```
Parse the config, extract every domain, check every cert — one pipeline. The nginx adapter feeds the SSL adapter. No scripting glue. This is what "everything is a URI" actually means in practice.

**Reveal reads itself:**
```bash
reveal reveal://rules/security/S001.py        # how the hardcoded-secrets rule works
reveal reveal://analyzers/python.py           # how Python files get analyzed
```
`reveal://` is a real adapter. The tool uses its own interface to document and explain itself. If you want to understand how any rule or adapter works, point reveal at it.

**Schema drift between live databases:**
```bash
reveal diff://mysql://localhost/users:mysql://staging/users
```
The same `diff://` that compares git branches compares live database schemas. Production vs staging, caught in one command. Nobody thinks of diff as something you run against databases.

**Find suspicious code by combining two filters:**
```bash
reveal 'ast://src?complexity>10&lines<50'    # high complexity, suspiciously short
reveal 'ast://src?complexity<5&lines>50'     # simple but huge — usually dead or data
```
Neither filter is the smell. The combination is.

**Git blame for AI interactions:**
```bash
reveal 'claude://files/auth.py'
```
Every Claude Code session that touched `auth.py` — with Read/Write/Edit counts. Not "who committed this" but "which agent sessions changed it and when."

→ **[More surprising recipes: the full showcase](reveal-surprising-recipes.md)**

---

## Who This Is For

**If you're building with AI agents** — Claude Code, Cursor, Copilot, or your own — Reveal is the context layer that makes agents competent on large codebases. Put `reveal --agent-help` in your CLAUDE.md once. The agent learns the workflow; it won't go back to `cat`.

**If you're a developer using AI assistance** — You're the one who decides what context the agent gets. Reveal lets you hand it structural understanding of a 50-file module in 400 tokens instead of 400,000. The agent's answers get better because its input gets better.

**If you're doing infrastructure work** — SSL cert monitoring, nginx audits, domain health checks, cPanel user audits. Everything with the same syntax, composable into pipelines, exit-code-governed for CI integration.

---

## The Design Philosophy (Short Version)

Reveal is built on one constraint: **structure before content, always.** It's not optional, not configurable, not a flag you pass. The architecture enforces it.

This matters because agents don't naturally exercise restraint. Left to their own devices, they read everything. Reveal makes the efficient path the only path.

The secondary constraint: **everything is composable.** Outputs are structured data. Adapters pipe into each other. Every check is a valid CI gate. The Unix philosophy applied to semantic queries.

---

## Try It

```bash
pip install reveal-cli

reveal .                    # Start here — see your codebase
reveal --agent-help         # If you're integrating with an AI agent
reveal help://              # Self-guided tour from the CLI
```

Five minutes to understand what it does. The productivity change is immediate — the first time your agent navigates a 50-file module in one context window instead of five.

---

**[Full documentation](/systems/reveal)** · **[Benchmarks](https://github.com/Semantic-Infrastructure-Lab/reveal/blob/main/docs/BENCHMARKS.md)** · **[MCP Setup](https://github.com/Semantic-Infrastructure-Lab/reveal/blob/main/docs/MCP_SETUP.md)** · **[CI Recipes](https://github.com/Semantic-Infrastructure-Lab/reveal/blob/main/docs/CI_RECIPES.md)**
