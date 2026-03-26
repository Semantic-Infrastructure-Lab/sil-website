# Articles

**Purpose:** Product introductions, tool tutorials, and technical deep-dives with accessible, engaging presentation.

**Audience:** Developers, AI practitioners, tool users, people discovering SIL through specific projects

**Last updated:** 2026-03-26

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

### [From Filing Cabinets to Agentic Minds](/articles/information-retrieval-history-and-agentic-future)
**Date:** 2026-03-22
**Topics:** Information retrieval, search history, semantic search, RAG, agentic AI, embeddings
**Audience:** Developers, AI practitioners, technical leaders

The seventy-year arc of how machines learned to find what we know — from Luhn's inverted index in 1957 through TF-IDF, PageRank, Word2Vec, dense retrieval, RAG, and into agentic systems that reason about what they find. Companion piece to the RFQ matching article.

**Key points:**
- The inverted index and TF-IDF as the foundation of all modern search
- PageRank as the first social consensus relevance signal
- The semantic revolution: Word2Vec → BERT → SBERT → DPR
- RAG: what it solved, where it breaks
- Agentic retrieval: five capabilities classic RAG can't have
- The architectural tension: index cost vs. inference cost

**From session:** lingering-ice-0322

---

### [Find Every Caller in Your Codebase With One Command](/articles/reveal-call-graphs)
**Date:** 2026-03-15
**Topics:** Reveal, call graphs, impact analysis, refactoring, dead code, architecture
**Audience:** Developers, AI practitioners

The `calls://` adapter answers three questions that grep can't: who calls this function, what does it call, and which functions are most architecturally coupled. Covers transitive call chains, graph visualization, and practical workflows for refactoring, dead code detection, and understanding unfamiliar codebases.

**Key points:**
- Impact analysis before refactoring: find every caller in one command
- Forward lookup: trace exactly what a function depends on
- Coupling analysis: identify architectural hotspots
- How calls:// differs from grep (semantic vs. textual)
- Transitive callers and call chain visualization

**From session:** atomic-zeppelin-0322

---

### [Two Commands That Change How You Work With Code](/articles/reveal-pack-and-review)
**Date:** 2026-03-15
**Topics:** Reveal, pack, review, token budget, PR review, AI agents, context curation
**Audience:** Developers, AI practitioners, teams using AI for code review

`reveal pack` solves context curation — token-budgeted snapshots that give AI agents the right files, not all the files. `reveal review` automates PR review from a git range. Together they eliminate the assembly step between "I want AI help with this codebase" and actually getting it.

**Key points:**
- `reveal pack`: priority-ranked file selection within a token or line budget
- `--focus` flag: boost domain-relevant files to the top of the pack
- `reveal review`: structured PR review from `git diff` in one command
- CI gate integration: automated review on every PR
- Using them together for agent context + review workflows

**From session:** atomic-zeppelin-0322

---

### [The Too-Many-Sausages Problem](/articles/rfq-matching-modern-architecture)
**Date:** 2026-03-23
**Topics:** Information retrieval, RFQ matching, semantic search, embeddings, agentic AI, manufacturing, enterprise
**Audience:** ML engineers, software engineers, technical leaders in manufacturing and distribution

Every industrial distributor has a version of this story: 200,000 RFQ line items, 14 million catalog products, two weeks to respond. This article traces the full arc from why exact match and monolithic semantic search both fail, through the category-first pipeline architecture that handles 85-90% of volume, to the agentic retrieval layer that handles what pipelines can't — and the hard-negative training strategy that makes all of it work.

**Key points:**
- The too-many-sausages problem: semantic search returns the whole neighborhood, but you need the certified interchangeable part
- Category routing reduces search space 14× and enables per-category accuracy measurement
- ANCE hard negative mining, LoRA adapters, and GISTEmbedLoss as the training stack
- ReAct agent with structured Corrective RAG escalation for the low-confidence tail
- Full failure mode analysis: catalog drift, classifier degradation, score miscalibration

**From sessions:** lingering-ice-0322, mountain-whirlwind-0322, oceanic-sea-0322, expanding-meteorite-0322

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
