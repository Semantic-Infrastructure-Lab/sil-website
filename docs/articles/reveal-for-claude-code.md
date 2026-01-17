---
title: "Reveal + Claude Code"
subtitle: "Teaching Your AI Agent to See Structure Before Reading Code"
author: "Scott Senkeresty"
date: "2026-01-06"
type: "article"
status: "draft"
audience: "developers"
topics: ["reveal", "claude-code", "ai-agents", "token-efficiency", "progressive-disclosure"]
related_projects: ["reveal"]
reading_time: "6 minutes"
beth_topics: [reveal, claude-code, ai-agents, token-efficiency, progressive-disclosure]
---

# Reveal + Claude Code

When Claude Code explores your codebase, it reads files. All of them. Every line, every comment, every import that won't matter.

Ask it to "fix the auth bug" and watch:
- Reads `auth.py` (3,200 tokens)
- Reads `config.py` because auth imports it (1,800 tokens)
- Reads `utils.py` for good measure (2,100 tokens)
- Finds the bug on line 47

You spent 7,100 tokens to fix a one-line typo.

**Reveal fixes this.** It shows Claude Code the structure of your code without reading every line.

```bash
reveal auth.py        # ~100 tokens - see what functions exist
reveal auth.py login  # ~50 tokens - extract just that function
```

Same answer. Fraction of the tokens.

---

## What Reveal Actually Does

Reveal parses your code and shows its structure:

```bash
$ reveal reveal/main.py

File: main.py (12.2KB, 389 lines)

Imports (15):
  reveal/main.py:3      import sys
  reveal/main.py:4      import os
  reveal/main.py:6      from .base import get_all_analyzers, FileAnalyzer
  ...

Functions (18):
  reveal/main.py:26     _setup_windows_console() [10 lines, depth:2]
  reveal/main.py:87     main() [21 lines, depth:3]
  reveal/main.py:136    _main_impl() [24 lines, depth:2]
  reveal/main.py:321    run_schema_validation(...) [65 lines, depth:3]
  ...

Classes (1):
  reveal/main.py:53     TeeWriter
```

That's real output from reveal's own codebase. 389 lines summarized in ~100 tokens.

Then extract what you need:

```bash
$ reveal reveal/main.py main

reveal/main.py:87-107 | main

     87  def main():
     88      """Main CLI entry point."""
     89      _setup_windows_console()
     90
     91      copy_setup = _setup_copy_mode()
     92      if copy_setup:
     93          tee_writer, captured_output, original_stdout = copy_setup
     94          sys.stdout = tee_writer
     95      else:
     96          captured_output = None
     97          original_stdout = None
     98
     99      try:
    100          _main_impl()
    101      except BrokenPipeError:
    102          devnull = os.open(os.devnull, os.O_WRONLY)
    103          os.dup2(devnull, sys.stdout.fileno())
    104          sys.exit(0)
    105      finally:
    106          if copy_setup:
    107              _handle_clipboard_copy(captured_output, original_stdout)
```

21 lines. Exactly what Claude Code needs to understand the entry point.

---

## Teaching Claude Code

Add this to your project's `CLAUDE.md`:

```markdown
## Code Exploration

When exploring unfamiliar code, use reveal before reading files:

1. `reveal <directory>` - See what files exist
2. `reveal <file>` - See structure (functions, classes, imports)
3. `reveal <file> <element>` - Extract specific function or class
4. Only use Read tool when you need the complete file

Example workflow:
reveal src/           # What's in src?
reveal src/api.py     # What functions are in api.py?
reveal src/api.py handle_request  # Show me that function
```

Claude Code will follow these instructions. It runs bash commands natively, so reveal just works.

---

## The Workflow

**Orient → Navigate → Focus**

```bash
# 1. ORIENT - What exists here?
$ reveal src/

src/
├── api/
│   ├── routes.py (456 lines, Python)
│   ├── middleware.py (234 lines, Python)
│   └── models.py (567 lines, Python)
├── core/
│   ├── auth.py (342 lines, Python)
│   └── config.py (189 lines, Python)
└── utils.py (123 lines, Python)

# 2. NAVIGATE - What's the shape of this file?
$ reveal src/core/auth.py

Functions (12):
  auth.py:45   authenticate [23 lines, depth:2]
  auth.py:89   validate_token [15 lines, depth:1]
  auth.py:112  refresh_session [34 lines, depth:2]
  ...

# 3. FOCUS - Extract what matters
$ reveal src/core/auth.py authenticate

[actual code appears here]
```

Each step: ~50-100 tokens. Reading all those files: ~5,000+ tokens.

---

## Finding Code Without Grepping

Reveal has an AST query adapter. Instead of grep:

```bash
# Find all functions with "auth" in the name
$ reveal 'ast://./src?name=*auth*'

Results: 7
  src/core/auth.py:45   authenticate [23 lines]
  src/core/auth.py:89   validate_token [15 lines]
  src/api/middleware.py:12  check_auth [8 lines]
  ...

# Find complex functions (cyclomatic complexity > 10)
$ reveal 'ast://./src?complexity>10'

Results: 3
  src/core/auth.py:112  refresh_session [34 lines, complexity: 12]
  src/api/routes.py:89  handle_upload [67 lines, complexity: 15]
  ...

# Find long functions (likely refactoring candidates)
$ reveal 'ast://./src?lines>50'
```

No file reading required. The AST adapter parses and queries directly.

---

## Quality Checks

Reveal has 43 quality rules. Claude Code can check as it works:

```bash
$ reveal reveal/main.py --check

reveal/main.py: Found 3 issues

reveal/main.py:8:101 ℹ️  E501 Line too long (120 > 100 characters)
  💡 Break line into multiple lines or refactor

reveal/main.py:321:1 ⚠️  C902 Function is too long: run_schema_validation (65 lines)
  💡 Consider refactoring if it grows beyond 100 lines

reveal/main.py:321:101 ℹ️  E501 Line too long (105 > 100 characters)
  💡 Break line into multiple lines or refactor
```

Real output. Real issues in reveal's own code.

Rule categories:
- **B** - Bugs (bare except, @staticmethod with self)
- **C** - Complexity (cyclomatic complexity, function length)
- **S** - Security (hardcoded secrets, Docker :latest)
- **E** - Style (line length)
- **D** - Duplicates

---

## Codebase Overview

For unfamiliar codebases:

```bash
$ reveal stats://./

Codebase Statistics: ./

Files:      205
Lines:      44,598 (31,449 code)
Functions:  1,261
Classes:    183
Complexity: 1.00 (avg)
Quality:    97.3/100
```

```bash
$ reveal 'imports://./?circular'

Circular Dependencies: 17

1. base.py -> registry.py -> treesitter.py -> base.py
2. base.py -> registry.py -> base.py
3. type_system.py -> elements.py -> type_system.py
...
```

Claude Code now knows:
- This is a medium-sized codebase (205 files, 44K lines)
- Quality is high (97.3/100)
- There's technical debt (17 circular deps)
- Where to focus attention

---

## What Reveal Supports

**Languages** (24 built-in): Python, JavaScript, TypeScript, Go, Rust, Java, C, C++, C#, Ruby, PHP, Lua, Scala, Bash, SQL, GDScript, plus tree-sitter fallback for 30+ more

**Config files**: YAML, JSON, TOML, Dockerfile, Nginx

**Documents**: Markdown (with link/code extraction), HTML, Jupyter notebooks

**Adapters** (10 URI schemes):
- `ast://` - Query code by complexity, name, size
- `stats://` - Codebase metrics
- `imports://` - Dependency analysis, circular detection
- `diff://` - Semantic structural diff
- `python://` - Python environment debugging
- `json://` - JSON navigation and queries
- `help://` - Built-in documentation

---

## Installation

```bash
pip install reveal-cli
reveal --version  # Should show 0.31.0 or later
```

## Quick Reference

| Task | Command |
|------|---------|
| Directory structure | `reveal src/` |
| File structure | `reveal file.py` |
| Extract element | `reveal file.py function_name` |
| Hierarchical view | `reveal file.py --outline` |
| Quality check | `reveal file.py --check` |
| Find by name | `reveal 'ast://.?name=*pattern*'` |
| Find complex code | `reveal 'ast://.?complexity>10'` |
| Codebase stats | `reveal stats://.` |
| Circular deps | `reveal 'imports://.?circular'` |
| Built-in help | `reveal help://` |

---

## The Point

Reveal doesn't make Claude Code smarter. It gives Claude Code what humans get naturally: the ability to see structure before diving into details.

When your context window holds structure instead of raw code, Claude Code can:
- Explore larger codebases
- Maintain context across longer conversations
- Handle complex refactors without "forgetting"

That's the value. Not magic—just better tools for how AI agents actually work.

---

## Learn More

- `reveal help://` - Built-in documentation
- `reveal --agent-help` - Reference guide for AI agents (~2,400 tokens)
- [GitHub](https://github.com/scottsen/reveal) - Source and issues
- [PyPI](https://pypi.org/project/reveal-cli/) - Package

---

*Reveal is part of the [Semantic Infrastructure Lab](https://semanticinfrastructurelab.org)*
