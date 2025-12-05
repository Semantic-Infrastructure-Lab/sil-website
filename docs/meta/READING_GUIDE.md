# SIL Documentation - Reading Guide

**Welcome to the Semantic Infrastructure Lab.**

This guide helps you navigate SIL's documentation efficiently. Choose your reading path based on your goal.

**Last Updated:** 2025-11-30

---

## 🧭 Quick Navigation

### **"I want a 5-minute overview"**
→ **`canonical/SIL_MANIFESTO.md`** - Why SIL exists, what we're building

### **"I want to try working tools TODAY"**
→ **`tools/`** - Production tools you can use now (Reveal on PyPI)

### **"I want the complete technical architecture"**
→ **`architecture/UNIFIED_ARCHITECTURE_GUIDE.md`** ⭐ **THE ROSETTA STONE**

### **"I need to look up a term"**
→ **`canonical/SIL_GLOSSARY.md`** - Keep this open while reading

### **"I want design principles"**
→ **`canonical/SIL_PRINCIPLES.md`** - The 14 research infrastructure principles

### **"I want to see what's built"**
→ **`../projects/PROJECT_INDEX.md`** - 11 SIL projects mapped by layer

### **"I want research papers"**
→ **`research/`** - Formal research + standards (RAG, agent-help implemented in Reveal v0.13+)

---

## 📖 Curated Reading Paths

### **Path 1: "Skeptical Engineer" (30 minutes)**
**Perfect for:** Developers who want proof, not promises

```
1. tools/README.md (5 min)
   ↓ See real tools that work today

2. tools/REVEAL.md (10 min)
   ↓ Try: pip install reveal-cli

3. canonical/SIL_MANIFESTO.md (10 min)
   ↓ Understand the vision

4. ../projects/PROJECT_INDEX.md (5 min)
   ↓ See all 11 projects, 3,250+ tests
```

**Output:** You've tried working code and understand what SIL is building.

---

### **Path 2: "Research Collaborator" (2 hours)**
**Perfect for:** Academics, researchers who want technical depth

```
1. canonical/SIL_MANIFESTO.md (10 min)
   ↓ Understand the problem

2. architecture/UNIFIED_ARCHITECTURE_GUIDE.md (30 min) ⭐
   ↓ Learn the universal pattern

3. canonical/SIL_GLOSSARY.md (15 min - keep open)
   ↓ Learn the vocabulary

4. canonical/SIL_SEMANTIC_OS_ARCHITECTURE.md (20 min)
   ↓ Understand the 6-layer stack

5. research/RAG_AS_SEMANTIC_MANIFOLD_TRANSPORT.md (30 min)
   ↓ See rigorous research

6. research/AGENT_HELP_STANDARD.md (15 min)
   ↓ See implemented standard (validated in Reveal v0.13+)
```

**Output:** You understand SIL's technical foundation and research direction.

---

### **Path 3: "Curious Outsider" (20 minutes)**
**Perfect for:** Non-technical visitors who want the big picture

```
1. canonical/SIL_MANIFESTO.md (10 min)
   ↓ Why does SIL exist?

2. tools/README.md (5 min)
   ↓ What have they built?

3. canonical/FOUNDERS_LETTER.md (5 min)
   ↓ Personal perspective
```

**Output:** You understand what SIL is and why it matters.

---

### **Path 4: "Complete Mastery" (3-4 hours)**
**Perfect for:** Core team, stewards, deep contributors

```
1. canonical/SIL_MANIFESTO.md (10 min)
   ↓ Start with the "why"

2. architecture/UNIFIED_ARCHITECTURE_GUIDE.md (30 min) ⭐
   ↓ The Rosetta Stone - universal pattern

3. canonical/SIL_GLOSSARY.md (15 min - keep open)
   ↓ Vocabulary reference

4. canonical/SIL_PRINCIPLES.md (10 min)
   ↓ The 14 research infrastructure principles

5. canonical/SIL_SEMANTIC_OS_ARCHITECTURE.md (30 min)
   ↓ The 6-layer Semantic OS

6. tools/ (30 min)
   ↓ Understand production tools (Reveal)

7. research/ (1 hour)
   ↓ RAG paper + agent-help standard

8. ../projects/PROJECT_INDEX.md (30 min)
   ↓ All 11 projects in depth

9. canonical/SIL_STEWARDSHIP_MANIFESTO.md (15 min)
   ↓ How SIL operates and governs itself
```

**Output:** Complete understanding of SIL's philosophy, architecture, tools, and governance.

---

## 👤 By Role

### **Software Developer**
→ **Path 1 (Skeptical Engineer)** - See tools first, then vision

### **Architect/Steward**
→ **Path 4 (Complete Mastery)** - Deep dive into everything

### **Researcher/Academic**
→ **Path 2 (Research Collaborator)** - Focus on technical depth and papers

### **Just Curious**
→ **Path 3 (Curious Outsider)** - Start with Manifesto

---

## 📚 Document Categories

### **Core Identity** (Start Here)
The foundation - who we are and why we exist.

- **SIL_MANIFESTO.md** (12KB) - Why SIL exists
- **SIL_PRINCIPLES.md** (5KB) - 14 research infrastructure principles
- **SIL_GLOSSARY.md** (8KB) - Canonical vocabulary (keep this open!)
- **FOUNDERS_LETTER.md** (3KB) - Personal perspective from the founder

### **Technical Foundation** (The Architecture)
How to think architecturally about semantic systems.

- **UNIFIED_ARCHITECTURE_GUIDE.md** ⭐⭐⭐ - The Rosetta Stone (THE most important doc)
- **SIL_SEMANTIC_OS_ARCHITECTURE.md** - The 6-layer Semantic OS stack

### **Tools** (Try This Today)
Production-ready tools demonstrating SIL principles.

- **tools/README.md** - Tools overview and economic impact
- **tools/REVEAL.md** - Reveal code explorer (pip install reveal-cli)

### **Research** (Rigorous Deep-Dives)
Formal research on semantic infrastructure problems.

- **RAG_AS_SEMANTIC_MANIFOLD_TRANSPORT.md** - RAG as geometric meaning transport
- **AGENT_HELP_STANDARD.md** - Agent-help standard (implemented & validated in Reveal v0.13+)
- See `research/README.md` for future papers

### **Governance** (How We Operate)
Values and accountability.

- **SIL_STEWARDSHIP_MANIFESTO.md** - How SIL governs itself

### **Projects** (What's Built)
The ecosystem of 11 SIL projects.

- **../projects/PROJECT_INDEX.md** - All projects mapped to 6-layer architecture

### **Meta** (Context)
- **DEDICATION.md** - Tribute to Alan Turing

---

## 📊 Documentation Structure

```
docs/
├── READING_GUIDE.md           ← You are here
│
├── canonical/                 # Core identity
│   ├── SIL_MANIFESTO.md       ⭐⭐⭐ Start here
│   ├── SIL_PRINCIPLES.md
│   ├── SIL_GLOSSARY.md        ⭐ Keep this open
│   ├── SIL_SEMANTIC_OS_ARCHITECTURE.md
│   ├── SIL_STEWARDSHIP_MANIFESTO.md
│   ├── FOUNDERS_LETTER.md
│   └── README.md
│
├── architecture/              # The pattern
│   ├── UNIFIED_ARCHITECTURE_GUIDE.md  ⭐⭐⭐ The Rosetta Stone
│   └── README.md
│
├── tools/                     # Production tools (NEW!)
│   ├── README.md              ⭐⭐ Economic impact + overview
│   └── REVEAL.md              ⭐⭐⭐ Try: pip install reveal-cli
│
├── research/                  # Research papers
│   ├── RAG_AS_SEMANTIC_MANIFOLD_TRANSPORT.md
│   ├── AGENT_HELP_STANDARD.md  ⭐ Implemented in Reveal v0.13+
│   └── README.md
│
├── meta/                      # Meta-documentation
│   ├── DEDICATION.md
│   └── README.md
│
└── ../projects/               # Project catalog
    └── PROJECT_INDEX.md       ⭐⭐ See what's built
```

---

## 🎯 Tips for Reading

### 1. **Keep the Glossary Open**
`canonical/SIL_GLOSSARY.md` defines every core term. Open it in a second window and reference it as you read.

### 2. **Start with UNIFIED_ARCHITECTURE_GUIDE**
If you can only read ONE document, make it `architecture/UNIFIED_ARCHITECTURE_GUIDE.md`. It's the Rosetta Stone that makes everything else click.

### 3. **Try the Tools**
Don't just read ABOUT SIL - try Reveal: `pip install reveal-cli`
See progressive disclosure in action.

### 4. **Don't Skip the Manifesto**
`canonical/SIL_MANIFESTO.md` explains WHY we're building this. Understanding the problem is essential to understanding the solution.

### 5. **Read in Order**
The reading paths above are sequenced intentionally. Each document builds on the previous one.

---

## 💰 Why the Economic Framing?

You'll notice SIL documentation emphasizes cost savings and energy efficiency. This isn't marketing - it's core to our mission:

**The Problem:**
- AI agents waste billions of tokens on inefficient patterns
- Estimated $110M+ wasted annually across the industry
- Massive energy consumption from preventable loops

**SIL's Solution:**
- Progressive disclosure (Reveal): 86% cost reduction
- Agent-help standard: 50-86% reduction in workflows
- At scale: Billions of dollars + kWh saved

**This is about economic and environmental responsibility, not just elegant code.**

See `tools/README.md` for the detailed math.

---

## 📖 Cross-References

### If you're reading this and want to know:
- **How projects map to architecture layers:** See `../projects/PROJECT_INDEX.md`
- **How to use Reveal effectively:** See `tools/REVEAL.md`
- **Why agent-help matters:** See `research/AGENT_HELP_STANDARD.md` (implemented & validated)
- **SIL's governance model:** See `canonical/SIL_STEWARDSHIP_MANIFESTO.md`

---

## ❓ Still Lost?

**Can't find what you need?**
1. Check `canonical/SIL_GLOSSARY.md` for term definitions
2. Try the glossary search (if website has it)
3. See `../projects/PROJECT_INDEX.md` for project-specific docs

**Want to understand the ecosystem?**
- See `../projects/PROJECT_INDEX.md` for all 11 SIL projects
- See `tools/` for production-ready tools

**Want to contribute?**
- Install Reveal: `pip install reveal-cli`
- Read `research/AGENT_HELP_STANDARD.md` for proposed standards
- Check project GitHub repos for contribution guidelines

---

## 📝 Reference Docs to Keep Open

While working with SIL:
1. **`canonical/SIL_GLOSSARY.md`** - Term definitions
2. **`canonical/SIL_PRINCIPLES.md`** - Design philosophy
3. **`architecture/UNIFIED_ARCHITECTURE_GUIDE.md`** - The pattern

---

## 🚀 Next Steps After Reading

### If you're a Developer:
→ Install Reveal: `pip install reveal-cli`
→ Explore the 11 projects: `../projects/PROJECT_INDEX.md`
→ See `--agent-help` implementation in Reveal (research/AGENT_HELP_STANDARD.md)

### If you're a Researcher:
→ Read the RAG paper: `research/RAG_AS_SEMANTIC_MANIFOLD_TRANSPORT.md`
→ Review implemented standards: `research/AGENT_HELP_STANDARD.md`
→ Check SIL's research agenda (coming in Tier 2)

### If you're a Potential Collaborator:
→ Read stewardship model: `canonical/SIL_STEWARDSHIP_MANIFESTO.md`
→ See what's built: `../projects/PROJECT_INDEX.md`
→ Reach out via GitHub

---

**The most important document:** `architecture/UNIFIED_ARCHITECTURE_GUIDE.md` ⭐⭐⭐

Start there if you're impatient or confused.

---

**Last Updated:** 2025-11-30
**Launch Content:** This guide reflects Tier 1 launch content (10-13 docs)
