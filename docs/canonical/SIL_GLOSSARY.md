# **SIL Glossary (v1)**

**Canonical definitions for the Semantic Operating System and its components.**

---

## A

### **Agent**

An entity executing workflows under orchestration rules.
Agents apply operators, read/write semantic memory through authorized pathways, and emit provenance for all actions.

### **Artifact**

Any semantic object produced by an operator or engine, including derived structures, intermediate outputs, or final results.

### **Assumption**

A declared, typed parameter or condition associated with an operator invocation or model. Must be recorded in provenance.

---

## C

### **Constraint**

A declarative restriction or condition applied to semantic objects or USIR graphs. Must be validated by domain modules or engines.

### **Contract (Lowering/Lifting)**

A formal specification of preconditions, postconditions, invariants, and provenance requirements for transforming between representations.
Not an algorithm; a structural agreement.

### **Cross-Domain Coherence**

A system-wide condition where representations across domains interoperate through shared type fragments, invariant structures, and USIR relations.

---

## D

### **Decision Artifact**

A semantic object representing an agent’s choice, including operator selection, routing, parameter binding, or workflow branching. Must be traceable via provenance.

### **Derived Object**

Any semantic object produced through a transformation or operator application, with explicit provenance linking to inputs.

### **Domain Module**

A bounded, versioned package containing schemas, invariants, operator families, validation rules, and tool adapters for a specific domain.

### **Domain Object**

A semantic object defined within a domain module schema and validated by domain invariants.

---

## E

### **Engine**

A computational component that executes operators over USIR structures.
Engines emit typed outputs, validation artifacts, diagnostics, and complete provenance metadata.

### **Equivalence Relation**

A formally defined criterion used to evaluate reproducibility for non-deterministic or approximate operator outputs.

### **Execution Context**

Typed metadata describing the environment, engine/tool configuration, and state snapshot used during operator execution.

---

## G

### **Graph (USIR)**

A typed directed multigraph representing semantic structures, operator applications, workflows, or constraints.

---

## I

### **Invariant**

A declarative condition that must hold for semantic objects, USIR structures, or workflows.
Violations generate diagnostics and may halt execution.

### **Interface (Human)**

A read-only or operator-mediated surface for inspection, visualization, and debugging of semantic structures and provenance.

### **Interpretation Layer (SIM)**

A semantic exploration and inspection environment that exposes USIR, semantic memory, invariants, and provenance with consistent visualization contracts.

---

## L

### **Lineage (Temporal)**

The chain of creation, modification, and derivation events associated with a semantic object. Must be queryable.

### **Lowering**

A structured transformation from a more abstract representation to a more concrete one, executed through a lowering contract.

---

## M

### **Memory Access Protocol**

Rules governing how agents read, write, or snapshot semantic memory under orchestration control.

### **Metadata (Execution)**

Structured engine/tool information emitted during operator execution, including environment parameters, tolerances, and runtime status.

### **Module Boundary**

The operational limits of a domain module, beyond which it must defer to USIR or other domains and may not violate global invariants.

### **Mutation Path**

An operator-mediated modification to semantic objects. All mutations must be recorded via provenance.

---

## O

### **Operator**

A typed transformation with explicit signatures, preconditions, postconditions, effect scopes, and provenance emission requirements.

### **Operator Family**

A set of operators within a domain or global layer sharing structure, inputs/outputs, or invariants.

### **Orchestration**

The deterministic execution environment governing workflows, agent lifecycle, memory protocols, and provenance guarantees.

---

## P

### **Pantheon IR**

The Universal Semantic Intermediate Representation - a typed intermediate representation (IR) designed for cross-domain semantic transformations. Pantheon IR serves as the "assembly language for meaning," providing a common substrate for representing concepts, relationships, and operators across different domains (code, infrastructure, knowledge, computation).

### **Parameter (Typed)**

An explicit value or configuration passed to an operator, validated against type requirements and recorded in provenance.

### **Persistent Object**

Any semantic object stored durably in semantic memory with schema and version references.

### **Provenance**

A structured record capturing lineage, operator invocation details, inputs/outputs, assumptions, environment, diagnostics, and state snapshots.

---

## R

### **Relation (USIR)**

A typed connection between USIR nodes with defined semantics and integrity rules (e.g., dependency, derivation, constraint, containment).

### **Replayability**

The ability to re-execute a workflow with equivalent results under defined equivalence relations and snapshot semantics.

### **Reproducibility**

A contract defining the expected stability of outputs for a given operator or engine (deterministic, bounded, or non-reproducible).

---

## S

### **Schema**

A versioned definition of the structure, fields, allowed relations, invariants, and types of a semantic object or USIR pattern.

### **Semantic Contract**

A complete specification binding an operator, transformation, or system component, consisting of:
- **Signature**: input/output types, arity, required parameters
- **Invariants**: preconditions, postconditions, preserved properties
- **Provenance requirements**: emission rules, completeness guarantees
- **Reproducibility guarantees**: deterministic, bounded, or non-reproducible
- **Effects**: scope of mutations, side effects on semantic memory

All operators, domain modules, and engines operate under semantic contracts. Specialized contracts (lowering/lifting, reproducibility) are instances of this pattern.

### **Semantic Object**

Any object stored in semantic memory, compliant with a schema, versioned, typed, and linked via provenance.

### **Semantic Memory**

The persistent, typed, provenance-complete storage layer for all semantic objects and their relations.

### **SIM (Semantic Information Mesh)**

The interactive environment exposing the structure of semantic memory, USIR, and workflows for navigation, exploration, and debugging.

### **Snapshot (State)**

A versioned capture of relevant semantic memory and execution context used for reproducible runs and inspection.

---

## T

### **Transformation**

Any operator-driven modification to semantic objects, USIR structures, or workflows.

### **Type Fragment**

A component of the USIR type system provided by core or domain modules. Must be versioned and validated.

### **Typed Relation**

A relation with declared source and target types, validation rules, and semantics. Required for all USIR edges.

---

## U

### **USIR (Universal Semantic Intermediate Representation)**

A typed, explicit, graph-structured intermediate representation unifying cross-domain structures, operators, workflows, and transformations.

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