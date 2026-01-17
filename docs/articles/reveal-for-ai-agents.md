---
title: "Reveal for AI Agents"
subtitle: "How Claude Code, Cursor, and Copilot Explore Code 25x Faster"
author: "Scott Senkeresty"
date: "2026-01-05"
type: "article"
status: "draft"
audience: "developers"
topics: ["reveal", "ai-agents", "claude-code", "cursor", "copilot", "token-efficiency"]
related_projects: ["reveal"]
reading_time: "7 minutes"
beth_topics: [reveal, ai-agents, token-efficiency, progressive-disclosure]
---

# Reveal for AI Agents

Your AI coding assistant reads too much.

When you ask Claude Code to "fix the auth bug," it reads `auth.py` (3,200 tokens), then `config.py` (1,800 tokens), then `utils.py` (2,100 tokens). It finds the bug on line 47. You just spent 7,100 tokens on a one-line fix.

**Reveal changes this.**

```bash
reveal auth.py          # 100 tokens - see structure
reveal auth.py login    # 50 tokens - extract the function
```

Same answer. 70x fewer tokens.

---

## The Problem: AI Agents Think Like Humans

When humans explore code, we scroll. We skim. We skip boring parts. Our eyes do progressive disclosure automatically.

AI agents can't skim. They read everything. Every line. Every comment. Every import statement that will never matter.

This is why your context window fills up. This is why Claude "forgets" what you said 10 minutes ago. This is why complex refactors fail halfway through.

**The solution isn't smarter AI. It's better tools.**

---

## How Reveal Works

Reveal gives AI agents what humans get for free: structure before content.

```bash
$ reveal src/auth/handler.py

File: handler.py (342 lines, Python)

Imports (8):
  handler.py:1    from fastapi import APIRouter, Depends
  handler.py:2    from ..models import User, Session
  ...

Functions (12):
  handler.py:45   authenticate [23 lines, depth:2]
  handler.py:89   validate_token [15 lines, depth:1]
  handler.py:112  refresh_session [34 lines, depth:2]
  ...

Classes (2):
  handler.py:156  AuthHandler
  handler.py:234  TokenManager
```

**100 tokens instead of 3,400.** The agent now knows:
- What functions exist
- How complex they are (line count, nesting depth)
- Where to look for the bug

Then it extracts only what it needs:

```bash
$ reveal src/auth/handler.py authenticate

handler.py:45-67 | authenticate

    45  async def authenticate(
    46      credentials: Credentials,
    47      db: Session = Depends(get_db)
    48  ) -> AuthResult:
    49      """Authenticate user with credentials."""
    50      user = await db.query(User).filter_by(
    51          email=credentials.email
    52      ).first()
    53
    54      if not user:
    55          raise InvalidCredentials()
    56      ...
```

**50 more tokens.** Now it has exactly what it needs.

---

## Integration: Claude Code

Claude Code can use reveal directly:

```bash
# In your CLAUDE.md or system prompt:
When exploring unfamiliar code:
1. Use `reveal <path>` to see structure first
2. Use `reveal <path> <element>` to extract specific code
3. Only use `cat` or `Read` when you need the full file

# Example workflow:
reveal src/              # What directories exist?
reveal src/api/          # What's in the API layer?
reveal src/api/routes.py # What endpoints are defined?
reveal src/api/routes.py create_user  # Show me this one
```

**Token savings in practice:**

| Task | Without Reveal | With Reveal | Savings |
|------|----------------|-------------|---------|
| Find a function | 7,500 tokens | 150 tokens | 50x |
| Understand a module | 15,000 tokens | 400 tokens | 37x |
| Explore new codebase | 50,000 tokens | 2,000 tokens | 25x |

---

## Integration: Cursor

Add reveal to your Cursor rules (`.cursorrules`):

```
When exploring code structure, prefer reveal over reading entire files:

- `reveal .` shows directory structure
- `reveal file.py` shows functions/classes without reading code
- `reveal file.py function_name` extracts specific element
- `reveal 'ast://./src?complexity>10'` finds complex functions

Use reveal first, then read specific sections as needed.
```

Cursor's AI will learn to check structure before diving into code.

---

## Integration: GitHub Copilot

For Copilot Chat, use reveal in your terminal alongside:

```bash
# You ask Copilot: "Where is authentication handled?"
# Instead of Copilot reading everything, you run:

reveal 'ast://./src?name=*auth*'

# Output:
# src/auth/handler.py:45  authenticate [23 lines]
# src/auth/middleware.py:12  verify_auth [15 lines]
# src/api/routes.py:89  auth_router [8 lines]

# Now you can tell Copilot exactly where to look
```

---

## The Breadcrumb System

Reveal tells agents what to do next:

```bash
$ reveal src/api/

├── routes.py (456 lines, Python)
├── middleware.py (234 lines, Python)
├── models.py (567 lines, Python)
└── utils.py (123 lines, Python)

Next: reveal src/api/<file>   # See file structure
      reveal 'ast://src/api?complexity>10'   # Find complex code
```

These aren't hints for humans. They're **instructions for agents**. The agent reads the breadcrumb and knows exactly what command to run next.

---

## Beyond Files: URI Adapters

Reveal isn't just for code files. It has 10 URI adapters for querying different resources:

### Find Complex Code
```bash
reveal 'ast://./src?complexity>10'
reveal 'ast://./src?lines>100'
reveal 'ast://./src?complexity>15&lines>50'  # Combined
```

### Codebase Health
```bash
reveal stats://./src

# Output:
# Files: 205
# Lines: 44,598
# Functions: 1,261
# Quality: 97.3/100
```

### Circular Dependencies
```bash
reveal 'imports://./src?circular'

# Output:
# Circular Dependencies: 17
# 1. base.py -> registry.py -> treesitter.py -> base.py
# 2. ...
```

### Python Environment
```bash
reveal python://doctor    # Is the environment healthy?
reveal python://packages  # What's installed?
```

### Structural Diff
```bash
reveal 'diff://old.py:new.py'

# Shows semantic changes:
# + new_function [NEW - 45 lines]
# - removed_function [REMOVED]
# ~ modified_function [signature changed]
```

### JSON Navigation
```bash
reveal json://package.json              # Pretty-printed with metadata
reveal json://package.json/scripts      # Navigate to specific key
reveal json://config.json?schema        # Infer type structure
reveal json://data.json?flatten | grep database  # Grep-friendly format
```

AI agents work with JSON constantly—`package.json`, `tsconfig.json`, config files. The `?schema` feature is perfect for understanding unknown JSON structure without reading the whole file.

### Quality Hotspots
```bash
reveal stats://./src --hotspots

# Output:
# Top Hotspots (10):
# 1. providers/gamma.py - Quality: 68.6/100 | Score: 30.1
# 2. services/inference.py - Quality: 83.4/100 | Score: 24.0
# ...
```

Instantly find the worst files in a codebase. Perfect for prioritizing refactoring.

---

## Advanced Workflows

### Pipeline Integration

Reveal works with Unix pipelines via `--stdin`:

```bash
# Check quality of files changed in last 3 commits
git diff --name-only HEAD~3 | reveal --stdin --check

# See structure of all changed Python files
git diff --name-only | grep '\.py$' | reveal --stdin --outline

# Find complex functions in changed files
git diff --name-only origin/main | reveal --stdin --format=json | \
  jq '.structure.functions[] | select(.complexity > 10)'
```

### Semantic Slicing

For large files or JSONL logs, slice by semantic units (not lines):

```bash
reveal large_module.py --head 5     # First 5 functions
reveal large_module.py --tail 3     # Last 3 functions
reveal conversation.jsonl --range 48-52  # Records 48-52
```

This is critical for exploring conversation logs, JSONL data, or long modules without reading everything.

### PR Review Speedrun

```bash
# 1. What changed?
git diff --name-only origin/main | reveal --stdin

# 2. Quality issues in changed files?
git diff --name-only origin/main | grep '\.py$' | reveal --stdin --check

# 3. Any new complex functions?
git diff --name-only origin/main | grep '\.py$' | \
  xargs -I{} reveal 'ast://{}?complexity>10'
```

### Python Environment Debugging

When imports fail or code changes don't take effect:

```bash
reveal python://doctor

# Output:
# Health Score: 50/100
# Issues:
#   ✗ Found 71 stale .pyc files
#   ✗ Multiple editable .pth files for 'package'
# Recommendations:
#   > find . -type d -name __pycache__ -exec rm -rf {} +
```

This catches the "why isn't my code change working?" class of bugs instantly.

---

## Quality Checks

Reveal has 43 quality rules. Agents can check code as they work:

```bash
reveal src/handler.py --check

# Output:
# handler.py:45:1 C901 Function too complex (15 > 10)
# handler.py:89:101 E501 Line too long (120 > 100)
# handler.py:156:1 B003 Property with side effects
```

Categories:
- **B** - Bugs (bare except, static method with self, etc.)
- **C** - Complexity (cyclomatic complexity, function length)
- **S** - Security (hardcoded secrets, insecure patterns)
- **D** - Duplicates (copy-pasted code)
- **N** - Nginx configuration issues
- **V** - Validation (schema conformance)

---

## The Anti-Pattern

**Don't do this:**
```bash
cat src/auth/handler.py        # 3,400 tokens
cat src/auth/middleware.py     # 1,200 tokens
cat src/auth/models.py         # 2,800 tokens
grep -r "authenticate" src/    # 500 tokens
# Total: 7,900 tokens
```

**Do this:**
```bash
reveal src/auth/                              # 50 tokens
reveal 'ast://src/auth?name=*authenticate*'   # 30 tokens
reveal src/auth/handler.py authenticate       # 80 tokens
# Total: 160 tokens
```

Same information. 50x fewer tokens.

---

## Why This Matters

Token efficiency isn't about cost savings (though that's nice). It's about **capability**.

With 100K context window:
- Without reveal: ~15 files before context fills up
- With reveal: ~500 files of structural understanding

That's the difference between "I can help with small fixes" and "I can refactor your entire authentication system."

**Reveal doesn't make AI smarter. It makes AI capable of bigger tasks.**

---

## Getting Started

```bash
pip install reveal-cli

# Try it on your project
reveal .
reveal src/main.py
reveal src/main.py main
reveal --agent-help    # Built-in guide for AI agents
```

---

## Built-in Documentation

Reveal has comprehensive help for AI agents:

```bash
reveal --agent-help       # Quick reference (~2,400 tokens)
reveal --agent-help-full  # Complete guide (~12,000 tokens)
reveal help://            # Interactive help system
```

The `--agent-help` flag is designed to be included in system prompts. It teaches AI agents the reveal workflow.

---

## Learn More

- [Reveal Quick Start](/articles/reveal-quickstart) - 3-minute intro
- [Reveal Deep Dive](/articles/reveal-introduction) - Philosophy and architecture
- [GitHub](https://github.com/scottsen/reveal) - Source and issues
- [PyPI](https://pypi.org/project/reveal-cli/) - Installation

---

*Reveal is part of the [Semantic Infrastructure Lab](https://semanticinfrastructurelab.org) - building infrastructure for transparent, efficient AI agents.*
