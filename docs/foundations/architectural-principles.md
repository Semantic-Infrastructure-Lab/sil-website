# **SIL Principles (v1)**

*Durable constraints for building semantic infrastructure.*

---

## 0. Purpose of the Principles

These principles define how SIL conducts research, designs systems, and evaluates correctness.
They are constraints, not values.
They exist to keep the Semantic OS coherent, inspectable, reproducible, and extensible over long time horizons.

They apply to every layer, every domain, every operator, and every contribution.

### **Scope of These Principles**

These 14 principles govern the **research infrastructure and Semantic OS architecture**. They are foundational constraints for the entire system that apply to every layer, every domain, every operator, and every contribution.

**Related Document:** For practical design patterns and implementation guidance, see [SIL Design Principles](SIL_DESIGN_PRINCIPLES) which covers 9 applied principles for building SIL-aligned tools and systems.

---

## 1. Principles

### **1. Structure Before Heuristics**

All SIL systems prioritize explicit structure—schemas, types, relations, operators—before heuristics or statistical inference.
Heuristics may propose; structure decides.

### **2. Meaning Must Be Explicit**

All meaningful objects must be represented as typed, inspectable semantic structures.
Implicit meaning is not permitted in core representations.

### **3. Provenance Everywhere**

Every transformation must produce a provenance record: inputs, outputs, operator, assumptions, and context.
No silent changes.

### **4. Invariants Define Correctness**

Correctness is defined by invariants, not by expectation or intuition.
All operators must either preserve declared invariants or fail explicitly.

### **5. Determinism When Promised, Bounded Reproducibility When Not**

When operations declare determinism, the system must enforce it.
When full determinism is infeasible, operators must define equivalence relations and tolerances, and produce metadata that makes variability inspectable.

### **6. Cross-Domain Coherence Is a First-Class Goal**

Domain schemas, operators, and invariants must fit into a unified semantic substrate.
No domain is allowed to form an isolated island.

### **7. Operators Are the Only Way to Change State**

All mutations of semantic objects, [USIR](/foundations/SIL_GLOSSARY) graphs, and workflows must occur through declared operators.
No direct writes, no bypasses, no implicit edits.

### **8. Version Everything**

Schemas, operators, domains, objects, and mappings must be versioned.
Nothing substantial may change without recording what changed and why.

### **9. Visibility and Inspectability Are Mandatory**

Users and agents must be able to inspect structure, provenance, operator chains, and validation outcomes.
Opaque internals are not acceptable.

### **10. Reproducibility Over Performance**

Whenever there is a conflict between reproducibility and performance, reproducibility wins.
Performance can improve; lost traceability cannot.

### **11. Stability of Contracts Over Breadth of Features**

SIL favors stable, minimal interfaces over feature-rich but drifting APIs.
A small number of well-defined contracts outperforms a large number of ad hoc capabilities.

### **12. Play + Rigor as the Discovery Method**

Exploration, tinkering, hypothesis generation, and prototyping are encouraged—
but nothing enters the substrate without formalization, validation, and provenance.

### **13. Stewardship Protects Coherence**

Openness is encouraged, but stewards maintain the coherence of semantic memory, schemas, types, and operators.
All contributions enter through review for structural correctness.

### **14. Representations and Operators Are Long-Lived Artifacts**

The Semantic OS is infrastructure.
Schema and operator longevity matters more than short-term convenience or trends.

---

## Why These Principles Matter

### For Researchers
These principles define what "good" semantic infrastructure looks like. They're constraints that ensure SIL systems remain interpretable, composable, and verifiable over decades—not just demos that work once.

### For Developers
They explain why SIL systems behave the way they do. When you wonder "Why does this require explicit types?" or "Why can't I just use a heuristic here?", these principles provide the answer. They're not bureaucracy—they're the invariants that make composition possible.

### For Organizations
They predict how SIL tools will compose with your existing systems. Tools built on these principles don't create integration nightmares—they expose structure, track provenance, and fail explicitly rather than silently corrupting downstream data.

### The Core Promise
Following these 14 principles means SIL infrastructure will still be coherent, inspectable, and composable in 2035. The semantic substrate doesn't rot.

---

## Principles in Practice: reveal as Living Example

SIL principles are not aspirational—they're operational in production tools today.

**reveal** (v0.23.0 on PyPI, 100+ downloads/day as of Dec 2025) demonstrates how these principles manifest in working software. It's proof that semantic infrastructure isn't hypothetical—it's solving real problems for developers and AI agents.

### **Principle #1: Structure Before Heuristics**

**In reveal:**
- Shows code structure (imports, functions, classes) BEFORE showing implementation
- Directory → File → Element (progressive disclosure)
- Pattern detection uses explicit rules, not statistical inference
- Structure enables smart defaults: file type → appropriate analyzer (automatic routing)

**Example:**
```bash
$ reveal app.py
📄 app.py

Functions (3):
  app.py:15   load_config(path: str) -> Dict
  app.py:28   setup_logging(level: str) -> None
  app.py:42   main() -> int
```

Structure visible at a glance. No need to read full file (500 tokens) to understand organization (50 tokens).

### **Principle #2: Meaning Must Be Explicit**

**In reveal:**
- Code structure made explicit: what functions exist, what classes, what imports
- Pattern detection makes code quality explicit (not buried in developer mental model)
- No implicit behavior: everything visible via `--help`, `--rules`, `--explain`

**Example:**
```bash
$ reveal app.py --check --select B,S
app.py:47  [B001] Bare except clause - catches all exceptions
app.py:103 [S701] Using :latest tag in Docker (security risk)
```

Not "this code might have issues" (heuristic). "This code violates explicit semantic rules."

### **Principle #3: Provenance Everywhere**

**In reveal:**
- Every output line: `filename:line` format
- Always traceable: `vim app.py:95` jumps directly to source
- Git integration: `git blame app.py -L 15,27` follows provenance chain
- No "magic" - every result points to exact source location

**Example:**
```bash
$ reveal app.py | grep "Database"
  app.py:95     class Database

$ vim app.py:95  # Opens directly to line 95
```

Lightweight but complete provenance. Enables composition with vim, git, grep.

### **DESIGN_PRINCIPLE #2: Simplicity**

**In reveal:**
- Zero configuration: works immediately (`pip install reveal-cli` → `reveal app.py`)
- Smart defaults: auto-detect file type, choose output format
- Progressive disclosure: show only what's needed (structure first, detail on request)

**Why it works:**
Semantic types enable automatic routing. When reveal sees `.py` file, structure tells it which analyzer to use. No configuration files, no setup—types are the interface.

### **DESIGN_PRINCIPLE #3: Composability**

**In reveal:**
- Perfect Unix integration: pipes, grep, vim, git, find, jq
- Doesn't replace tools—augments them
- `filename:line` format is universal interface
- Works in pipelines: `find . -name "*.py" | xargs reveal | grep "TODO"`

**Example:**
```bash
# Compose with grep
$ reveal app.py | grep "config"
  app.py:15   load_config(path: str) -> Dict
  app.py:67   _config: Dict = {}

# Compose with git
$ reveal app.py | grep "load_config"
$ git blame app.py -L 15,27

# Compose with find
$ find src/ -name "*.py" -exec reveal {} \; | grep "Database"
```

Semantic tool that plays perfectly with 50-year-old Unix utilities.

### **DESIGN_PRINCIPLE #5: Verifiability**

**In reveal:**
- Precise line numbers (`app.py:15-27`)
- Reproducible output (same input → same structure)
- Explicit error messages when parsing fails
- Tree-sitter ensures reliable, verifiable parsing

**Example:**
```bash
$ reveal app.py load_config
app.py:15-27 | load_config

   15  def load_config(path: str) -> Dict:
   16      """Load configuration from JSON file."""
   ...
   27      return config
```

Exact line range. Verifiable. Reproducible.

---

### **Universal Resource Exploration: Principles Transcend Domains**

reveal's URI adapter system (v0.17.0+) proves these principles generalize beyond code:

**Same progressive disclosure pattern, different resources:**

```bash
# Code files (traditional)
$ reveal app.py
Functions: 5, Classes: 2, Imports: 3

# Environment variables (v0.17.0)
$ reveal env://
env://
├── PATH (753 chars, 8 directories)
├── HOME (/home/user)
└── PYTHONPATH (2 directories)

$ reveal env://PATH
/usr/local/bin
/usr/bin
/bin
...

# Databases (planned)
$ reveal postgres://prod
Tables: users, posts, comments

$ reveal postgres://prod users
Columns: id, email, created_at

$ reveal postgres://prod users email
Column: email | Type: VARCHAR(255) | Nullable: false
```

**Same principles:**
- Structure before content (database → tables → columns)
- Explicit meaning (types, constraints visible)
- Provenance (postgres://prod/users/email)
- Composability (works in pipes: `reveal postgres://prod | grep "users"`)

**Lesson:**
When you prioritize structure, meaning, and provenance, the patterns apply to ANY structured resource. This IS the semantic substrate—unified exploration across all domains.

---

### **Economic Impact: Why These Principles Matter**

**Token Efficiency (AI Agents):**
- Reading full file: 500-5000 tokens
- `reveal app.py`: 50 tokens
- **10x-100x savings** for AI context windows

**Zero Configuration:**
- No setup → immediate value
- Enabled by: structure determines behavior (file type → analyzer)

**Reliability:**
- Explicit errors, not silent failures
- Verifiable output (reproducible parsing)

**Composability:**
- Integrates with existing workflows (vim, git, grep)
- Doesn't force tool replacement

---

### **Why This Matters for SIL**

reveal demonstrates that:

1. **These principles WORK** - Not just theory, production use at scale
2. **They generalize** - Same pattern: code → env vars → databases → APIs
3. **They compound** - Each new feature leverages previous semantic structure
4. **They're economical** - 10x token savings, zero config, perfect composition

**The Question Shifts:**

Not "Can semantic infrastructure work?" (reveal proves it does)

But "How fast can we expand this pattern to ALL domains?"

That's what SIL is building: semantic substrate where these principles apply everywhere—code, data, processes, knowledge, agents, computation.

---

## 2. Boundary Notes (Clarifications)

* These principles do **not** prohibit the use of ML models—only untraceable reasoning.
* They do **not** require perfect determinism—only clear declaration of limits.
* They do **not** demand universal formalization—only that formalized components obey the substrate.
* They do **not** enforce one epistemology—only that epistemic commitments are explicit and inspectable.

---

## 3. Change Policy

These principles evolve only when:

1. A change clearly improves semantic clarity or system integrity;
2. The change is versioned, documented, and justified;
3. Integrity tests confirm compatibility;
4. Provenance captures the rationale for evolution.

Principles change slowly. Coherence changes never.