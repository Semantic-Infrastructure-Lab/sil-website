# SIL Tools - Stop Wasting Money on Agent Loops

Production-ready tools demonstrating SIL principles. Use them today.

## The Problem

AI agents waste billions of tokens (and dollars) on inefficient exploration patterns. Poor tool design forces agents into costly loops:
- Reading entire 500-line files when they need one function
- Parsing unstructured output with brittle regex
- Repeated exploration because tools don't guide strategic usage

**The scale:** Across millions of agents, structural inefficiency compounds into billions of wasted tokens—measurable economic and environmental cost.

## Our Solution: Agent-Native Tools

Tools designed for agents from day one, with:
- **Progressive disclosure** - Structure before detail (10x token reduction)
- **Strategic guidance** - When to use this vs alternatives
- **Composable design** - Pipes, JSON output, unix philosophy
- **Clear contracts** - Predictable output, reliable parsing

**Impact:**
- 💰 **85-90% token reduction** for exploration workflows (theoretical)
- ⚡ **Structure-first patterns** eliminate wasteful file reading
- 🌍 **Energy efficiency** at infrastructure level (not just optimization)

---

## reveal - Semantic Code Explorer ⭐

**The simplest way to understand code.** Point it at a directory, file, or function. Get exactly what you need.

**Status:** ✅ Production (v0.15.0) | [PyPI](https://pypi.org/project/reveal-cli/) | [GitHub](https://github.com/semantic-infrastructure-lab/reveal)

### Quick Start

```bash
pip install reveal-cli

# Directory → tree view
reveal src/

# File → structure (functions, classes, imports)
reveal app.py

# Element → extraction (with line numbers)
reveal app.py load_config
```

**Token efficiency:**
- Without Reveal: Read 500-line file = 500 tokens
- With Reveal: Structure (50) + Extract (20) = 70 tokens
- **Result: 7x reduction**

### Why It Matters

Reveal demonstrates **progressive disclosure** - a core SIL principle. Instead of forcing agents (or humans) to read entire files, it provides:

1. **Structure first** - See what's in a file (classes, functions, imports)
2. **Extract what you need** - Get specific elements with line numbers
3. **Compose with other tools** - Pipes to grep, jq, vim

This pattern will extend across all SIL systems:
- Semantic graphs (Pantheon IR)
- Provenance chains (GenesisGraph)
- Multi-agent reasoning (Agent Ether)

**NEW in v0.15.0:**
- `ast://` queries - Find functions by complexity, size, type across entire codebase
- `help://` system - Self-documenting adapters with auto-discovery
- Pluggable architecture - New adapters register automatically

```bash
reveal 'ast://src?complexity>10'    # Find technical debt
reveal help://ast                   # Learn query syntax
```

**[→ Learn more about Reveal](./REVEAL.md)** | **[Try it now](https://pypi.org/project/reveal-cli/)**

---

## More Tools Coming Soon

As SIL projects mature, more production tools will be featured here:

- **morphogen** - Cross-domain computation (audio, physics, circuits) - *active development*
- **tiacad** - Declarative parametric CAD in YAML - *coming soon*
- **genesisgraph** - Verifiable process provenance - *coming soon*

See all **[Projects →](/projects)**

---

## The Agent-Help Standard: Implemented in Reveal

We've **implemented** `--agent-help` in Reveal v0.13.0+, following the llms.txt pattern (600+ websites adopted).

**Two-tier system:**
- `--agent-help` - Quick strategic guide (~50 lines)
- `--agent-help-full` - Comprehensive patterns (~200 lines)

**The pattern:**
- Agents get strategic guidance (not just syntax)
- Decision trees show when to use reveal vs alternatives
- Anti-patterns prevent common mistakes
- Workflow sequences demonstrate composition

**[Read the full standard →](/docs/research/agent-help-standard)**

**Why this matters:**
- CLI tools need agent interfaces (like websites need llms.txt)
- Strategic guidance reduces trial-error exploration
- Pattern should become standard across all agent-facing tools
- Network effects: more adoption = more efficiency

---

## Economic Framing: Theory & Calculation

**The structural inefficiency:**

Agents reading full files when only structure is needed waste 85-90% of tokens. This is arithmetic, not measurement.

**Example calculation (1000 agents, 100 file explorations/day):**
- Traditional: Read 500 tokens/file = $54,750/year
- Progressive: Structure (50) + extract (20) = 70 tokens/file = $7,670/year
- **Theoretical savings: ~$47K/year**

**Assumptions stated:**
- Average file: 500 tokens (varies: 100-2000)
- Exploration frequency: 100/day per agent (high but plausible)
- Token pricing: $0.003/1K (varies by provider)

**Energy argument:**
- Every token = computation = energy
- Billions of unnecessary tokens = terawatt-hours of waste
- Progressive disclosure eliminates this structurally
- Infrastructure-level efficiency, not incremental optimization

**[Full analysis →](/docs/tools/economic-impact)**

SIL tools demonstrate semantic infrastructure principles—making waste architecturally impossible.

---

**Last Updated:** 2025-12-03
**Questions?** [GitHub Issues](https://github.com/semantic-infrastructure-lab/reveal/issues)
