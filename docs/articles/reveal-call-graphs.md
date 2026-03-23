---
title: "Find Every Caller in Your Codebase With One Command"
subtitle: "reveal calls://: cross-file call graph queries for impact analysis, dead code, and refactoring"
author: "Scott Senkeresty"
date: "2026-03-15"
type: "article"
status: "published"
audience: "developers"
topics: ["reveal", "call-graph", "static-analysis", "refactoring", "code-navigation", "ast"]
beth_topics:
  - reveal
  - call-graph
  - calls-adapter
  - static-analysis
  - refactoring
  - code-navigation
  - ast-adapter
related_docs:
  - "reveal-introduction.md"
  - "reveal-pack-and-review.md"
canonical_url: "https://semanticinfrastructurelab.org/articles/reveal-call-graphs"
reading_time: "7 minutes"
---

# Find Every Caller in Your Codebase With One Command

**`calls://` — cross-file call graph queries for impact analysis, refactoring, and understanding code flow**

---

There's a question that comes up constantly when working on a codebase:

*"If I change this function, what breaks?"*

The answer requires knowing every place that function is called — across all files, not just the current one. With grep you can get close, but you'll miss indirect calls, get false positives from comments and strings, and have to mentally filter what's actually a caller vs a usage.

Reveal's `calls://` adapter builds a proper call graph index and answers the question directly.

> **Note:** `calls://` is marked experimental. It works well on Python codebases; coverage on other languages varies.


```bash
reveal 'calls://src/?target=validate_token'
```

**Output:**
```
Callers of validate_token (4 found):

src/auth/middleware.py:23     authenticate_request
src/auth/middleware.py:89     refresh_session
src/api/routes/users.py:47    get_user_profile
src/api/routes/admin.py:156   check_admin_access

Next: reveal 'calls://src?target=validate_token&depth=2'   # Callers-of-callers
      reveal src/auth/middleware.py authenticate_request   # Read a caller
```

Four callers, exact file and line numbers, no noise.

---

## The three questions calls:// answers

### 1. Who calls this? (impact analysis)

Before changing `validate_token`, you need to know its blast radius:

```bash
reveal 'calls://src/?target=validate_token'
```

If you get 12 callers across 8 files, that's a significant change. If you get 1, it's a targeted edit. Either way, you know before you start.

### 2. What does this call? (forward lookup)

Sometimes you want to trace *down* rather than up — understand what a function depends on:

```bash
reveal 'calls://src/?callees=validate_token'
```

**Output:**
```
validate_token calls:

src/auth/tokens.py:14    decode_jwt
src/auth/tokens.py:23    check_expiry
src/models/session.py:67 load_session
(3 builtins hidden — use ?builtins=true to include)
```

Python builtins (`len`, `str`, `ValueError`, etc.) are filtered by default — you almost never care that a function calls `len`. Add `?builtins=true` to include them.

### 3. Which functions are most coupled? (architectural analysis)

Which functions in your codebase are called from the most places? High in-degree means high coupling — changes there have high blast radius.

```bash
reveal 'calls://src/?rank=callers&top=10'
```

**Output:**
```
Most-called functions: src/
Ranking by:            caller count (in-degree)
Showing:               top 10 of N unique callees

  validate_item  (18 callers)
    src/validation.py:23  check_input
    src/validation.py:67  validate_batch
    src/api/routes.py:44  create_item
    … and 15 more

  get_db_connection  (14 callers)
    src/database.py:88  execute_query
    src/models/user.py:34  get_user
    src/models/item.py:21  save_item
    … and 11 more
  ...
```

One thing to expect on real Python projects: builtins like `get`, `append`, `join` will appear at the top with hundreds of callers. Filter them out mentally or use `?top=20` to get past them to your domain functions.

The top domain functions in this list are your architectural hot zone — the ones worth abstracting, documenting carefully, and testing thoroughly.

---

## How it differs from grep

```bash
grep -r "validate_token" src/    # Text search
```

vs.

```bash
reveal 'calls://src/?target=validate_token'   # Call graph query
```

The difference:
- Grep finds **text occurrences** — strings, comments, variable names, imports
- `calls://` finds **actual function calls** — only invocations, only within function bodies

You get fewer results with `calls://`, but all of them are real.

---

## Transitive callers (call chains)

Sometimes you need to know not just who calls your function, but who calls *those callers*:

```bash
reveal 'calls://src/?target=validate_token&depth=2'
```

```
Callers of validate_token (depth=2):

Level 1 (direct callers):
  middleware.py:23    authenticate_request
  routes/users.py:47  get_user_profile

Level 2 (callers of callers):
  middleware.py:23    authenticate_request
    ← wsgi.py:15     dispatch_request
    ← wsgi.py:38     handle_error
  routes/users.py:47  get_user_profile
    ← router.py:67   route_request
```

Depth is capped at 5 to prevent combinatorial explosion on tightly-coupled codebases.

---

## Visualizing call graphs

`calls://` supports Graphviz dot output for documentation and presentation:

```bash
reveal 'calls://src/?target=validate_token&format=dot' | dot -Tsvg > call_graph.svg
```

Or PNG:
```bash
reveal 'calls://src/?target=main&format=dot' | dot -Tpng > architecture.png
```

Good for: architecture docs, onboarding materials, "what does this module touch?" diagrams.

---

## Within a single file (the cheaper option)

For within-file call analysis, use `ast://` — it doesn't build a project-wide index so it's faster:

```bash
# See what functions exist in a file and what they call
reveal 'ast://src/auth.py?show=calls'

# Find callers of a function within the same file
reveal 'ast://src/auth.py?calls=validate_token'
```

Use `ast://` when you're looking within one file. Use `calls://` when you need cross-file coverage.

---

## Practical workflows

### Before refactoring a function

```bash
# 1. How many callers?
reveal 'calls://src/?target=process_payment'

# 2. What does it call?
reveal 'calls://src/?callees=process_payment'

# 3. Now you have the full picture: blast radius + dependencies
```

### Finding dead code

```bash
# Surface all uncalled functions across the project at once
reveal 'calls://src/?uncalled'
```

**Output:**
```
Dead code candidates: src/
Total defined:        847 functions/methods
Uncalled:             12
Note: excludes __dunder__ methods and @property/@classmethod/@staticmethod

  src/legacy/sync.py:33   legacy_sync_handler  (function)
  src/utils/compat.py:91  _py2_fallback         (function, private)
  src/api/deprecated.py:14  old_create_endpoint (function)
  ...
```

This scans the entire project and lists every function with no callers — much faster than checking one at a time. Excludes dunder methods, properties, and classmethods automatically (they're called implicitly).

For targeted confirmation on a specific function:
```bash
reveal 'calls://src/?target=legacy_sync_handler'
# → No callers found.
```

Combine with `reveal check src/ --select R` (refactoring rules) to surface candidates systematically.

### Understanding an unfamiliar codebase

```bash
# Start with the most-called functions — they're the core abstractions
reveal 'calls://src/?rank=callers&top=20'

# Then explore one by one
reveal 'calls://src/?callees=get_db_connection'
```

### Architecture documentation

```bash
# Generate a call graph for your main entry point
reveal 'calls://src/?target=main&depth=3&format=dot' | dot -Tsvg > docs/call_graph.svg
```

---

## Performance

`calls://` builds an index the first time you run it on a directory and caches it by file modification time. Subsequent runs on unchanged code are fast. Large projects (10K+ Python files) may take a few seconds on first run; after that, cached.

The index is directory-scoped — `calls://src/` and `calls://src/auth/` build separate indexes.

---

## The broader picture

`calls://` is one piece of Reveal's approach to treating code as structured data rather than text. Grep treats your codebase as a pile of strings. `calls://` treats it as a graph of semantic relationships.

The difference shows up when you need answers that text search can't give you cleanly — impact analysis, dead code detection, coupling metrics, architectural understanding. Those answers are in the graph. Reveal surfaces them directly.

```bash
pip install reveal-cli

reveal help://calls            # Full reference with examples
reveal 'calls://src/?target=YOUR_FUNCTION'
```

---

*Part of the Reveal documentation series. See also:*
- *[Two Commands That Change How You Work With Code](/articles/reveal-pack-and-review) — pack and review*
- *[Stop Reading Code. Start Understanding It.](/articles/reveal-introduction) — the big picture*
