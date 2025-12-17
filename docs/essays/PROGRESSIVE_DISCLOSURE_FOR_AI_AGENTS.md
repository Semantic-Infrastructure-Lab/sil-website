---
title: Progressive Disclosure for AI Agents
subtitle: Why your AI assistant wastes 99% of its context window reading code—and a pattern to fix it
author: Scott Senkeresty
date: 2025-12-14
type: essay
status: published
publication: semanticinfrastructurelab.org
beth_topics:
  - reveal
  - reveal-v0.23
  - progressive-disclosure
  - token-efficiency
  - glass-box
  - semantic-infrastructure
  - type-first-architecture
related:
  - /lab/products/reveal
  - /foundation/SCOPE_OF_HOPE.md
  - /lab/architecture/SEMANTIC_OS_LAYERS.md
---

# Progressive Disclosure for AI Agents

*Why your AI assistant wastes 99% of its context window reading code—and a pattern to fix it*

---

## The $7,500 File

Here's what happens millions of times per day:

```
User: "How does authentication work in this codebase?"
Agent: *reads auth.py* (2,400 lines, 7,500 tokens)
Agent: "The authentication system uses JWT tokens..."
```

The agent read everything. It needed three functions. You paid for 7,500 tokens to learn what 50 could have told you.

This isn't a bug in your agent. It's a missing layer in our infrastructure—and it's costing more than money.

---

## The Pattern We're Missing

Human developers don't read files top-to-bottom. We scan, orient, then dive into what matters:

1. **Orient**: What's in this file? (table of contents)
2. **Navigate**: Where's the relevant section? (function names, class structure)
3. **Focus**: Give me that specific piece (just the code I need)

This is **progressive disclosure**—a UX pattern from the 1980s that we somehow forgot to build for AI agents.

Every code editor has this. Fold code, jump to definition, outline view. But when an agent needs to understand code? It gets raw text. No structure. No navigation. Just bytes.

---

## What Progressive Disclosure Looks Like

**Without progressive disclosure:**
```bash
cat auth.py        # 2,400 lines → 7,500 tokens
```

**With progressive disclosure:**
```bash
reveal auth.py                    # Structure → 50 tokens
# Functions: login, logout, verify_token, refresh_token, ...
# Classes: AuthManager, TokenStore, SessionHandler

reveal auth.py verify_token       # Just what we need → 45 tokens
def verify_token(token: str) -> Optional[User]:
    """Verify JWT and return user if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return User.get(payload["user_id"])
    except jwt.InvalidTokenError:
        return None
```

That's **150x fewer tokens** for the same understanding. Not a marginal improvement—a categorical shift.

---

## This Isn't About Saving Money

Yes, 150x token reduction cuts cost. But that's the least interesting part.

**What actually matters:**

**Longer sessions.** Context windows are finite. An agent burning 7,500 tokens per file exhausts its context in minutes. One spending 50 tokens per exploration can work for hours, building genuine understanding.

**Better reasoning.** Less noise, clearer signal. When 90% of an agent's context is irrelevant code, its reasoning degrades. Progressive disclosure keeps the window clean.

**Composable workflows.** When file exploration is cheap, agents can explore freely—checking this file, cross-referencing that one, verifying assumptions. The cognitive loop that makes senior developers effective becomes possible for machines.

**Democratized access.** Smaller models can do sophisticated code work when they're not drowning in tokens. Progressive disclosure makes capable agents cheaper to run.

---

## The Real Test: Shipping Software

This month, I released v0.23.1 of an open-source tool. Here's the complete transcript of my prompts to the AI agent:

```
1. "boot. load context"
2. "dogfood reveal"
3. "lets reveal docs and prepare for a release"
4. "push"
```

Four prompts. The agent:
- Loaded context from a prior session
- Tested the new features by using them on the codebase
- Updated version numbers and changelog
- Ran 465 tests (all passed)
- Committed, tagged, pushed
- Triggered the PyPI release

Total human typing: 25 words.

This wasn't a demo. It was a real release, now live on PyPI. The agent could work this effectively because it wasn't drowning in context. When file exploration costs 50 tokens instead of 7,500, the agent can explore freely—checking this file, cross-referencing that one, verifying assumptions. The same cognitive loop that makes senior developers effective becomes possible for machines.

---

## Why This Matters Beyond Efficiency

There's a deeper problem than wasted tokens.

**The 2025 AI landscape is broken.** OpenAI's latest reasoning models hallucinate at 48% rates on factual questions. 77% of businesses consider AI unreliability a major concern. Explainability tools create what researchers call a "false sense of understanding"—dashboards that look scientific but explain nothing.

The dominant AI systems are **black boxes**. You can't see their reasoning. You can't audit their decisions. You can't trace where conclusions came from. When they're wrong—and they're wrong a lot—you have no way to understand why.

Progressive disclosure is part of a different philosophy: **glass box** systems where structure is visible, reasoning is traceable, and you can inspect what's happening at every level.

When you run `reveal auth.py`, you're not just saving tokens. You're making the codebase *legible*. You see the architecture before the details. You understand the shape before the implementation. The agent's exploration becomes something you can follow, verify, question.

This is the same principle we need for AI systems themselves: structure first, detail on demand, everything auditable. The opposite of "trust me, I'm intelligent."

---

## The Architecture: URI-Based Resource Protocol

Progressive disclosure isn't just for code. The same pattern applies to any structured resource:

```bash
reveal app.py                     # Code structure
reveal env://DATABASE_URL         # Environment variable
reveal json://config.json/auth    # JSON path navigation
reveal ast://.?complexity>10      # Query code as data
reveal python://packages/requests # Installed package info
```

One command, one pattern: **show me the structure, let me navigate, extract what I need.**

The underlying principle: resources should expose an **agent-readable interface**. Not raw bytes. Not pixel-optimized GUIs. A semantic layer designed for machine understanding with human oversight.

We're extending this to databases, APIs, containers. Same pattern everywhere:

```bash
reveal postgres://prod/users      # Table structure (future)
reveal docker://my-app/logs       # Container inspection (future)
reveal https://api.github.com     # API schema exploration (future)
```

---

## Why This Should Be a Standard

Every agent framework solves this problem ad-hoc. LangChain has file loaders. AutoGPT has browsing tools. Cursor has codebase indexing. Each reinvents partial solutions that don't compose.

What's missing is a **protocol**—a shared convention for agent-readable resources.

HTTP gave us a standard for document retrieval. GraphQL gave us a standard for data queries. We need the equivalent for agent resource exploration: a way to say "show me the structure" and "give me this piece" that works across resource types.

The pattern is simple:
1. **Orientation**: What's here? (structure, schema, outline)
2. **Navigation**: What can I explore? (paths, queries, filters)
3. **Extraction**: Give me exactly this (targeted retrieval)

Any resource that exposes these three capabilities becomes agent-friendly. The efficiency follows automatically.

---

## The Larger Vision

Progressive disclosure is one layer of something bigger: a semantic infrastructure stack for intelligent systems.

**The problem:** AI systems today are epistemically brittle. No stable memory. No inspectable reasoning. No provenance. They're powerful pattern matchers operating in a semantic void—nothing underneath, nothing to build on.

**The deeper problem:** They're opaque. When 77% of businesses don't trust AI for critical work, the issue isn't just capability—it's visibility. You can't audit what you can't see. You can't trust what you can't verify.

**The vision:** A substrate where meaning is explicit, reasoning is traceable, and agents can build on solid semantic foundations. We call it **glass box AI**—not because the systems are simple, but because you can see through them.

Progressive disclosure makes code semantically navigable. Other layers solve other problems:

- **Semantic memory** that persists and compounds across sessions
- **Provenance tracking** so you know where conclusions came from
- **Tool contracts** that make agent capabilities composable
- **Human interfaces** that keep humans in the loop at the right abstraction level

We call this the Semantic OS. It's a 10-year vision. But progressive disclosure? That's working today. You can install it right now.

---

## What's Next

We're actively developing. The v0.23.1 release includes major architectural improvements—a 64% reduction in core module size through systematic extraction into focused packages, plus a new Type-First Architecture with decorator-aware code intelligence. The codebase is now significantly more maintainable: clear separation between data fetching (adapters), display logic (rendering), and file structure output.

**The Type-First Architecture** is designed and implementation is underway. The current architecture treats code structure as flat lists of functions and classes. The next version computes **containment relationships** from type invariants—methods know they belong to classes, nested functions know their parents.

This enables navigation patterns like:

```python
structure = reveal('app.py')
for method in structure / 'AuthManager':  # Navigate into class
    if method.complexity > 10:
        print(f"Complex: {method.name}")
```

Types become first-class citizens. Containment is computed, not stored. The semantic layer gets richer.

**Also in v0.23.0:** The `reveal://` meta-adapter lets Reveal introspect itself—listing analyzers, adapters, and quality rules. The new `--typed` flag shows hierarchical code structure with decorator awareness (`@property`, `@staticmethod`). It's the same progressive disclosure pattern applied recursively: Reveal understands Reveal.

---

## Try It

```bash
pip install reveal-cli
reveal your_file.py                    # See what's there
reveal your_file.py --outline          # Hierarchical view
reveal your_file.py function_name      # Extract specific code
reveal help://                         # Discover capabilities
```

The source is at [github.com/Semantic-Infrastructure-Lab/reveal](https://github.com/Semantic-Infrastructure-Lab/reveal). It's MIT licensed. The patterns are more valuable than the code—take them, adapt them, build better versions.

---

## The Question I'm Left With

If progressive disclosure is obviously right—and I think the 150x efficiency gain makes the case—why don't we have it everywhere?

Why can't I say `reveal postgres://prod/users` and get a navigable table structure? Why can't agents progressively explore API schemas the way developers explore codebases?

Part of the answer is that the tooling didn't exist. Now some of it does.

But the deeper answer might be that we've been building AI tools *for humans who then hand context to AI*—not building AI-native infrastructure from first principles. We gave agents human interfaces and wondered why they struggled.

The agents are here. The infrastructure is catching up. Progressive disclosure is one pattern.

What others are we missing?

---

*I'm Scott Senkeresty. I run the [Semantic Infrastructure Lab](https://semanticinfrastructurelab.org), where we're building the semantic substrate for intelligent systems—infrastructure that makes AI legible, auditable, and trustworthy. If this pattern resonates, I'd love to hear what you're building. If you think it's wrong, I'd love to hear that too.*

*[scott@semanticinfrastructurelab.org](mailto:scott@semanticinfrastructurelab.org)*

---

## Appendix: The Numbers

For those who want the data:

| Metric | Traditional | Progressive | Improvement |
|--------|-------------|-------------|-------------|
| Tokens to understand file structure | 7,500 | 50 | 150x |
| Tokens to extract one function | 7,500 | 45 | 166x |
| Context exhaustion (100K window) | ~13 files | ~2,000 explorations | 150x |
| Cost per codebase exploration | ~$0.15 | ~$0.001 | 150x |

*Measured on typical Python files (500-2,500 lines). Results vary by language and file structure.*

**What this enables:**
- Agent sessions that last hours, not minutes
- Smaller models doing sophisticated code work
- Exploration workflows that match human cognition
- Composable tool chains with predictable costs

The pattern is simple. The implications compound.

---

## Appendix: Validation

We dogfooded Reveal against its own codebase and beyond. Results from v0.24.0:

| Test | Result |
|------|--------|
| Files scanned | 571+ |
| Test suite | 465 tests passing (100%) |
| Token reduction | 10-150x confirmed |
| Complex functions found (AST query) | 1,122 |
| Quality rules | 28 rules across 10 categories |
| Analyzers | 14 language-specific + TreeSitter fallback |
| URI adapters | 6 (ast://, env://, help://, json://, python://, reveal://) |
| Architecture | 64% core module reduction via modular extraction |
| Real bugs discovered | 1 (bare except clause) |
| Overall grade | A |

This isn't marketing. It's measured.

---

**Related:**
- [Reveal on GitHub](https://github.com/Semantic-Infrastructure-Lab/reveal)
- [Reveal on PyPI](https://pypi.org/project/reveal-cli/)
- [About the Semantic Infrastructure Lab](https://semanticinfrastructurelab.org)
