# Architecture Guides

**Understanding SIL's system design and architectural principles**

This guide explains **how to think architecturally** about semantic systems. It provides the mental models, frameworks, and decision criteria for designing SIL-compliant components.

---

## Essential Reading

### [Unified Architecture Guide](UNIFIED_ARCHITECTURE_GUIDE.md) ⭐⭐⭐ The Rosetta Stone
**30-45 minutes** | The canonical framework for understanding all SIL projects

**This is THE most important document.** It:
- Defines canonical vocabulary (Intent, IR, Execution, Domain, Adapter, Primitive, Service, Kernel)
- Reveals the universal pattern that ALL projects follow (Intent → IR → Execution)
- Shows the two architectural styles (Adapter vs Microkernel)
- Maps every existing project to the unified framework
- Provides decision frameworks for adding new components

**Start here before diving into any individual project.**

**Who should read this:**
- ✅ New to SIL? Read this first
- ✅ Implementing a new component? This shows you where it fits
- ✅ Confused about terminology? This clarifies everything
- ✅ Want to understand how Pantheon, Morphogen, Prism relate? This connects them

---

## How This Relates to Other Docs

```
UNIFIED_ARCHITECTURE_GUIDE.md (The Pattern)
    ↓ Applies
../canonical/SIL_PRINCIPLES.md (The Principles)
    ↓ Implements
../canonical/SIL_SEMANTIC_OS_ARCHITECTURE.md (The 6-Layer Stack)
    ↓ Realized in
../../projects/PROJECT_INDEX.md (Concrete Implementations)
```

**Reading order:**
1. **Unified Architecture Guide** - Learn the universal pattern
2. **SIL Principles** - Learn the design philosophy
3. **Semantic OS Architecture** - Understand the 6-layer stack
4. Individual project docs - See concrete implementations

---

## Connection to Other Docs

### This is a guide, not a spec

**Architecture guide** (this directory):
- Mental models and frameworks
- Decision criteria
- "How to think about semantic systems"

**Canonical documents** (`../canonical/`):
- Formal specifications
- Definitive reference
- Principles and foundations

**Tools** (`../tools/`):
- Production implementations
- See principles in action

**Research papers** (`../research/`):
- Why things are designed this way
- Theoretical foundations

---

## For Different Audiences

### New Engineer/Contributor
**Read:** Unified Architecture Guide → SIL Principles
**Time:** 1 hour
**Outcome:** Understand the pattern and philosophy

### Architect/Steward
**Read:** Unified Architecture Guide + all Canonical docs
**Time:** 3-4 hours
**Outcome:** Can design SIL-compliant systems

### Researcher
**Read:** Unified Architecture Guide + Research Papers
**Time:** Variable
**Outcome:** Understand architectural foundations

---

## Key Concepts Explained

**From Unified Architecture Guide:**
- Intent → IR → Execution pattern
- Adapter vs Microkernel architectures
- When to use which architectural style
- How all 11 SIL projects map to the framework
- Universal vocabulary for all projects

**This is the Rosetta Stone** - it makes everything else make sense.

---

## Next Steps

After reading this guide:

**To understand the principles:**
→ Read [SIL Principles](../canonical/SIL_PRINCIPLES.md)

**To understand the 6-layer stack:**
→ Read [Semantic OS Architecture](../canonical/SIL_SEMANTIC_OS_ARCHITECTURE.md)

**To see concrete implementations:**
→ Read [Project Index](../../projects/PROJECT_INDEX.md)

**To try working tools:**
→ Try [Reveal](../tools/REVEAL.md)

**To understand the research:**
→ Read [Research Papers](../research/)

---

## Navigation

- **Parent:** [Documentation Hub](../READING_GUIDE.md)
- **Related:** [Canonical Documents](../canonical/), [Tools](../tools/)
- **Projects:** [Project Index](../../projects/PROJECT_INDEX.md)

---

**Last Updated:** 2025-11-30
**Documents:** 1 (Unified Architecture Guide)
**Reading Time:** ~45 minutes
**Status:** Complete and stable
