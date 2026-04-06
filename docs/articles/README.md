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

*13 articles live on the website. LinkedIn status noted per article.*

### [Trained to Please, Empowered to Act](/articles/trained-to-please-empowered-to-act)
**Date:** 2026-03-12
**LinkedIn:** ✅ Posted
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
**LinkedIn:** ✅ Posted
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
**LinkedIn:** ✅ Posted
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
**LinkedIn:** ⬜ Not yet posted
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
**LinkedIn:** ⬜ Not yet posted
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
**LinkedIn:** ✅ Posted
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

### [Session Archaeology: Excavating Your Claude Code History](/articles/claude-session-archaeology)
**Date:** 2026-03-31
**LinkedIn:** ✅ Posted
**Topics:** Reveal, Claude Code, session analysis, token cost, workflow observability, cost attribution
**Audience:** Developers using Claude Code

`reveal claude://` is a git blame for your thinking process, not just your code. Seven scenarios covering the full surface area of session observability: recovering where a session left off, diagnosing session quality from tool success rates, understanding turn-by-turn token cost, tracing the step-by-step workflow with failure markers, finding which files keep coming up across sessions, reconstructing a multi-session bug arc, and reading your own prompt patterns as data.

**Key points:**
- The drill-down rule: `?last` → `?summary` → full read (50 tokens vs. re-reading 150 messages)
- Tool success rates as a session quality proxy: Bash > 95% is clean execution, < 85% is significant thrash
- Cache attribution: real sessions run at 93–99% hit rate; compaction mid-session is where costs spike
- `/workflow` reads like a story: orientation → failure → diagnosis → fix → verification
- Loop detection: failure followed by the same command vs. failure followed by a `Read`
- `claude://history` as the mirror — not what Claude did, but what you kept needing to ask

**From session:** dark-matter-0331

---

### [Your Project Has an API Now](/articles/reveal-project-api)
**Date:** 2026-04-06
**LinkedIn:** ⬜ Not yet posted
**Topics:** Reveal, composability, infrastructure, AST, SSL, diff, AI agents, token efficiency
**Audience:** Developers, engineering teams, AI practitioners

The flagship meta-article. 22 adapters, one syntax — code structure, SSL certs, structural diffs, databases, markdown docs, and AI session history all queryable with the same query language. Covers the pipeline composability story (Reveal pipes into itself), token math across domains, and `reveal review` as the composed PR review workflow. Thesis: your project is a database, you just couldn't query it.

**From session:** swift-dragon-0406

---

### [Stop Scrolling. Start Navigating.](/articles/reveal-nav-flags)
**Date:** 2026-04-06
**LinkedIn:** ✅ Posted
**Topics:** Reveal, code navigation, AST, token efficiency, debugging, AI agents
**Audience:** Developers, AI practitioners

Four nav flags (`--outline`, `--scope`, `--varflow`, `--calls`) as four questions every developer already asks when reading a complex function. Includes a real debugging walkthrough using Reveal's own `_walk_var` internals — structure, variable trace, and scope check — without reading 124 lines of code. Token math table shows 7-25x reduction vs. `cat`.

**From session:** celestial-moon-0406

---

### [The Diff That Shows What Actually Changed](/articles/reveal-diff)
**Date:** 2026-04-06
**LinkedIn:** ✅ Posted
**Topics:** Reveal, diff, code review, CI/CD, complexity, AST, refactoring
**Audience:** Developers, engineering teams

`git diff` is a line counter. `reveal diff://` is a question answerer. Covers four workflows: pre-commit sanity check, PR review orientation, CI complexity gate (with full bash script), and refactor validation (proving complexity went down). Includes import tracking as a signal alongside functions. Real complexity numbers from production code.

**From session:** swift-dragon-0406

---

### [Reveal: The Surprising Recipes](/articles/reveal-surprising-recipes)
**Date:** 2026-03-27
**LinkedIn:** ⬜ Not yet posted
**Topics:** Reveal, recipes, patterns, AST, infrastructure adapters

**From session:** (see frontmatter)

---

### [From 15 Files to 500: What Reveal Makes Possible for AI Agents](/articles/reveal-what-it-makes-possible)
**Date:** 2026-03-27
**LinkedIn:** ⬜ Not yet posted
**Topics:** Reveal, AI agents, token efficiency, MCP, scale

**From session:** (see frontmatter)

---

### [Progressive Disclosure for AI Agents](/articles/progressive-disclosure-agents)
**Date:** 2025-12-14
**LinkedIn:** ⬜ Not yet posted
**Topics:** Progressive disclosure, Reveal, token efficiency, semantic infrastructure
**Audience:** Developers, AI practitioners

**From session:** azure-gem-1222

---

### [Configuration as Semantic Contract](/articles/configuration-semantic-contract)
**Date:** 2025-12-23
**LinkedIn:** ⬜ Not yet posted
**Topics:** Configuration, progressive disclosure, semantic infrastructure, architecture validation
**Audience:** Developers, team leads, architects

**From session:** stormy-gale-1223

---

## Forthcoming Articles

**Next article candidates (in priority order):**
- "How AI Agents Should Read Code" — MCP server + `--format json` + schema introspection
- "Your Infrastructure Has an API Now" — `ssl://`, `nginx://`, `domain://`, `reveal health` category
- "Reveal as a CI/CD Tool" — `--check`, `diff://`, `review` pipeline gates

**LinkedIn queue (not yet posted, ready now):**
- reveal-project-api ← flagship, post this next
- reveal-call-graphs
- reveal-pack-and-review
- reveal-surprising-recipes
- reveal-what-it-makes-possible
- progressive-disclosure-agents
- configuration-semantic-contract
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
