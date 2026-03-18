---
title: "Two Commands That Change How You Work With Code"
subtitle: "reveal pack and reveal review: token-budgeted context + automated PR review"
author: "Scott Senkeresty"
date: "2026-03-15"
type: "article"
status: "published"
audience: "developers"
topics: ["reveal", "ai-agent", "token-efficiency", "code-review", "ci-cd", "progressive-disclosure"]
beth_topics:
  - reveal
  - token-efficiency
  - code-review
  - ci-cd
  - ai-agent
  - progressive-disclosure
  - reveal-pack
  - reveal-review
related_docs:
  - "reveal-for-ai-agents.md"
  - "reveal-introduction.md"
canonical_url: "https://semanticinfrastructurelab.org/articles/reveal-pack-and-review"
reading_time: "8 minutes"
---

# Two Commands That Change How You Work With Code

**`reveal pack` and `reveal review` — token-budgeted context snapshots and automated PR review**

---

Two of the most useful things Reveal does are also the least documented.

`reveal pack` solves the "I need to give an AI agent context about this codebase but I don't know which files matter" problem.

`reveal review` solves the "I want real code review feedback without running three separate tools" problem.

Both are single commands. Both produce structured, actionable output. Both work in CI.

---

## `reveal pack` — The Right Files, Not All the Files

Here's a frustrating loop that happens constantly with AI coding agents:

1. You start a task: "refactor the authentication layer"
2. The agent reads `auth.py` — but auth imports `config.py`, `models.py`, `middleware.py`...
3. The agent reads those too
4. You're 40K tokens in before any actual work happens
5. You hit the context limit and the agent forgets the beginning

**The problem isn't that agents are bad at reading. It's that nobody curates what they should read.**

`reveal pack` does the curation:

```bash
reveal pack .
```

**Output:**
```
Selected 8 files within 4000-token budget:

  Entry points:
    app.py              (247 lines, 1,840 tokens)
    cli.py              (89 lines, 680 tokens)

  Key directories:
    src/auth/handler.py (156 lines, 1,190 tokens)
    src/models/user.py  (94 lines, 720 tokens)

  Recently modified:
    src/auth/tokens.py  (67 lines, 510 tokens)

  Budget used: 3,940 / 4000 tokens
  Skipped: 34 files (stubs, tests, generated)
```

You get the files that matter, sized to fit. Not all 39 Python files. Not random guesses. The ones that are most likely to give an agent useful orientation.

### Controlling the budget

```bash
reveal pack . --budget 10000              # More files, bigger context
reveal pack . --budget 500-lines          # Line count instead of tokens
reveal pack . --focus authentication      # Boost auth-related files to top
reveal pack ./src --verbose               # Show per-file token counts
```

The `--focus` flag is particularly useful: it doesn't filter out other files, it just boosts files whose paths match your topic to the front of the queue.

### For AI agents specifically

```bash
# Get the file list as JSON for programmatic use
reveal pack . --format json | jq '.selected[].relative'
```

This is the intended agent workflow:
1. Agent calls `reveal pack . --format json`
2. Gets back a list of 8–12 file paths
3. Reads *those* files instead of crawling the whole project
4. Has context budget left over for actual reasoning

### How it decides what matters

The priority algorithm is intentional, not magic:

1. **Entry points** — `main.py`, `app.py`, `cli.py`, config files. These are where execution starts and where you understand architecture.
2. **Focus matches** — if you said `--focus auth`, files with `auth` in their path come next.
3. **Key directories** — `core/`, `api/`, `models/`, `auth/` — these names signal importance.
4. **Recency** — files modified recently are more likely to be relevant to the current task.
5. **Near-empty files excluded** — stub `__init__.py` files with 2 lines of content don't earn a slot.

---

## `reveal review` — PR Review in One Command

Code review usually means running several things and assembling the picture yourself:

```bash
git diff main..feature           # See what changed
reveal check src/ --select B,S  # Quality check
reveal hotspots src/             # Find complexity problems
```

`reveal review` does all three in one pass and formats the result for humans and CI alike:

```bash
reveal review main..feature
```

**Output:**
```
Structural Changes (6 files)
  src/auth/handler.py      modified
  src/auth/tokens.py       modified
  src/models/user.py       modified
  tests/test_auth.py       added
  tests/test_tokens.py     added
  config/defaults.yaml     modified

Quality Violations (3)
  ERROR   B006  src/auth/handler.py:47   Silent exception swallowing
  WARNING C001  src/auth/tokens.py:23    Complexity 18 (threshold: 10)
  WARNING I003  src/models/user.py:5     Unused import: datetime

Hotspots
  src/auth/handler.py   quality: 71/100, complexity: 22
  src/auth/tokens.py    quality: 84/100

Complex Functions
  handler.py:35  refresh_session  complexity: 22
  tokens.py:23   validate_claims  complexity: 18

Recommendation: ⚠️  Review required — 1 error, 2 warnings
```

One command, complete picture.

### CI gate integration

```bash
# Gate on any errors (exit code 2 = has errors)
reveal review main..HEAD --format json \
  | jq '.sections.violations | map(select(.severity=="error")) | length == 0'

# Gate on overall status
reveal review . --format json | jq '.overall_status == "pass"'
```

Exit codes: `0` = clean, `1` = warnings only, `2` = errors. Shell-script friendly.

In a GitHub Actions workflow:
```yaml
- name: Reveal Review
  run: reveal review ${{ github.base_ref }}..${{ github.head_ref }}
  # exits 2 (and fails) if there are errors
```

### Reviewing without a git range

When you just want quality feedback on the current state of a directory:

```bash
reveal review .            # Review everything in working directory
reveal review ./src        # Review just src/
```

This runs the full quality check + hotspot analysis, no diff needed. Good for: "I just refactored this module, how does it look?"

---

## Using them together

The natural workflow for starting a new task with an AI agent:

```bash
# Step 1: Let pack curate what's relevant
reveal pack . --focus authentication --format json > /tmp/context.json

# Step 2: Review the current state before touching anything
reveal review src/auth/
```

Now the agent has:
- A curated reading list (not 100 files, the right 10)
- A quality baseline (what was already broken before you started)

After the work:
```bash
# Step 3: Review what you changed
reveal review main..HEAD
```

You get a diff + quality check + hotspot analysis — all in one.

---

## The point

`reveal pack` and `reveal review` are workflow tools. They don't do anything you couldn't assemble yourself from lower-level commands. What they do is eliminate the assembly step so you can focus on the actual work.

`pack` answers: *what should I read?*
`review` answers: *is this any good?*

Both questions come up on every PR. Both now have one-command answers.

```bash
pip install reveal-cli

reveal pack . --help
reveal review . --help
reveal help://pack
reveal help://review
```

---

*Part of the Reveal documentation series. See also:*
- *[Reveal for AI Agents](/articles/reveal-for-ai-agents) — complete agent workflow guide*
- *[Stop Reading Code. Start Understanding It.](/articles/reveal-introduction) — the big picture*
- *[Reveal Quick Start](/articles/reveal-quickstart) — get going in 5 minutes*
