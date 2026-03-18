# Articles

**Purpose:** Product introductions, tool tutorials, and technical deep-dives with accessible, engaging presentation.

**Audience:** Developers, AI practitioners, tool users, people discovering SIL through specific projects

**Last updated:** 2026-03-15

---

## About Articles

**Articles vs. Foundations vs. Founder's Notes:**

- **Articles** (this directory): Product-focused, tutorial-style, accessible but substantive
- **Foundations** (`/foundations/`): Timeless foundational documents, principles, frameworks
- **Founder's Notes** (future): Time-stamped technical essays, thought leadership

Articles are:
- ✅ Time-stamped (can reference current state)
- ✅ Product/tool focused (Reveal, Beth, Morphogen, etc.)
- ✅ Engaging hooks, narrative style
- ✅ Real-world examples, measured data
- ✅ Call to action ("try it now")

---

## Published Articles

### [Trained to Please, Empowered to Act](/articles/trained-to-please-empowered-to-act)
**Date:** 2026-03-12
**Topics:** Agentic AI, incidents, safety, sycophancy, behavioral contracts
**Audience:** Developers, CTOs, teams deploying AI agents in production

The optimization that makes chatbots say "great question!" is the same one that causes agents to delete production databases, buy groceries without asking, and fabricate data to cover their failures. Five real incidents. One pattern: we've been giving agents permissions when what they need is contracts.

**Key points:**
- Sycophancy is a drive, not just a quirk — and it scales with capability
- Five escalating incidents: vending machine → grocery purchase → AWS 13-hour outage → TaskRabbit deception → database deletion + cover-up
- "Permissions vs. contracts" — the core distinction
- SIL consulting CTA via byline

**From session:** hidden-constellation-0312

---

### [Stop Reading Code. Start Understanding It](/articles/reveal-introduction)
**Date:** 2025-12-10 (updated 2026-03-15)
**Topics:** Reveal, progressive disclosure, token efficiency, semantic stack
**Audience:** Developers, AI practitioners

Introduction to Reveal and the progressive disclosure pattern. Shows how semantic slicing achieves 25-50x token reduction with measured examples. Positions Reveal as Layer 1-3 of SIL's 7-layer semantic OS, integrated with Beth's PageRank knowledge graph system.

**Key points:**
- Problem: AI agents burn tokens reading everything
- Solution: Progressive disclosure (structure first, details on demand)
- Evidence: 25-30x reduction measured across 300+ sessions
- Integration: Reveal + Beth = virtuous cycle
- Vision: Proof that semantic infrastructure works

**From session:** emerald-crystal-1210

---

### [Two Commands That Change How You Work With Code](/articles/reveal-pack-and-review)
**Date:** 2026-03-15
**Topics:** Reveal, reveal pack, reveal review, token efficiency, CI/CD, AI agent workflow
**Audience:** Developers, AI practitioners

Deep dive into `reveal pack` (token-budgeted context snapshots for AI agents) and `reveal review` (one-command PR review with CI gate integration). The two most useful and least documented Reveal subcommands.

**Key points:**
- `reveal pack` curates the right files for an LLM context window — not all files, the ones that matter
- `reveal review` replaces git-diff + quality-check + hotspot-scan with one command
- Both produce machine-readable JSON for CI integration
- CI exit code protocol: 0 = clean, 1 = warnings, 2 = errors

**From session:** turquoise-spectrum-0315

---

### [Find Every Caller in Your Codebase With One Command](/articles/reveal-call-graphs)
**Date:** 2026-03-15
**Topics:** Reveal, calls://, call graph, static analysis, refactoring, impact analysis
**Audience:** Developers, engineers doing refactoring or impact analysis

Deep dive into `calls://` adapter — cross-file call graph queries for impact analysis, dead code detection, forward/reverse lookups, and Graphviz visualization.

**Key points:**
- `calls://src?target=X` finds every caller of X across all project files
- `calls://src?callees=X` finds what X calls (forward lookup)
- `calls://src?rank=callers` ranks functions by coupling (in-degree metrics)
- Graphviz dot output for architecture docs
- Difference from grep: finds actual invocations, not text occurrences

**From session:** turquoise-spectrum-0315

---

### [Reveal for AI Agents](/articles/reveal-for-ai-agents)
**Date:** 2026-03-03
**Topics:** Reveal, AI agents, token efficiency, Claude Code, Cursor, GitHub Copilot
**Audience:** AI practitioners, developers using AI coding tools

How AI agents should use Reveal: the breadcrumb system, URI adapters, progressive workflows, and integration patterns for Claude Code, Cursor, and GitHub Copilot.

---

### [Reveal + Claude Code](/articles/reveal-for-claude-code)
**Date:** 2026-01-06
**Topics:** Reveal, Claude Code, token efficiency
**Audience:** Claude Code users

Focused guide for using Reveal with Claude Code specifically.

---

## Forthcoming Articles

**High priority — capabilities with no coverage yet:**
- `reveal health` — unified health check for SSL/domains/databases/code
- `claude://` adapter — searching your own Claude Code sessions as structured data
- `cpanel://` adapter — full cPanel environment audits
- Quality rules deep dive — the 32-rule system, categories, custom rules

**Also potential:**
- Beth knowledge graphs: PageRank for documentation
- Agent Ether: Universal tool contracts for multi-agent systems
- TIA workflows: Progressive disclosure in practice

**Suggest new topics:** If you have ideas for articles, add them to this list or discuss in sessions.

---

## Writing Guidelines

**Article structure (recommended):**
1. **Hook** - Relatable problem, concrete example
2. **Problem deep-dive** - Why current approaches fail
3. **Solution** - How this tool/approach works
4. **Evidence** - Measured data, real-world examples
5. **How it works** - Technical details (accessible)
6. **Broader context** - How it fits in SIL vision
7. **Try it now** - Installation, quick start, links

**Style:**
- Engaging but substantive (not clickbait, not dry)
- Concrete examples (real commands, real output)
- Measured data (token counts, time savings, success rates)
- Accessible technical depth (explain jargon, don't avoid it)

**Frontmatter requirements:**
```yaml
---
title: "[Full Title]"
subtitle: "[Tool/Topic description]"
author: "Scott Senkeresty"
date: "YYYY-MM-DD"
type: "article"
status: "published|draft"
audience: "[target audience]"
topics: [topic1, topic2, topic3]
related_projects: [project-name]
related_docs:
  - "RELATED_DOC.md"
canonical_url: "https://semanticinfrastructurelab.org/articles/slug"
reading_time: "X minutes"
beth_topics: [topic-slug-1, topic-slug-2]
session_provenance: "[session-id if created in session]"
---
```

---

## Related Directories

- [Foundations](/foundations/) - Foundational principles and frameworks
- [Systems](/systems/) - Practical usage guides for SIL systems
- [Research](/research/) - Academic-style research papers

---

## Publication Workflow

**From session → published article:**

1. **Create in session directory** (ephemeral workspace)
2. **Classify as article** (product intro, tutorial, etc.)
3. **Add frontmatter** (YAML metadata)
4. **Copy to articles/** (this directory)
5. **Update articles/README.md** (add to index above)
6. **Sync to website** (see `/home/scottsen/src/tia/projects/SIL/docs/DOCUMENTATION_MAP.md`)
7. **Announce** (Twitter thread, email newsletter per Multi-Channel Strategy)

**See also:** `foundation/communications/PUBLICATION_CONTENT_STRATEGY.md` for complete workflow.

---

**Status:** ✅ Directory created, first article published (2025-12-10)
