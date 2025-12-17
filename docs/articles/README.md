# Articles

**Purpose:** Product introductions, tool tutorials, and technical deep-dives with accessible, engaging presentation.

**Audience:** Developers, AI practitioners, tool users, people discovering SIL through specific projects

**Last updated:** 2025-12-10

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

### [Stop Reading Code. Start Understanding It](reveal-introduction)
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

## Forthcoming Articles

**Potential topics:**
- Beth knowledge graphs: PageRank for documentation
- Agent Ether: Universal tool contracts for multi-agent systems
- TIA workflows: Progressive disclosure in practice
- Morphogen deterministic computation: Reproducible AI workflows

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
