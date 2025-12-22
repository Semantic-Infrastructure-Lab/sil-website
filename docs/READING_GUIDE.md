# SIL Reading Guide

**Curated paths through the Semantic Infrastructure Lab documentation**

---

## How to Use This Guide

SIL has comprehensive documentation across multiple domains. This guide provides **curated reading paths** based on your goals, time available, and background.

**First time here?** Start with [Path 1: The Essentials](#path-1-the-essentials-30-minutes).

---

## Path 1: The Essentials (30 minutes)

**Goal:** Understand what SIL is, why it exists, and what it's built

### Required Reading

1. **[START_HERE](/foundations/start-here)** (5 min)
   - The single front door to SIL
   - Overview of architecture, tools, and philosophy

2. **[Manifesto](/manifesto/yolo)** (15 min)
   - The problem: AI without semantic substrate
   - What SIL builds and why it matters
   - **Start here** if you read only one document

3. **[Principles](/foundations/design-principles)** (10 min)
   - The 14 principles that guide all SIL work
   - Core: Clarity, Simplicity, Composability, Correctness, Verifiability
   - Operational: Structure before heuristics, Provenance everywhere, etc.

### Outcome

You'll understand SIL's mission, approach, and what makes it different from other AI infrastructure efforts.

---

## Path 2: Technical Understanding (1.5 hours)

**Goal:** Deep understanding of SIL's technical architecture and guarantees

### Prerequisites
- Path 1 (Essentials)
- Familiarity with systems programming, type theory, or formal methods

### Reading Sequence

1. **[Semantic OS Architecture](/foundations/semantic-os-architecture)** (30 min)
   - The 7-layer architecture (Semantic Memory → Agent Orchestration)
   - How layers compose and interact
   - Design invariants and guarantees

2. **[Technical Charter](/foundations/technical-charter)** (45 min)
   - Formal specification of invariants
   - Semantic contracts and provenance requirements
   - Verifiability guarantees

3. **[Glossary](/foundations/glossary)** (Reference)
   - Keep open while reading — 108 canonical terms
   - Precise definitions for all core concepts

4. **[Unified Architecture Guide](/architecture/unified-architecture-guide)** (60 min)
   - How all 12 SIL projects fit together
   - Layer-by-layer implementation details
   - Integration patterns and data flow

### Outcome

You'll understand the technical depth: how SIL achieves explicit meaning, stable memory, and verifiable provenance.

---

## Path 3: Hands-On Builder (45 minutes)

**Goal:** Use SIL tools immediately and understand how to build with them

### Prerequisites
- Basic command-line familiarity
- Python or general programming background

### Action Sequence

1. **[Quickstart](/foundations/quickstart)** (10 min)
   - Install Reveal
   - Try progressive disclosure hands-on
   - Experience semantic structure exploration

2. **[Reveal Documentation](/systems/reveal)** (15 min)
   - Complete feature guide
   - Semantic navigation patterns
   - Pipeline composition with git, find, jq

3. **[Agent Help Standard](/research/agent-help-standard)** (20 min)
   - How to make CLI tools agent-friendly
   - The `--agent-help` pattern
   - Examples from production tools

4. **[Progressive Disclosure Guide](/research/progressive-disclosure-guide)** (30 min)
   - Theory behind progressive disclosure
   - Token efficiency analysis
   - Workflow patterns

### Outcome

You'll have working tools installed and understand how to build agent-friendly infrastructure.

---

## Path 4: Research Deep-Dive (2-3 hours)

**Goal:** Understand SIL's research contributions and theoretical foundations

### Prerequisites
- Path 2 (Technical Understanding)
- Background in semantics, type theory, or knowledge representation

### Reading Sequence

1. **Research Papers** (90 min total)
   - [Semantic Feedback Loops](/research/semantic-feedback-loops) (30 min)
   - [Semantic Observability](/research/semantic-observability) (30 min)
   - [RAG as Semantic Manifold Transport](/research/rag-as-semantic-manifold-transport) (30 min)

2. **Framework Documents** (60 min total)
   - [Hierarchical Agency Framework](/research/hierarchical-agency-framework) (30 min)
   - [Multi-Agent Protocol Principles](/research/multi-agent-protocol-principles) (30 min)

3. **Research Agenda** (20 min)
   - [Research Agenda Year 1](/research/research-agenda-year-1)
   - Open problems and directions

### Outcome

You'll understand SIL's theoretical foundations and research trajectory.

---

## Path 5: Innovation Portfolio (1 hour)

**Goal:** See all production tools and techniques SIL has built

### Reading Sequence

1. **[Innovation Overview](/systems/overview)** (10 min)
   - Summary of all innovations
   - Impact metrics and adoption

2. **Production Tools** (30 min)
   - [Reveal](/systems/reveal) — Progressive disclosure for code
   - [Morphogen](/systems/morphogen) — Cross-domain unified primitives
   - [Pantheon](/systems/pantheon) — Universal typed IR

3. **Key Techniques** (20 min)
   - [Progressive Disclosure](/research/progressive-disclosure-guide)
   - [Agent Ether](/systems/agent-ether)
   - [GenesisGraph](/systems/genesisgraph) — Cryptographic provenance

### Outcome

You'll see concrete evidence of SIL's working infrastructure and production impact.

---

## Path 6: Founder & Philosophy (45 minutes)

**Goal:** Understand the vision, values, and human context behind SIL

### Reading Sequence

1. **[Founder's Letter](/foundations/founders-letter)** (10 min)
   - Personal perspective on why SIL exists
   - The gap SIL fills in AI infrastructure

2. **[Founder Background](/meta/founder-background)** (10 min)
   - Working systems and production metrics
   - Track record of semantic infrastructure

3. **[Influences & Acknowledgments](/meta/influences-and-acknowledgments)** (15 min)
   - Intellectual lineage
   - Who and what shaped SIL's approach

4. **[Stewardship Manifesto](/meta/stewardship-manifesto)** (20 min)
   - Values and governance
   - Long-term commitments and accountability

### Outcome

You'll understand the human context, values, and long-term vision behind the technical work.

---

## Path 7: Complete Mastery (4-6 hours)

**Goal:** Comprehensive understanding of all SIL work

### Sequence

Follow paths in order:
1. Path 1: Essentials (30 min)
2. Path 2: Technical Understanding (1.5 hr)
3. Path 3: Hands-On Builder (45 min)
4. Path 4: Research Deep-Dive (2-3 hr)
5. Path 5: Innovation Portfolio (1 hr)
6. Path 6: Founder & Philosophy (45 min)

### Additional Reading
- [FAQ](/meta/faq) — Common questions
- [Safety Thresholds](/meta/safety-thresholds) — Risk management
- [Project Index](../projects/project-index) — All 12 projects detailed

### Outcome

Complete understanding of SIL's mission, architecture, research, tools, and governance.

---

## Document Categories

### 📚 Canonical
Core foundational documents defining SIL's mission, principles, and architecture.
→ [View all canonical docs](/foundations/overview)

### 🔬 Research
Research contributions and theoretical frameworks.
→ [View research directory](/research/overview)

### 🛠 Tools
Documentation for production tools (Reveal, TIA, Beth).
→ [View tools directory](/systems/overview)

### 🏗 Architecture
Technical architecture and system design.
→ [View architecture docs](/architecture/overview)

### 💡 Innovations
Innovation portfolio — techniques and tools built.
→ [View innovations](/systems/overview)

### 👤 Meta
About the founder, influences, FAQ.
→ [View meta directory](/meta/overview)

### 📦 Projects
All 12 SIL projects detailed.
→ [View project index](../projects/project-index)

---

## How to Navigate

### If you want to...

**Understand the vision**
→ [Manifesto](/manifesto/yolo), [Founder's Letter](/foundations/founders-letter)

**See technical depth**
→ [Semantic OS Architecture](/foundations/semantic-os-architecture), [Technical Charter](/foundations/technical-charter)

**Try it hands-on**
→ [Quickstart](/foundations/quickstart), [Reveal Docs](/systems/reveal)

**Review research**
→ [Research Directory](/research/overview), [Research Agenda](/research/research-agenda-year-1)

**Understand governance**
→ [Stewardship Manifesto](/meta/stewardship-manifesto), [Safety Thresholds](/meta/safety-thresholds)

**See what's built**
→ [Project Index](../projects/project-index), [Innovation Portfolio](/systems/overview)

**Get questions answered**
→ [FAQ](/meta/faq), [Glossary](/foundations/glossary)

---

## Tips for Reading

1. **Keep the Glossary open** — [SIL_GLOSSARY.md](/foundations/glossary) defines all 108 terms
2. **Follow the breadcrumbs** — Each doc has "Related Reading" sections
3. **Use progressive disclosure** — Start with summaries, drill into details as needed
4. **Reference the principles** — The [14 principles](/foundations/design-principles) guide everything
5. **Try the tools** — Understanding deepens when you use Reveal yourself

---

## Still Have Questions?

- **[FAQ](/meta/faq)** — Common questions answered
- **[START_HERE](/foundations/start-here)** — Single front door to all content
- **[GitHub](https://github.com/semantic-infrastructure-lab)** — Source code and issues

---

**Welcome to the Semantic Infrastructure Lab. Choose your path and begin.**
