# Articles

**Purpose:** Product introductions, tool tutorials, and technical deep-dives with accessible, engaging presentation.

**Audience:** Developers, AI practitioners, tool users, people discovering SIL through specific projects

**Last updated:** 2025-12-23
**Status:** ✅ 3 articles published

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

### [Stop Reading Code. Start Understanding It](/articles/reveal-introduction)
**Date:** 2025-12-10
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

### [Progressive Disclosure for AI Agents](/articles/progressive-disclosure-agents)
**Date:** 2025-12-14
**Topics:** Progressive disclosure, Reveal, token efficiency, semantic infrastructure
**Audience:** Developers, AI practitioners, tool users

Deep dive into the progressive disclosure pattern and why AI agents waste 99% of their context reading code. Explains the URI-based resource protocol, shows measured impact ($7,500 file → 50 tokens), and positions progressive disclosure as foundational infrastructure for AI interaction.

**Key points:**
- Problem: AI agents read entire files (7,500 tokens) to extract tiny insights (50 tokens needed)
- Pattern: Structure first, details on demand (scan → orient → dive)
- Architecture: URI-based resource protocol (`python://`, `ast://`, `json://`)
- Evidence: 25-150x token reduction, proven across 300+ sessions
- Vision: This should be a standard, not a tool feature

**From session:** azure-gem-1222 (moved from essays)

---

### [Configuration as Semantic Contract](/articles/configuration-semantic-contract)
**Date:** 2025-12-23
**Topics:** Configuration, progressive disclosure, semantic infrastructure, architecture validation
**Audience:** Developers, team leads, architects

Deep dive into configuration as semantic contract—why config files should declare meaning, not just tune parameters. Introduces the Progressive Configuration Pattern (3 levels: intelligent defaults, project overrides, custom extensions) and shows how Reveal's architecture validation enforces semantic contracts.

**Key points:**
- Problem: Binary choice between zero config and configure everything
- Pattern: Progressive configuration (defaults → overrides → extensions)
- Solution: Declare architecture in config, tools enforce automatically
- Evidence: Real architecture validation examples from Reveal
- Vision: Configuration as Layer 3 of Semantic OS (composition)

**From session:** stormy-gale-1223

---

## Content Pipeline

**📋 See [CONTENT_INVENTORY.md](CONTENT_INVENTORY.md) for complete publication pipeline**

**Quick Stats:**
- ✅ **3 published** (ready to post to LinkedIn/blog)
- 🔄 **14 adaptable research papers** (2-3 hours each to make accessible)
- 📦 **7 systems docs** (need expansion into articles)
- 🏗️ **9 architecture docs** (deep dives or series)
- 💡 **Unlimited future ideas** (case studies, hot takes, thought leadership)

**Total: 30+ articles in the pipeline**

---

## Forthcoming Articles (Next 12 Weeks)

**Weeks 4-6: Agentic Engineering**
- How to Build AI Agents That Don't Go Rogue (HIERARCHICAL_AGENCY_FRAMEWORK.md)
- Why You Can't Debug AI Agents (SEMANTIC_OBSERVABILITY.md)
- Building Multi-Agent Systems That Work (MULTI_AGENT_PROTOCOL_PRINCIPLES.md)

**Weeks 7-9: Production Systems**
- How PageRank Beats Vector Search (beth.md)
- Why Production AI Needs Provenance (PROVENANCE_FIRST.md)
- Deterministic AI Workflows (morphogen.md)

**Weeks 10-12: Advanced Topics**
- RAG as Geometry Problem (RAG_AS_SEMANTIC_MANIFOLD_TRANSPORT.md)
- Why AI Agents Fail at Your Docs (AI_DOCUMENTATION_STANDARDS.md)
- Universal Tool Contracts (agent-ether.md)

**See CONTENT_INVENTORY.md for full editorial calendar and content status.**

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

- [Foundations](/foundations/overview) - Foundational principles and frameworks
- [Systems](/systems) - Practical usage guides for SIL systems
- [Research](/research/overview) - Academic-style research papers

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

**Status:** ✅ 3 articles published
