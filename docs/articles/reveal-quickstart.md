---
title: "Reveal: See Code Structure, Not Code"
subtitle: "50 tokens instead of 7,500"
author: "Scott Senkeresty"
date: "2026-01-05"
type: "article"
status: "draft"
audience: "developers"
topics: ["reveal", "progressive-disclosure", "ai-agents", "code-exploration"]
related_projects: ["reveal"]
reading_time: "3 minutes"
beth_topics: [reveal, progressive-disclosure, token-efficiency]
---

# Reveal: See Code Structure, Not Code

```bash
$ cat app.py      # 7,500 tokens - Claude reads everything
$ reveal app.py   # 50 tokens - Claude sees structure
```

That's it. That's the pitch.

---

## Install

```bash
pip install reveal-cli
```

## Try It

```bash
reveal .                    # Directory structure
reveal app.py               # File structure (imports, functions, classes)
reveal app.py main          # Extract just the main function
reveal app.py --check       # Find quality issues
```

---

## The Pattern

**Orient → Navigate → Focus**

```bash
# 1. ORIENT - What exists?
reveal .
reveal src/

# 2. NAVIGATE - What's the shape?
reveal app.py              # Flat list
reveal app.py --outline    # Hierarchy

# 3. FOCUS - Extract what you need
reveal app.py process_data
```

Each step costs ~50 tokens. Reading the whole file costs ~7,500.

---

## For AI Agents

Reveal was built for Claude Code, Cursor, and Copilot. The breadcrumbs tell agents what to do next:

```
reveal app.py

Functions (8):
  app.py:23    validate_token [12 lines, depth:1]
  app.py:47    load_config [23 lines, depth:1]
  ...

Next: reveal app.py <function>   # Extract specific element
      reveal app.py --check      # Check code quality
```

**Progressive disclosure**: Structure first, code second.

---

## Beyond Files

Reveal has 10 URI adapters for different resources:

```bash
reveal 'ast://./src?complexity>10'      # Find complex functions
reveal 'stats://./src'                  # Codebase metrics
reveal 'imports://./src?circular'       # Detect circular deps
reveal 'diff://old.py:new.py'           # Semantic diff
reveal help://                          # Discover more
```

---

## Quality Checks

43 rules across 12 categories:

```bash
reveal app.py --check

# Output:
# app.py:47:1 C901 Function too complex (15 > 10)
# app.py:89:101 E501 Line too long (120 > 100)
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Directory | `reveal .` |
| File structure | `reveal file.py` |
| Hierarchy | `reveal file.py --outline` |
| Extract element | `reveal file.py function_name` |
| Quality check | `reveal file.py --check` |
| Find complex | `reveal 'ast://.?complexity>10'` |
| Codebase stats | `reveal stats://./src` |
| All adapters | `reveal help://adapters` |

---

## Learn More

- [Reveal Deep Dive](/articles/reveal-introduction) - Philosophy and architecture
- [GitHub](https://github.com/scottsen/reveal) - Source and issues
- `reveal help://` - Built-in documentation

---

*Reveal is part of the [Semantic Infrastructure Lab](https://semanticinfrastructurelab.org) - building tools for transparent, efficient AI agents.*
