# SIL Content Inventory & Publication Pipeline

**Purpose:** Track all content that can be published as articles, blog posts, or LinkedIn Newsletter content.

**Owner:** Scott Senkeresty
**Last Updated:** 2026-01-02
**Status:** Living Document

---

## TL;DR

- **✅ Published**: 3 articles ready to post (just copy/paste to LinkedIn/blog)
- **🔄 Adaptable**: 14 research papers (need 2-3 hours to make accessible)
- **📦 Systems**: 7 systems docs (need expansion into articles)
- **🏗️ Architecture**: 9 architecture docs (deep dives or series)
- **💡 Future**: Unlimited ideas from consulting work, case studies, hot takes
- **Total Pipeline**: 30+ articles available

**Next Action**: Start with 3 published articles (Week 1-3), then adapt research papers (2-3 hours/week)

---

## Table of Contents

1. [Published Articles (Ready to Post)](#published-articles-ready-to-post)
2. [Adaptable Research Papers](#adaptable-research-papers)
3. [Systems Documentation](#systems-documentation)
4. [Architecture Deep Dives](#architecture-deep-dives)
5. [Future Article Ideas](#future-article-ideas)
6. [12-Week Editorial Calendar](#12-week-editorial-calendar)
7. [Publication Workflow](#publication-workflow)
8. [Success Metrics](#success-metrics)

---

## Published Articles (Ready to Post)

**Status**: ✅ Already written, publication-ready
**Location**: `/docs/articles/`
**Effort**: 30 min each (just post to LinkedIn Newsletter + SIL blog)

### 1. Stop Reading Code. Start Understanding It

**File**: `reveal-introduction.md` (599 lines, 19KB)
**Date Written**: 2025-12-10
**Topics**: Reveal, progressive disclosure, token efficiency, semantic stack
**Audience**: Developers, AI practitioners
**Session**: emerald-crystal-1210

**LinkedIn Hook**: "I built a tool that reduces AI agent costs 25x. Here's how progressive disclosure saves $7,500 per file read..."

**Key Points**:
- Problem: AI agents burn tokens reading everything
- Solution: Progressive disclosure (structure first, details on demand)
- Evidence: 25-30x reduction measured across 300+ sessions
- Integration: Reveal + Beth = virtuous cycle
- Vision: Proof that semantic infrastructure works

**CTA**: "Try reveal-cli today: `pip install reveal-cli`"

**Status**: ✅ Ready to publish
**LinkedIn Newsletter**: Not yet posted
**SIL Blog**: Published at `/articles/reveal-introduction`

---

### 2. Progressive Disclosure for AI Agents

**File**: `progressive-disclosure-agents.md` (349 lines, 15KB)
**Date Written**: 2025-12-14
**Topics**: Progressive disclosure, Reveal, token efficiency, semantic infrastructure
**Audience**: Developers, AI practitioners, tool users
**Session**: azure-gem-1222

**LinkedIn Hook**: "Your AI agents waste 99% of their context. Here's the pattern that fixes it."

**Key Points**:
- Problem: AI agents read entire files (7,500 tokens) to extract tiny insights (50 tokens needed)
- Pattern: Structure first, details on demand (scan → orient → dive)
- Architecture: URI-based resource protocol (`python://`, `ast://`, `json://`)
- Evidence: 25-150x token reduction, proven across 300+ sessions
- Vision: This should be a standard, not a tool feature

**CTA**: "See how progressive disclosure works in Reveal: [link]"

**Status**: ✅ Ready to publish
**LinkedIn Newsletter**: Not yet posted
**SIL Blog**: Published at `/articles/progressive-disclosure-agents`

---

### 3. Configuration as Semantic Contract

**File**: `configuration-semantic-contract.md` (642 lines, 21KB)
**Date Written**: 2025-12-23
**Topics**: Configuration, progressive disclosure, semantic infrastructure, architecture validation
**Audience**: Developers, team leads, architects
**Session**: stormy-gale-1223

**LinkedIn Hook**: "Stop choosing between zero config and configure everything. Here's the progressive configuration pattern."

**Key Points**:
- Problem: Binary choice between zero config and configure everything
- Pattern: Progressive configuration (defaults → overrides → extensions)
- Solution: Declare architecture in config, tools enforce automatically
- Evidence: Real architecture validation examples from Reveal
- Vision: Configuration as Layer 3 of Semantic OS (composition)

**CTA**: "See how Reveal implements progressive configuration"

**Status**: ✅ Ready to publish
**LinkedIn Newsletter**: Not yet posted
**SIL Blog**: Published at `/articles/configuration-semantic-contract`

---

## Adaptable Research Papers

**Status**: 🔄 Need adaptation (2-3 hours each to make accessible)
**Location**: `/docs/research/`
**Audience**: Technical decision-makers, architects, senior engineers

**Adaptation Process**:
1. Extract core insight (5-10 sentences)
2. Add relatable hook/problem
3. Simplify jargon (explain, don't avoid)
4. Add practical examples
5. Include measured data
6. End with "try it" or "hire me" CTA

---

### 1. How to Build AI Agents That Don't Go Rogue

**Source**: `HIERARCHICAL_AGENCY_FRAMEWORK.md` (1020 lines)
**Effort**: 2-3 hours
**Priority**: ⭐⭐⭐ HIGH (core consulting topic)

**Hook**: "Most AI agents fail because they have too much or too little autonomy. Here's the framework that fixes it."

**Core Insight**: Agency is stratified. Well-designed systems have a smooth gradient from strategic (high autonomy, deep context) to execution (zero autonomy, minimal context).

**Article Structure**:
- Problem: AI agents either go rogue or are useless
- The 4 levels: Strategic, Operational, Tactical, Execution
- Real-world examples from organizational theory
- How this maps to AI agent architecture
- Implementation guide
- CTA: "Building production agentic systems? Let's talk."

**Related Docs**: MULTI_AGENT_PROTOCOL_PRINCIPLES.md (companion doc)

**Status**: 📋 Not started
**Target Week**: Week 4 in editorial calendar

---

### 2. Why You Can't Debug AI Agents (And How to Fix It)

**Source**: `SEMANTIC_OBSERVABILITY.md` (1134 lines)
**Effort**: 2-3 hours
**Priority**: ⭐⭐⭐ HIGH (production systems credibility)

**Hook**: "Production AI agents are black boxes. Semantic observability changes that."

**Core Insight**: Traditional observability (logs, metrics, traces) doesn't work for semantic systems. You need provenance tracking, semantic state inspection, and causal reasoning.

**Article Structure**:
- Problem: Can't debug why AI agent made a decision
- Why traditional observability fails
- What semantic observability means
- Architecture patterns (provenance graphs, semantic snapshots)
- Implementation examples
- CTA: "Need production-grade AI observability? I can help."

**Status**: 📋 Not started
**Target Week**: Week 5

---

### 3. RAG Isn't a Retrieval Problem—It's a Geometry Problem

**Source**: `RAG_AS_SEMANTIC_MANIFOLD_TRANSPORT.md` (854 lines)
**Effort**: 3 hours (complex math to simplify)
**Priority**: ⭐⭐ MEDIUM (thought leadership, differentiation)

**Hook**: "Most RAG systems fail due to geometric distortion, not bad retrieval. Here's the math."

**Core Insight**: RAG is semantic manifold transport across 4 misaligned spaces (human concepts → embeddings → LLM latents → fusion states). Distortion at each transition causes failures.

**Article Structure**:
- Problem: RAG systems work in demos, fail in production
- Why it's not about retrieval quality
- The 4 manifolds and distortion sources
- Alignment strategies (scaffolding, reranking, provenance)
- Implementation roadmap
- CTA: "Building production RAG? Let's discuss alignment strategies."

**Status**: 📋 Not started
**Target Week**: Week 10

---

### 4. Building Multi-Agent Systems That Actually Work Together

**Source**: `MULTI_AGENT_PROTOCOL_PRINCIPLES.md` (462 lines)
**Effort**: 2 hours
**Priority**: ⭐⭐⭐ HIGH (enterprise consulting angle)

**Hook**: "Most multi-agent systems devolve into chaos. Here are the protocols that prevent it."

**Core Insight**: Multi-agent coordination requires explicit protocols for task negotiation, resource sharing, conflict resolution, and state synchronization.

**Article Structure**:
- Problem: Agents step on each other, duplicate work, conflict
- The 5 protocol principles
- Real-world failure modes
- Architecture patterns that work
- Implementation checklist
- CTA: "Building multi-agent systems? I've solved this."

**Status**: 📋 Not started
**Target Week**: Week 6

---

### 5. Why AI Agents Fail at Your Documentation

**Source**: `AI_DOCUMENTATION_STANDARDS.md` (477 lines)
**Effort**: 2 hours
**Priority**: ⭐⭐ MEDIUM (practical, actionable)

**Hook**: "Your documentation is great for humans, terrible for AI agents. Here's the standard that fixes it."

**Core Insight**: AI agents need structured metadata, progressive disclosure, type information, and provenance. Human-only docs create 10x overhead.

**Article Structure**:
- Problem: Agents can't navigate your docs
- What makes docs AI-readable
- The Agent Help Standard
- Before/after examples
- Implementation guide
- CTA: "Need AI-ready documentation? Let's fix it."

**Status**: 📋 Not started
**Target Week**: Week 11

---

### 6. The Missing Standard: Agent-Readable Documentation

**Source**: `AGENT_HELP_STANDARD.md` (403 lines)
**Effort**: 2 hours
**Priority**: ⭐⭐ MEDIUM (standards/thought leadership)

**Hook**: "Every tool speaks a different help language. Here's the universal standard for agent-readable help."

**Core Insight**: The `help://` URI scheme and structured help metadata enable agents to discover capabilities without trial-and-error.

**Status**: 📋 Not started
**Target Week**: Week 12+

---

### 7. How AI Agents Learn (Without Training Data)

**Source**: `SEMANTIC_FEEDBACK_LOOPS.md` (891 lines)
**Effort**: 3 hours
**Priority**: ⭐⭐ MEDIUM (advanced topic)

**Hook**: "AI agents don't need retraining to improve. Semantic feedback loops enable runtime learning."

**Core Insight**: Agents improve through semantic feedback (validation, refinement, provenance tracking) without model updates.

**Status**: 📋 Not started
**Target Week**: Week 12+

---

### 8. Building Trust in Multi-Agent Systems

**Source**: `TRUST_ASSERTION_PROTOCOL.md` (775 lines)
**Effort**: 2-3 hours
**Priority**: ⭐ LOW (niche topic)

**Hook**: "How do agents know who to trust? The trust assertion protocol."

**Status**: 📋 Backlog

---

### 9. Who Decides? Authorization in Agentic Systems

**Source**: `AUTHORIZATION_PROTOCOL.md` (653 lines)
**Effort**: 2 hours
**Priority**: ⭐⭐ MEDIUM (security angle)

**Hook**: "Authorization for AI agents isn't like authorization for users. Here's what's different."

**Status**: 📋 Backlog

---

### 10. How Reveal + Beth Create a Knowledge Flywheel

**Source**: `REVEAL_BETH_PROGRESSIVE_KNOWLEDGE_SYSTEM.md` (563 lines)
**Effort**: 2 hours
**Priority**: ⭐⭐⭐ HIGH (showcases both tools)

**Hook**: "Progressive disclosure + knowledge graphs = compounding efficiency gains"

**Status**: 📋 Not started
**Target Week**: Week 12+

---

### 11. Teaching AI Agents to Reason by Analogy

**Source**: `ANALOGY_DISCOVERY_IN_SEMANTIC_SPACE.md` (585 lines)
**Effort**: 3 hours
**Priority**: ⭐ LOW (research-heavy)

**Hook**: "The most powerful reasoning pattern humans use—now available to AI agents"

**Status**: 📋 Backlog

---

### 12. How AI Agents Track 'Who Is Who' Across Systems

**Source**: `IDENTITY_MAPPING.md` (366 lines)
**Effort**: 2 hours
**Priority**: ⭐ LOW (niche)

**Hook**: "Identity resolution for multi-agent systems"

**Status**: 📋 Backlog

---

### 13. The Implementation Guide: Progressive Disclosure in Production

**Source**: `PROGRESSIVE_DISCLOSURE_GUIDE.md` (933 lines)
**Effort**: 2 hours (already somewhat accessible)
**Priority**: ⭐⭐⭐ HIGH (implementation guide)

**Hook**: "How to implement progressive disclosure in your systems: A practical guide"

**Core Insight**: The 3 levels (Orient → Navigate → Focus), design patterns, anti-patterns, measuring success.

**Status**: 📋 Not started
**Target Week**: Week 7-8

---

### 14. Progressive Disclosure System Design

**Source**: `progressive-disclosure-system.md` (343 lines)
**Effort**: 1-2 hours
**Priority**: ⭐⭐ MEDIUM (may overlap with #13)

**Status**: 📋 Review for uniqueness vs PROGRESSIVE_DISCLOSURE_GUIDE.md

---

## Systems Documentation

**Status**: 📦 Need expansion (2-3 hours each to turn into articles)
**Location**: `/docs/systems/`
**Format**: Currently 300-400 line system docs, need narrative expansion

---

### 1. Reveal (DONE) ✅

**Source**: `reveal.md` (361 lines)
**Status**: ✅ Already covered in published articles

---

### 2. How PageRank for Documentation Beats Vector Search

**Source**: `beth.md` (376 lines)
**Effort**: 2 hours
**Priority**: ⭐⭐⭐ HIGH (unique differentiation)

**Hook**: "Vector search is everywhere. Here's why graph-based ranking works better for AI agents."

**Core Insight**: Beth uses PageRank on documentation graphs + keyword indexing to achieve better relevance than embeddings alone.

**Article Structure**:
- Problem: Vector search misses connections
- Why graph ranking works
- Beth's architecture (9,941 files, 31,349 keywords)
- Performance comparison
- Integration with Reveal
- CTA: "Building knowledge systems? Let's talk."

**Status**: 📋 Not started
**Target Week**: Week 7

---

### 3. Deterministic AI Workflows: Why Reproducibility Matters

**Source**: `morphogen.md` (300 lines)
**Effort**: 2-3 hours
**Priority**: ⭐⭐⭐ HIGH (production credibility)

**Hook**: "AI workflows are non-deterministic nightmares. Here's how to make them reproducible."

**Core Insight**: Morphogen achieves deterministic cross-domain computation through dependency tracking, multirate scheduling, and provenance.

**Article Structure**:
- Problem: Can't reproduce AI workflow results
- Why determinism matters in production
- Morphogen's architecture
- Real-world use cases
- Implementation patterns
- CTA: "Need reproducible AI systems? I can help."

**Status**: 📋 Not started
**Target Week**: Week 9

---

### 4. Universal Tool Contracts for Multi-Agent Systems

**Source**: `agent-ether.md` (412 lines)
**Effort**: 2-3 hours
**Priority**: ⭐⭐⭐ HIGH (multi-agent consulting)

**Hook**: "Every AI agent speaks a different language. Agent Ether creates universal tool contracts."

**Core Insight**: Agent Ether enables cross-agent tool invocation through semantic contracts and capability discovery.

**Article Structure**:
- Problem: Agents can't share tools
- What universal contracts mean
- Agent Ether architecture
- How it integrates with Layer 6
- Implementation examples
- CTA: "Building multi-agent systems? This solves interop."

**Status**: 📋 Not started
**Target Week**: Week 12

---

### 5. Building a Universal Semantic IR

**Source**: `pantheon.md` (406 lines)
**Effort**: 3 hours (complex topic)
**Priority**: ⭐⭐ MEDIUM (architecture thought leadership)

**Hook**: "How to build representations that work across domains: The Universal Semantic IR"

**Core Insight**: Pantheon provides Layer 1 (USIR) that enables cross-domain semantic operations with type safety and provenance.

**Status**: 📋 Backlog (complex, may need series)

---

### 6. How I Built an AI Agent That Manages My Projects

**Source**: `tia.md` (259 lines)
**Effort**: 2 hours
**Priority**: ⭐⭐⭐ HIGH (personal story, relatable)

**Hook**: "TIA manages 67 projects, 14,549 files, and 1,402 topics. Here's how it works."

**Core Insight**: TIA is a production agentic system that demonstrates all SIL principles in a real-world use case.

**Article Structure**:
- Problem: Managing complex projects manually
- How TIA works (transparent agent)
- Real-world impact (300+ sessions, 25x efficiency)
- Architecture decisions
- Lessons learned
- CTA: "Want an agent like this for your org? Let's talk."

**Status**: 📋 Not started
**Target Week**: Week 8 or Week 12+

---

### 7. Knowledge Graphs That Actually Understand Context

**Source**: `genesisgraph.md` (416 lines)
**Effort**: 2-3 hours
**Priority**: ⭐⭐ MEDIUM

**Hook**: "Most knowledge graphs are static. GenesisGraph understands context and evolves."

**Status**: 📋 Backlog

---

### 8. Bringing AI Agents to CAD Design

**Source**: `tiacad.md` (139 lines)
**Effort**: 2 hours
**Priority**: ⭐ LOW (niche audience)

**Hook**: "Agentic AI for CAD: How TIA generates OpenSCAD models"

**Status**: 📋 Backlog (niche, but interesting cross-domain example)

---

## Architecture Deep Dives

**Status**: 🏗️ Deep technical content
**Location**: `/docs/architecture/`
**Format**: Can become standalone articles or multi-part series

---

### 1. The 7-Layer Semantic OS Architecture

**Source**: `UNIFIED_ARCHITECTURE_GUIDE.md` (582 lines)
**Effort**: 3 hours (or 7-part series, 1 layer per week)
**Priority**: ⭐⭐⭐ HIGH (foundational thought leadership)

**Option A: Single Article**
**Hook**: "How to build a Semantic OS: The 7-layer architecture"

**Option B: 7-Part Series**
- Part 1: Layer 0 (Semantic Memory)
- Part 2: Layer 1 (Universal Semantic IR)
- Part 3: Layer 2 (Semantic Object Graph)
- Part 4: Layer 3 (Composition & Multi-Agent)
- Part 5: Layer 4 (Domain Engines)
- Part 6: Layer 5 (Semantic Interaction Model)
- Part 7: Layer 6 (Agent Ether)

**Status**: 📋 Not started
**Target**: Week 12+ (or monthly series)

---

### 2. Why Production AI Needs Provenance Tracking

**Source**: `PROVENANCE_FIRST.md` (347 lines)
**Effort**: 2 hours
**Priority**: ⭐⭐⭐ HIGH (production systems credibility)

**Hook**: "When your AI agent makes a mistake, can you trace why? Provenance-first architecture makes it possible."

**Core Insight**: Provenance isn't optional in production AI—it's foundational. Every decision needs traceable causality.

**Status**: 📋 Not started
**Target Week**: Week 8

---

### 3. Design Invariants for Multi-Layer AI Systems

**Source**: `INVARIANTS_OVER_LAYERS.md` (465 lines)
**Effort**: 2-3 hours
**Priority**: ⭐⭐ MEDIUM (advanced architecture)

**Hook**: "What properties must hold across all layers of an AI system? Here are the invariants."

**Status**: 📋 Backlog

---

### 4. How to Build Distributed Semantic Storage

**Source**: `DISTRIBUTED_STORAGE_ARCHITECTURE.md` (1522 lines - largest doc!)
**Effort**: 6-9 hours (3-part series recommended)
**Priority**: ⭐⭐ MEDIUM (advanced topic)

**Series Structure**:
- Part 1: Why distributed semantic storage is different
- Part 2: Architecture patterns and trade-offs
- Part 3: Implementation guide

**Status**: 📋 Backlog (consider for Month 4-6)

---

### 5. Comparing AI Architecture Models: What Works in Production

**Source**: `LAYER_MODELS_COMPARISON.md` (345 lines)
**Effort**: 2 hours
**Priority**: ⭐⭐ MEDIUM (comparison/evaluation)

**Hook**: "We evaluated 5 AI architecture models. Here's what actually works in production."

**Status**: 📋 Backlog

---

### 6-9. Additional Architecture Docs

- `ARCHITECTURE_CHEAT_SHEET.md` (109 lines) - Quick reference, may not need article
- `MODEL_EVALUATION.md` (369 lines) - Could become article
- `SYNTHESIS_MAP.md` (225 lines) - Potentially integrate into unified guide
- `README.md` (134 lines) - Navigation doc

**Status**: 📋 Review for article potential

---

## Future Article Ideas

**Status**: 💡 Ideas for Month 4-6 and beyond
**Source**: Consulting work, case studies, hot takes

---

### Case Studies (From Consulting Engagements)

**Format**: "How [Company] achieved [Result] using [Approach]"

**Potential Topics**:
1. "How [Company] Reduced AI Agent Costs 80% in 30 Days"
2. "Building a Production Agentic System: A Real-World Case Study"
3. "From Prototype to Production: Deploying AI Agents at Scale"
4. "How We Debugged a $50K/Month AI Agent Failure"
5. "Migrating from LangChain to Production Architecture"

**Status**: 📋 Wait for consulting engagements to generate

---

### Thought Leadership / Hot Takes

**Format**: Opinion pieces, trend analysis, predictions

**Potential Topics**:
1. "Why Most AI Agent Startups Will Fail"
2. "The Agentic AI Hype Cycle: Where We Really Are in 2026"
3. "What Enterprises Get Wrong About AI Agents"
4. "Stop Building AI Agents on Prompt Engineering"
5. "Why 'Agentic AI' Isn't About Autonomy"
6. "The Missing Infrastructure Layer in AI"
7. "RAG is Dead. Long Live Semantic Transport."

**Status**: 📋 Draft when inspired / reactive to industry news

---

### Technical Deep Dives

**Format**: Advanced implementation guides

**Potential Topics**:
1. "Implementing the Agent Help Standard in Your Tool"
2. "Building a Progressive Disclosure API"
3. "How to Add Provenance Tracking to Your AI Agent"
4. "Semantic Observability: Implementation Guide"
5. "Cross-Domain Type Systems for AI"

**Status**: 📋 As needed for technical audience

---

### Personal Story / Journey Articles

**Format**: First-person narrative with lessons

**Potential Topics**:
1. "I Built an AI Agent Tool with 88K Downloads. Here's What I Learned."
2. "300 Sessions with AI Agents: Lessons from the Trenches"
3. "Why I'm Building a Semantic OS (And You Should Care)"
4. "From Biochar to AI Agents: My Unconventional Path"
5. "What Building Reveal Taught Me About Production AI"

**Status**: 📋 High-impact for credibility, write when ready

---

## 12-Week Editorial Calendar

**Goal**: Publish 1 article per week on LinkedIn Newsletter + SIL blog
**Effort**: 2-3 hours/week average
**Target Audience**: CTOs, Engineering Leaders, Senior Developers building agentic systems

### Weeks 1-3: Published Articles (30 min each)

| Week | Article | Source | Status |
|------|---------|--------|--------|
| 1 | Stop Reading Code. Start Understanding It | reveal-introduction.md | ✅ Ready |
| 2 | Progressive Disclosure for AI Agents | progressive-disclosure-agents.md | ✅ Ready |
| 3 | Configuration as Semantic Contract | configuration-semantic-contract.md | ✅ Ready |

### Weeks 4-6: Agentic Engineering (2-3 hours each)

| Week | Article | Source | Priority |
|------|---------|--------|----------|
| 4 | How to Build AI Agents That Don't Go Rogue | HIERARCHICAL_AGENCY_FRAMEWORK.md | ⭐⭐⭐ |
| 5 | Why You Can't Debug AI Agents | SEMANTIC_OBSERVABILITY.md | ⭐⭐⭐ |
| 6 | Building Multi-Agent Systems That Work | MULTI_AGENT_PROTOCOL_PRINCIPLES.md | ⭐⭐⭐ |

### Weeks 7-9: Production Systems (2-3 hours each)

| Week | Article | Source | Priority |
|------|---------|--------|----------|
| 7 | How PageRank Beats Vector Search | beth.md | ⭐⭐⭐ |
| 8 | Why Production AI Needs Provenance | PROVENANCE_FIRST.md | ⭐⭐⭐ |
| 9 | Deterministic AI Workflows | morphogen.md | ⭐⭐⭐ |

### Weeks 10-12: Advanced Topics (2-3 hours each)

| Week | Article | Source | Priority |
|------|---------|--------|----------|
| 10 | RAG as Geometry Problem | RAG_AS_SEMANTIC_MANIFOLD_TRANSPORT.md | ⭐⭐ |
| 11 | Why AI Agents Fail at Your Docs | AI_DOCUMENTATION_STANDARDS.md | ⭐⭐ |
| 12 | Universal Tool Contracts | agent-ether.md | ⭐⭐⭐ |

### Weeks 13-16: Flexible / Responsive

**Options**:
- Continue with backlog research papers
- Write case studies from consulting work
- Create thought leadership pieces
- Start 7-layer architecture series
- Personal story articles

---

## Publication Workflow

### For Published Articles (Weeks 1-3)

**Time**: 30 minutes per article

1. **Copy content** from `docs/articles/*.md`
2. **Post to LinkedIn Newsletter**:
   - Go to LinkedIn → Write Article → Create Newsletter
   - Paste content (adjust formatting for LinkedIn)
   - Add hook as subtitle
   - Publish and notify subscribers
3. **Verify on SIL blog**: Already published at `/articles/[slug]`
4. **Amplify on Twitter/X**:
   - Thread with key insights
   - Link to LinkedIn Newsletter
   - Tag relevant accounts
5. **Track metrics**: Views, comments, profile visits, leads

---

### For Adapted Research Papers (Weeks 4+)

**Time**: 2-3 hours per article

1. **Read source research paper** (30 min)
2. **Extract core insight** (15 min):
   - What's the single most important idea?
   - Why does it matter for production systems?
3. **Write accessible article** (60-90 min):
   - Hook: Relatable problem
   - Problem deep-dive
   - Solution/framework
   - Evidence/examples
   - Implementation guidance
   - CTA: "Building this? Let's talk."
4. **Add frontmatter** (5 min):
   - Title, subtitle, author, date
   - Topics, audience, related_docs
   - Beth topics, session provenance
5. **Save to** `docs/articles/[new-slug].md`
6. **Post to LinkedIn Newsletter** (10 min)
7. **Copy to SIL blog** (sync via normal workflow)
8. **Amplify on Twitter** (10 min)
9. **Update this inventory doc** (5 min) - mark as published

---

### For Systems/Architecture Articles

**Time**: 2-3 hours per article

1. **Read source doc** (30 min)
2. **Expand into narrative** (90-120 min):
   - Add problem/solution framing
   - Include real-world examples
   - Explain architecture decisions
   - Show measured impact
   - Provide implementation guide
3. **Follow publication workflow** above

---

## Success Metrics

### Content Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Articles published** | 12 in 12 weeks | Count in this doc |
| **Views per article** | 500-2,000 | LinkedIn analytics |
| **Engagement rate** | 5-10% | Comments + reactions / views |
| **Shares** | 10-50 per article | LinkedIn analytics |
| **Blog traffic** | 500-2,000/month | SIL website analytics |

### Business Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Consulting inquiries** | 10-20 per 12 weeks | Email/LinkedIn DMs |
| **Discovery calls** | 5-10 per 12 weeks | Calendar bookings |
| **Deals closed** | 1-3 per 12 weeks | Contracts signed |
| **Revenue** | $50K-150K per 12 weeks | Actual consulting revenue |

### Authority Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **LinkedIn followers** | +500 per 12 weeks | Profile analytics |
| **Newsletter subscribers** | 200-1,000 | LinkedIn newsletter analytics |
| **Conference talk invitations** | 1-2 | Inbound CFP invites |
| **Podcast appearances** | 1-2 | Invitations received |

---

## Notes & Decision Log

### 2026-01-02: Initial Inventory Created
- **Decision**: Start with 3 published articles (weeks 1-3) to validate format
- **Rationale**: Zero content creation time, immediate momentum
- **Next**: Adapt HIERARCHICAL_AGENCY_FRAMEWORK.md for Week 4

### Future Decisions

**When to write case studies?**
- After securing 1-2 consulting clients (can write real case studies)
- Placeholder: Week 13+

**When to start 7-layer architecture series?**
- After 12-week calendar complete
- Consider monthly cadence (7 months) vs weekly

**Should we serialize long research papers?**
- Yes for DISTRIBUTED_STORAGE_ARCHITECTURE.md (1522 lines → 3 parts)
- Consider for RAG_AS_MANIFOLD (854 lines → 2 parts?)

---

## Quick Reference

**Total Pipeline**: 30+ articles

| Category | Count | Status |
|----------|-------|--------|
| Published (ready) | 3 | ✅ |
| Adaptable research | 14 | 🔄 |
| Systems docs | 7 | 📦 |
| Architecture | 9 | 🏗️ |
| Future ideas | Unlimited | 💡 |

**Immediate Next Actions**:
1. Publish "Stop Reading Code" to LinkedIn Newsletter (Week 1)
2. Schedule Week 2-3 articles
3. Start adapting HIERARCHICAL_AGENCY_FRAMEWORK.md for Week 4
4. Track metrics in this doc

---

**Last Updated**: 2026-01-02
**Owner**: Scott Senkeresty
**Location**: `/docs/articles/CONTENT_INVENTORY.md`
