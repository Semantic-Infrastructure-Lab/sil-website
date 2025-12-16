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

1. **[START_HERE](canonical/START_HERE.md)** (5 min)
   - The single front door to SIL
   - Overview of architecture, tools, and philosophy

2. **[Manifesto](canonical/SIL_MANIFESTO.md)** (15 min)
   - The problem: AI without semantic substrate
   - What SIL builds and why it matters
   - **Start here** if you read only one document

3. **[Principles](canonical/SIL_PRINCIPLES.md)** (10 min)
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

1. **[Semantic OS Architecture](canonical/SIL_SEMANTIC_OS_ARCHITECTURE.md)** (30 min)
   - The 7-layer architecture (Semantic Memory → Agent Orchestration)
   - How layers compose and interact
   - Design invariants and guarantees

2. **[Technical Charter](canonical/SIL_TECHNICAL_CHARTER.md)** (45 min)
   - Formal specification of invariants
   - Semantic contracts and provenance requirements
   - Verifiability guarantees

3. **[Glossary](canonical/SIL_GLOSSARY.md)** (Reference)
   - Keep open while reading — 108 canonical terms
   - Precise definitions for all core concepts

4. **[Unified Architecture Guide](architecture/UNIFIED_ARCHITECTURE_GUIDE.md)** (60 min)
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

1. **[Quickstart](QUICKSTART.md)** (10 min)
   - Install Reveal
   - Try progressive disclosure hands-on
   - Experience semantic structure exploration

2. **[Reveal Documentation](tools/REVEAL.md)** (15 min)
   - Complete feature guide
   - Semantic navigation patterns
   - Pipeline composition with git, find, jq

3. **[Agent Help Standard](research/AGENT_HELP_STANDARD.md)** (20 min)
   - How to make CLI tools agent-friendly
   - The `--agent-help` pattern
   - Examples from production tools

4. **[Progressive Disclosure Guide](canonical/PROGRESSIVE_DISCLOSURE_GUIDE.md)** (30 min)
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
   - [Semantic Feedback Loops](canonical/SEMANTIC_FEEDBACK_LOOPS.md) (30 min)
   - [Semantic Observability](canonical/SEMANTIC_OBSERVABILITY.md) (30 min)
   - [RAG as Semantic Manifold Transport](research/RAG_AS_SEMANTIC_MANIFOLD_TRANSPORT.md) (30 min)

2. **Framework Documents** (60 min total)
   - [Hierarchical Agency Framework](canonical/HIERARCHICAL_AGENCY_FRAMEWORK.md) (30 min)
   - [Multi-Agent Protocol Principles](canonical/MULTI_AGENT_PROTOCOL_PRINCIPLES.md) (30 min)

3. **Research Agenda** (20 min)
   - [Research Agenda Year 1](canonical/SIL_RESEARCH_AGENDA_YEAR1.md)
   - Open problems and directions

### Outcome

You'll understand SIL's theoretical foundations and research trajectory.

---

## Path 5: Innovation Portfolio (1 hour)

**Goal:** See all production tools and techniques SIL has built

### Reading Sequence

1. **[Innovation Overview](innovations/INNOVATIONS.md)** (10 min)
   - Summary of all innovations
   - Impact metrics and adoption

2. **Production Tools** (30 min)
   - [Reveal](tools/REVEAL.md) — Progressive disclosure for code
   - [Morphogen](innovations/MORPHOGEN.md) — Cross-domain unified primitives
   - [Pantheon](innovations/PANTHEON.md) — Universal typed IR

3. **Key Techniques** (20 min)
   - [Progressive Disclosure](innovations/PROGRESSIVE_DISCLOSURE.md)
   - [Agent Ether](innovations/AGENT_ETHER.md)
   - [GenesisGraph](innovations/GENESISGRAPH.md) — Cryptographic provenance

### Outcome

You'll see concrete evidence of SIL's working infrastructure and production impact.

---

## Path 6: Founder & Philosophy (45 minutes)

**Goal:** Understand the vision, values, and human context behind SIL

### Reading Sequence

1. **[Founder's Letter](canonical/FOUNDERS_LETTER.md)** (10 min)
   - Personal perspective on why SIL exists
   - The gap SIL fills in AI infrastructure

2. **[Founder Background](meta/FOUNDER_BACKGROUND.md)** (10 min)
   - Working systems and production metrics
   - Track record of semantic infrastructure

3. **[Influences & Acknowledgments](meta/INFLUENCES_AND_ACKNOWLEDGMENTS.md)** (15 min)
   - Intellectual lineage
   - Who and what shaped SIL's approach

4. **[Stewardship Manifesto](canonical/SIL_STEWARDSHIP_MANIFESTO.md)** (20 min)
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
- [FAQ](meta/FAQ.md) — Common questions
- [Safety Thresholds](canonical/SIL_SAFETY_THRESHOLDS.md) — Risk management
- [Project Index](../projects/PROJECT_INDEX.md) — All 12 projects detailed

### Outcome

Complete understanding of SIL's mission, architecture, research, tools, and governance.

---

## Document Categories

### 📚 Canonical
Core foundational documents defining SIL's mission, principles, and architecture.
→ [View all canonical docs](canonical/README.md)

### 🔬 Research
Research contributions and theoretical frameworks.
→ [View research directory](research/README.md)

### 🛠 Tools
Documentation for production tools (Reveal, TIA, Beth).
→ [View tools directory](tools/README.md)

### 🏗 Architecture
Technical architecture and system design.
→ [View architecture docs](architecture/README.md)

### 💡 Innovations
Innovation portfolio — techniques and tools built.
→ [View innovations](innovations/INNOVATIONS.md)

### 👤 Meta
About the founder, influences, FAQ.
→ [View meta directory](meta/)

### 📦 Projects
All 12 SIL projects detailed.
→ [View project index](../projects/PROJECT_INDEX.md)

---

## How to Navigate

### If you want to...

**Understand the vision**
→ [Manifesto](canonical/SIL_MANIFESTO.md), [Founder's Letter](canonical/FOUNDERS_LETTER.md)

**See technical depth**
→ [Semantic OS Architecture](canonical/SIL_SEMANTIC_OS_ARCHITECTURE.md), [Technical Charter](canonical/SIL_TECHNICAL_CHARTER.md)

**Try it hands-on**
→ [Quickstart](QUICKSTART.md), [Reveal Docs](tools/REVEAL.md)

**Review research**
→ [Research Directory](research/README.md), [Research Agenda](canonical/SIL_RESEARCH_AGENDA_YEAR1.md)

**Understand governance**
→ [Stewardship Manifesto](canonical/SIL_STEWARDSHIP_MANIFESTO.md), [Safety Thresholds](canonical/SIL_SAFETY_THRESHOLDS.md)

**See what's built**
→ [Project Index](../projects/PROJECT_INDEX.md), [Innovation Portfolio](innovations/INNOVATIONS.md)

**Get questions answered**
→ [FAQ](meta/FAQ.md), [Glossary](canonical/SIL_GLOSSARY.md)

---

## Tips for Reading

1. **Keep the Glossary open** — [SIL_GLOSSARY.md](canonical/SIL_GLOSSARY.md) defines all 108 terms
2. **Follow the breadcrumbs** — Each doc has "Related Reading" sections
3. **Use progressive disclosure** — Start with summaries, drill into details as needed
4. **Reference the principles** — The [14 principles](canonical/SIL_PRINCIPLES.md) guide everything
5. **Try the tools** — Understanding deepens when you use Reveal yourself

---

## Still Have Questions?

- **[FAQ](meta/FAQ.md)** — Common questions answered
- **[START_HERE](canonical/START_HERE.md)** — Single front door to all content
- **[GitHub](https://github.com/semantic-infrastructure-lab)** — Source code and issues

---

**Welcome to the Semantic Infrastructure Lab. Choose your path and begin.**
