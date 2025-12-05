# Reveal - Semantic Code Explorer

**Tagline:** The simplest way to understand code. Point it at a directory, file, or function. Get exactly what you need.

**Status:** ✅ Production (v0.16.0) | Available on [PyPI](https://pypi.org/project/reveal-cli/)

**Latest:** v0.16.0 adds type system for semantic relationships - understand how code connects, not just what exists. Query system (`ast://`), self-documenting adapters (`help://`), and pluggable architecture from v0.15.0.

---

## Quick Start

**Install:**
```bash
pip install reveal-cli
```

**Use:**
```bash
reveal src/                    # Directory → tree view
reveal app.py                  # File → structure
reveal app.py load_config      # Element → extraction
```

That's it. No flags, no configuration, just works.

---

## The Problem

Developers and AI agents waste time reading entire files when they only need to understand structure or extract specific functions.

**Example:** You want to see what's in `app.py` - do you really need to read all 500 lines?

**The structural inefficiency:**
- Agent reads entire file: 500 tokens when only 50 (structure) needed
- This pattern repeats: millions of agents, billions of unnecessary tokens
- Real economic cost + unnecessary energy consumption

---

## The Solution: Progressive Disclosure

**Reveal** provides three levels of detail - start broad, drill down as needed:

### 1. Directory Structure
```bash
$ reveal src/
📁 src/
├── app.py (247 lines, Python)
├── database.py (189 lines, Python)
└── models/
    ├── user.py (156 lines, Python)
    └── post.py (203 lines, Python)
```

### 2. File Structure
```bash
$ reveal app.py
app.py (247 lines, Python)
├── Imports (5)
├── Classes (2)
│   ├── Config (lines 15-34)
│   └── Application (lines 36-198)
└── Functions (6)
    ├── load_config (lines 201-215)
    ├── init_database (lines 217-230)
    └── ...
```

### 3. Element Extraction
```bash
$ reveal app.py load_config
app.py:201-215
def load_config(config_path: str) -> Config:
    """Load configuration from YAML file."""
    with open(config_path) as f:
        data = yaml.safe_load(f)
    return Config(**data)
```

**Result:** 10x more efficient than reading full files. Perfect for AI agents working within token budgets.

---

## SIL Principles in Action

Reveal demonstrates SIL's core principles ([see SIL Principles](/docs/sil-principles)):

✅ **Clarity** - Structure is visible, not hidden (see what's in a file without reading it)
✅ **Simplicity** - Zero configuration, smart defaults (just works)
✅ **Composability** - Unix tool composition (pipes to grep, jq, vim)
✅ **Correctness** - Reliable parsing via Tree-sitter (AST-based, not regex)
✅ **Verifiability** - Precise `filename:line` format (vim/git/grep compatible)

**Layer in Semantic OS:** Layer 5 (Human Interfaces / SIM) - makes structure visible and navigable

---

## Supported Languages (18 built-in)

**Programming:**
- 🐍 Python (.py)
- 📜 JavaScript (.js) - ES6+, classes, arrow functions, async/await
- 🔷 TypeScript (.ts, .tsx) - Type annotations, interfaces, React/TSX
- 🦀 Rust (.rs)
- 🔷 Go (.go)
- 🎮 GDScript (.gd) - Godot game engine

**Scripts & DevOps:**
- 🐚 Bash/Shell (.sh, .bash)
- 🐳 Docker (Dockerfile)

**Data & Docs:**
- 📓 Jupyter (.ipynb)
- 📝 Markdown (.md)
- 📋 JSON (.json)
- 📋 YAML (.yaml, .yml)
- 📋 TOML (.toml)

Run `reveal --list-supported` to see the current list.

---

## Advanced Features

### Pattern Detection (v0.13.0+)
Check code quality with industry-aligned rules:

```bash
reveal app.py --check              # All rules
reveal app.py --check --select B,S # Bugs + Security only
reveal --rules                     # List available rules
reveal --explain B001              # Explain specific rule
```

**Built-in rules:** Bare excepts, Docker :latest tags, function complexity, line length, insecure URLs

**Extensible:** Drop custom rules in `~/.reveal/rules/` - zero configuration!

### Code Query System (v0.15.0+)
Query your codebase like a database:

```bash
reveal 'ast://./src?complexity>10'     # Find complex functions
reveal 'ast://app.py?lines>50'         # Find long functions
reveal 'ast://.?lines>30&complexity<5' # Long but simple
reveal 'ast://src?type=function'       # All functions
```

**Query filters:**
- `lines` - Line count (operators: `>`, `<`, `>=`, `<=`, `==`)
- `complexity` - Cyclomatic complexity
- `type` - function, class, method

**Use cases:**
- **Technical debt discovery:** `ast://src?complexity>10`
- **Refactoring candidates:** `ast://src?lines>100`
- **Find good examples:** `ast://src?complexity<3&lines<20`
- **Export for analysis:** `ast://src --format=json | jq`

**Impact:** Find problems across entire codebase without reading every file. Query semantics eliminate exploration loops.

### Type System & Semantic Relationships (v0.16.0+)

Understand how code connects with semantic relationships:

```bash
reveal app.py --format=typed
```

**What you get:**
- **Entities with types** - Function, method, class, decorator (explicit semantic tagging)
- **Relationships** - Calls, inheritance, decorators, imports (how code connects)
- **Bidirectional edges** - Automatic reverse relationships (calls ↔ called_by)
- **Call graphs** - See complete dependency chains
- **Type counts** - Summary statistics for quick assessment

**Example output:**
```json
{
  "entities": [
    {"type": "function", "name": "process", "line": 10, "signature": "(data: dict)"},
    {"type": "method", "name": "handle", "line": 50, "parent_class": "Handler"}
  ],
  "relationships": {
    "calls": [{"from": {"type": "method", "name": "handle"}, "to": {"type": "function", "name": "process"}}],
    "called_by": [{"from": {"type": "function", "name": "process"}, "to": {"type": "method", "name": "handle"}}],
    "inherits": [{"from": "Handler", "to": "BaseHandler"}]
  },
  "type_counts": {"function": 10, "method": 15, "class": 3}
}
```

**Use cases:**
- **Impact analysis:** "What breaks if I change this function?" - see all callers instantly
- **Refactoring safety:** Understand dependency chains before making changes
- **Architecture review:** Visualize call graphs and inheritance hierarchies
- **Agent reasoning:** LLMs can reason about dependencies without executing code

**Why it matters:** Agents don't just find code - they understand how it works together. This is the foundation for semantic understanding across all of SIL.

**100% backward compatible:** Existing analyzers work unchanged. Type system only activates when types are defined. Falls back to standard JSON gracefully.

**SIL Pattern Proof:** Same relationship model extends to Pantheon IR - prove it works for code first, then apply to CAD, physics, reasoning, and all semantic domains.

### Self-Documenting Adapters (v0.15.0+)
Discover all capabilities through help:// system:

```bash
reveal help://                    # List all help topics
reveal help://ast                 # Learn ast:// queries
reveal help://env                 # Environment variables
reveal help://adapters            # All available adapters
```

**Pluggable architecture:** New adapters (postgres://, diff://, https://) auto-register with zero changes to core code. Each adapter self-documents via `get_help()` method.

### Environment Adapters
Explore beyond files:

```bash
reveal env://PATH              # Environment variables
reveal postgres://prod users   # Database schema (coming soon)
reveal https://api.github.com  # REST APIs (coming soon)
```

See [Reveal Roadmap](https://github.com/semantic-infrastructure-lab/reveal/blob/main/ROADMAP.md) for adapter evolution.

---

## Agent-Help Implementation (v0.13.0+)

Reveal validates SIL's proposed [agent-help standard](/docs/agent-help-standard) with a production two-tier implementation:

```bash
reveal --agent-help          # Quick strategic guide
reveal --agent-help-full     # Comprehensive patterns
reveal help://agent          # URI-based help access
```

**What agents get:**
- **Decision trees** - When to use reveal vs alternatives (cat, grep, etc.)
- **Token efficiency analysis** - 7-150x reduction patterns with real examples
- **Anti-patterns** - What NOT to do (e.g., reading full file before checking structure)
- **Workflow sequences** - Codebase exploration, PR review, refactoring patterns
- **Pipeline composition** - Integrate with git, find, jq, vim

### Why Two Tiers?

**Quick guide (`--agent-help`):** Brief decision guidance (~50 lines)
- Use when: Agent needs fast decision ("should I use this tool?")
- Token cost: Minimal (~50 tokens)

**Comprehensive guide (`--agent-help-full`):** Complete patterns (~200 lines)
- Use when: Agent doing complex work, needs deep pattern knowledge
- Token cost: Moderate (~200 tokens)

**Progressive disclosure in practice:** Agents load brief guide first, expand to full guide only when needed.

### Why This Pattern Matters

The agent-help standard follows llms.txt (600+ websites adopted):
- Agents need strategic guidance, not just syntax
- Progressive disclosure for help text itself
- Network effects: more tools adopt = more efficient ecosystem

**The pattern works:** Two-tier system lets agents get quick guidance or deep patterns as needed.

**See the full standard:** [Agent-Help Standard](/docs/research/agent-help-standard)

---

## Use Cases

### For Developers
- **Quick file overview** without opening editor
- **Find functions/classes** rapidly (`reveal file.py | grep "def "`)
- **Jump to code** with vim integration (`vim $(reveal app.py | grep load_config)`)
- **Terminal workflows** - perfect for SSH sessions

### For AI Agents
- **Token efficiency** - See structure (50 tokens) before reading full file (500 tokens)
- **Context gathering** - Extract only relevant functions
- **Codebase exploration** - Discover structure progressively
- **Integration** - Works with LangChain, Claude Code, etc.

### For Teams
- **Code reviews** - Understand structure before detailed review
- **Onboarding** - New team members explore codebase efficiently
- **Documentation** - Generate structure docs automatically
- **Refactoring** - See dependencies before changes

---

## Economic Impact: Theory & Calculation

### The Structural Inefficiency

**Traditional workflow (reading full files):**
- Agent reads 500-token file when only 50 tokens (structure) needed
- 90% of tokens wasted on unnecessary content
- Repeated across millions of operations = billions of wasted tokens

**Progressive disclosure (structure-first):**
- Structure: 50 tokens
- Extract specific element: 20 tokens
- Total: 70 tokens vs 500 = 86% reduction

**Example calculation (1000 agents, 100 file explorations/day):**
- Traditional: $54,750/year
- Progressive: $7,670/year
- **Theoretical savings: ~$47K/year**

**Assumptions:**
- Average file: 500 tokens (varies 100-2000)
- Exploration frequency: 100/day per agent (high but plausible)
- Token pricing: $0.003/1K (varies by provider)

This is a **calculation based on theory**, not measured production data. Real results depend on actual agent workflows.

### Energy Efficiency Argument

**The principle:**
- Every token processed = computation = energy
- Reading 500 tokens instead of 50 = 10x unnecessary computation
- Across millions of agents = terawatt-hours of waste

**Progressive disclosure eliminates this structurally:**
- Not "optimize this query" (incremental)
- But "make waste architecturally impossible" (foundational)

Infrastructure-level efficiency, not application-level tricks.

---

## Why Reveal Matters for SIL

**Progressive disclosure** is a core SIL principle - start broad, drill down as needed.

Reveal proves this pattern works for code exploration. As SIL evolves, this same pattern will extend to:
- **Semantic graphs** (Pantheon IR)
- **Provenance chains** (GenesisGraph)
- **Multi-agent reasoning** (Agent Ether)
- **Domain schemas** (Morphogen, TiaCAD, SUP)

**Reveal today:** Explore code semantically
- **Structure-first:** `reveal app.py` (50 tokens vs 500)
- **Query-based discovery:** `reveal 'ast://src?complexity>10'` (find debt across codebase)
- **Element extraction:** `reveal app.py load_config` (20 tokens)
- **Semantic relationships:** `reveal app.py --format=typed` (understand connections) ← **NEW v0.16.0**
- **Self-documentation:** `reveal help://ast` (agents discover capabilities)

**Evolution of semantic understanding:**
```
v0.13-14: Syntax → Structure (what exists)
v0.15.0:  Properties → Queries (find by attributes)
v0.16.0:  Semantics → Relationships (how things connect)
```

**Pattern demonstrated:**
- Progressive disclosure works (proven in production)
- Query semantics reduce exploration loops
- **Relationship understanding scales** (code → CAD → physics) ← **NEW**
- Self-documentation reduces agent trial-error
- Pluggable architecture enables evolution

**SIM vision:** Apply this pattern to ALL semantic structures
- Semantic graphs: `query pantheon://project?depth>3`
- Provenance: `query genesis://artifact?confidence<0.8`
- Agent reasoning: `query ether://session?cost>threshold`

**Future Integration Vision:** Detailed roadmap for Semantic OS integration (coming soon)

---

## Get Started

**Install from PyPI:**
```bash
pip install reveal-cli
```

**Try it:**
```bash
reveal --version          # Check installation
reveal --list-supported   # See supported file types
reveal .                  # Explore current directory
```

**Learn more:**
- [GitHub Repository](https://github.com/semantic-infrastructure-lab/reveal)
- [Full Documentation](https://github.com/semantic-infrastructure-lab/reveal/blob/main/README.md)
- [Changelog](https://github.com/semantic-infrastructure-lab/reveal/blob/main/CHANGELOG.md)
- [PyPI Package](https://pypi.org/project/reveal-cli/)

**Report issues or contribute:**
- [GitHub Issues](https://github.com/semantic-infrastructure-lab/reveal/issues)
- [Contributing Guide](https://github.com/semantic-infrastructure-lab/reveal/blob/main/CONTRIBUTING.md)

---

## Related SIL Projects

- [**morphogen**](https://github.com/semantic-infrastructure-lab/morphogen) - Cross-domain computation (audio, physics, circuits)
- [**tiacad**](https://github.com/semantic-infrastructure-lab/tiacad) - Declarative parametric CAD in YAML
- [**genesisgraph**](https://github.com/semantic-infrastructure-lab/genesisgraph) - Verifiable process provenance

See the complete [Project Index](/projects) for all 11 SIL projects.

---

**Last Updated:** 2025-12-04
**Document Version:** 1.2 (v0.16.0 type system release)
