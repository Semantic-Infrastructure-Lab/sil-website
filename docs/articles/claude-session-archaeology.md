---
title: "Session Archaeology: Excavating Your Claude Code History with reveal claude://"
subtitle: "A git blame for your thinking process, not just your code"
author: "Scott Senkeresty"
date: "2026-03-31"
type: "article"
status: "published"
audience: "developers"
topics: ["reveal", "claude-code", "session-analysis", "token-efficiency", "cost-attribution", "workflow-analysis", "ai-observability"]
related_docs:
  - "reveal-introduction.md"
  - "reveal-call-graphs.md"
  - "reveal-pack-and-review.md"
canonical_url: "https://semanticinfrastructurelab.org/articles/claude-session-archaeology"
reading_time: "10 minutes"
beth_topics:
  - reveal
  - claude
  - sessions
  - tokens
  - cost
  - audit
  - workflow
  - archaeology
  - observability
  - history
---

# Session Archaeology: Excavating Your Claude Code History with `reveal claude://`

---

Something in production is behaving wrong. You know Claude touched `auth.py` — you watched it happen. But you can't remember exactly what it changed, whether it also modified `middleware.py`, or whether there was a failing test it powered past and you glossed over. The session ended, you moved on, and now the record is a closed tab.

That session is still there — all of it. Every file it touched, every command it ran, every token it spent, every failure it hit and recovered from. It's sitting in `~/.claude/projects/`, unread.

`git blame` tells you who changed a line and when. There's no equivalent for your AI collaboration history — nothing that tells you which session introduced a decision, what Claude was trying when it hit a wall, or which file it came back to across fifteen conversations.

`reveal claude://` is that tool: a git blame for your *thinking process*, not just your code.

I ran it on my own history. The first thing it surfaced: three sessions across two weeks where I'd investigated the same bug — each time from a slightly different angle, each time producing a partial fix. The pattern was invisible in `git log`. It was obvious in session history.

When a session costs real money and takes two hours, the record matters. When you've run hundreds of sessions across a complex codebase, the pattern in that history is operational data you're not reading. Here's how to read it.

```bash
pip install reveal-cli
```

---

## Getting oriented

Before you can query a session, you need to find it.

```bash
reveal 'claude://sessions/'
```

```
Claude Sessions: 847 total | showing 20 | --all to show all | --head N for more | --since YYYY-MM-DD (or today)

  SESSION                              MODIFIED            SIZE  R  PROJECT       TITLE
  ------------------------------------ ----------------- ------  -  ------------  -------------------------
  4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b 2026-03-15 16:44   892kb  ✓  auth-service  mobile auth timeout
  7a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d 2026-03-14 11:22   445kb  ✓  auth-service  slow query on users table
  9c1d2e3f-4a5b-6c7d-8e9f-0a1b2c3d4e5f 2026-03-12 10:15  1247kb  ✓  auth-service  auth refactor
  c3d4e5f6-a7b8-9c0d-1e2f-3a4b5c6d7e8f 2026-03-11 14:39   234kb  ✗  auth-service  flaky integration test
  e5f6a7b8-c9d0-1e2f-3a4b-5c6d7e8f9a0b 2026-03-09 09:55   678kb  ✓  api           rate limit middleware
  b5c6d7e8-f9a0-1b2c-3d4e-5f6a7b8c9d0e 2026-03-08 09:44   312kb  ✗  auth-service  login failures prod
```

The `R` column tells you whether the session has a saved summary (`✓`) or ended abruptly without one (`✗`). The `PROJECT` column shows which repo the session ran in — useful when you work across multiple codebases. Size is a proxy for depth: a 1.2MB session had a lot happening; a 234KB session was probably quick. Filter by date with `--since=2026-03-01` or show everything with `--all`.

You find the session you want by its `TITLE` — Claude Code sets this from your first message. The `SESSION` UUID is what you pass to subsequent commands.

Once you've found a session, get its fingerprint:

```bash
reveal 'claude://session/4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b'
```

```
Claude Session: 4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b
Title: mobile auth timeout
Messages: 156
User: 58 | Assistant: 89
Duration: 42m 17s
README: ✓ present

Files: 4 (src/auth.py, src/middleware.py, src/session.py, tests/test_auth.py)

Tools Used:
  Bash: 63
  Edit: 6
  Read: 8
  Write: 1

Tokens: 82 in / 18,441 out  |  cache hit 96%  (2,841,920 read)

Context: src/auth-service | branch=main | v2.1.45
Last: Fixed the token propagation in middleware.py — the JWT refresh wasn't forwarding
the new expiry timestamp to the response header. Test suite passing.
```

Forty-two minutes. 63 bash commands. 6 edits across 4 files. 96% cache hit rate. `Context` shows the working directory and branch — which version of the codebase this ran against. `Last` is the final assistant message, truncated: where the session ended, in one line. That's a complete picture of the session's character before you've read a word of the conversation.

---

## Scenario 1: "What was the last thing Claude said?"

```bash
reveal 'claude://session/4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b?last'
```

```
Messages: 4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b (1 assistant turn)

[turn 18 / msg 151] 2026-03-15 16:43
Fixed the token propagation in middleware.py — the JWT refresh wasn't forwarding
the new expiry timestamp to the response header. Test suite passing.

Still open: the mobile client caches the old token for up to 15 minutes even
after refresh. That's a client-side issue, not server-side. Filed as #892.
```

The last assistant turn. ~50 tokens. Where were we, what's resolved, what's still open — in one command instead of re-reading 156 messages.

**The drill-down rule:** `?last` → `?summary` → full session read. Start at 50 tokens, go deeper only if needed.

---

## Scenario 2: "Was this session any good?"

Not every session is equally productive. Tool success rates tell you the story before you read anything.

```bash
reveal 'claude://session/4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b?summary'
```

```
Analytics: 4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b
Title: mobile auth timeout
Duration: 42m 17s
Messages: 156 (user: 58, assistant: 89)

Tool Success Rates:
  Bash: 92.1% (58/63, 5 failed)
  Edit: 100.0% (6/6)
  Read: 100.0% (8/8)
  Write: 100.0% (1/1)

Message Sizes: avg 1,240 chars, max 8,943 chars
Thinking: 8 blocks (~2,100 tokens)
```

Now compare a session that struggled:

```bash
reveal 'claude://session/b5c6d7e8-f9a0-1b2c-3d4e-5f6a7b8c9d0e?summary'
```

```
Analytics: b5c6d7e8-f9a0-1b2c-3d4e-5f6a7b8c9d0e
Title: login failures prod
Duration: 1h 44m 12s
Messages: 437 (user: 164, assistant: 238)

Tool Success Rates:
  Bash: 83.5% (96/115, 19 failed)
  Edit: 75.0% (3/4, 1 failed)
  Read: 100.0% (9/9)
  Write: 100.0% (1/1)

Message Sizes: avg 2,180 chars, max 14,220 chars
Thinking: 31 blocks (~18,400 tokens)
```

First session: 42 minutes, 92% Bash success — execution with a handful of recoverable failures. Second: 1h44m, 83.5% Bash success and 19 failures — significant thrash. The `?summary` tells you which in 3 seconds.

**What the numbers mean:**
- Bash > 95% → clean execution; Claude knew what it was doing
- Bash < 85% → significant thrash; pull `/workflow` to find where it got stuck
- High message count + few edits → exploration or review, not implementation
- Edit failures → often a "read before write" ordering problem; the error message will confirm it
- High thinking block count with large token estimates → Claude was reasoning extensively, not just executing; the struggling session's 31 blocks at 18K tokens is where a significant portion of its cost went

---

## Scenario 3: "Where is my money going?"

The `?tokens` route gives you a turn-by-turn cost breakdown — not just totals, but the per-turn data you need to understand *why* a session was expensive.

```bash
reveal 'claude://session/4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b?tokens'
```

```
Token Breakdown: 4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b
Turns: 47

   #  timestamp                  input    output    cache_read   cache_crt    cumul_in
────  ──────────────────────  ────────  ────────  ────────────  ──────────  ──────────
   1  2026-03-15 14:01:22            3       148        11,270      20,443      31,716
   2  2026-03-15 14:02:05            1        92        31,713         519      64,244
   3  2026-03-15 14:02:31            1       203        32,232       4,891     101,326
   ...
  22  2026-03-15 15:18:40            1     2,841        68,992       1,204   3,241,880
   ...

Totals: 82 in / 18,441 out
Cache:  2,841,920 read / 71,660 created  (hit rate 96%)
```

Turn 22: output spikes to 2,841 tokens — something made Claude write a lot. Cross-reference with `/workflow` to see which step that was.

But output volume is only one dimension of cost. The cache columns tell a more structural story about what the session actually costs per token.

**What the cache numbers mean:**
- **Cache reads cost 0.1× vs. uncached input** — but cache_creation tokens cost 1.25×, so real per-session savings are 5–9×, not 10×
- **Real Claude Code sessions run at 93–99% hit rate** — if yours is lower, context compaction mid-session reset your cache
- **`cache_crt` spike early** → something large loaded that session hadn't seen before — a long file, a big doc — replays cheaply at cache price every subsequent turn
- **Hit rate drops mid-session** → context compaction (Claude's automatic context reset when the window fills) invalidated the cache; costs rise until it rebuilds

---

## Scenario 4: "What was Claude actually doing for that hour?"

The `/workflow` route is a step-by-step view of every tool call in order, with success and failure markers.

```bash
reveal 'claude://session/4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b/workflow'
```

```
Workflow: 4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b
Total Steps: 72

[  1] Bash    Run test suite
[  2] Bash    Check recent auth-related commits
[  3] Read    src/auth.py
[  4] Read    src/middleware.py
[  5] Bash    Reproduce the timeout locally ✗
[  6] Bash    Check JWT library version
[  7] Bash    Test with extended expiry window
[  8] Read    src/session.py
[  9] Bash    Trace token refresh call chain ✗
[ 10] Bash    Add debug logging to middleware
[ 11] Edit    src/middleware.py
[ 12] Bash    Run targeted auth tests
[ 13] Bash    Check response headers in test output
...
[ 71] Write   session-notes.md
[ 72] Bash    Commit changes
```

The `✗` on steps 5 and 9 show where it hit walls. Steps 6–10 are the recovery arc: check the library version, try a different repro approach, add logging, then try again. You can read a session like a story: orientation → failure → diagnosis → fix → verification.

**To count failures directly:**

```bash
reveal 'claude://session/4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b/workflow' | grep "✗"
```

5 failures in 72 steps is 93% clean — normal for investigative work. 19 failures in 115 steps is a session that was struggling.

**Two patterns worth watching for:**

A failure followed by the exact same command = a loop. Claude ran it, it failed, and it ran it again without new information. That's a sign the session got stuck.

A failure followed by a `Read` or schema check = intelligent diagnosis. It failed, it gathered new information, it tried a different approach. That's normal.

**The last step tells you how the session ended.** A session that ends on a `Write` to a notes file or a `Bash` commit completed cleanly. A session that ends on a failed Bash command had something go wrong at the very end.

When you spot failures in the workflow and want the full error output, pull them directly:

```bash
reveal 'claude://session/4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b?errors'
```

```
Errors: 4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b
Total: 5

[  1] Message 14 | Bash | exit_code
      Input: docker run --rm auth-test pytest tests/test_auth.py -x
      Error: ModuleNotFoundError: No module named 'jwt'

[  2] Message 23 | Bash | exit_code
      Input: python -c "from src.auth import decode_token; decode_token('test')"
      Error: jwt.exceptions.InvalidSignatureError: Signature verification failed
```

The `?errors` route shows every failed tool call with its full input and error output — no scrolling through the workflow looking for `✗` markers.

---

## Scenario 5: "Which files keep coming up?"

The `/files` route shows every file the session touched, with operation counts.

```bash
reveal 'claude://session/4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b/files'
```

```
Files Touched: 4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b
Total Operations: 23
Unique Files: 4

Read:
   3x src/auth.py
   2x src/middleware.py
   2x src/session.py
   1x src/config.py

Edit:
   3x src/middleware.py
   2x src/auth.py
   1x src/session.py

Write:
   1x session-notes.md
```

`middleware.py` was read twice and edited three times in one session. Edited once, probably wasn't right. Edited again, still something off. Edited a third time, done. Files edited more than twice in a single session are often the location of a subtle bug — not wrong in an obvious way, but wrong in a way that takes multiple attempts to nail down.

**The question this raises:** What happens when you look at file patterns *across* sessions? A file that Claude reads in twenty sessions but rarely edits is probably a load-bearing reference document. A file edited in session after session has either too much responsibility or a recurring correctness problem. Per-session `/files` tells you what happened; the cross-session pattern — assembled by running this against multiple sessions — tells you *why*.

---

## Scenario 6: "Find every session where we dealt with this bug"

A bug that took two weeks to fix has a full conversation trail across multiple sessions. Here's how to reconstruct it.

```bash
reveal 'claude://sessions/?search=token+expiry&since=2026-01-01'
```

```
Cross-session search: "token expiry"  since 2026-01-01
Scanned 847 sessions  |  Found 8 matches

4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b  2026-03-15 14:01  user
  ...mobile clients are getting logged out even after token refresh — track down the expiry...

9c1d2e3f-4a5b-6c7d-8e9f-0a1b2c3d4e5f  2026-03-12 10:33  assistant
  ...moved the token expiry logic into middleware.py so it's applied consistently...

b5c6d7e8-f9a0-1b2c-3d4e-5f6a7b8c9d0e  2026-03-08 09:44  user
  ...users getting logged out every 15 minutes — check if this is related to token expiry...

e5f6a7b8-c9d0-1e2f-3a4b-5c6d7e8f9a0b  2026-02-13 15:22  assistant
  ...note: the token expiry window is hardcoded at 900s — should probably be configurable...
```

Four sessions, spanning five weeks. The February session flagged the hardcoded expiry as something worth fixing — and nothing happened until users started hitting the problem in March. You can now see the full arc: early warning, ignored, problem manifests, three sessions investigating it, fix landed.

That's five weeks of reasoning, visible in one command. Combined with `/workflow`: find the session where the fix landed, pull its workflow to see exactly which files changed, cross-reference with `git log`. You get the complete chain: conversation → reasoning → code change → commit.

---

## Scenario 7: "What patterns am I creating?"

All of Scenarios 1–6 look at what Claude did. This one looks at what you asked for.

```bash
reveal 'claude://history'
```

```
Recent Prompts: last 50 across all projects

  2026-03-15 16:01  4f8a9c1e-2b3d-4e5f-a6b7-c90d1e2f3a4b  mobile clients are getting logged out even after token refresh — track down the expiry
  2026-03-12 10:33  9c1d2e3f-4a5b-6c7d-8e9f-0a1b2c3d4e5f  ok let's move the token expiry logic into middleware so it's applied consistently
  2026-03-08 09:44  b5c6d7e8-f9a0-1b2c-3d4e-5f6a7b8c9d0e  users getting logged out every 15 minutes — check if this is related to token expiry
  2026-02-13 15:22  e5f6a7b8-c9d0-1e2f-3a4b-5c6d7e8f9a0b  the rate limiting is in, but note the token expiry window is still hardcoded at 900s
```

Three prompts about token expiry across five weeks. Each one opened a new session. The February one flagged a hardcoded value worth fixing — and nothing happened until users hit the problem in March.

```bash
reveal 'claude://history?search=token+expiry'
```

That query surfaces this pattern in one command. Three variations of the same investigation across three sessions isn't three bugs — it's one incomplete fix being revisited. The prompt history shows it before `git log` does, before the bug tracker does, before anyone files a ticket.

The same prompt appearing with slight variations — "check why X is failing", "X is still broken" — is a sign that fixes are landing in the wrong place. The session history tells you what Claude did. The prompt history tells you what you kept needing to ask.

---

## The picture this gives you

Each route is useful on its own. Together, they're session observability — the same idea as application observability, applied to your AI workflow. Patterns that were invisible become obvious once you can query for them.

What becomes visible:

**Cost attribution.** Not just "I spent $X this month" but which sessions, which workflows, which habits drove it. Well-cached sessions run 5–9× cheaper than uncached work. A `cache_crt` spike or mid-session compaction is where the money goes.

**Agent characterization.** A session with 60 Bash calls and 90% success is different from one with 60 Bash calls and 75% success. The `?summary` surfaces this in seconds; the `/workflow` shows you where it broke down.

**File hotspots.** Which files Claude returns to across sessions — reading them, editing them, editing them again. Files that get edited in fifteen sessions are telling you something about the design.

**Decision archaeology.** Architecture decisions get made in conversation. They don't always land in docs. "When did we decide to use Redis instead of Postgres for sessions?" is a question `claude://sessions/?search=redis+sessions` can answer.

**Your own patterns.** Prompt history as data. The same investigation repeated across sessions is a signal — not about Claude, about the underlying system's reliability.

| Question | Route |
|----------|-------|
| Where did we leave off? | `?last` — last assistant turn only |
| Was this session productive? | `?summary` — tool success rates + thinking blocks |
| What did it cost? | `?tokens` — turn-by-turn with cache breakdown |
| What happened, step by step? | `/workflow` — every tool call with `✗` markers |
| What went wrong exactly? | `?errors` — failed tools with full input + error output |
| Which files did it touch? | `/files` — with operation counts |
| What commands did it run? | `?tools=Bash` — every command with descriptions |
| Search within a session | `?search=TERM` — scans text, tool inputs, thinking |
| Find a past conversation | `claude://sessions/?search=TERM&since=DATE` |
| Spot recurring prompt patterns | `claude://history` / `claude://history?search=TERM` |

None of this requires parsing JSONL files or writing custom scripts. Every route produces human-readable output by default and structured JSON via `--format json` for automation.

---

## Quick reference

```bash
# List sessions
reveal 'claude://sessions/'
reveal 'claude://sessions/?since=2026-03-01'
reveal 'claude://sessions/' --all

# Session overview (messages, tools, duration, branch, last message)
reveal 'claude://session/NAME'

# Last assistant message only — fastest recovery (~50 tokens)
reveal 'claude://session/NAME?last'

# Last N assistant turns
reveal 'claude://session/NAME?tail=3'

# Tool success rates, thinking blocks, message sizes
reveal 'claude://session/NAME?summary'

# Turn-by-turn token cost with cache attribution
reveal 'claude://session/NAME?tokens'

# Step-by-step workflow with success/failure markers
reveal 'claude://session/NAME/workflow'

# Failed tools with full input + error output
reveal 'claude://session/NAME?errors'

# Files touched, with operation counts
reveal 'claude://session/NAME/files'

# Every Bash command the agent ran (also: Edit, Read, Write)
reveal 'claude://session/NAME?tools=Bash'

# Search within a session (text, tool inputs, thinking)
reveal 'claude://session/NAME?search=TERM'

# Cross-session content search
reveal 'claude://sessions/?search=TERM&since=YYYY-MM-DD'

# Your full prompt history
reveal 'claude://history'
reveal 'claude://history?search=TERM'

# Audit your Claude install: MCP servers, agents, hooks, memory
reveal 'claude://config'
reveal 'claude://agents'
reveal 'claude://hooks'
reveal 'claude://memory'

# Claude Code installation paths
reveal 'claude://info'
```

For sessions stored outside the default `~/.claude/projects/` location:
```bash
reveal 'claude://sessions/' --base-path /path/to/sessions
```

---

## Try it

```bash
pip install reveal-cli

# See your sessions
reveal 'claude://sessions/'

# Pick any recent one and get the fingerprint
reveal 'claude://session/NAME'

# Where did it leave off?
reveal 'claude://session/NAME?last'

# Was it any good?
reveal 'claude://session/NAME?summary'

# What did it cost?
reveal 'claude://session/NAME?tokens'

# What went wrong?
reveal 'claude://session/NAME?errors'

# What do you keep asking about?
reveal 'claude://history'
```

The data has always been there. `reveal` makes it legible.

---

*Reveal v0.70.0 — 7,209 tests, 23 URI adapters, 69 quality rules, 190+ languages. MIT license.*

*Part of the Reveal documentation series. See also:*
- *[Stop Reading Code. Start Understanding It](/articles/reveal-introduction) — the big picture*
- *[Find Every Caller in Your Codebase](/articles/reveal-call-graphs) — call graph analysis*
- *[Two Commands That Change How You Work With Code](/articles/reveal-pack-and-review) — pack and review*
