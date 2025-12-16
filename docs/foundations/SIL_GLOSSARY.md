# **SIL Glossary (v2.2)**

**Canonical definitions for the Semantic Operating System and its components.**

**Last Updated**: 2025-12-12
**Terms**: 119 (includes 8 Governance OS Primitives from infinite-quicksilver-1212)

---

## A

### **Adapter**

A bidirectional translation layer that converts between a domain-specific representation and Pantheon IR, enabling cross-domain composition. Examples: Morphogen adapter, TiaCAD adapter, GenesisGraph adapter.

### **Agency**

The scope of autonomous decision-making authority granted to an agent at a specific hierarchical level (Strategic, Operational, Tactical, or Execution).

### **Agent**

An entity executing workflows under orchestration rules. Agents apply operators, read/write semantic memory through authorized pathways, and emit provenance for all actions.

### **Agent Ether**

Universal tool orchestration layer providing Tool Behavior Contracts (TBC) for predictable multi-agent coordination. Enables agents to discover tool capabilities, execution modes, and interfaces through metadata-driven contracts.

### **Artifact**

Any semantic object produced by an operator or engine, including derived structures, intermediate outputs, or final results.

### **Assumption**

A declared, typed parameter or condition associated with an operator invocation or model. Must be recorded in provenance.

### **Audit Trail**

A complete, traceable, tamper-evident record of all transformations, decisions, and state changes within a workflow or system. Essential for compliance and reproducibility.

### **Authorization**

Explicit permission to perform actions within defined scope and constraints (distinct from capability/trust). An OS-level primitive providing the permission model complementary to TAP's capability model. Grants specify: principal (who grants), agent (who receives), scope (what actions), constraints (budgets/limits), and temporal bounds. See: AuthorizationGrant, AUTHORIZATION_PROTOCOL.md, TRUST_ASSERTION_PROTOCOL.md (TAP vs Authorization).

### **AuthorizationGrant**

Semantic OS primitive (Layer 1) encoding explicit permission for agent actions. Schema: `{ principal, agent, scope, actions, constraints, valid_from, valid_until }`. Distinct from TAP assertions (which prove capability). Required for operations with side effects to establish legal/security authority. Stored in GenesisGraph, checked by Agent Ether before delegation. See: AUTHORIZATION_PROTOCOL.md, HIERARCHICAL_AGENCY_FRAMEWORK.md.

---

## B

### **Backend (Compilation)**

Domain-specific output format or execution target in Pantheon's compilation model (e.g., MLIR, CadQuery, React, hardware descriptors). One Pantheon IR can compile to multiple backends.

### **Beth**

Knowledge graph and semantic search system within TIA, providing topic-based exploration with relationship traversal. Uses 14K+ indexed files with keyword extraction for rapid discovery.

### **Blast Radius**

The maximum scope of impact or damage a tool, operation, or failure can cause within the system. Used for security analysis and permission scoping.

### **BindingAct**

OS primitive (Layer 5) for cryptographically-signed user confirmations on irreversible operations. Design pattern: visual distinction + explicit confirmation + time delay + cryptographic signature. Addresses "apparent authority" risk where UX signifiers create legal obligations (semiotics: what user sees = what system/court interprets as consent). Distinguishes binding consent from casual interactions. See: UX_TRUST_BOUNDARY.md, SIL_SAFETY_THRESHOLDS.md.

### **BrowserBridge**

Human-AI collaboration layer enabling shared browser context between agents and humans. Allows agents to observe, assist, and coordinate through the browser interface (Layer 6: Intelligence).

---

## C

### **Channel**

Communication pathway for tool I/O in Tool Behavior Contracts. Types include stdin, stdout, stderr, events, logs, and progress. Each channel has defined format (structured/unstructured) and semantics.

### **Composition**

The ability to combine operators, workflows, or domain representations to create higher-level functionality. Cross-domain composition is enabled by Pantheon IR's universal semantic substrate (Layer 3).

### **Constraint**

A declarative restriction or condition applied to semantic objects or USIR graphs. Must be validated by domain modules or engines.

### **Contract (Lowering/Lifting)**

A formal specification of preconditions, postconditions, invariants, and provenance requirements for transforming between representations. Not an algorithm; a structural agreement.

### **Cross-Domain Coherence**

A system-wide condition where representations across domains interoperate through shared type fragments, invariant structures, and USIR relations.

---

## D

### **Decision Artifact**

A semantic object representing an agent's choice, including operator selection, routing, parameter binding, or workflow branching. Must be traceable via provenance.

### **Derived Object**

Any semantic object produced through a transformation or operator application, with explicit provenance linking to inputs.

### **DelegationGrant**

OS primitive (Layer 3) formalizing agent-to-agent delegation with explicit constraints. Schema: `{ delegator, delegatee, task_scope, max_depth, can_subdelegate, scope_narrowing }`. Prevents unbounded delegation chains ("infinite loops"). Enforces: depth limits, scope narrowing at each level, chain reconstructability in provenance. Required for safe multi-agent coordination. See: HIERARCHICAL_AGENCY_FRAMEWORK.md (delegation constraints section).

### **Determinism Profile**

OS primitive (Layer 4) classifying operator reproducibility: DETERMINISTIC (exact replay), BOUNDED (equivalent within tolerance), STOCHASTIC (approximate, inherently nondeterministic). Declared in operator metadata. Paired with ExecutionBudget to track cumulative nondeterminism and escalate when replay becomes unreliable. See: DETERMINISM_MANAGEMENT.md.

### **Domain Module**

A bounded, versioned package containing schemas, invariants, operator families, validation rules, and tool adapters for a specific domain.

### **Domain Object**

A semantic object defined within a domain module schema and validated by domain invariants.

---

## E

### **Edge (Pantheon)**

A typed semantic connection in a Pantheon graph carrying domain-specific metadata, units, constraints, and rates. Examples: dependency, derivation, composition, data flow.

### **Engine**

A computational component that executes operators over USIR structures. Engines emit typed outputs, validation artifacts, diagnostics, and complete provenance metadata.

### **Epistemic Type**

OS primitive (Layer 0) labeling evidence quality in provenance edges. Enum: OBSERVATION (direct evidence), CLAIM (inference/derived), DECISION (binding choice), ASSUMPTION (default/unverified), ASSERTION (trust-based). Prevents "claim inflation" where agent inferences masquerade as ground truth. High-stakes operators require OBSERVATION-level evidence. Confidence decay rules track claims-based-on-claims. See: EPISTEMIC_PROVENANCE.md, SEMANTIC_OBSERVABILITY.md.

### **Equivalence Relation**

A formally defined criterion used to evaluate reproducibility for non-deterministic or approximate operator outputs.

### **Execution Budget**

OS primitive (Layer 4) tracking cumulative nondeterminism during workflow execution. Paired with DeterminismProfile. Tracks entropy sources (LLM sampling, web calls, time, filesystem) and escalates when `consumed > limit`, signaling replay unreliability. Prevents silent replay failures in forensic reconstruction. See: DETERMINISM_MANAGEMENT.md.

### **Execution Context**

Typed metadata describing the environment, engine/tool configuration, and state snapshot used during operator execution.

### **Execution Level**

Lowest tier of hierarchical agency with narrow scope, minimal context, and tool-level invocation authority. Executes specific operations without strategic planning.

### **Execution Mode**

Tool behavior classification in TBC: sync (immediate return), async (background with callback), job (long-running with tracking), or session (multi-turn interactive).

---

## F

### **Feedback Loop**

A reflection-measurement-correction cycle enabling semantic systems to achieve precision through continuous adjustment. Analogous to op-amps in electronics; a first-class primitive in SIL (Layer 5: Intent).

### **Fitness Metric**

Multi-dimensional measure of system health combining alignment, efficiency, and satisfaction. Used in semantic observability to evaluate intent-execution matching.

### **Frontend (Compilation)**

Domain-specific input format or authoring environment in Pantheon's compilation model (e.g., Morphogen DSL, TiaCAD YAML, GenesisGraph provenance). Compiles to Pantheon IR for universal composition.

---

## G

### **GenesisGraph**

Cryptographically verifiable provenance system with selective disclosure (A/B/C levels). Solves "certification vs IP protection" dilemma through Merkle trees, hash chains, and SD-JWT (Layer 2: Structures, Layer 3: Composition).

### **Graph (USIR)**

A typed directed multigraph representing semantic structures, operator applications, workflows, or constraints.

---

## H

### **Hash Chain**

Tamper-evident provenance structure in GenesisGraph where each record's hash includes the previous record's hash, creating an immutable audit trail.

### **Hierarchical Agency Framework**

Four-tier decision-making model defining agency scope: Strategic (meta-planning), Operational (planning), Tactical (method selection), Execution (tool invocation). Prevents over/under-scoping agent authority.

---

## I

### **Intent-Execution Alignment**

Primary health signal in semantic observability measuring how well system outputs match user intentions. Detected through vector embeddings and multi-dimensional fitness metrics.

### **IntentContract**

OS primitive (Layer 5) formalizing user intent with ambiguity scoring and escalation thresholds. Schema: `{ goal, constraints, preferences, ambiguity_score (0.0-1.0), escalation_threshold }`. Classification: AUTONOMOUS (<0.3, agent decides), BOUNDED_DISCRETION (0.3-0.7, agent proposes), MANDATORY_ESCALATION (>0.7, agent clarifies first). Enables breach detection when execution deviates from intent constraints. Prevents autonomous action on ambiguous goals. See: INTENT_VERIFICATION_PROTOCOL.md, MULTI_AGENT_PROTOCOL_PRINCIPLES.md.

### **Invariant**

A declarative condition that must hold for semantic objects, USIR structures, or workflows. Violations generate diagnostics and may halt execution.

### **Interface (Human)**

A read-only or operator-mediated surface for inspection, visualization, and debugging of semantic structures and provenance.

### **Interpretation Layer (SIM)**

A semantic exploration and inspection environment that exposes USIR, semantic memory, invariants, and provenance with consistent visualization contracts.

---

## J

### **Job**

Long-running task execution mode in TBC where tools provide progress tracking, status queries, and result retrieval through defined channels. Enables agent monitoring without blocking.

---

## L

### **Layer 0: Substrate**

Hardware foundation layer in the 7-layer Semantic OS. Home to Philbrick (analog/digital hybrid computing platform) and RiffStack (live performance interface).

### **Layer 1: Primitives**

Computational primitives layer providing 40+ unified domains (audio, physics, chemistry, field simulation, agent-based modeling). Implemented by Morphogen with physical unit enforcement.

### **Layer 2: Structures**

Data structures layer providing geometric modeling (TiaCAD with SpatialRef), provenance structures (GenesisGraph with Merkle trees), and semantic graph foundations.

### **Layer 3: Composition**

Cross-domain composition layer enabling universal semantic integration. Implemented by Pantheon IR (typed graphs), GenesisGraph (provenance composition), and SUP (semantic UI compilation).

### **Layer 4: Dynamics**

Temporal execution and multirate scheduling layer. Morphogen's deterministic scheduler handles 48kHz audio, 240Hz physics, 60Hz control with precise temporal coordination.

### **Layer 5: Intent**

Validation, constraint solving, and semantic correctness layer. Pantheon validation framework enforces type safety, domain constraints, and feedback loops for precision.

### **Layer 6: Intelligence**

Agent coordination and multi-agent orchestration layer. Agent Ether (Tool Behavior Contracts) and BrowserBridge (human-AI collaboration) enable predictable agentic workflows.

### **Lineage (Temporal)**

The chain of creation, modification, and derivation events associated with a semantic object. Must be queryable.

### **Lowering**

A structured transformation from a more abstract representation to a more concrete one, executed through a lowering contract.

---

## M

### **Memory Access Protocol**

Rules governing how agents read, write, or snapshot semantic memory under orchestration control.

### **Merkle Tree**

Cryptographic data structure in GenesisGraph enabling efficient verification of provenance integrity. Each node's hash includes children hashes, allowing selective disclosure without revealing entire tree.

### **Meta-Layer: Observability**

Cross-cutting observability layer in the 7-layer Semantic OS. Reveal provides progressive disclosure across all layers, enabling structure-before-content exploration.

### **Metadata (Execution)**

Structured engine/tool information emitted during operator execution, including environment parameters, tolerances, and runtime status.

### **Module Boundary**

The operational limits of a domain module, beyond which it must defer to USIR or other domains and may not violate global invariants.

### **Morphogen**

Cross-domain deterministic computation system unifying 40+ domains (audio, physics, chemistry, circuits, CAD, etc.) in one type system with physical unit enforcement. Provides bitwise-identical reproducibility (Layer 1: Primitives, Layer 4: Dynamics).

### **Multi-Shot Learning**

Agent learning pattern where knowledge accumulates across multiple interaction cycles, building institutional memory. Enables progressive improvement through reflection and pattern recognition.

### **Multirate Scheduler**

Deterministic temporal coordination system in Morphogen handling different domain update rates simultaneously (48kHz audio, 240Hz physics, 60Hz control) with precise synchronization.

### **Mutation Path**

An operator-mediated modification to semantic objects. All mutations must be recorded via provenance.

---

## N

### **Node (Pantheon)**

Typed graph element in Pantheon IR representing operators, entities, components, or modules. Includes domain semantics, parameters with units, and metadata. Foundation of universal composition.

---

## O

### **Operational Level**

Second tier of hierarchical agency with medium scope, partial context, and planning authority. Translates strategic goals into executable plans but doesn't set high-level direction.

### **Operator**

A typed transformation with explicit signatures, preconditions, postconditions, effect scopes, and provenance emission requirements.

### **Operator Family**

A set of operators within a domain or global layer sharing structure, inputs/outputs, or invariants.

### **Orchestration**

The deterministic execution environment governing workflows, agent lifecycle, memory protocols, and provenance guarantees.

---

## P

### **Pantheon IR**

The Universal Semantic Intermediate Representation - a typed intermediate representation (IR) designed for cross-domain semantic transformations. Pantheon IR serves as the "assembly language for meaning," providing a common substrate for representing concepts, relationships, and operators across different domains (code, infrastructure, knowledge, computation). Enables one source to compile to multiple backends (Layer 3: Composition, Layer 5: Intent).

### **Parameter (Typed)**

An explicit value or configuration passed to an operator, validated against type requirements and recorded in provenance.

### **Permission**

Declared capability requirement in TBC security model. Examples: filesystem-read, filesystem-write, network-access, process-spawn. Enables blast radius analysis and security auditing.

### **Persistent Object**

Any semantic object stored durably in semantic memory with schema and version references.

### **Philbrick**

Modular analog/digital hybrid computing substrate enabling software/hardware co-design. Morphogen code can compile to Philbrick hardware configurations and vice versa (Layer 0: Substrate).

### **Physical Units**

Type system feature in Morphogen and Pantheon enforcing dimensional correctness at compile-time (Hz, dB, m, kg, K, etc.). Prevents unit mismatch errors and enables semantic type checking.

### **Prism**

Set stack query system enabling complex filtering and relationship traversal across semantic structures. Designed for analytics and pattern discovery across provenance graphs (Layer 3: Composition).

### **Progressive Disclosure**

Structure-before-content exploration pattern reducing token usage by 10x-86x. Three-phase workflow: Orient (structure), Navigate (outline), Focus (detail). Implemented by Reveal across all layers.

### **Progress Model**

Tool progress reporting specification in TBC: percent (0-100%), steps (N of M), or indeterminate (unknown duration). Enables agents to estimate completion and allocate resources.

### **Provenance**

A structured record capturing lineage, operator invocation details, inputs/outputs, assumptions, environment, diagnostics, and state snapshots.

---

## R

### **Rate Limit**

Throttling constraint in TBC security model specifying maximum invocations per time period. Prevents resource exhaustion and abuse.

### **Relation (USIR)**

A typed connection between USIR nodes with defined semantics and integrity rules (e.g., dependency, derivation, constraint, containment).

### **Replayability**

The ability to re-execute a workflow with equivalent results under defined equivalence relations and snapshot semantics.

### **Reproducibility**

A contract defining the expected stability of outputs for a given operator or engine (deterministic, bounded, or non-reproducible).

### **Reveal**

Progressive disclosure tool providing structure-before-content code exploration. Outputs AST-based outlines, extracts specific functions, and enables 86% token reduction for agent workflows (Meta-Layer: Observability).

### **RiffStack**

Live performance interface and 6-layer creative compiler for Morphogen.Audio. Provides temporal abstractions for musical expression with real-time synthesis (Layer 0: Substrate, Layer 1: Primitives).

### **Round-Trip Fidelity**

Property of Pantheon adapters where domain → Pantheon IR → domain transformations preserve semantic meaning without loss. Essential for composition guarantees.

---

## S

### **Safety Threshold**

Operational limit or constraint defining safe operating boundaries for systems, agents, or workflows. Part of SIL's governance model ensuring controlled execution.

### **Schema**

A versioned definition of the structure, fields, allowed relations, invariants, and types of a semantic object or USIR pattern.

### **SD-JWT (Selective Disclosure JWT)**

JSON Web Token standard used by GenesisGraph enabling cryptographic proof of claims without revealing underlying data. Enables A/B/C disclosure levels.

### **Selective Disclosure**

Three-level provenance visibility model in GenesisGraph: Level A (public summary), Level B (authorized detail), Level C (full reproduction). Solves certification vs IP protection dilemma.

### **Semantic Contract**

A complete specification binding an operator, transformation, or system component, consisting of:
- **Signature**: input/output types, arity, required parameters
- **Invariants**: preconditions, postconditions, preserved properties
- **Provenance requirements**: emission rules, completeness guarantees
- **Reproducibility guarantees**: deterministic, bounded, or non-reproducible
- **Effects**: scope of mutations, side effects on semantic memory

All operators, domain modules, and engines operate under semantic contracts. Specialized contracts (lowering/lifting, reproducibility) are instances of this pattern.

### **Semantic Memory**

The persistent, typed, provenance-complete storage layer for all semantic objects and their relations.

### **Semantic Object**

Any object stored in semantic memory, compliant with a schema, versioned, typed, and linked via provenance.

### **Semantic Observability**

Framework for automated intent-execution alignment detection using vector embeddings, multi-dimensional fitness metrics, and frustration/satisfaction classification. Enables continuous system optimization.

### **Semantic Passport**

A bundle of Trust Assertions packaged for a specific purpose (e.g., job application, agent authorization, access request). Signed by the subject to prove control, with purpose-specific context limiting scope. See: Trust Assertion Protocol (TAP).

### **Semantic Time**

Domain-specific temporal model where each domain defines its own time units, resolution, and causal horizons. Examples: audio (samples @ 48kHz), music (beats @ tempo), animation (frames @ 60fps). Logical time supersedes wall-clock time.

### **Semantic Type**

Type carrying meaning and constraints beyond structural shape. Includes physical units, domain semantics, valid ranges, and invariants. Enables compile-time validation of semantic correctness.

### **Session**

Multi-turn interactive execution mode in TBC where tools maintain state across invocations. Enables conversational workflows and stateful interactions (e.g., REPL, debugger, database connection).

### **SIM (Semantic Information Mesh)**

The interactive environment exposing the structure of semantic memory, USIR, and workflows for navigation, exploration, and debugging.

### **Snapshot (State)**

A versioned capture of relevant semantic memory and execution context used for reproducible runs and inspection.

### **SpatialRef**

TiaCAD's unified position + orientation abstraction enabling composable spatial relationships in parametric CAD. Eliminates manual coordinate frame transformations (Layer 2: Structures).

### **Stewardship**

Governance model prioritizing long-term responsibility and community accountability over ownership. Core principle of SIL's organizational structure and decision-making.

### **Strategic Level**

Highest tier of hierarchical agency with full scope, deep context, and meta-planning authority. Sets direction, allocates resources, defines success criteria.

### **SUP (Semantic UI Compilation)**

Semantic-first UI compilation system translating semantic structures into responsive UI components. Enables provenance-aware interfaces and automatic control generation from parameters (Layer 3: Composition).

---

## T

### **Tactical Level**

Third tier of hierarchical agency with limited scope, local context, and method selection authority. Chooses approaches and techniques within operational plans.

### **TBC (Tool Behavior Contract)**

Metadata-driven specification in Agent Ether where tools declare execution mode, channels, progress model, permissions, and interfaces. Enables predictable tool orchestration for multi-agent systems.

### **TIA (The Intelligent Agent)**

Unified AI workspace and agent framework providing semantic search (Beth), task management, Git workflows, and progressive discovery patterns. Foundation for agent-assisted development (Layer 6: Intelligence).

### **TiaCAD**

Parametric CAD system with SpatialRef unification, reproducible geometry, and visual regression testing. Compiles to Pantheon IR for cross-domain composition (Layer 2: Structures).

### **TAP (Trust Assertion Protocol)**

Pantheon IR schema for expressing typed, contextual, verifiable trust claims. Core shape: `Issuer → Claim → Subject + Context + Proof + Provenance`. Seven claim types: `has-capability`, `has-credential`, `has-relationship`, `controls-key`, `has-history-with`, `passed-check`, `belongs-to`. Stored as GenesisGraph edges, queried by Agent Ether for delegation decisions.

### **Token Efficiency**

Measured reduction in LLM token usage through progressive disclosure, structure-before-content exploration, and targeted information retrieval. Reveal achieves 10x-86x reduction in practice.

### **Trust Assertion**

The atomic unit of machine-readable trust in TAP. A structured statement: `Issuer → Claim → Subject + Context + Proof + Provenance`. Replaces ad-hoc trust signals (résumés, reputation scores) with typed, cryptographically verifiable claims that both humans and agents can reason about.

### **Trust Claim Types**

TAP's minimal ontology for trust claims:
- `has-capability`: Skills, competencies (with levels: novice → authoritative)
- `has-credential`: Degrees, licenses, certifications
- `has-relationship`: Mentored-by, collaborated-with, employed-by
- `controls-key`: Cryptographic key ownership (identity binding)
- `has-history-with`: Track record of past interactions
- `passed-check`: Safety evaluations, compliance audits, assessments
- `belongs-to`: Organizational membership

### **Transformation**

Any operator-driven modification to semantic objects, USIR structures, or workflows.

### **Type Fragment**

A component of the USIR type system provided by core or domain modules. Must be versioned and validated.

### **Typed Relation**

A relation with declared source and target types, validation rules, and semantics. Required for all USIR edges.

---

## U

### **USIR (Universal Semantic Intermediate Representation)**

A typed, explicit, graph-structured intermediate representation unifying cross-domain structures, operators, workflows, and transformations. See also: Pantheon IR.

---

## V

### **Validation**

A process that checks schema correctness, type soundness, invariant satisfaction, and provenance completeness.

### **Versioned Identifier**

A stable pair consisting of (id, version) used for semantic objects, schemas, operators, and domain modules.

---

## W

### **Workflow**

A versioned, structured operator graph with explicit dependencies, execution semantics, artifact bindings, and replay contracts. Workflow versions are immutable once committed and referenced in all execution provenance.

---

## Summary Statistics

- **Total Terms**: 119 (v1: 46, v2: +62, v2.1: +4, v2.2: +7)
- **SIL Projects**: 12/12 defined
- **7-Layer Architecture**: Complete
- **Tool Behavior Contract**: Complete
- **Pantheon Concepts**: Complete
- **Observability & Agency**: Complete
- **Governance OS Primitives**: Complete
- **Trust (TAP)**: Complete

**Version History**:
- v1.0 (2025-12-05): Initial 46 terms, core semantic OS concepts
- v2.0 (2025-12-07): Expanded to 108 terms, added projects, architecture, TBC, Pantheon, observability, agency framework
- v2.1 (2025-12-08): Added Trust Assertion Protocol (TAP) terms: TAP, Trust Assertion, Trust Claim Types, Semantic Passport
- v2.2 (2025-12-12): Added Governance OS Primitives: Authorization, AuthorizationGrant, BindingAct, DelegationGrant, DeterminismProfile (enhanced), EpistemicType, ExecutionBudget, IntentContract
