---
title: "Inside the Function: Reveal's Fourth Level of Progressive Disclosure"
subtitle: "Seven new flags let you query a function's control flow, side effects, and variable movement — without opening the file"
author: "Scott Senkeresty"
date: "2026-04-19"
type: "article"
status: "published"
audience: "developers"
topics: ["reveal", "progressive-disclosure", "nav-flags", "function-navigation", "static-analysis", "ai-agents", "mcp", "php", "python"]
related_projects: ["reveal", "sil"]
related_docs:
  - "reveal-introduction.md"
  - "../systems/reveal.md"
canonical_url: "https://semanticinfrastructurelab.org/articles/reveal-inside-the-function"
reading_time: "10 minutes"
beth_topics: [reveal, progressive-disclosure, nav-flags, boundary, sideeffects, returns, ifmap, varflow, mcp, php, function-navigation]
session_provenance: "pazevaxe-0419"
version: "v0.81.0"
linkedin_posted: false
---

# Inside the Function: Reveal's Fourth Level of Progressive Disclosure

**Seven new flags let you query a function's control flow, side effects, and variable movement — without opening the file.**

---

Reveal's progressive disclosure model has three levels:

```
reveal src/          # Level 1: directory structure   ~100 tokens
reveal src/auth.py   # Level 2: file outline          ~250 tokens
reveal src/auth.py validate_token  # Level 3: function body  ~150 tokens
```

Three levels is enough for most functions. You learn what exists, what's in a file, then read the part you need.

But large functions break this model. Legacy controllers. AST walkers. Plugin hooks. Dispatch tables. Some functions are 150, 200, 400 lines — too large to hold in working memory, too entangled to read top to bottom. Level 3 shows the implementation. For large functions, that's still too much.

**v0.81.0 adds a fourth level: querying inside a function without reading it.**

---

## The Seven Flags, Grouped

Instead of reading a function, you ask structured questions about it. The flags fall into three categories:

**Control flow** — the skeleton of decisions and exits:
```bash
reveal file.py func --ifmap       # if/elif/else tree with line spans
reveal file.py func --catchmap    # try/except/finally structure
reveal file.py func --returns     # every return path with its gate condition
```

**Data flow** — how values move:
```bash
reveal file.py func --varflow VAR # how a specific variable moves through the body
reveal file.py func --mutations   # what gets written in a range
```

**External interaction** — what the function touches outside itself:
```bash
reveal file.py func --sideeffects # classified calls: db, http, cache, log, file, sleep, hard_stop
reveal file.py func --boundary    # external inputs (INPUTS / ENVIRONMENT / EFFECTS)
```

All seven work on Python and PHP. All support `--format json`. All are accessible through the `reveal_nav` MCP tool without subprocess overhead.

---

## "What does this function do to my process?"

`_dispatch_nav` in Reveal's own codebase is a 200-line routing function. It looks at which nav flag was requested and calls the appropriate analysis. Nothing alarming on the surface.

```bash
reveal file_handler.py _dispatch_nav --sideeffects
```

```
L159     hard_stop  sys.exit(1)
L184     hard_stop  sys.exit(1)
L204     hard_stop  sys.exit(1)
L250     hard_stop  sys.exit(1)
L316     hard_stop  collect_exits(func_node...)
L321     hard_stop  render_exits(exits...)
```

Six `sys.exit` calls. This "routing function" can terminate the process.

You would not find this by reading the header. You would not find it quickly by grepping — `sys.exit` appears in dozens of files. `--sideeffects` surfaces it in under a second, with line numbers.

The classifier recognizes seven categories: **db**, **http**, **cache**, **log**, **file**, **sleep**, **hard_stop**. The categories matter for refactoring and testing: a function with database writes cannot be safely tested without a real database. A function with `hard_stop` calls needs special handling in agent pipelines. One command answers the question before you read a line.

---

## "How many ways can this function exit?"

```bash
reveal file_handler.py _dispatch_nav --returns
```

```
RETURN    L193:  return
          gate: getattr(args, 'scope', False) (L176)

RETURN    L222:  return
          gate: getattr(args, 'around', None) is not None (L196)

RETURN    L268:  return
          gate: getattr(args, 'outline', False) (L258)

RETURN    L282:  return
          gate: getattr(args, 'varflow', None) (L271)

RETURN    L294:  return
          gate: getattr(args, 'calls', None) is not None (L285)

RETURN    L310:  return
          gate: getattr(args, 'ifmap', False) or getattr(args, 'catchmap', False) (L297)

RETURN    L322:  return
          gate: getattr(args, 'exits', False) or getattr(args, 'flowto', False) (L313)

RETURN    L337:  return
          gate: getattr(args, 'deps', False) (L325)

RETURN    L352:  return
          gate: getattr(args, 'mutations', False) (L340)

RETURN    L367:  return
          gate: getattr(args, 'sideeffects', False) (L355)
```

Ten return paths. Each gated on a different flag argument. Without reading the function, you now know it is a routing table — one branch per nav flag. The architecture is visible in the return map.

This is the output you hand an agent before asking it to add a new route. The pattern is explicit: one `if` check, one dispatch, one `return`. The agent can follow it precisely — no file reading required.

---

## "What's the decision tree?"

`--ifmap` strips the implementation and shows only the branching skeleton:

```bash
reveal file_handler.py _dispatch_nav --ifmap
```

```
IF  not isinstance(analyzer, TreeSitterAnalyzer) or not analyzer.tree  L153→L159
IF  getattr(args, 'scope', False)  L176→L193
  IF  syntax['type'] != 'line'  L178→L184
  IF  as_json  L187→L192
  ELSE  L189→L192
IF  getattr(args, 'around', None) is not None  L196→L222
  IF  syntax['type'] != 'line'  L198→L204
  IF  as_json  L211→L221
  ELSE  L218→L221
IF  func_node is None  L231→L253
  ...
IF  getattr(args, 'outline', False)  L258→L268
  IF  as_json  L264→L267
  ELSE  L266→L267
...
```

The top-level branches are the dispatch cases. The inner branches are `as_json` forks — every flag has a text path and a JSON path. Structure understood in seconds.

On `_walk_var` — a recursive AST walker with complexity 40 — `--ifmap` produces 14 branches, each handling a different tree-sitter node type. Reading the 112-line function to understand its design would take minutes. The skeleton takes seconds.

---

## "Is this function pure?"

`--boundary` answers the external-interaction question from the opposite direction: not what the function calls, but what it depends on from outside.

```bash
reveal nav_varflow.py _walk_var --boundary
```

```
INPUTS (undefined reads):
  node, var_name, from_line, to_line, get_text, events, ctx ...

EFFECTS:
  none in L35–L146
```

`EFFECTS: none` is the answer you want before parallelizing, mocking, or extracting. No database. No filesystem. No stdout. One command confirms the function is safe to test in isolation and safe to call concurrently.

In PHP, `--boundary` adds a third section — **ENVIRONMENT** — that surfaces superglobals separately from parameter inputs:

```
INPUTS:   $user_id, $action, $token
ENVIRONMENT:
  $_POST                          first read L12
  $_GET                           first read L18
  $_SESSION                       first write L24
EFFECTS:
  ...
```

A function that reads `$_POST` is an HTTP boundary. One that writes `$_SESSION` is session-coupled. These are architectural facts — the kind you want visible before a refactor, not discoverable only after reading the body.

---

## The same flags on PHP

All seven flags work on PHP. Here's `--returns` on a 187-line PHP probe:

```bash
reveal SideEffectsProbe.php run --returns
```

```
RETURN    L52:  return null;
          gate: $line < $this->from || $line > $this->to (L51)

RETURN    L61:  return null;
          gate: !($node instanceof Node\Expr\FuncCall) (L60)

RETURN    L103:  return null;
          gate: $funcName === 'header' (L94)

RETURN    L112:  return null;
          gate: in_array($funcName, ['curl_exec', 'curl_multi_exec'], true) (L107)

RETURN    L130:  return null;
          gate: in_array($funcName, ['memcache_get', ...]) (L116)

...14 total
```

Fourteen guard-clause returns, each eliminating a different function category. The function's design — a classification chain — is visible in the return map before reading a line of implementation.

And `--ifmap` confirms the same structure as a decision tree: 11 top-level branches, one per side-effect category, with line spans for each.

---

## Agents: codebases as queryable systems

All seven flags are available through `reveal_nav` in `reveal-mcp`:

```json
{
  "tool": "reveal_nav",
  "arguments": {
    "path": "src/auth.py",
    "element": "validate_token",
    "flag": "sideeffects"
  }
}
```

```json
{
  "tool": "reveal_nav",
  "arguments": {
    "path": "src/auth.py",
    "element": "validate_token",
    "flag": "varflow",
    "flag_value": "token"
  }
}
```

This turns a codebase into a **queryable system** for agents — not just text to read. An agent can ask structured questions about any function's behavior without file access, without token waste, without reading code that isn't relevant.

Each level of the hierarchy now has a corresponding tool: `reveal_structure` for directory and file outline, `reveal_element` for function extraction, `reveal_nav` for function internals. The agent always has a disciplined option. It never has to dump a file to answer a structural question.

---

## Honest limitations

These flags are structural analysis, not runtime behavior:

- `--sideeffects` finds calls by name pattern. A side effect inside an `if False:` branch will appear. One hidden behind a lambda or dynamic dispatch won't.
- `--varflow` tracks by variable name. Two variables with the same name in different scopes may overlap. Best for uniquely-named parameters.
- `--boundary` identifies "undefined reads" — variables used before being assigned in the visible scope. In PHP, `$this` and other implicit references appear as inputs by design.
- PHP `foreach` loop variables show as READ instead of WRITE — a known limitation.

The right model: structural maps for orientation and scoping, runtime tooling for verification.

---

## The fourth level

```bash
reveal file.py func --ifmap       # What's the decision tree?
reveal file.py func --returns     # How many exits, under what conditions?
reveal file.py func --sideeffects # What does this touch outside itself?
reveal file.py func --varflow x   # How does variable x move through the body?
reveal file.py func --boundary    # What enters from outside — and what does it change?
```

Same syntax on PHP. Same output format. Same JSON envelope for agents.

Levels 1–3 orient you: what exists, what's in a file, what a function contains. Level 4 investigates the structure of a specific function — its branches, its effects, its dependencies, its exit paths — without reading the implementation.

Stop reading functions. Start querying them.

---

**Install:**

```bash
pip install --upgrade reveal-cli    # CLI
pip install --upgrade reveal-mcp    # MCP server for Claude Code / Cursor / Windsurf
```

**GitHub:** [Semantic-Infrastructure-Lab/reveal](https://github.com/Semantic-Infrastructure-Lab/reveal)
**PyPI:** [reveal-cli](https://pypi.org/project/reveal-cli/)

---

*Reveal v0.81.0 — 7,913 tests, 23 URI adapters, 69 quality rules, 190+ languages. MIT license.*
