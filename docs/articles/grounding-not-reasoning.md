---
title: "The Hard Part of Agentic AI Isn't Reasoning — It's Grounding"
subtitle: "Four cheap habits that make an agent dramatically stronger for fewer tokens — and the open-source tool that gets you most of the way there"
author: "Scott Senkeresty"
date: "2026-07-13"
type: "article"
status: "published"
audience: "developers, AI engineers, agent builders"
reading_time: "12 minutes"
canonical_url: "https://semanticinfrastructurelab.org/articles/grounding-not-reasoning"
topics: [agentic-ai, grounding, progressive-disclosure, token-efficiency, context-management, orientation]
beth_topics:
  - agentic-ai
  - grounding
  - progressive-disclosure
  - token-efficiency
  - reveal
  - orientation
  - sil
related_projects: [reveal, SIL]
related_docs:
  - docs/articles/progressive-disclosure-agents.md
  - docs/articles/information-retrieval-history-and-agentic-future.md
  - docs/articles/claude-session-archaeology.md
  - docs/articles/reveal-subagents.md
session_provenance: "iridescent-gradient-0713"
linkedin_posted: true
---

# The Hard Part of Agentic AI Isn't Reasoning — It's Grounding

*Four cheap habits that make an agent dramatically stronger for fewer tokens — and the one open-source tool that gets you most of the way there.*

Most discussion of agentic AI focuses on the model: bigger context windows, better tool use, smarter planning. But after months of running an AI agent as a daily working partner across a dozen real software projects, the bottleneck hasn't been intelligence. It's been *grounding* — getting the right information into the agent's head, cheaply, before it does anything.

Every agent session starts from zero. It doesn't remember yesterday. It doesn't know which of fifty files in a repo matter for today's task. It doesn't know that the last three attempts at this bug already failed, or which approach got ruled out and why. Left unaddressed, an agent burns a huge fraction of its context window — and your money — re-deriving facts a human teammate would carry in their head for free. Get grounding wrong and the agent is expensive, slow, and confidently wrong. Get it right and the *same model* becomes dramatically more capable, because almost all its budget goes to the actual work instead of archaeology.

Four patterns have done most of the heavy lifting. None are exotic — they're closer to good information architecture than to prompt engineering:

| Pillar | The cheap move | The trap it saves you from |
|---|---|---|
| **1. Continuity** | Write a handoff when a session ends; read it when the next one starts | Re-deriving yesterday's context from scratch |
| **2. Finding docs** | Search metadata for *candidates*; open only the best one or two | Grepping every doc — or ignoring them all |
| **3. Structure first** | Read the shape; extract only the slice you actually need | Dumping whole files into the context window |
| **4. Externalized tasks** | Keep the to-do list in the repo, surfaced at orientation time | Losing open work the moment the window closes |

What follows is each one, the design principle that makes it transferable, and a concrete example of it paying off. At the end I'll pull out the cross-cutting rules that matter most, and name honestly what this approach *doesn't* solve.

But first, the move that sits above all four: **an orientation doc is not a manual.** The single highest-leverage artifact in the whole system is the guide the agent reads on startup — and its most important discipline is what it *leaves out*. Ours states the rule in its own config: *"Signal over noise — show what matters, make the rest on-demand. Command reference removed: the guide is the authoritative reference; duplicating it at boot burns tokens every session."* Teach the agent *how to find things*, then get out of the way. Everything below is a variation on that one idea.

## 1. Continuity across sessions, not just within one

> *Leave your next self the note you'd have killed for this morning.*

A single conversation is not the unit of work — a project is. Sessions end, context windows fill, days pass. The fix isn't a bigger window; it's a deliberate handoff artifact written at the *end* of every session and read at the *start* of the next: what got done, what decisions were made and why, what's still open, and where to look next.

The economics are what make this work — writing the handoff is *asymmetrically cheap*. It costs a few hundred tokens at the end of a session that already has full context loaded and hot. Reading it costs a few hundred at the start of the next. The alternative — re-reading recent commits, re-running the failing test, rediscovering the constraint that ruled out the obvious approach — costs tens of thousands of tokens and still misses things a human would remember instantly.

Two design decisions made ours reliable. First: **the agent that did the work writes the handoff — this is never delegated to a summarizer.** Only the agent with the full session in context knows which of the day's twenty turns actually mattered. The save tool is explicit about this: "no auto mode." Second: **the maintenance cost of keeping the search index fresh is bounded by change, not by size.** Each save re-indexes only what changed since the last save — tracked by a watermark, not a time window or a full rescan — so keeping a year-old project searchable costs the same as a week-old one. That "bound cost by delta-since-last-checkpoint, not by total corpus" idea is worth stealing on its own.

A real example of the payoff: a session investigating a subtle correctness bug ended with a handoff naming the exact commit range the bug was live in, plus one open item — "confirm the bug window didn't contaminate results produced on two other machines during that window." The next session opened, read the handoff, and went *straight* to comparing file timestamps on both machines against that named range. No re-reading the original bug report, no re-deriving the fix. Twenty minutes of targeted verification closed an incident that a cold start would have re-investigated from scratch.

The trap to design around is fragility: if there's only one path to "what happened last time," a single bad handoff derails the next session. Redundant recovery paths — a structured summary, a searchable history, the ability to pull the raw prior conversation — matter less for daily use and more as insurance for the day the primary path fails.

## 2. Finding the right document without reading all of them

> *Search to find, not to read.*

Any project with history accumulates dozens or hundreds of documents — design notes, changelogs, postmortems, half-finished plans. An agent that greps all of them to answer one question burns tokens on noise; an agent that ignores them re-derives context someone already wrote down.

The pattern that works is a search layer built for *finding*, not reading — closer to an inverted index than a semantic search engine. Given two or three specific terms, it returns a short ranked list of *candidate documents*, not their contents. The agent then decides which to actually open, the way a person scans search results before clicking.

The ranking is where the interesting design lives, and it's worth being concrete because the mechanism transfers. Our index scores a document like this — a real result:

```
7.0 = base 2.9 × 1.40 (quality) × 1.72 (links: 5 inbound)
```

Two things fall out of that formula. **Link count is a direct authority multiplier** — a well-connected canonical doc outranks an isolated duplicate or a stale draft, the same way link structure ranks the web. And **ephemeral records are deliberately down-weighted**: session logs get a ×0.5 penalty against canonical docs even when they match the query better on raw text, because they're history, not truth. The system also *degrades gracefully* — a weak query doesn't return nothing; it returns its best guesses plus a suggestion of vocabulary that actually co-occurs in the corpus, so the agent can immediately re-query with better terms instead of concluding "no docs exist."

The catch: this only works if documents are *written to be found* — consistent front matter, a few well-chosen topic tags, and links to related docs. Findability is an authoring discipline, not a search-algorithm problem: miss the metadata and a brilliant document is invisible.

You don't need to build the ranked index to get most of this, though. If your docs already carry front matter, an open-source tool called **reveal** (more on it below) queries it directly off disk — `reveal 'markdown://docs/?type=runbook'` returns every doc in that tree whose front matter says `type: runbook`, no index to build and nothing to keep fresh. It's an exact-match filter rather than a ranked fuzzy search, and it's scoped to a directory rather than your whole world — but it's the zero-infrastructure version of this pillar, and for a single project it's often all you need.

And finding the document is only half the job — the document can be *wrong*. During one migration, the agent cross-checked a backlog entry marked "open, not yet deployed" against the actual commit history and found the fix had shipped a week earlier under a different note. The doc wasn't useless — it pointed at the right area — but treating it as truth rather than a claim to verify would have produced a wasted re-fix. The durable rule: **docs are a fast way to find where to look, never a substitute for checking what's actually true.**

## 3. Reading structure before content

> *Look at the shape before you pay for the substance.*

Even after finding the right file, reading it in full is usually the wrong move. A thousand-line file might have one function that matters; a design doc, one relevant section. The efficient pattern is progressive disclosure: look at the *shape* first — headings, function signatures, a directory tree — before pulling in the full content of any one piece.

This is the highest-leverage habit an agent can have, because the savings compound on every file, every session, for the life of the project. This is also the pillar with the most mature open-source implementation — **reveal** (`pip install reveal-cli`), whose entire design is progressive disclosure enforced by default. `reveal file.py` returns the function-and-class outline, not the file; `reveal file.py load_config` extracts just that one function; a directory gives a tree, a markdown doc gives its headings. You reach for the full contents only when the cheap structural view tells you that you have to. The tiers are explicit, with published token costs:

```
Overview      ~300–500 tokens   (structure, counts, entry points)
   ↓
Specific      ~500–1000          (one function, one section, one aspect)
   ↓
Filtered      ~400–800           (only the errors / only the matches)
   ↓
Full content  ~1500–7500+        (the whole thing — last resort)
```

The rule is "start shallow, drill down only when needed," and the gap between tiers is enormous. In our toolset, the *complete* reference for a single command runs ~40,000 tokens — but a distilled "which of my options fits this task?" version of the same material costs ~300. That's a hundredfold difference for the common case, with the expensive version reserved for the rare moment nothing cheaper answers the question. Multiply that across every file and doc a session touches, and it's the difference between running out of context on a small problem and having budget left for the real work.

A subtle but important refinement: **the outline is not the content.** A heading titled "Root Cause" is not the root cause; a function's name is not its behavior. Structure tells you *where* to look, and you extract the specific slice you need — but you don't get to skip reading it and pretend the label was the answer.

The principle generalizes past code, and reveal's adapters follow it everywhere: outline before you read, for documents; git history as structured query, not raw log; diff before whole file, for changes. It even applies to reviewing the agent's *own* history — `reveal 'claude://session/<id>/exchanges'` collapses a 66-turn conversation down to just the real human-prompt-to-final-answer pairs, skipping all the intermediate tool calls, truncated by default with an explicit "expand this one" pointer. Anywhere content can be large, ask: *what's the cheapest view that tells me whether I need the expensive one?*

## 4. Externalizing "what's left to do"

> *Keep the to-do list in the repo, not in the chat.*

An agent's context window is a terrible place to keep a task list — it vanishes when the session ends and competes for space while it's alive. Work that isn't captured somewhere durable gets forgotten or re-discovered at full cost.

Building this well turned out to require more care than expected, and the design process is itself the lesson. Rather than invent a format, we surveyed four projects that had each hand-rolled a task list in a markdown file — and found *the same three weaknesses independently in every one*:

1. **No real ID counter.** "Next ID" was always inferred by scanning the file for the highest number — fine solo, but a race the moment two sessions file tickets at once, silently producing duplicate IDs.
2. **No structured status field.** Status lived in prose (`DONE`, `✅`, `[x]`, emoji) with no consistent enum, making "what's actually open" a text-scanning problem instead of a filter — and producing entries with five stacked revisions because there was no field to just overwrite.
3. **Narrative depth didn't fit a rigid schema.** Real entries carry evidentiary weight — statistics, cross-references, doc pointers — that a table-only format would flatten.

We also trialed an off-the-shelf tool and read its source directly: its headline "multi-agent coordination" was broken as shipped (dependencies silently unenforced, a graph-traversal bug that dropped tasks). The conclusion: the *shape* — human-readable markdown with structured fields per task — was right, validated by four independent projects converging on it by hand. The *mechanics* (a real counter, a status enum, validated links) were the part worth building deliberately, because every existing implementation got them wrong in a different way.

That produced three transferable design commitments:

- **The durable artifact outlives the tool.** The task list is plain, hand-editable markdown-plus-YAML committed in the project's own repo. It works with *zero* of our tooling installed — the CLI is a convenience layer over the format, never the only way to mutate it. If the tool vanishes, the data is still perfectly usable.
- **Self-hosted IDs survive external-tool churn.** A project we work with had migrated its tracker and watched every historical link die *and the ticket numbers themselves get renumbered*. The fix that stuck: a prefix+sequential ID the project owns (`PROJ-142`), referenced everywhere, that no external tool controls.
- **Record facts explicitly; don't derive them from conventions that can drift.** Which commit resolved a task is stored as a validated reference, not scraped from commit-message patterns that silently break.

The payoff showed up immediately on adoption: the very migration onto this format surfaced two items sitting marked "not done" for over a week after they'd actually shipped — dead weight that would eventually have sent a future session to redo finished work — and caught two tickets colliding on the same ID, flagged only because the tool validates IDs at write time instead of trusting whoever typed the entry.

The failure mode to design against isn't building the tracker — it's building it and not *connecting* it. A task list nobody sees at session start, that isn't searchable alongside the docs, that the agent has to remember to check, is a task list in name only. The value comes from it being surfaced automatically at the same moment the agent orients on everything else.

## What actually transfers

Step back from the four pillars and the same handful of principles keep reappearing. These, more than any specific tool, are what I'd hand another team building for their own agent:

- **Make orientation cheap enough that skipping it is never worth it.** Every pattern here is designed so the grounded path costs *less* than the ungrounded one. A boot sequence with a hard sub-five-second budget; a search that returns candidates not contents; help that starts at 300 tokens. If doing it right is also the fast path, the agent does it right by default.
- **Bound cost by change, not by size.** Freshness that re-indexes only what moved; a handoff written from already-hot context. The expensive version of everything exists, but stays a last resort behind an explicit escape hatch.
- **The durable artifact must outlive the tool that writes it.** Plain text, in the repo, human-readable, no proprietary format. Tools come and go; the ground truth shouldn't.
- **Findability is an authoring discipline.** Metadata, links, and structure are what make later retrieval cheap. Unenforced, they rot — and a document nobody can find might as well not exist.
- **Treat every retrieved fact as a claim to verify, not truth.** Docs point you at where to look; commits, tests, and timestamps tell you what's actually true. The cheapest grounding still has to touch reality.

## The honest limit

All four pillars are "context-in" optimizations: they get the right information loaded as cheaply as possible *before* the agent acts. That's not an accident — it's the genuinely expensive part of agentic work, and a well-grounded, moderately clever agent consistently beats a brilliant one re-deriving basics every session, the same way a well-briefed junior beats a genius handed zero context.

But it's worth naming what these patterns *don't* cover. None of them govern whether the work done *after* grounding is correct, or whether the system gets smarter from one session to the next. Cheap orientation gets an agent to the starting line fast; it doesn't guarantee a good race. The next layer worth building — once orientation is solid — is closing that loop: verifying outcomes instead of assuming a plausible-looking diff is a correct one, and capturing durable lessons somewhere they'll actually resurface, so a mistake made once isn't made again.

The encouraging part is that the raw material for that loop already exists in the same toolset. Because reveal treats a Claude Code session as just another queryable resource, an agent can inspect its *own* run: `reveal 'claude://session/<id>/tools'` reports per-tool success rates (in one real session, `Bash: 94.9%`, `Edit: 100%`); `?errors` lists every failed call with its context; `?tokens` shows where the budget actually went, turn by turn. An agent that can read its own error log and token-waste profile has everything it needs to get more reliable over time — the learning loop isn't a missing capability so much as an unbuilt habit.

## The one piece you can adopt today

Most of the machinery above is glue specific to one setup, but the progressive-disclosure engine at the center of it is open source and worth trying on its own. **reveal** (`pip install reveal-cli`, MIT-licensed, [github.com/Semantic-Infrastructure-Lab/reveal](https://github.com/Semantic-Infrastructure-Lab/reveal)) is a local-first CLI whose whole premise is the pillar-3 discipline enforced by design: *"How AI agents understand codebases without wasting tokens."* Point your agent at `reveal <dir>` and `reveal <file> <symbol>` instead of reflexive full-file reads, and its adapters (`markdown://` for front-matter search, `git://` for history, `claude://` for self-reflection) give you cheap footholds on the other pillars too. It's the single highest-leverage change you can make without building anything — the grounding floor, in one command.

Grounding well is the floor, not the ceiling. But it's the floor everything else stands on — and it's the part almost every agentic setup gets wrong first.
