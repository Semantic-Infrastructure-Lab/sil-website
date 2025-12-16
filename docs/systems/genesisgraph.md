# GenesisGraph: Verifiable Provenance with Selective Disclosure

> *Proving how things were made—without revealing how you made them*

## The Problem

**The Certification vs. IP Protection Dilemma**

Industries face an impossible choice:

- **Regulators demand transparency:** "Show us your AI training data, model parameters, and decision process"
- **Businesses need IP protection:** "We can't reveal our proprietary pipeline or competitive advantages"
- **Current solution:** Choose between compliance and competitive moat

**Real-world blockers:**
- **AI/ML:** FDA wants to see model training process → Can't reveal proprietary architectures
- **Manufacturing:** ISO 9001 requires process documentation → Can't expose trade secret recipes
- **Research:** Journals require reproducibility → Can't share sensitive experimental data
- **Healthcare:** HIPAA compliance requires audit trails → Can't reveal patient information

**Result:** Regulated industries avoid adoption of advanced techniques because verification requires total transparency.

---

## The Innovation

**Three-level selective disclosure (A/B/C) solves the "certification vs IP" dilemma:**

GenesisGraph enables cryptographically verifiable provenance where you choose exactly what to reveal:

### Level A: Full Disclosure (Open Science)
**Use when:** Open source projects, public research, transparency required
```yaml
# Show everything: full pipeline, parameters, intermediate results
operations:
  - id: train
    tool: pytorch
    parameters:
      learning_rate: 0.001
      batch_size: 32
      epochs: 100
    inputs: [training_data]
    outputs: [model_v1]
```

### Level B: Partial Envelope (Verified Privacy)
**Use when:** Prove constraints without exact values
```yaml
# Reveal that constraints were met, hide exact parameters
operations:
  - id: train
    tool: pytorch
    sealed_parameters:
      # Hash of actual parameters
      digest: "sha256:abc123..."
      # Provable constraints
      constraints:
        - "learning_rate < 0.01"
        - "batch_size >= 16"
        - "epochs >= 50"
    inputs: [training_data]  # Can seal these too
    outputs: [model_v1]
```

### Level C: Sealed Subgraph (Zero-Knowledge)
**Use when:** Hide entire pipeline segments, prove policy compliance only
```yaml
# Replace proprietary pipeline with Merkle root commitment
sealed_subgraph:
  root_hash: "sha256:def456..."
  inputs: [raw_data]      # Show what went in
  outputs: [final_model]  # Show what came out
  policies:
    - claim: "FDA 21 CFR Part 11 compliant"
      signature: "..."
    - claim: "No PII in training data"
      signature: "..."
```

**The magic:** Cryptographic commitments (Merkle trees, hash chains) enable proving properties without revealing values.

---

## Quick Example: AI Model with Trade Secret Protection

**Scenario:** Train AI model with proprietary architecture, prove FDA compliance, protect IP.

```python
from genesisgraph import GenesisGraph, Entity, Operation, SealedSubgraph

gg = GenesisGraph(spec_version="0.3.0")

# Level A: Public data preprocessing (show everything)
gg.add_operation(Operation(
    id="preprocess",
    tool="pandas",
    parameters={"method": "normalize", "axis": 0},
    inputs=["raw_data"],
    outputs=["clean_data"]
))

# Level C: Proprietary training pipeline (seal completely)
gg.add_sealed_subgraph(SealedSubgraph(
    root_hash="sha256:abc123...",
    inputs=["clean_data"],
    outputs=["model_v1"],
    policies=[
        {"claim": "FDA 21 CFR Part 11 compliant", "signature": "..."},
        {"claim": "No patient PII in training data", "signature": "..."},
        {"claim": "Model accuracy > 95% on validation set", "signature": "..."}
    ]
))

# Level A: Public model evaluation (show everything)
gg.add_operation(Operation(
    id="evaluate",
    tool="sklearn",
    parameters={"metrics": ["accuracy", "f1"]},
    inputs=["model_v1", "test_data"],
    outputs=["evaluation_report"]
))

# Export provenance graph
gg.save_yaml("ai_pipeline.gg.yaml")
```

**What regulators see:**
- ✅ Complete audit trail (inputs → sealed training → outputs → evaluation)
- ✅ Cryptographic proof of policy compliance (FDA 21 CFR Part 11)
- ✅ Verifiable integrity (Merkle tree commitments)

**What competitors don't see:**
- ❌ Proprietary training architecture
- ❌ Hyperparameter optimization strategy
- ❌ Custom loss functions
- ❌ Data augmentation techniques

**Both verified with cryptographic certainty.**

---

## Status & Adoption

**Current Version:** v0.3.0 (Production-Ready)

**Production Metrics:**
- ✅ **320 comprehensive tests** across all modules
- ✅ **76% overall test coverage** (up from 71% in v0.2)
- ✅ **98% SD-JWT coverage** - IETF standard selective disclosure
- ✅ **99% BBS+ coverage** - Zero-knowledge credential proofs
- ✅ **97% ZKP templates coverage** - Range proofs, membership proofs
- ✅ **90% DID support** - Multi-method decentralized identity (did:key, did:web, did:ion, did:ethr)

**Novel Research Contributions:**

1. **Three-Level Selective Disclosure Model (A/B/C)**
   - Level A: Full transparency for open science
   - Level B: Constraint proofs without exact values (SD-JWT)
   - Level C: Sealed subgraphs with policy assertions (Merkle commitments)
   - **Industry first:** Unified framework spanning full transparency → zero-knowledge

2. **Merkle Tree Provenance Commitments**
   - Hash-only lineage for proprietary pipeline segments
   - Selective exposure of input/output digests
   - Optional inclusion proofs without revealing full tree
   - RFC 6962 transparency log integration

3. **Industry-Specific Profile Validators**
   - **gg-ai-basic-v1**: AI/ML pipeline validation (FDA 21 CFR Part 11 compliance)
   - **gg-cam-v1**: Computer-aided manufacturing (ISO 9001:2015 compliance)
   - Automated compliance checking for regulated industries

4. **Cryptographic Privacy Features**
   - SD-JWT (Selective Disclosure JWT) for claim-level privacy
   - BBS+ signatures with unlinkable selective disclosure
   - Holder binding prevents credential replay attacks
   - Predicate proofs (e.g., "age > 21" without revealing exact age)

**What This Unlocks:**
- **Regulated AI adoption** - FDA/EMA approval without IP disclosure
- **Manufacturing compliance** - ISO 9001 certification with trade secret protection
- **Research reproducibility** - Verify methods without sharing sensitive data
- **Healthcare audit trails** - HIPAA compliance with patient privacy

**SDKs Available:**
- Python SDK: `pip install genesisgraph` (93% coverage)
- JavaScript/TypeScript SDK: `npm install @genesisgraph/sdk`
- Full builder API, validation, DID resolution, signature verification

**v1.0 Release Timeline:** Active development
- Enterprise adoption (Fortune 500 pilots)
- Standards body submission (W3C, IETF)
- Blockchain integration (Ethereum, Hyperledger)

---

## Technical Deep Dive

**Full Documentation:**
- [GenesisGraph GitHub Repository](https://github.com/Semantic-Infrastructure-Lab/genesisgraph)
- [Complete Specification](https://github.com/Semantic-Infrastructure-Lab/genesisgraph/blob/main/docs/specifications/main-spec.md)
- [Disclosure Levels Guide](https://github.com/Semantic-Infrastructure-Lab/genesisgraph/blob/main/docs/user-guide/disclosure-levels.md) - A/B/C model explained
- [Selective Disclosure Cryptography](https://github.com/Semantic-Infrastructure-Lab/genesisgraph/blob/main/docs/user-guide/selective-disclosure.md) - SD-JWT, BBS+, ZKP
- [Profile Validators](https://github.com/Semantic-Infrastructure-Lab/genesisgraph/blob/main/docs/user-guide/profile-validators.md) - Industry compliance

**Example Gallery:**
- [AI/ML Pipelines](https://github.com/Semantic-Infrastructure-Lab/genesisgraph/blob/main/examples/level-a-full-disclosure.gg.yaml)
- [Manufacturing Workflows](https://github.com/Semantic-Infrastructure-Lab/genesisgraph/blob/main/examples/level-b-partial-envelope.gg.yaml)
- [Research Reproducibility](https://github.com/Semantic-Infrastructure-Lab/genesisgraph/blob/main/examples/level-c-sealed-subgraph.gg.yaml)

**Getting Started:**
```bash
pip install genesisgraph
genesisgraph validate workflow.gg.yaml --verify-profile
```

---

## Part of SIL's Semantic OS Vision

**GenesisGraph's Role in the 7-Layer Semantic OS:**

- **Layer 2 (Structures):** Provenance data structures
  - Directed acyclic graphs (DAGs) for process lineage
  - Merkle trees for cryptographic commitments
  - Hash chains for temporal ordering

- **Layer 3 (Composition):** Provenance graph composition
  - Graphs compose: Subgraphs seal and embed in larger workflows
  - Selective disclosure composes: Mix A/B/C levels in single graph
  - Policy assertions compose: Multiple compliance claims per operation

- **Cross-Cutting Concern:** Provenance infrastructure across all layers
  - Enables verifiable transformations at every layer (primitives → intelligence)
  - Universal audit trail for semantic operations
  - Foundation for trustworthy AI and autonomous systems

**Composes With:**
- **Pantheon (Layer 3):** Provenance-aware IR - Track semantic graph transformations
- **Morphogen (Layer 1/4):** Deterministic execution - Provenance for computational workflows
- **Agent Ether (Layer 6):** Multi-agent systems - Verifiable agent actions and decisions
- **Semantic Trust Fabric:** Trust assertions stored as typed graph edges with full provenance
- **IPFS Storage (Layer 0):** Content-addressed artifact storage - **See:** [Distributed Storage Architecture](../architecture/DISTRIBUTED_STORAGE_ARCHITECTURE.md) for integration strategy
- **All SIL projects:** Universal provenance layer enables "show your work" across the stack

---

## Trust Layer Integration

GenesisGraph serves as the storage layer for the **Trust Assertion Protocol (TAP)**. Trust Assertions become typed edges in the graph:

```yaml
# Trust assertion as GenesisGraph edge
edge:
  type: trust_assertion
  issuer: "did:key:z6Mk..."
  subject: "did:key:z6Mn..."
  claim:
    type: has-capability
    value: distributed-systems
    level: expert
  provenance:
    graph_node: "gg:node:12345"
    timestamp: "2025-02-15T12:00:00Z"
    chain: ["gg:node:12344", "gg:node:12343"]
  proof:
    type: zk-snark
    statement: ">50 commits to distributed systems repos"
```

**What this enables:**

1. **Trust with Provenance** — Every trust assertion has full lineage
2. **Multi-hop Trust Reasoning** — Query "who trusts whom, and why?"
3. **Contextual Trust** — Filter trust by domain, scope, validity period
4. **ZK-blinded Trust** — Prove trust relationships without revealing details
5. **Agent Capability Verification** — Verify agent claims before delegation

**Integration Points:**

| Component | GenesisGraph Role |
|-----------|------------------|
| Trust Assertion Protocol (TAP) | Assertions stored as graph edges |
| Agent Ether | Agent capabilities verified via graph queries |
| Semantic Passports | Bundles of assertions with provenance chains |

**See:** [Trust Assertion Protocol](../canonical/TRUST_ASSERTION_PROTOCOL.md) for the full TAP specification.

---

**Architectural Principle:** *Verification Without Revelation*

GenesisGraph proves that privacy and verifiability are not opposites—they're composable. When you can cryptographically commit to properties without revealing values, compliance and competition can coexist.

**The Innovation:**
Most provenance systems are binary (public or private). GenesisGraph introduces a **spectrum of disclosure** (A/B/C) that adapts to context:
- Open science: Full transparency builds trust
- Regulated industries: Prove compliance, protect IP
- Competitive markets: Selective disclosure enables verification without revelation

This solves adoption blockers in regulated industries where existing provenance standards force impossible choices.

---

## Impact: Real-World Adoption Paths

**Before GenesisGraph:**
- Prove FDA compliance → Reveal proprietary AI architecture → Lose competitive advantage
- ISO 9001 certification → Expose manufacturing trade secrets → Competitors clone process
- Research reproducibility → Share sensitive patient data → HIPAA violation

**With GenesisGraph:**
- Seal proprietary pipeline segments (Level C)
- Prove policy compliance cryptographically (Merkle commitments, signatures)
- Regulators verify integrity, competitors see only commitments
- **First technology that enables verification without revelation at scale**

**Use Cases Enabled:**

1. **AI/ML Pipelines**
   - FDA/EMA approval for medical AI without exposing training process
   - Model cards with verifiable provenance (training data lineage, bias testing)
   - Responsible AI compliance (fairness, transparency, accountability)

2. **Manufacturing & Supply Chain**
   - ISO 9001 certification with trade secret protection
   - Quality control audit trails (machine calibration, tolerance tracking)
   - Supplier verification without revealing proprietary recipes

3. **Scientific Research**
   - Reproducible research with sensitive data protection
   - Peer review with selective disclosure (methods public, data sealed)
   - Clinical trials with patient privacy (HIPAA compliance)

4. **Enterprise IT**
   - Software supply chain security (SBOM with selective disclosure)
   - DevOps audit trails (deployment provenance, compliance checks)
   - Zero-trust architectures with verifiable process lineage

**Adoption Metrics (v1.0 Goals):**
- 10+ Fortune 500 pilots across AI, manufacturing, healthcare
- 2+ standards body submissions (W3C, IETF)
- 100+ open source projects integrating GenesisGraph SDKs

---

**Version:** 0.3.0 → 1.0 (Active Development)
**License:** Apache 2.0
**Status:** Production-ready with enterprise adoption path

**Learn More:**
- [GitHub Repository](https://github.com/Semantic-Infrastructure-Lab/genesisgraph)
- [5-Minute Quickstart](https://github.com/Semantic-Infrastructure-Lab/genesisgraph/blob/main/docs/getting-started/quickstart.md)
- [Vision & Roadmap](https://github.com/Semantic-Infrastructure-Lab/genesisgraph/blob/main/docs/strategic/vision.md)
