# TiaCAD - Declarative Parametric CAD

**Tagline:** Parametric CAD in YAML. Semantic constraints, not just geometry.

**Status:** ✅ Production v3.1.2 | Available on [GitHub](https://github.com/Semantic-Infrastructure-Lab/tiacad)

**Latest:** v3.1.2 features visual regression testing, complete cone primitive support, and comprehensive documentation.

---

## Quick Start

**Define a parametric assembly:**
```yaml
parts:
  base:
    primitive: box
    parameters: {width: 100, height: 5, depth: 100}

  pillar:
    primitive: cylinder
    parameters: {radius: 5, height: 50}

operations:
  pillar_positioned:
    type: transform
    input: pillar
    transforms:
      - translate:
          to: base.face_top  # Semantic anchor, auto-generated!
```

Parts are peers with spatial references—not nested hierarchies.

---

## The Problem

Traditional CAD tools embed parts in rigid parent-child hierarchies. Change one thing, break everything downstream. Test one part? You need the whole assembly.

**The result:**
- Hidden dependencies between parts
- Fragile assemblies that break on refactoring
- Impossible to test parts independently
- No semantic meaning—just geometry coordinates

---

## The Solution: Reference-Based Composition

TiaCAD treats parts as independent, composable units connected through **spatial references**:

### Peer Parts (Not Hierarchies)
```yaml
parts:
  bracket:
    primitive: box
    parameters: {width: 20, height: 30, depth: 5}

  mount_hole:
    primitive: cylinder
    parameters: {radius: 3, height: 10}
```

Parts are defined independently. No coupling.

### Semantic Anchors
```yaml
operations:
  hole_positioned:
    type: transform
    input: mount_hole
    transforms:
      - translate:
          to: bracket.face_front  # Auto-generated semantic reference
```

`face_front`, `face_top`, `center`—TiaCAD generates meaningful anchors automatically.

### Explicit Dependencies
Every relationship is visible in the YAML. No hidden hierarchies, no implicit couplings.

---

## SIL Principles in Action

TiaCAD demonstrates core SIL architectural principles:

| Principle | TiaCAD Implementation |
|-----------|----------------------|
| **Explicit Meaning** | YAML declarations with semantic anchors |
| **Traceable Transformations** | Operations log every transform step |
| **Inspectable Reasoning** | Spatial resolver shows reference resolution |
| **Composable Systems** | Parts combine like pure functions |

---

## Production Validated

**Real metrics from production use:**

- **1,080+ tests** with 92% coverage
- **Visual regression testing** for geometric correctness
- **3 backends** (OpenCascade, CadQuery, OpenSCAD)
- **v3.0+ stable** since November 2025

---

## Why TiaCAD Matters for SIL

**CAD for the Semantic Age** — TiaCAD is the first CAD system designed as a semantic artifact:

- Parts are **independently testable** (no coupling to assemblies)
- Dependencies are **explicit** (no hidden hierarchies)
- Compositions are **orchestratable** (by TIA or any semantic system)
- Everything is **verifiable** (deterministic, testable geometry)

This is what CAD looks like when meaning matters as much as measurement.

---

## Get Started

```bash
# Clone and explore
git clone https://github.com/Semantic-Infrastructure-Lab/tiacad
cd tiacad

# Run examples
python -m tiacad examples/bracket.yaml --output bracket.step
```

---

## Related SIL Projects

- **[Reveal](/tools/reveal)** — Progressive code exploration
- **[Morphogen](/innovations/morphogen)** — Cross-domain computation substrate
- **[GenesisGraph](/innovations/genesisgraph)** — Provenance tracking for transforms
