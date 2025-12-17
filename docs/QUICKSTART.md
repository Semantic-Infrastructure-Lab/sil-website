# SIL Quickstart

**Get hands-on with Semantic Infrastructure Lab tools in 10 minutes**

> **Navigation:** This is the hands-on path.
> - **You are here:** Install tools, try them immediately
> - [Start Here](canonical/START_HERE) — Prefer concepts first? Start there
> - [Reading Guide](READING_GUIDE) — 7 paths for different audiences

---

## What You'll Learn

- Install and use production SIL tools (Reveal, TIA)
- Experience progressive disclosure firsthand
- Understand how semantic infrastructure works in practice

---

## 1. Install Reveal (2 minutes)

Reveal is SIL's semantic code exploration tool — experience progressive disclosure immediately:

```bash
# Install via pip
pip install reveal-cli

# Or via uvx (no install needed)
uvx reveal-cli
```

**Verify installation:**

```bash
reveal --version
```

---

## 2. Try Progressive Disclosure (5 minutes)

Progressive disclosure means seeing structure before detail. Let's explore code semantically:

```bash
# Use any project (or your own codebase)
cd /path/to/any/project  # or: git clone https://github.com/Semantic-Infrastructure-Lab/reveal

# Level 1: Directory structure
reveal src/

# Level 2: File structure (no code, just outline)
reveal src/main.py

# Level 3: Specific element (function, class)
reveal src/main.py function_name

# Level 4: Check code quality
reveal src/main.py --check
```

**What just happened?**
- You went from 0 → specific code without reading everything
- Token usage: ~50 tokens vs ~7,500 for full file
- Semantic structure revealed the path

---

## 3. Explore SIL Documentation (3 minutes)

Now that you've experienced progressive disclosure, understand the principles:

### The 30-Minute Path

1. **[Manifesto](canonical/SIL_MANIFESTO)** (15 min) — Why semantic infrastructure matters
2. **[Principles](canonical/SIL_PRINCIPLES)** (10 min) — The 14 principles that guide all work
3. **[START_HERE](canonical/START_HERE)** (5 min) — Navigate to deeper topics

### The Hands-On Path

1. **[Reveal Documentation](tools/REVEAL)** — Learn all reveal features
2. **[Agent Help Standard](research/AGENT_HELP_STANDARD)** — How to make tools agent-friendly
3. **[Progressive Disclosure Guide](canonical/PROGRESSIVE_DISCLOSURE_GUIDE)** — The theory behind what you just experienced

### The Technical Deep-Dive Path

1. **[Semantic OS Architecture](canonical/SIL_SEMANTIC_OS_ARCHITECTURE)** (30 min) — The 7-layer architecture
2. **[Technical Charter](canonical/SIL_TECHNICAL_CHARTER)** (45 min) — Formal invariants and guarantees
3. **[Unified Architecture Guide](architecture/UNIFIED_ARCHITECTURE_GUIDE)** (60 min) — How all 12 projects fit together

---

## 4. Join the Community

- **Email:** scott@semanticinfrastructurelab.org
- **GitHub:** [github.com/semantic-infrastructure-lab](https://github.com/semantic-infrastructure-lab)
- **Website:** [semanticinfrastructurelab.org](https://semanticinfrastructurelab.org)
- **Documentation:** Complete documentation in [docs/](.)

---

## What's Next?

Choose your path based on your interest:

- **Researchers:** [Research Agenda Year 1](canonical/SIL_RESEARCH_AGENDA_YEAR1)
- **Developers:** [Project Index](../projects/PROJECT_INDEX) — See all 12 projects
- **Collaborators:** [FAQ](meta/FAQ) — Common questions answered
- **Founders/Stewards:** [Stewardship Manifesto](canonical/SIL_STEWARDSHIP_MANIFESTO)

---

## Core Idea in One Sentence

**SIL builds the semantic substrate that makes meaning explicit, memory stable, reasoning inspectable, and provenance traceable.**

Welcome to the Semantic Infrastructure Lab.
