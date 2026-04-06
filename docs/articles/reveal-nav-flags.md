---
title: "Stop Scrolling. Start Navigating."
subtitle: "Four commands for understanding a complex function without reading it line by line"
author: "Scott Senkeresty"
date: "2026-04-06"
type: "article"
status: "published"
linkedin_posted: true
audience: "developers"
topics: ["reveal", "code-navigation", "ast", "ai-agent", "token-efficiency", "debugging"]
beth_topics:
  - reveal
  - code-navigation
  - ast-adapter
  - token-efficiency
  - ai-agent
  - debugging
  - nav-flags
related_docs:
  - "reveal-introduction.md"
  - "reveal-call-graphs.md"
canonical_url: "https://semanticinfrastructurelab.org/articles/reveal-nav-flags"
reading_time: "7 minutes"
session_id: "celestial-moon-0406"
---

# Stop Scrolling. Start Navigating.

**Four commands for understanding a complex function without reading it line by line**

---

You get a bug report. The stack trace says `processor.py:285`. You open the file. The function is 180 lines.

You don't read 180 lines. You scan, you guess, you jump to what looks relevant, and you hope you didn't miss the branch that matters.

What you're actually doing — what every experienced developer does — is asking four questions:

1. **What's the structure?** Where are the branches, loops, and exits?
2. **Where am I?** What scope is this line actually in?
3. **What happened to this variable?** Where was it set, and where was it used?
4. **What does this section call?** What does it depend on?

These are navigation moves, not reading moves. And until recently, you had to perform them manually — scrolling, searching, holding structure in your head.

Reveal v0.72.0 makes each question a single command:

| Question | Command |
|----------|---------|
| What's the structure? | `--outline` |
| Where am I? | `--scope :LINE` |
| What happened to this variable? | `--varflow VAR` |
| What does this section call? | `--calls START-END` |

Together, they let you triangulate to exactly what you need without reading the full function body.

---

## The four moves

### 1. What's the structure? (`--outline`)

Before you read anything, see the shape:

```bash
reveal src/processor.py handle_request --outline
```

```
DEF handle_request  L1→L180
  FOR  item in queue  L12→L60
    IF  item.valid  L15→L45
      TRY  L20→L44
        EXCEPT  ValidationError  L38→L44
    ELIF  item.pending  L47→L59
  IF  retry_count > MAX_RETRIES  L62→L70
    RETURN  None  L70
  WHILE  not result.complete  L85→L140
    IF  result.status == 'error'  L92→L105
  RETURN  result  L178
```

One glance tells you: there's a `FOR` loop with validation, a retry gate, a `WHILE` loop that processes, and a return at the end. You now know where the branches are. You know where to look.

The default depth is 3. Go deeper with `--depth 5` if the function is heavily nested.

---

### 2. Where am I? (`--scope :LINE`)

You have a line number from a stack trace or a grep result. What scope is it in?

```bash
reveal src/processor.py :92 --scope
```

```
DEF     L1→L180        handle_request
  WHILE   L85→L140       while not result.complete
    IF      L92→L105       if result.status == 'error'

      ▶ L92: if result.status == 'error':
```

You're inside the `IF` block at L92, which is inside the `WHILE` loop, which is inside `handle_request`. That's context you'd normally build by scrolling up from line 92. Now it's one command.

---

### 3. What happened to this variable? (`--varflow VAR`)

Before you read any logic, you want to know: where does `result` come from, and where is it used?

```bash
reveal src/processor.py handle_request --varflow result
```

```
WRITE     L23:   result = None
WRITE     L88:   result = self._start_job(item)
READ/COND L92:   if result.status == 'error':
READ      L99:   self.log(result.error)
READ/COND L112:  if result.complete:
WRITE     L118:  result = self._retry(result)
READ      L178:  return result
```

Every assignment. Every conditional read. Every usage. In document order.

You can see immediately that `result` is initialized to `None` at L23, then assigned at L88, then read repeatedly — and reassigned at L118 if a retry happens. If something is wrong with `result`, the writes are at L23, L88, and L118. You didn't need to read the function to know that.

---

### 4. What does this section call? (`--calls START-END`)

You've identified a suspicious section — say, lines 88-105. What does it actually call?

```bash
reveal src/processor.py handle_request --calls 88-105
```

```
L88:   self._start_job(item)
L92:   result.status
L99:   self.log(result.error)
L101:  self.metrics.increment('errors')
L104:  raise ProcessingError(result.error)
```

Every call site in that range, with callee name and line number. No reading required.

---

## A real example: navigating a bug in Reveal itself

The best demonstration is a real one.

Reveal's `_walk_var` function — the function that *implements* `--varflow` — is 124 lines and composed entirely of inner closures: `_walk_assignment`, `_walk_named_expression`, `_walk_for`, `_walk_with`, `_walk_if_while`. Recently, a bug was reported: variable flow tracking was producing incorrect results for augmented assignments (`x += 1`).

Here's how we investigated it using the same tools.

**First: get the skeleton.**

```bash
reveal reveal/adapters/ast/nav.py _walk_var --outline
```

```
DEF _walk_var  L364→L488
  DEF  walk(n: Any, c: str) -> None  L379→L405
    IF  n.end_point[0] + 1 < from_line or line > to_line  L385→L386
      RETURN  L386
    IF  ntype == 'identifier' and get_text(n) == var_name  L388→L391
    IF  ntype in ('assignment', 'augmented_assignment')  L393→L405
    ELIF  ntype == 'named_expression'  L395→L396
    ELIF  ntype == 'for_statement'  L397→L398
    ...
  DEF  _walk_assignment(n: Any, ntype: str, c: str) -> None  L407→L425
    IF  left  L411→L414
      IF  ntype == 'augmented_assignment'  L412→L413
    IF  right  L415→L416
    FOR  child in n.children  L423→L425
      IF  (child.start_byte, child.end_byte) not in processed  L424→L425
  DEF  _walk_for(n: Any, c: str) -> None  L434→L451
    ...
```

The skeleton reveals immediately that the logic for `augmented_assignment` lives in `_walk_assignment`, specifically around L412. That's where to look.

**Second: trace the `processed` set.**

The `processed` set is used to avoid revisiting nodes. If it's broken, the whole traversal breaks.

```bash
reveal reveal/adapters/ast/nav.py _walk_var --varflow processed
```

```
WRITE     L419:  processed = {
READ/COND L424:  if (child.start_byte, child.end_byte) not in processed:
WRITE     L439:  processed: set = set()
READ      L441:  processed.add((left.start_byte, left.end_byte))
READ      L444:  processed.add((right.start_byte, right.end_byte))
READ      L447:  processed.add((body.start_byte, body.end_byte))
READ/COND L450:  if (child.start_byte, child.end_byte) not in processed:
WRITE     L480:  processed: set = set()
READ      L482:  processed.add((cond.start_byte, cond.end_byte))
READ/COND L485:  if (child.start_byte, child.end_byte) not in processed:
```

Three separate `WRITE` sites. The `processed` set is being initialized *three times*, in three different inner functions. That means three separate sets — they don't share state.

Now look at the write at L419:

```bash
reveal reveal/adapters/ast/nav.py :419 --scope
```

```
DEF     L364→L488       DEF  _walk_var(
  DEF     L407→L425       DEF  _walk_assignment(n: Any, ntype: str, c: str) -> None

    ▶ L419: processed = {
```

The `processed` set at L419 is initialized inside `_walk_assignment`. Its scope is that one closure call. When `_walk_for` runs (L434), it creates *its own* `processed` set at L439. The sets never talk to each other.

The original code had used `id()` for node identity — and tree-sitter returns new Python wrapper objects on each node access, so `id()` comparisons never matched. The fix: key on `(start_byte, end_byte)` instead.

We found the structure of the bug — three separate `processed` sets with broken identity — without reading 124 lines of code. The outline showed where the closures were. The varflow showed the three write sites. The scope confirmed where each one lived.

---

## For AI agents

These flags matter more for agents than they do for humans.

When Claude Code encounters a 200-line function, the naive approach is to read all of it. That's ~7,500 tokens consumed before any reasoning happens. A large session might do this ten times — 75,000 tokens of raw file reading, most of it never referenced again.

The nav flags encode a different strategy:

```bash
# Step 1: structure (~80 tokens)
reveal src/handler.py process_event --outline

# Step 2: placement for the relevant line (~50 tokens)
reveal src/handler.py :285 --scope

# Step 3: the variable in question (~100 tokens)
reveal src/handler.py process_event --varflow payload

# Step 4: calls in the suspicious range (~60 tokens)
reveal src/handler.py process_event --calls 280-295

# Total: ~290 tokens
# vs. reading the function: ~7,500 tokens
```

That's not just a token saving — it's a different way of working. The agent isn't holding 200 lines in working memory and reasoning about all of it. It's asking targeted questions and getting targeted answers. The same way a senior developer would.

---

## Token math

| Operation | Approximate tokens |
|-----------|-------------------|
| `cat` a 200-line function | ~7,500 |
| `--outline` | ~80–200 |
| `--scope :LINE` | ~50–100 |
| `--varflow VAR` | ~60–200 |
| `--calls START-END` | ~50–150 |
| **All four nav flags** | **~250–650** |
| **Reduction** | **~7–25x** |

The savings compound. An agent investigating a bug across three functions might read 600 lines — 22,500 tokens — or run 12 nav commands — ~3,000 tokens. The investigation is faster, cheaper, and the results are more directly actionable.

---

## Getting started

```bash
pip install reveal-cli

# Skeleton of a function
reveal src/your_module.py your_function --outline

# Where is this line?
reveal src/your_module.py :LINE --scope

# Variable trace
reveal src/your_module.py your_function --varflow variable_name

# What does a range call?
reveal src/your_module.py your_function --calls START-END
```

`Class.method` syntax works everywhere:

```bash
reveal src/your_module.py MyClass.your_method --outline
```

Available since v0.72.0. Full reference: `reveal help://nav`.

---

You don't understand code by reading it — you understand it by interrogating it. These four commands are the questions.

---

*Part of the Reveal documentation series. See also:*
- *[Find Every Caller in Your Codebase With One Command](/articles/reveal-call-graphs) — cross-file call graph analysis*
- *[Two Commands That Change How You Work With Code](/articles/reveal-pack-and-review) — pack and review*
- *[Stop Reading Code. Start Understanding It.](/articles/reveal-introduction) — the big picture*
