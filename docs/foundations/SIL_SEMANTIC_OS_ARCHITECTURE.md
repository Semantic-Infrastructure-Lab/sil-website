---
tier: 3
order: 1
beth_topics:
  - sil
  - architecture
  - semantic-os
  - layers
  - infrastructure
  - provenance-first
  - invariants
updated: 2025-12-20
architecture_decision: Provenance-First model adopted (Dec 15, 2025)
---

# SIL Semantic OS Architecture

**Version:** 3.0 (December 2025)
**Architecture Model:** Provenance-First with Invariants Over Layers
**Canonical Reference:** [SIL_GLOSSARY.md](/foundations/glossary)

---

## TL;DR (2-minute overview)

**What is the Semantic OS?** A semantic infrastructure for human-AI coexistence—organized around provenance, meaning, and trust.

**The core insight:** Just as Unix made "everything is a file" the foundational abstraction, Semantic OS makes "everything has provenance and meaning" the foundational guarantee.

### The Provenance-First Layer Model

```
L6: Reflection       Learning from execution (observability)
L5: Execution        Agents working under constraints
L4: Composition      Cross-domain integration (Pantheon IR)
L3: Intent           What we're accomplishing (contracts)
L2: Trust            Who can do what (TAP, Authorization)
L1: Meaning          Embeddings, types, similarity (Beth)
L0: Provenance       Everything has lineage (GenesisGraph)
─────────────────────────────────────────────────────────────
L-1: Substrate       Physical/computational reality (Philbrick, optional)
```

**Key innovations:**
- **Provenance-first foundation** — Every artifact has cryptographic lineage
- **Trust as architecture** — Authorization explicit, not implicit
- **Glass Box reasoning** — All decisions inspectable (Reveal)
- **Deterministic execution** — Reproducible workflows (Morphogen)
- **Sustainable efficiency** — 100x token reduction proven

> 💡 **New to SIL?** Read [The Five Invariants](#the-five-invariants) first, then explore the layers.

---

## Architecture Decision (December 2025)

This document reflects the **Provenance-First architecture** adopted December 15-20, 2025, following rigorous evaluation of competing models.

**Why this model?**
- **Scored highest** (4.15 vs 3.05) on problem fit, clarity, and coherence
- **Mission-aligned** — Directly addresses LLM coexistence and human-AI collaboration
- **Founder intuition** — "Provenance when I hear Semantic OS"
- **Problem-centric** — Solves "how do we trust AI?" not "where do projects fit?"

**Decision rationale**: See [ARCHITECTURE_DECISION.md](/architecture/decisions/ARCHITECTURE_DECISION)

---

## The Five Invariants (Mission-Critical Guarantees)

Before diving into layers, understand the **invariants** — guarantees that must hold everywhere in the system:

| Invariant | What It Prevents | Enforcement | Status |
|-----------|------------------|-------------|--------|
| **Everything has lineage** | Epistemic collapse | GenesisGraph v0.3.0 | ✅ Production |
| **Reasoning is inspectable** | Black box dictatorship | Reveal v0.25.0 | ✅ Production |
| **Computation is grounded** | Hallucinated science | Morphogen v0.12.0 | 🟡 Prototype |
| **Contracts are explicit** | Brittle complexity | Agent Ether 0.1.0-alpha | 🔴 Spec only |
| **Efficiency is sustainable** | Compute as privilege | Beth + Reveal | ✅ Production |

**Overall Enforcement:** 67% (3.5/5 invariants production-ready)

**Known Gap:** Agent Ether is specification-only (no implementation yet). See [Agent Ether Roadmap](#agent-ether-implementation-priority).

### How Layers and Invariants Relate

**Use layers for:**
- Organizing documentation
- Explaining how tools relate
- Onboarding new contributors
- Navigating the codebase

**Use invariants for:**
- Architectural decisions
- Design reviews
- Mission alignment checks
- "Should we build X?" questions

Both are needed. Layers organize structure; invariants enforce mission.

---

## Layer 0: Provenance (Everything Has Lineage)

**Purpose:** Cryptographic chain of custody for every digital artifact — the foundation of trust.

**Why L0?** Without provenance, you can't trust LLM output, verify scientific results, or audit algorithmic decisions. Provenance isn't optional infrastructure—it's the bedrock.

### Core Capabilities

**GenesisGraph (v0.3.0 Production)**

1. **Cryptographic Attestation**
   - Ed25519 signatures for identity
   - DID resolution for decentralized identifiers
   - Certificate Transparency for public verification
   - SD-JWT for selective disclosure

2. **Immutable Lineage Tracking**
   - Every artifact linked to its source
   - Full derivation history: inputs → transformations → outputs
   - Content-addressable storage (hash = identifier)
   - Temporal versioning (knowledge evolves, lineage preserved)

3. **Verification Without Recomputation**
   - Third parties can verify claims without re-running expensive computations
   - Cryptographic proofs of correctness
   - Audit trails for regulatory compliance

### Design Principles

**Provenance-First:**
- Every assertion includes source metadata
- No "trust me" — always "verify the math"
- Reproducible derivations

**Privacy-Preserving:**
- Selective disclosure (show lineage without revealing sensitive data)
- Zero-knowledge proofs where appropriate
- DID-based sovereignty (users control their identity)

### Example Use Cases

**Scientific Reproducibility:**
- Researcher publishes paper with GenesisGraph provenance
- Other researchers verify claims cryptographically
- Replication crisis addressed through verifiable lineage

**Deepfake Detection:**
- Real photos/videos have provenance metadata
- Synthetic media lacks cryptographic attestation
- "Where did this come from?" becomes answerable

**Algorithmic Accountability:**
- Medical diagnosis AI shows provenance of training data and decision inputs
- Patients/doctors can audit the reasoning chain
- Regulators verify compliance without access to proprietary models

---

## Layer 1: Meaning (Semantic Understanding)

**Purpose:** Embeddings, types, similarity, and semantic search — how we understand what things mean.

**Why L1?** Provenance tells us "where," but meaning tells us "what." This layer enables semantic queries, concept discovery, and cross-domain understanding.

### Core Capabilities

**Beth (Production)**

1. **Semantic Indexing**
   - 14,549 files indexed across 60 projects
   - 1,402 topics automatically discovered
   - 30,026 keywords with strength scores

2. **Similarity Search**
   - Find similar documents/concepts across domains
   - Embedding-based retrieval
   - Topic clustering and exploration

3. **Efficient Discovery**
   - 25x token reduction measured across 300+ sessions
   - Progressive disclosure (structure before detail)
   - Breadth-first knowledge navigation

**Pantheon IR (Type System)**

1. **Universal Semantic Types**
   - Primitive types (integers, floats, strings, timestamps)
   - Composite types (structs, unions, algebraic data types)
   - Semantic types (entities, relationships, events)
   - Provenance types (lineage as first-class citizen)

2. **Cross-Domain Translation**
   - Domain-specific schema → Pantheon IR
   - Lossless round-tripping where possible
   - Graceful degradation when perfect translation impossible

### Design Principles

**Type-Safe:**
- Semantic operations type-check before execution
- Formal verification of translations
- Clear error messages when things don't type

**Human-Readable:**
- Pantheon IR can be read/written by humans
- Good error messages
- Self-documenting schemas

### Example Use Cases

**Knowledge Discovery:**
- "Find all work related to provenance and trust" (Beth semantic search)
- Results ranked by relevance, grouped by topic
- Progressive disclosure (titles → abstracts → full content)

**Cross-Domain Queries:**
- "Which healthcare facilities are downstream of this water treatment plant?"
- Requires joining Water and Healthcare schemas via Pantheon IR
- Type system ensures coherent composition

---

## Layer 2: Trust (Who Can Do What)

**Purpose:** Authorization, access control, and trust frameworks — making "who can do what" explicit.

**Why L2?** LLM coexistence requires explicit trust models. This layer makes authorization architectural, not an afterthought.

### Core Capabilities

**Trust Assertion Protocol (TAP)**

1. **Capability-Based Security**
   - Agents hold capabilities (cryptographic tokens granting permissions)
   - No ambient authority (must prove right to access)
   - Fine-grained access control

2. **Trust Metrics**
   - Reputation scores for agents
   - Historical performance tracking
   - Verification records

3. **Hierarchical Agency**
   - Delegation chains (principal → deputy → sub-deputy)
   - Auditable authority transfer
   - Revocation mechanisms

### Design Principles

**Explicit Over Implicit:**
- No hidden permissions
- Clear authorization chains
- Auditable access logs

**Privacy-Preserving:**
- Selective disclosure (prove authority without revealing all credentials)
- Zero-knowledge proofs for sensitive operations

### Example Use Cases

**Multi-Agent Collaboration:**
- AI agent requests access to dataset
- TAP checks: Does agent have capability token?
- If yes: access granted with audit log
- If no: request escalates to human approval

**Regulated Data Access:**
- Healthcare AI needs patient data for diagnosis
- TAP verifies: proper authorization + audit trail + consent
- Access granted only with full compliance chain

---

## Layer 3: Intent (What We're Accomplishing)

**Purpose:** Contracts, constraints, and specifications — making assumptions explicit.

**Why L3?** Multi-agent systems fail when assumptions are implicit. This layer makes "what should happen" clear and verifiable.

### Core Capabilities

**Agent Ether (0.1.0-alpha, Specification Only)**

🔴 **STATUS: Known Gap** — Agent Ether is currently specification-only with no implementation. This is the highest-priority gap in our architecture.

**Planned Capabilities (Specification):**

1. **Tool Behavior Contracts**
   - Inputs, outputs, preconditions, postconditions
   - Invariant declarations
   - Type-safe tool composition

2. **Agent Registry**
   - Capability advertisement ("I can analyze water networks")
   - Discovery mechanisms
   - Reputation tracking

3. **Protocol Suite**
   - Task delegation
   - Negotiation
   - Composition (complex workflows from simple capabilities)
   - Verification

### Design Principles

**Contracts Over Chaos:**
- All assumptions explicit
- Failures loud and early, not silent and late
- Deterministic tool use (no "vibes-based" coordination)

**Heterogeneous Agents:**
- Human and AI agents collaborate
- Type-safe communication via Pantheon IR
- Fault-tolerant coordination

### Implementation Priority

**Agent Ether Roadmap:**
- **Phase 1:** Registry + Metadata (4 weeks)
- **Phase 2:** Contract Validation (4 weeks)
- **Phase 3:** Runtime Enforcement (8 weeks)

See [Agent Ether Implementation Priority](#agent-ether-implementation-priority) for details.

---

## Layer 4: Composition (Cross-Domain Integration)

**Purpose:** Combining knowledge and capabilities across domains — making different systems talk.

**Why L4?** Real problems span domains (water + healthcare, education + governance). This layer enables cross-domain reasoning.

### Core Capabilities

**Pantheon IR (Composition Operators)**

1. **Semantic Composition**
   - Merge (combining knowledge from multiple sources)
   - Join (relating entities across domains)
   - Transform (applying functions to semantic data)
   - Validate (checking constraints and invariants)

2. **Domain Integration**
   - Water module ↔ Healthcare module via Pantheon IR
   - Automatic schema alignment
   - Conflict resolution

**SUP (Semantic UI Platform)**

1. **UI Component Composition**
   - Reusable semantic UI primitives
   - Cross-project component library
   - Consistent user experiences

### Example Use Cases

**Multi-Domain Analysis:**
- Water anomaly detection → Healthcare waterborne illness correlation
- Automatic cross-domain query via Pantheon IR
- Results composed into unified view

**Policy Simulation:**
- Governance module expresses policy in Pantheon IR
- Executable simulation in Morphogen (L5)
- Results visualized in SUP

---

## Layer 5: Execution (Doing Work Under Constraints)

**Purpose:** Deterministic, reproducible computation — making results verifiable.

**Why L5?** Scientific reproducibility and trust require deterministic execution. This layer makes "it works on my machine" obsolete.

### Core Capabilities

**Morphogen (v0.12.0 Prototype)**

1. **Hermetic Execution**
   - All dependencies explicitly declared
   - No hidden state or side effects
   - Sandboxed execution

2. **Content-Addressable Caching**
   - Results stored by hash of (inputs + code)
   - Identical inputs + code → cached result (no recomputation)
   - Massive speedup for repeated analyses

3. **Cryptographic Verification**
   - Every computation produces proof of correctness
   - Third parties verify without re-running
   - Audit trails for compliance

4. **Domain Grounding**
   - 39 production domains (physics, chemistry, CAD, etc.)
   - 1,705 tests ensuring correctness
   - Grounded in real math, not text approximations

### Design Principles

**Reproducibility First:**
- Same inputs + code → same outputs (always)
- Cryptographic proof of execution
- Full lineage tracking (GenesisGraph integration at L0)

**Performance Through Caching:**
- Determinism enables aggressive caching
- Mature systems: vast majority of computations are cache hits

### Example Use Cases

**Scientific Analysis:**
- Researcher analyzes dataset with Morphogen
- Results reproducible by anyone
- Published with cryptographic proof

**Infrastructure Optimization:**
- Water module optimizes pump schedules
- Deterministic and auditable
- Regulators verify without re-running expensive optimization

---

## Layer 6: Reflection (Learning From Execution)

**Purpose:** Observability, feedback loops, and learning — understanding what happened and why.

**Why L6?** Systems improve through reflection. This layer makes "why did this happen?" answerable.

### Core Capabilities

**Reveal (v0.25.0 Production)**

1. **Progressive Disclosure**
   - Structure-first exploration (file outline → specific function)
   - 10-150x token reduction proven
   - 27 file analyzers (Python, TypeScript, Rust, etc.)

2. **AST-Based Queries**
   - "Show me all functions that call X"
   - "Find classes implementing interface Y"
   - Semantic code navigation

3. **Provenance Visualization**
   - Show lineage of decisions
   - Trace execution paths
   - Audit algorithmic reasoning

**Semantic Observability**

1. **Intent-Execution Alignment**
   - Did execution match intent?
   - Where did deviations occur?
   - Feedback for improvement

2. **Uncertainty Tracking**
   - Confidence scores for predictions
   - Probabilistic assertions
   - "I don't know" instead of hallucination

### Example Use Cases

**Debugging Complex Workflows:**
- Multi-agent system fails at step 27
- Reveal shows execution trace
- Provenance identifies: input from Agent 5 was malformed
- Fix: add contract validation at Agent 5 (back to L3)

**Algorithmic Accountability:**
- Citizen questions loan denial
- Reveal shows decision tree
- Provenance traces inputs
- Human auditor verifies reasoning was sound

---

## Layer L-1: Substrate (Optional Physical Foundation)

**Purpose:** Physical and computational substrate — hardware, energy, physics.

**Why Optional?** Most Semantic OS operations are software-only. But for some applications (analog computing, edge devices), substrate matters.

### Core Capabilities

**Philbrick (Analog Computing, Planned)**

1. **Hardware-Software Co-Design**
   - Analog circuits for specific computations
   - Hybrid analog-digital systems
   - Energy-efficient specialized hardware

2. **Physical Grounding**
   - Direct physical measurement (not digitized approximation)
   - Real-time analog processing
   - Ultra-low latency

### Status

🟡 **Philbrick is vision-tier** (12-24 month timeline). Not blocking current work.

---

## Cross-Cutting Concerns

### 1. Provenance Everywhere

Provenance (L0) flows through all layers:
- L1 (Meaning): Provenance of knowledge sources
- L2 (Trust): Provenance of authorization chains
- L3 (Intent): Provenance of contracts and specifications
- L4 (Composition): Provenance of composed results
- L5 (Execution): Provenance of computations (GenesisGraph integration)
- L6 (Reflection): Provenance visualization

### 2. Security and Privacy

- L0: Cryptographic attestation
- L1: Type-safe operations
- L2: Capability-based security
- L3: Contract enforcement
- L4: Cross-domain access control
- L5: Sandboxed execution
- L6: Audit logs

### 3. Efficiency and Sustainability

- L0: Content-addressable deduplication
- L1: Semantic search (vs brute-force)
- L2: Minimal credential disclosure
- L3: Declarative contracts (vs imperative coordination)
- L4: Shared infrastructure
- L5: Aggressive caching
- L6: Progressive disclosure (Reveal: 100x reduction)

---

## Tools Span Layers (Not "In" Layers)

**Critical Insight:** Tools are like Unix utilities—they span multiple layers based on function.

| Tool | Layers Touched | Function |
|------|----------------|----------|
| **GenesisGraph** | L0 (primary) + all layers | Provenance tracking |
| **Beth** | L1 (Meaning) + L0 (Provenance of knowledge) | Semantic search |
| **Reveal** | L6 (Reflection) + L4 (Composition structure) | Progressive disclosure |
| **TIA** | L3 (Intent) + L5 (Execution) + L6 (Reflection) | Agent orchestration |
| **Morphogen** | L5 (Execution) + L1 (Domain types) | Deterministic computation |
| **Agent Ether** | L3 (Intent) + L2 (Trust) | Multi-agent coordination |

This explains why historical "where does X go?" debates were intractable—we were asking the wrong question.

---

## The Chief Scientist Test (Design Review Checklist)

Before approving architectural decisions, ask these six questions:

1. **Provenance:** Does this maintain traceable lineage?
2. **Transparency:** Is reasoning inspectable?
3. **Grounding:** Is computation connected to reality?
4. **Contracts:** Are assumptions explicit?
5. **Efficiency:** Is this sustainable at scale?
6. **Agency:** Does this keep humans as conductors?

If any answer is "no" or "unclear," revise the architecture.

---

## Agent Ether Implementation Priority

**Current Status:** 0.1.0-alpha (specification only, no implementation)

**Gap Impact:** "Contracts are explicit" invariant cannot be enforced today. Brittle complexity (one of the five structural failures SIL committed to fix) is NOT being prevented architecturally.

**Roadmap:**

### Phase 1: Registry + Metadata (4 weeks)
- Agent registry database
- Capability advertisement API
- Discovery mechanisms
- Basic metadata schema

**Deliverable:** Agents can register and discover each other

### Phase 2: Contract Validation (4 weeks)
- Tool Behavior Contract schema (Pantheon IR)
- Static validation of contracts
- Type checking
- Contract composition rules

**Deliverable:** Contracts can be declared and validated

### Phase 3: Runtime Enforcement (8 weeks)
- Runtime contract checking
- Precondition/postcondition verification
- Invariant monitoring
- Failure handling

**Deliverable:** Contracts enforced during execution

**Total Timeline:** 16 weeks (Q1 2026)

**Priority:** CRITICAL — This is the only invariant without enforcement tooling.

---

## Migration from Previous Models

**Previous Canonical Model:**
- L0: Substrate (Philbrick hardware)
- Product-centric ("where do our 12 projects fit?")
- Scored 3.05 in evaluation

**Current Provenance-First Model:**
- L0: Provenance (GenesisGraph)
- Problem-centric ("how do we trust AI?")
- Scored 4.15 in evaluation

**Why the change?**
- Provenance is foundational for LLM coexistence
- Hardware is necessary but not the semantic foundation
- Founder intuition: "Provenance when I hear Semantic OS"
- Mission alignment: addresses epistemic collapse directly

**What stayed the same:**
- Seven primary layers (L0-L6) + optional substrate (L-1)
- Cross-cutting concerns (provenance, trust, observability)
- Modular, open, interoperable design

**Migration Guide:** Existing projects map cleanly to new model. Tools that were "in" layers now explicitly "span" layers.

---

## Comparison to Traditional OS

| Traditional OS | Semantic OS |
|----------------|-------------|
| **Processes** | Agents (human + AI) |
| **Memory** | Semantic Knowledge (L1) |
| **File System** | Provenance Repository (L0) |
| **Kernel** | Pantheon IR + Morphogen (L4-L5) |
| **Security** | Trust Layer (L2) + TAP |
| **Device Drivers** | Domain Modules (via L4) |
| **System Calls** | Agent Ether Protocols (L3) |
| **Shell/GUI** | Reflection Tools (L6: Reveal, TIA) |

Just as Linux abstracts hardware and provides common services for applications, Semantic OS abstracts knowledge work and provides common services for human-AI collaboration.

---

## Architectural Principles

### 1. Provenance-First
- Every artifact has cryptographic lineage
- "Where did this come from?" always answerable
- Trust built on verification, not promises

### 2. Glass Box Over Black Box
- All reasoning inspectable
- Progressive disclosure (structure → detail)
- "Show your work" is mandatory, not optional

### 3. Mission Over Product
- Architecture serves "prevent the worst day"
- Invariants enforce mission alignment
- Layers organize, invariants decide

### 4. Modular and Open
- Each layer independently useful
- Well-defined interfaces
- Open source (Apache 2.0, MIT)

### 5. Long-Term Thinking
- Built for decades, not quarters
- Stable APIs
- Backwards compatibility guarantees

---

## Conclusion

The Semantic OS is **infrastructure for human-AI coexistence**. The Provenance-First architecture provides:

**Seven Layers:**
- **L0 Provenance** — Cryptographic lineage for every artifact (GenesisGraph)
- **L1 Meaning** — Semantic understanding and types (Beth, Pantheon IR)
- **L2 Trust** — Explicit authorization (TAP)
- **L3 Intent** — Contracts and specifications (Agent Ether - gap)
- **L4 Composition** — Cross-domain integration (Pantheon IR)
- **L5 Execution** — Deterministic computation (Morphogen)
- **L6 Reflection** — Learning from execution (Reveal)
- **L-1 Substrate** — Physical foundation (Philbrick - optional)

**Five Invariants:**
- Everything has lineage (prevents epistemic collapse)
- Reasoning is inspectable (prevents black box dictatorship)
- Computation is grounded (prevents hallucinated science)
- Contracts are explicit (prevents brittle complexity)
- Efficiency is sustainable (prevents compute as privilege)

**Current Status:**
- 67% invariant enforcement (3.5/5 production-ready)
- Known gap: Agent Ether (spec only, 16-week roadmap)
- Production tools: GenesisGraph, Reveal, Beth
- Prototype: Morphogen (aggressive v1.0 timeline Q2 2026)

This is the technical core of SIL's mission: **building Timeline B (Glass Box future) instead of defaulting to Timeline A (Grey Fog)**.

---

**Related Documents:**
- [SIL Glossary](/foundations/glossary) — Canonical terminology
- [Architecture Decision Record](/architecture/decisions/ARCHITECTURE_DECISION) — Why Provenance-First
- [The Fork: Two Futures for AI](/foundation/pitch/THE_FORK) — Five structural failures to fix
- [Scope of Hope](/foundation/SCOPE_OF_HOPE) — Five pillars of semantic infrastructure
- [Invariants Over Layers](/architecture/invariants-over-layers) — Mission-centric frame
- [Model Evaluation](/architecture/model-evaluation) — Scoring rationale (4.15)

**Last Updated:** 2025-12-20
**Architecture Version:** 3.0 (Provenance-First)
