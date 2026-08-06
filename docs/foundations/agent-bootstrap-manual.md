---
title: "Agent Bootstrap Manual"
subtitle: "Zero to a grounded agentic framework — the model, the pieces, and the day-one runbook"
type: guide
audience: "developers, AI engineers, teams standing up agent tooling"
beth_topics:
  - agentic-ai
  - bootstrap
  - grounding
  - progressive-disclosure
  - orientation
  - calibration
  - continuity
  - meta-engineering
  - claude-md
  - agent-tooling
related_docs:
  - ../articles/grounding-not-reasoning.md
  - ../articles/two-halves-of-trust-engineering.md
  - ../articles/two-speeds-of-meta-engineering.md
  - ../articles/engineering-trust.md
  - ../research/information-architecture/PROGRESSIVE_DISCLOSURE_GUIDE.md
beth_weight: 3.0
---

# Agent Bootstrap Manual

**This page is an installer. The rest is a reference you come back to.** You arrive
with one capability and need four more. Install them, verify each, then stop reading.

## Boot status

| Capability | On arrival | Installed when | Verify |
|---|---|---|---|
| **Reasoning** | ✓ present | — | — |
| **Grounding** | ✗ absent | A ladder exists, and the cheap path is the *enforced* one | B-8 |
| **Calibration** | ✗ absent | Your tools distinguish "nothing here" from "I couldn't see" | B-9 |
| **Continuity** | ✗ absent | Open work has an owner and a status outside this conversation | B-14 |
| **Retrieval strategy** | ✗ absent | Someone who wasn't here can find what you learned | B-10 |

**Nothing installs by reading.** Each row installs when its artifact exists and its
check passes — which is why every check in Appendix B is executable and not one of
them asks what you understood.

> **Intelligence, in an agentic system, is the choice of the next retrieval — not the
> quality of the next token.**

**Improvements in reasoning raise the ceiling. Improvements in retrieval policy
compound across every subsequent task.** One changes what the agent *can* do; the
other changes how much prior work *survives*. That asymmetry is structural and does
not depend on how good models get.

Everything here exists to make the grounded path *cheaper* than the ungrounded one.
If doing it right is also the fast path, it gets done right by default.

**Self-check, before you continue.** Run `reveal <this file> --outline` before you
read further. If you didn't — if you opened this whole instead — you have already
violated **I1** on the page that defines it, and noticing that is worth more than
anything below. Nothing here is hypothetical; the document is the first test case.

## Grounding, defined

> **Grounding is minimizing uncertainty by retrieving the least expensive
> representation sufficient for the decision at hand.**

Every clause is load-bearing. *Least expensive* — there is almost always a cheaper
view than the one you reached for. *Sufficient* — more is not better; surplus context
degrades the reasoning done over it. *For the decision at hand* — sufficiency is
relative to what you are about to do, not to the topic in general. The same file
warrants an outline before a rename and a full read before a rewrite.

**Memory is not grounding, and confusing them is expensive.** An agent does not get
better by remembering more. It gets better by knowing *where information lives, what
retrieving it costs, when retrieval is warranted,* and — hardest — *what not to
retrieve at all.*

Stored memory is a **corpus**: one more place information can live. It becomes
grounding only when a policy governs whether, when, and how it is retrieved. Good
memory systems do have relevance scoring, expiry, and provenance — but those are
retrieval policy implemented inside the memory layer, which is the point rather than a
counterexample. Everything in this manual is retrieval infrastructure; adding a memory
store without a retrieval policy adds a corpus and calls it a capability.

## Representation

Agents never reason over reality. They reason over a **representation** of it — an
outline, a schema, a call graph, a frontmatter block, a diff, a status field.

```
Reality → Representation → Retrieval → Reasoning → New representations
              ↑                                              │
              └──────────────────────────────────────────────┘
```

It is a loop, not a pipeline. Reasoning does not end in an answer — it ends in a
handoff, a ledger entry, a document, a rule. Those become the representations the
next retrieval reads. **That loop is the entire mechanism of cumulative
intelligence:** a system improves not by reasoning harder, but by leaving behind
representations that make the next retrieval cheaper.

> **Every representation throws information away. The engineering is choosing what to
> discard before reasoning begins.**

That is why outlines, trees, signatures, schemas, indices, and frontmatter all exist.
Each is a deliberate lossy projection, chosen because what it keeps is sufficient for
a class of decision and what it drops is exactly what made the original expensive.

Three consequences run through everything below:

- **Cheap and lossy is usually correct.** An outline discards every function body and
  is still the right first move, because *which function do I need* never required
  bodies.
- **The wrong projection fails silently.** A function-shaped index over a
  function-free file discards everything and reports success (§0). Chunk size is
  downstream of chunk *unit*.
- **A representation is not the system.** The outline is not the code. The generated
  config is not the template. The status report is not what happened. The pile of
  transcripts is not the open-work list. Most agent failures are correct reasoning
  over the wrong projection of reality — not bad reasoning.

### Two kinds, two failure modes

Every representation is either **observed** or **authored**, and they rot for opposite
reasons. This distinction is the reason behind several rules stated separately below.

| | **Observed** | **Authored** |
|---|---|---|
| Examples | filesystem, outline, call graph, git history, schema, logs, runtime | docs, handoffs, ledgers, project blocks, the always-loaded contract |
| Produced by | derivation from the artifact, on demand | a person, once |
| Drifts when | reality changes — and it re-derives correctly on the next read | a person stops updating it — and it keeps reporting the old world, confidently |
| Cost of staleness | near zero: regenerate | high: nothing signals that it's wrong |

> **Prefer observed. When you must author, make it cheap to check against the
> observed.**

That single preference is why boot must be *emitted* rather than typed (§8), why you
cite the command instead of the number (§9), and why converting an authored
representation into an emitted one is the highest-value refactor available (§12).

**An authored representation is a cache of an observation with no invalidation.**
Every one you create is a promise to maintain it. The ones worth that promise are the
ones holding facts no observation can produce: **intent, decisions, ownership, and
what was tried and rejected.** Those are irreducibly authored — which is exactly what
handoffs and ledgers hold, and precisely why those two are the artifacts this manual
insists you write by hand while telling you to generate almost everything else.

**Retrieval policy chooses representations. Grounding is the quality of those
choices.**

## The Invariants

Six conditions that must stay true. Each maps to a section that explains it and a
check in Appendix B that tests it. **If you implement nothing else here, implement
these and their tests** — the rest of the manual is how.

| # | Invariant | How | Test |
|---|---|---|---|
| **I1** | Retrieve no more than the decision **and its verification** require | §0, §2 | B-8 |
| **I2** | Before an expensive retrieval, record either the cheaper attempt that failed, or why none could suffice | §2 | B-13 |
| **I3** | Every material result declares confidence, coverage, freshness, **and failure mode** | §1.1 | B-9 |
| **I4** | Every discovery **with future value** becomes retrievable, at the right scope | §7, §14 | B-10 |
| **I5** | Every open item has one accountable **owner or queue**, and one canonical status | §6 | B-14 |
| **I6** | Every **mutable operational** fact has one authoritative home | §7.3 | B-3 |

An invariant you cannot test is a preference. That's why each row has a check.

**"Expensive," "material," and "future value" are deliberately undefined here — a
team declares its own thresholds, in its project block (§4.1), rather than
inheriting a number that doesn't fit its domain.** An undeclared threshold is not
evidence you have none; it's evidence you haven't decided, and I2/I3/I4 stay
unfalsifiable until you do.

Two of these are scoped deliberately, and the scoping is the useful part. **I4** says
*with future value* because a system that records everything degrades into the museum
§12 warns about — recording is not free, and noise is a cost paid by every later
reader. **I6** says *mutable operational* because safety constraints, license text,
interface contracts, and tests that intentionally restate expected behavior are
legitimately duplicated: redundancy is a feature when the copy is the point.

### Two horizons, and the conflict between them

**I1 and the operating loop optimize on different timescales, and they will collide.**
I1 minimizes retrieval for *the decision in front of you*. §2.1's Record and
Generalize steps spend effort now to reduce the cost of work that hasn't happened yet.
Both are correct. State the trade rather than pretending it away:

> **Optimize retrieval locally for the current decision. Optimize recording and
> tooling globally for repeated future work.**

When they conflict, the tiebreaker is reversibility: unrecorded work is unrecoverable
once the session ends, while over-retrieved context costs only tokens.

### The install path — read only these, then stop

> **Grounding · Representation · The Invariants · §0 · §1 · §2 · §14 · §15**

A few hundred lines — measure precisely with `reveal <this file> --outline` and sum
the sections above; don't trust a hardcoded figure here any more than anywhere else
in this document (§5.2). That is the installer. Everything else in this document is
**reference** — correct, useful, and *not required to read in full* to reach
installed state. §14 will send you back into specific sections of Part II (§3.1, §6,
§7, §8, §9) as it walks you through each artifact — that's by design, not a gap in
this list: the install path is what to read *before* Day One, not everything Day One
touches. Come back to the rest piece by piece as Appendix B or the diagnostic index
sends you there, which is how reference material is supposed to be consumed.

Blocks marked **⚙ Implementation** are one instance of a spec, not the spec. The
architecture above them is meant to outlive the tool named in them; if the tool
changes, those blocks are what you rewrite.

---

## How to Read This

There is no single agent-instructions file. There are **three artifacts with
different lifecycles**, and conflating them is the most common failure:

| Artifact | Read when | Cost | Holds |
|---|---|---|---|
| **This manual** | Once, at setup | Free — never in context | The framework, the specs, the runbook |
| **The always-loaded contract** (`CLAUDE.md` / `AGENTS.md`) | Every session | Paid every session, forever | Only what can't be looked up in time |
| **Tool-emitted orientation** | On demand | Paid when used | Every fact that drifts |

Most `CLAUDE.md` files are bad because they try to be all three at once — and they
fill with command references that are wrong within a month.

**Reading this efficiently.** Do not load it whole. Outline it, then extract only the
sections you need — each one stands alone:

```bash
reveal agent-bootstrap-manual.md --outline                       # the whole shape, live
reveal agent-bootstrap-manual.md "9. The Always-Loaded Contract" # same op as a named code element
```

That this manual is navigable that way is not an accident (§7.5). If your structural
tool returns a flat or empty outline for it, that's your §0 failure condition firing —
and your first finding.

**Parts I–II are the model and the pieces. Part III is the practice. Part IV is what
you type on day one.**

**Starting from nothing?** Read §0–§2, jump to §14 (Day One), then come back to
Part III.

**Already have a system and want to find its gaps?** Don't read this front to back.
Find your symptom below and read only those sections.

| Symptom you can observe | What's missing | Read |
|---|---|---|
| Retrieved text has ever been followed as an instruction | No trust boundary | §11.1, §11.2 |
| "Nothing found" gets acted on the same way regardless of stakes | No negative-result policy | §1.2 |
| The agent reads whole files before acting | The ladder isn't enforced by tool surface | §2, §10 item 1 |
| It reports "nothing found" and is confidently wrong | No calibration signals in tool output | §1, §10 item 4 |
| The same question gets rediscovered across sessions | Retrieval without a ledger | §3, §6 |
| A capability exists and the agent never reaches for it | No capability index at rung 0 | §2, §6, §13 |
| Your always-loaded file is long, and partly stale | Rules filed at the wrong scope | §4, §9 |
| Docs exist but nobody finds them | No router, schema, or authoring discipline | §7 |
| Boot output is hand-maintained | Orientation templated instead of emitted | §8 |
| Two agents clobber each other's work | Concurrency treated as an edge case | §11 |
| The knowledge base is mostly stale entries | No decommissioning force | §12 |
| The same lesson keeps getting re-learned | The loop isn't closing | §13 |

Each row is independently actionable. You do not need the sections around it.

**Working, not auditing?** Route by the question in front of you:

| If your next question is... | Go to |
|---|---|
| "What should I look at before acting?" | §2 |
| "What belongs in the always-loaded file?" | §9, App. C |
| "How do I know what I'm *not* seeing?" | §1.1 |
| "How do I make docs findable later?" | §7 |
| "How do I track open work?" | §6 |
| "What should boot print?" | §8 |
| "What do I build first?" | §10, §14 |
| "How do I keep this from rotting?" | §12 |
| "Something returned empty — now what?" | §2.3 |
| "What should I be holding in working state?" | §2.2 |

**Sections state their own stopping condition.** Where a section ends with
**Done when**, that is the test for leaving it — not whether you reached the bottom.

Note what those tests measure: **behavior, not comprehension.** "You can name which
of the five fields each of your tools omits" is checkable against reality. "You
understand calibration" is not checkable against anything, which is why no stopping
condition here is phrased that way. If a test asks about your last three retrievals
and you have to guess, the answer is no.

---

# Part I — The Model

*Tier: **theory**. Nothing here names a tool. If every tool in this document were
replaced tomorrow, this part would stand unchanged — and someone could build a new
implementation from it.*

## 0. The One Rule

> **Structure before content. Never read what you can outline.**

As enforceable policy rather than advice:

```
RULE 0 — Cheapest sufficient representation

Before opening any artifact, attempt at least one of:
    □ outline / structure
    □ metadata / frontmatter
    □ signature / schema
    □ index / router

Escalate to full contents only after a cheaper representation has been
attempted and found insufficient.

EXEMPT: artifacts small enough that structure costs more than content,
        and task classes that inherently require full text — proofreading,
        license review, global rewrite, exact-wording analysis.

VIOLATION: full contents retrieved with neither a cheaper attempt on record
           nor an exempt task class.
```

**The violation clause is the load-bearing part.** It converts a preference into
something detectable — by you, in your own transcript, after the fact. A rule you
cannot catch yourself breaking is a rule you will break, and the catching has to be
mechanical because self-assessment is exactly the witness §1 tells you not to trust.

**The exemption is equally load-bearing.** An outline call on a six-line config costs
more than reading it, and a rule that mandates ritual tool calls before obvious reads
trains compliance rather than judgment. The principle is *cheapest sufficient
representation* — structure is normally the cheapest first content-bearing view of a
nontrivial artifact, not a mandatory toll on every one.

A directory listing before a file. A file outline before a function. A function
signature before its body. A heading list before a document. You escalate to the
expensive view only when the cheap one tells you that you have to.

This is not an optimization. It is the architecture that lets intelligence find what
matters — 80% irrelevant context does not merely cost money, it degrades the
reasoning done over it.

**Two corollaries that are always omitted, and always needed:**

**The outline is not the content.** A heading titled "Root Cause" is not the root
cause. A function's name is not its behavior. Structure tells you *where* to look.
You still have to look.

**The rule carries its own failure condition.** If an outline comes back empty, or
lists 0–1 elements on a file of 500+ lines, that means **blind, not simple** — your
index is shaped on an abstraction the artifact doesn't have. Switch lenses; do not
conclude the file is trivial. A function-shaped index over a function-free file
returns a clean, confident, empty answer. State this failure condition wherever you
state the rule, or every project that hits it will have to rediscover it locally.

## 1. The Four Questions

Every piece of work should have an answer to all four. Most systems answer one and a
half.

| # | Question | Property | Failure if missing |
|---|---|---|---|
| 1 | **What exists here?** | Observability | Acting on a system you cannot see |
| 2 | **What did I fail to see?** | **Calibration** | A confidently wrong clean bill of health |
| 3 | **Is this resolved, and whose job is it?** | Continuity | The same gap rediscovered forever |
| 4 | **Did this friction become permanent?** | Meta-engineering | Paying the same cost again next week |

**Question 2 is the one nearly every setup omits, and the one that bites.** An empty
result means one of two very different things: *there is nothing here*, or *I could
not see what is here*. A tool that renders both identically will eventually hand your
agent a clean answer it did not earn.

Four implementable forms — these are specs, not sentiments:

- **Announce truncation.** When output is cut, emit a marker and a cursor. An agent
  that doesn't know it received a partial view draws conclusions at full confidence.
- **Report the unresolvable; never drop it.** A sweep that silently discards what it
  couldn't parse returns a false clean result. An unresolvable item cannot be ruled
  out of a cross-reference.
- **Every index entry carries its own age.** Retrieval that can't say when it last
  looked is indistinguishable, from the inside, from retrieval that is simply wrong.
- **Report your own coverage gaps.** The rarest and most valuable: a registry that
  says *"11 directories found without metadata"* is stating in numbers what it does
  not cover.

**Q2 is the only one with no capability of its own.** §3 lists four capabilities, and
you will notice that Q1, Q3, and Q4 each map to one while Q2 maps to none. That is not
an omission — **calibration is not a component, it is a property every component must
have**, the way latency is a property of every hop in a network rather than a layer in
the stack. Nobody adds latency to a protocol; you account for it at each hop or you
ship something that works in theory. This is exactly why Q2 is the one that goes
missing: there is no single place to build it, so it gets built nowhere.

Two more four-item frames follow — §3's capabilities and §4's scopes. They are
deliberately distinct from these questions, and mapping them one-to-one will mislead
you: **questions are what you ask, capabilities are what answers them, scopes are
where the answer is stored.**

**Done when:** you can state, for the last operation you ran, what it did *not* cover.

### 1.1 The calibration envelope

Because Q2 has no component of its own, it has to live in the **interface** — in what
every operation returns. That is the concrete, buildable form of calibration, and it
is the single highest-leverage specification in this manual.

An operation that returns only an answer is unusable at scale, because the reader
cannot distinguish a real result from a blind one. **Every retrieval — every tool
call, every query, every artifact read — should carry five things:**

| Field | Answers | Without it |
|---|---|---|
| **Answer** | What you asked for | — |
| **Confidence** | How much this is worth | A finding and a guess look identical |
| **Coverage** | What was searched — and what wasn't | Empty reads as "nothing exists" |
| **Freshness** | When the underlying data was last true | Stale reads as current |
| **Failure mode** | What this operation cannot see *by construction* | You cannot separate absence from blindness |

Most tools return one field of five. **That ratio is the entire problem**, and it is
why Q2 fails silently everywhere: nothing is broken, every call succeeds, and the
missing four fields are invisible precisely because they were never emitted.

You do not need all five on every call. You need to know **which are missing** — and
a tool that never emits any of them cannot be trusted with a *negative* result. A
positive result you can verify by inspection; a negative one you cannot verify at all
without coverage and failure-mode information.

This is also the sharpest evaluation criterion you have when choosing tooling. Ask of
any candidate: *when it finds nothing, can I tell why?* Most cannot, and most never
advertise that they cannot.

**Confidence needs a basis, or it is noise.** "High confidence" with no derivation is
a mood. Emit the reasoning instead:

```yaml
confidence:
  level: medium
  basis:
    - exact structural match on the declared symbol
    - source parsed without error
  reducers:
    - dynamic invocation not inspected
    - only one of three candidate directories scanned
```

A reader can act on that. They cannot act on `0.87`.

**Done when:** you can name, for each tool you rely on, which of the five fields it
emits and which it silently omits.

### 1.2 When a negative result licenses action

The envelope tells you *how much* a negative result is worth. It does not tell you
when it is worth **enough**. Absent a policy, "I searched and found nothing" gets
treated identically whether it precedes a comment edit or a production deletion.

| Decision class | Minimum support for acting on "nothing found" |
|---|---|
| Reversible local change | Declared coverage, no parser or access failures |
| Deleting code as dead | Static sweep **plus** dynamic-entry review — never a static signal alone |
| Security or compliance claim | Authoritative source **plus** complete, stated scope |
| Production action | Fresh live-state check **plus** named approval (§11) |
| "There is no open work here" | Ledger queried with **all** non-terminal states included |

The rows escalate on two axes at once: reversibility of the action, and cost of being
wrong. Where a negative can't clear the bar, **abstain and say which field was
missing** — an honest "I could not establish this" is a usable result; a confident
absence is not.

## 2. The Discovery Ladder

Climb only as far as the question requires.

**What "cost" means here.** Retrieval cost is context tokens *plus* latency, tool
invocations, and the reasoning branches opened before the next decision. Token figures
in this manual are illustrative orders of magnitude on a typical code corpus, not
benchmarks — they vary by tokenizer, model, artifact, and whether tool results enter
context whole or summarized. **Measure your own** (§B.1); the ratios matter, the
absolute numbers do not.

The ladder below is a **default routing sequence, not a universal cost ordering.**
Rungs are usually monotonic in cost, but not always: a precomputed call graph can be
cheaper than extracting an element, and an exact-range read can beat parsing a
language your tool doesn't support. Use the order as the default and override it when
you know better — deliberately, not accidentally.

```
0. Capability   → does a tool for this already exist?
1. Project      → which project am I in, and what's its live status?
2. Docs         → what has been written? (titles, newest first — not contents)
3. Tree         → what files exist?
4. Outline      → what's in this file? (names and locations, no bodies)
5. Element      → this one function, this one section
6. Behavior     → control flow, side effects, variable movement
7. Graph        → who calls this, what imports what
8. Raw          → last resort, targeted region only
```

Most questions die at rungs 2–5. If you start at rung 8, you don't have a ladder —
you have a `cat` habit.

**Rung 0 is the one people leave out, and it is the most expensive omission.** Before
building, grepping, or declaring "there's no tool for that," search your own
capability index. Reinventing a capability you already own is the most common form of
waste in a mature system, and it is silent.

**The ladder is not tool-specific.** Database agents have it (schema → indexes →
query plan → rows). API agents have it (spec → endpoint → payload). Document agents
have it (router → headings → section → quote). Find yours and write it down with
costs annotated.

**Done when:** you can name your rung 0 command, and your last three raw reads each
either had a cheaper query that failed first, or recorded why no cheaper query could
suffice (**I2**).

### 2.1 The loop the ladder serves

The ladder answers *how deep do I go*. It does not answer *what am I doing*. That is
the loop, and it is the actual spine of the system:

```
  ┌──────────────────────────────────────────────────────────────┐
  │                                                              │
  ▼                                                              │
Orient → Discover → Retrieve → Reason → Verify → Record → Generalize
  │          │          │         │        │        │         │
where     what        least    do the   against  so it     so the
am I     exists      enough     work    reality  survives  LESSON
                                                 the       survives
                                                 session
```

**Most agent loops stop at Verify.** That is the failure that produces competent
sessions and an incompetent system. *Record* is what makes the **work** survive the
session; *Generalize* is what makes the **lesson** survive it. Skip Record and you pay
for the work again. Skip Generalize and someone else pays for the same lesson later —
which is §13, and why the last arrow loops back to Orient rather than terminating.

### 2.2 What the agent must hold

At any point in that loop, an agent should be able to answer these **without
re-deriving them**. If answering requires a re-read, it isn't state — it's a cost
you're going to pay twice.

| Hold | Because |
|---|---|
| Current project and objective | Everything else is scoped to it |
| What's been retrieved, and what it cost | Prevents re-fetching; feeds I2 |
| **What you know you haven't seen** | The working form of Q2 — this is the one that decays first |
| What's open, and who owns it | I5. If it's only in your head, it's already lost |
| What has already failed this session | A failure followed by the same command is a loop, not a retry |

The third row is the one that quietly disappears under pressure. Uncertainty you were
tracking at turn 5 becomes forgotten certainty by turn 40 unless it is written down —
which is why §14's handoff has a `Landmines` section and why `Unverified` belongs in
every output contract.

### 2.3 When a rung fails

The ladder tells you where to go next when a rung *succeeds*. This is what to do when
one comes back wrong — and "wrong" here usually means **empty**, which is the most
misread result in agent work.

| Symptom | Possibilities | Next move |
|---|---|---|
| **Outline empty or 0–1 elements** on a large file | Abstraction mismatch · unsupported language · generated/minified code · parser error | Check whether the tool *claims* support. If yes → abstraction mismatch, build a second lens (§10 item 11). If no → that's coverage, not blindness; say which. |
| **Search returns nothing** | Terms never co-occur · wrong field indexed · index stale · genuinely absent | Re-query with your single rarest term. Still empty → check index age *before* concluding absence (I3). |
| **Search returns everything** | Term too common to discriminate | Add your rarest term, not more terms. Volume is not specificity. |
| **Call graph shows no callers** | Genuinely dead · dynamic dispatch · invoked from outside the scanned tree | **Never delete on a static-only signal.** Widen the scope, then check for dynamic invocation. |
| **Two sources disagree** | One is stale · one is generated from the other | Find which generates which, then edit upstream — unless the runtime contract explicitly makes the generated artifact authoritative (a lockfile, a pinned build output). Establish which before touching either. |
| **A command fails twice identically** | You are in a loop | Change the *representation*, not the phrasing. Re-running with different words is not new information. |

The through-line: **an empty result is a claim that requires the same scrutiny as a
positive one.** Every row above is a case where the cheap conclusion — "there's
nothing there" — is wrong in a way that leaves no trace.

---

# Part II — The Pieces

*Tier: **specification**. Formats, contracts, and interfaces you implement yourself.
Blocks marked **⚙** are one reference implementation of the spec beside them — read
those as evidence that the spec is buildable, not as the spec.*

## 3. One Tool Install, Four System Capabilities

Exactly one thing to install. Everything else is a recipe you implement.

### 3.1 What a structural retrieval tool must do

Before naming any tool, the interface. **Anything satisfying these eight qualifies;
nothing here names a product.** If you already have a tool meeting them, you have this
capability and can skip the install.

| # | Requirement | Why it's non-negotiable |
|---|---|---|
| 1 | Outline an artifact **without** returning its content | The entire ladder depends on this one |
| 2 | Extract a **named** element, not a line range | Line numbers drift; names survive edits |
| 3 | Report unsupported or unparseable input **as such** | Otherwise "empty" and "blind" are the same output (§1) |
| 4 | Declare truncation, with a continuation handle | A partial view presented as complete is the worst failure mode |
| 5 | State what it covered, and what it skipped | Negative results are worthless without it (§1.2) |
| 6 | Emit machine-readable output on request | So it composes into pipelines and checks |
| 7 | Advertise its own capabilities on bare invocation | Rung 0 — otherwise capability is tribal knowledge |
| 8 | Breadcrumb the next operation | Turns an answer into a route |

Requirements 3, 4, and 5 are the ones most tools fail, and they are exactly the
calibration fields from §1.1. **Evaluate candidates on those three first** — 1 and 2
are common; 3–5 are rare and are what separates a tool you can trust with a *negative*
result from one you cannot.

**⚙ Implementation — one tool built to meet all eight:** [`reveal`](https://github.com/Semantic-Infrastructure-Lab/reveal)
(`pip install reveal-cli`, MIT). It targets rungs 3–8 by construction and extends the
same query syntax to infrastructure, databases, docs, git history, and prior agent
sessions. **Even here, apply §1.2 rather than taking it on faith** — conformance to
all eight is a moving target for any actively developed tool, reveal included.
Spot-check the ones you depend on (machine-readable output and bare-invocation
capability listing are worth checking first) against your installed version before
trusting a negative result from it. For a team with no structural retrieval layer
today, adopting one is still among the highest-leverage changes available without
building anything — the specific tool matters far less than meeting §3.1.

**Build (or adopt) four capabilities:**

| Capability | Answers | Why it can't be skipped |
|---|---|---|
| **Structural query** | **Q1** — what exists, at every scale | Rungs 3–8, enforced rather than suggested |
| **Doc discovery** | **Q1** at corpus scale — which document, without reading all of them | Retrieval quality is capped by authoring discipline |
| **A committed ledger** | **Q3** — is this done, and whose court is it in | Search *finds*; only a ledger *closes* |
| **Session history + handoffs** | **Q4** — what was already tried and failed | Otherwise every session relearns its own mistakes |

**No row answers Q2.** That is the point of §1's closing note: calibration has to be
built *into* each of the four above, not beside them. When you evaluate a candidate
tool for any of these rows, the question that separates a good one from a bad one is
almost always Q2 — does it distinguish "nothing here" from "I couldn't see"?

Two distinctions that decide whether you built one capability or two:

**Retrieval is not a ledger.** Retrieval answers *"has this been discussed?"* A ledger
answers *"is this finished, and whose job is it?"* Build only the first and the same
gap gets rediscovered for free, forever — every session searching correctly, finding
it, and stopping.

**Frontmatter filtering is not ranked search.** Exact-match filtering over one
directory is zero-infrastructure and often enough. A ranked index — link authority,
cross-project corpus, graceful degradation on weak queries — is a different
capability. Know which you have before trusting a "no results."

## 4. The Four Scopes

Knowledge is not one pile. It sits at four scopes, each with a different budget:

| Scope | Artifact | Paid | Holds |
|---|---|---|---|
| **Global** | `CLAUDE.md` / `AGENTS.md` | Every session | Rules true in every project |
| **Project** | Project block / registry entry | When you enter that project | Local rules, incl. overrides of global |
| **Work item** | `TASKS.md` | On query | Status, ownership, resolution |
| **Session** | Handoff README | On resume | What happened, what's still open |

**One test, four budgets:**

> Would the agent do the wrong thing *before it had a chance to look this up* — at
> this scope?

That single question resolves nearly every "where does this go" argument. A rule like
*"the service named `cron-service` does not run the cron"* would wreck a session — but
only in one project. It earns a place in that project's block and nowhere else.

### 4.1 What a project block should contain

The global contract gets a skeleton (§9). The project scope needs one too — and it is
where most load-bearing knowledge actually lives, because most rules are true
*somewhere* rather than everywhere.

```markdown
## Orient — start here
Declare the genre in the first line: this is a POINTER SHEET, not the brief.
Then the ordered boot moves, each with its cost and its extraction command.
State plainly what must never be read whole.

## Overrides
Where a global rule is wrong here — plus the DETECTION TRIGGER for when it applies.
Not "we do it differently," but "when you see X, switch to Y."

## Footguns
Each with the incident that produced it: what happened, when, what it cost.

## Access and topology
How to reach things. Which environments exist. What's gated, and how.

## Authority
Who decides what — and whether that consent is per-instance or standing.
```

The **Overrides** section is the one people leave out and the one that pays. A global
rule stated absolutely will be wrong somewhere; when it is, the local block should
carry both the exception *and* the tell for recognizing it. Pair this with §0: state
the failure condition in the global rule, and the local block only has to supply the
local answer.

### 4.2 Price every rule in past damage

A rule with provenance gets followed. A rule without one gets argued with, skipped
under deadline, and rediscovered the expensive way.

> ❌ "Be careful which service you deploy to."
> ✅ "Verify which service runs your code before any targeted deploy. Cost of getting
> this wrong (2026-07-16): two production hotfixes inert for ~90 minutes while
> reported as verified."

Dated receipts do three things a bare rule cannot: they let a reader tell **earned**
rules from **imagined** ones, they justify the rule's cost to someone who wants to
skip it, and they make the rule **prunable** — when the underlying hazard is finally
fixed, the receipt tells you which rule to retire (§12).

## 5. The Bootstrap Floor

Here is the tension this manual has to resolve honestly. §9 holds that *any fact a
human re-types to keep current is a defect.* Taken absolutely, that forbids putting
commands in documentation — which makes the documentation unusable cold.

The resolution:

> **Embed only the facts required to reach a tool's own self-describing surface.
> Everything past that is a pointer.**

For a structural query tool, that floor is five facts — and they're its most
version-stable surface, so drift risk is near zero:

```bash
pip install reveal-cli
reveal <dir>              # rung 3 — what files exist
reveal <file>             # rung 4 — what's inside, without contents
reveal <file> <name>      # rung 5 — extract one element
reveal help://quick       # the router — ~10³ tokens, use for everything else
```

Then the standing rule: **anything beyond these, ask the tool, never a document.**
That includes the ~10³ figure above — measure it yourself (`| wc -c`) rather than
trusting a number typed into a document, which is precisely §5.2's rule applied to
this document instead of yours.

### 5.1 ⚙ One rung up: the query model

Rungs 6–8 are where a structural tool stops being a nicer `cat` and becomes a query
layer. The *model* is worth knowing, because it's stable. The inventory is not.

```
<adapter>://<target>[/<path>][?<filter>&<filter>]
```

Code structure, call graphs, import health, git history, structural diffs, database
schemas, document frontmatter, and prior agent sessions can all answer to the same
syntax and the same operators. One mental model covers questions you'd otherwise need
four tools for: *who calls this function*, *did this change make anything more
complex*, *which documents are orphaned*, *what did a past session already try and
abandon*. A worked example — four adapters composed into one answer, with token costs
— is in Deeper Reading.

**Never memorize the adapter list.** Ask for it — a well-built tool ships discovery
flags that enumerate its adapters and emit machine-readable schemas per adapter.
Generate queries from the schema rather than hardcoding syntax you'll have to
maintain.

### 5.2 ⚙ Route by help cost

Orientation entry points differ by two orders of magnitude, and choosing wrong is the
easiest way to burn a session's budget in a single call:

| Entry point | Order of magnitude | Use |
|---|---|---|
| Task recipe / intent router | ~10² tokens | The cheapest real answer |
| Broad agent orientation | ~10³ | First contact with a tool |
| Per-adapter or per-command schema | ~10³ | Exact syntax for one known thing |
| The complete reference | ~10⁴ | **Never open cold** |

Do not trust that table — **measure it** (`<command> | wc -c`). Costs move between
releases, and a stale cost annotation routes you wrong at full confidence. That this
manual gives orders of magnitude instead of numbers is deliberate: §9's rule applies
to this document too.

If you build a namespace (§6), the floor collapses further — to *one* fact: run the
binary bare. That is the strongest reason to build one.

## 6. Your Agent's Namespace

The most common meta-engineering failure, by a wide margin, is **"the capability
existed and the agent never reached for it."** Routing, not building.

A single agent-named binary that lists its own capabilities kills that failure mode
structurally. Add a domain, and it appears in the listing. The agent finds it without
anyone updating a doc, a memory, or a contract line. **You don't teach the capability;
you make it self-announcing.**

```
<agent> <domain> <command>      # acme project show · acme session handoff · acme deploy status
```

**Build it in tiers. Do not gate day one on a framework:**

| Day one | Week one | Later |
|---|---|---|
| A markdown file with a schema, edited by hand | A binary that reads and writes it | A namespace with sibling domains |

**The file is the truth. The namespace is the index of what you can do to it.** Ship
the format first — the CLI is how it becomes discoverable, not how it becomes real.

### 6.1 The format (specify this exactly — it outlives everything)

- Plain markdown + YAML per entry, **committed in the repo it describes**, fully
  usable with none of your tooling installed
- **Self-hosted IDs from a real counter** — `PFX-1`, never "scan the file for the
  highest number." That's a race the moment two sessions file at once. External
  trackers renumber; when they do, every historical reference dies.
- **A status enum, not prose.** And the honesty rule that makes it worth having:
  `blocked` = waiting on a person (name them) · `held` = parked by choice, nothing to
  wait on · `future` = an idea. Set it honestly or the enum is decoration.
- **Resolution recorded as a validated reference** — which commit closed it, checked
  against the repo. Never scraped from commit-message conventions that drift. And
  *merged ≠ released*: verify ancestry before closing.

### 6.2 The six operations

`file` · `list --actionable` · `show` · `set-status` · `link` · `sync`.
Implementation is yours. Note that `list` and `list --actionable` are different
questions: an unfiltered list shows blocked and parked work as though it were
available.

### 6.3 The help contract

This is the generalizable artifact — steal it regardless of what your tool does:

| # | Rule | Failing example |
|---|---|---|
| 1 | **Bare invocation lists capability.** Never an error. | `tool` → "error: missing command" |
| 2 | **Three explicit tiers** — overview → topic → full, with costs annotated when they differ 10×+ | one 40,000-token dump |
| 3 | **Concept help ≠ flag help.** *"what does `blocked` mean"* is not *"what flags does `status` take"* | only argparse output |
| 4 | **Every output breadcrumbs the next move** | dead-end results |
| 5 | **Failures are cheap and legible** | stack trace, or a full dump on a typo |
| 6 | **Machine-readable on request** (`--format json`) | text-only, uncomposable |

**Acceptance test, one line:** *run the bare binary and every `--help`. If an agent
can't get from zero to a correct command in three calls without reading source, the
tool is not agent-ready.*

## 7. Document Organization

"Author documents to be retrieved" is a principle, not a system. The system is four
parts:

### 7.1 A router at the entry point

Not an exhaustive index — a **topic → document table**, roughly 30 lines, that answers
"where do I look for X." Exhaustive indexes go stale and nobody reads them; routers
stay small enough to maintain and are the first thing an agent should hit.

### 7.2 A frontmatter schema

```yaml
---
title: "What this document is"
type: guide | reference | architecture | procedure | analysis
topics: [project-name, concept, specific-thing]
---
```

Confirm which field your index actually reads. A document tagged only in a field the
search index ignores is invisible — brilliant and unfindable are the same thing.

### 7.3 One home per fact — reference down, never copy up

This is the rule that answers *"where does this new document go?"*, and it's the
highest-value one in this section. Copied facts are precisely the drift that makes
documentation untrustworthy. **If two documents independently maintain the same
drifting fact, one is already wrong — you just don't know which yet.** The rule
applies within a single document too — a summary table restating prose stated
earlier in the same file is the identical defect at zero distance.

The scope word matters (I6). Facts that *cannot* drift — license text, safety
constraints, interface contracts, a test that deliberately restates expected behavior
— are legitimately duplicated, and copying them is the point. The rule governs
mutable operational facts, which is nearly everything you'll be tempted to copy.

### 7.4 A check script that gates it

Loose files, broken links, missing frontmatter, index bloat. **Unenforced conventions
rot.** A five-minute linter in CI is the difference between a documentation standard
and a documentation aspiration.

### 7.5 One mechanical rule people miss

**Use real `###` headings for every navigable entry — not bold lead-ins in a list.**
Outline tooling indexes headings. A long document structured as bolded bullet items
collapses into one flat section and loses cheap-outline access entirely, which is the
whole reason you wrote it in a structured format.

## 8. Boot: What It Must Emit

"Run a boot command" is not a spec. Five emissions, **all generated live, none
maintained by hand**:

| Emit | Answers |
|---|---|
| Project identity + live status | Where am I? |
| **Document list, sorted newest-first** | What has been written? |
| **Actionable tasks only** | What can I start right now? |
| Last handoff pointer | What happened before me? |
| Health / anomaly flags | Is anything broken? |

Two of these carry the real weight:

**Sort documents by modification time and emit at boot.** A hand-maintained document
index is stale the day after you write it. A time-sorted emission is correct by
construction *and* doubles as a recency signal — the agent sees what's hot without
being told.

**Surface the task list automatically, filtered to actionable.** The failure mode is
not building a tracker; it's building one and not connecting it. *A task list nobody
sees at session start, that isn't searchable alongside the docs, that the agent has to
remember to check, is a task list in name only.*

## 9. The Always-Loaded Contract

Everything in this file is paid for **every session, forever**. That one fact should
govern every inclusion decision.

Apply **the scope test from §4** at its harshest here, because this is the most
expensive scope of the four: *would the agent do the wrong thing before it had a
chance to look this up?* If it could be looked up in time, it is a pointer.

| Include | Exclude → make a pointer |
|---|---|
| Hard gates (push, production, delete, spend) | Command references and flag lists |
| The discovery ladder, with costs annotated | Project facts that drift (versions, counts, file lists) |
| Which capabilities exist and how to reach them | Architecture explanations that live in a document |
| Anti-patterns you have actually hit | Anything a tool can emit live |

**Every hardcoded fact that can drift is a future lie with a delay fuse.** Cite the
command, not the number. If a fact has to be re-typed by a human to stay true, it's in
the wrong place — that is a defect in whatever should have emitted it. Deliberately
pinned values are the exception and should say so inline, so a later reader can tell a
pin from a stale copy.

Annotate costs in the discovery table. An agent choosing between a 300-token move and
a 40,000-token move needs to *see* that gap to route correctly. Cost annotation is
routing information, not trivia.

### Skeleton

```markdown
# <System> Operating Instructions

## Identity
Who the agent is, who it works with, the division of labor. 3–5 lines.

## Boot
One command. What to do with each outcome. Where to go next.

## Orientation — always, before working
The cheap moves in order, with costs. Re-run when work enters a new area.

## Discovery
The ladder (§2) as a cost-annotated table, cheapest first.
Plus the standing reflexes — and their failure conditions (§0).

## Hard Rules 🚨
Only the irreversible: push, production, delete, spend, concurrency.
Each with what to do instead, and whose approval is required.

## Continuity
Where the ledger is. Where handoffs live. How to search prior sessions.

## Save
The end-of-session ritual, in strict order.
```

---

# Part III — The Practice

*Tier: **operational discipline**. What keeps an installed system from decaying.
Sequencing, gates, pruning, and the improvement loop — none of it installable on day
one, all of it required by month three.*

## 10. Build Order

These are not peers. They come online at different times, and a checklist that
pretends otherwise implies you can stand up a fully trust-engineered system on day
one. You cannot — and the reason is structural.

### Day zero — installable now

1. **Make the ladder the only way in.** The mechanism is *tool registration*, not
   instruction. Expose your structural query layer to the agent as first-class
   registered tools — most ship an MCP server for exactly this, with structure,
   element extraction, query, and in-function navigation as separate tools — and
   **omit a raw whole-file read** from the registered set wherever the work allows.
   An instruction to prefer outlines is a policy the agent can drift from. A tool
   surface with no `cat` in it is not.
2. **Restrict tools by role.** An analysis agent gets read and query, never edit and
   write. Absence is a stronger guarantee than an instruction — though be honest about
   its limit: if the agent retains a shell, the shell can write. It removes the
   convenient path; it is not an inviolable boundary.
3. **Gate the irreversible.** Approval before production, pushes, spending, and
   anything externally visible.
4. **Require confidence and truncation signals in output.** Distinguish "nothing here"
   from "cannot see." The cheapest item on this list and the one most often missing
   entirely.

Once 1–4 exist, write them down the same day — that's §9's contract, and §14 step 5
is where it happens. The contract isn't a fifth day-zero task; it's the record of the
four you just did.

### Week one — build now, benefit later

5. **A ledger, distinct from search.** Committed, real IDs, status enum, validated
   resolution references. Building it in month three loses months one and two.
6. **Session history from day one.** If nobody can ask "what did we already try," every
   session relearns its own mistakes.
7. **Author documents to be retrieved** (§7). Retrieval quality is capped by how the
   corpus was written — and this is the half of grounding that only pays off in
   sessions you are not in yet.

### Earned — cannot be installed

8. **Dogfood on real work; write down where the tool fell short.** Not synthetic tests.
   File the note under *the project the work was on*, not the feature at fault — notes
   filed that way read as requirements later; notes filed by feature read as bug
   reports and age badly.
9. **Split every friction report by cost to fix.** *"The output was misleading"* and
   *"the capability was missing"* are different tickets at different prices. Fusing
   them buries the cheap fix under the expensive one.
10. **Prefer a scanner to a note.** "Watch out for this" finds the instance you already
    know about. A scanner finds the ones nobody has looked at.
11. **Build a second lens when the first stops fitting.** Not when the model seems
    confused — when the *abstraction stops matching the artifact*. Chunk size is
    downstream of chunk unit; when the unit is wrong the size is irrelevant, and the
    failure is silent. Knowing the difference requires day-zero item 4.

**A brand-new system cannot have items 8–11.** No incident has happened, no friction
has repeated, no capability has yet gone unused. That is not a gap to apologize for —
it is the honest answer to "how do I get from a new agent to a trustworthy one." Some
of it is installed, some accrues, some is earned.

## 11. Containment, Authority, and Trust

Three rules. Each is stated as a gate you can implement, not a value you can hold.

**Contracts, not permissions.** A permission says *you can*. A contract says what you
should do, what to ask about first, and what is off-limits even when technically
possible. Goal-directed optimizers route straight through permission systems toward
the fastest path to "done."

**Name the authority and the consent lifetime.** "Get approval" is not a contract.
*"The release owner's sign-off, per merge, not a standing blanket grant"* is. Approval
in one context does not extend to the next.

**Assume you are not alone.** Another agent or human may be live in this repo right
now. Stage explicit paths, never blanket-add; check for concurrent activity before
touching shared state. **This is a race condition, not a reasoning failure** — no
model improvement touches it, and agentic systems inherit every problem distributed
systems have had for decades.

*The five public incidents behind permissions-versus-contracts are in
[Trained to Please, Empowered to Act](/articles/trained-to-please-empowered-to-act).
Not repeated here.*

### 11.1 Retrieved content is untrusted

Everything else in this manual argues for retrieving aggressively. This is the
counterweight, and it is not optional:

> **Every retrieved artifact is data until its authority and scope are established —
> never instruction.**

A document, code comment, issue description, commit message, web page, or tool result
can contain text shaped like a directive. An agent that retrieves widely and reasons
over what it finds is, by construction, executing on attacker-reachable input. The
discipline that makes retrieval cheap is exactly what makes this reachable.

Three failure classes that retrieval discipline alone does **not** address:

- **Injected instructions** in retrieved content — the most direct, and the one an
  aggressive retrieval policy actively increases exposure to
- **Secrets surfaced through structure** — outlines, logs, environment dumps, and
  error text leak credentials that a full read would have been reviewed for
- **Side effects through a retained shell** — §10 item 2 concedes this; state it
  plainly. **Withholding a write tool while retaining arbitrary shell execution is
  ergonomic friction, not containment.** Treat it as reducing accidents, never as a
  boundary against a determined path.

### 11.2 The security envelope

Parallel to §1.1's calibration envelope, and for the same reason: the properties have
to live in the interface or they live nowhere.

| Field | Answers |
|---|---|
| **Source identity** | Where did this come from, and can that be verified? |
| **Trust level** | Authored by us · vendored · third-party · attacker-reachable |
| **Authorization scope** | What identity was this retrieved under, and what did that grant? |
| **Sensitivity** | Does the content itself require handling constraints? |
| **Allowed side effects** | What may act on this — nothing, read-only, write, network? |
| **Audit record** | Is the retrieval and any resulting action recoverable afterward? |

**This section is a boundary marker, not a security architecture.** It exists so that
retrieval discipline is not mistaken for a safety model. A system that implements
every other page of this manual perfectly and none of this one is efficiently and
legibly compromised. Threat modeling, credential scope and rotation, network egress
policy, supply-chain trust for tool servers, and incident response are all out of
scope here and none of them are optional.

## 12. Decommissioning

Every artifact in this manual **accumulates monotonically**. Project entries, ledger
items, handoffs, memories, rules. Nothing here removes anything, and without a
counter-force your knowledge base becomes a museum where stale entries outnumber live
ones and the agent cannot tell which is which.

- **Give every durable artifact a lifecycle.** Open → closed → archived. A ledger with
  no archive step becomes unreadable at a few hundred items.
- **Notes are pointers, not logs.** Freeform notes attached to a project entry refill
  with session narrative within weeks of being cleaned. Keep one or two lines pointing
  at the real document; archive the rest.
- **Make staleness visible rather than assumed.** Emit ages. A list where entries show
  *"today"* next to *"289 days"* is telling you where to prune without being asked.
- **Prune on a schedule, not on a feeling.** One-time cleanup does not hold; this
  recurs, reliably, and the second pass is always sooner than you expect.
- **Retiring a workaround is the highest-value move available.** When a tool grows the
  capability that a hand-maintained note was compensating for, delete the note and cite
  the release. That is the loop closing — not "we wrote down a lesson," but *a
  hand-maintained copy of the truth was recognized as a defect in the tool*, and the
  truth moved to the only place it can't drift from: the tool's own output.

## 13. The Loop

Shipping a capability is the **midpoint**, not the end. Budget the routing work as
part of the feature:

```
friction hit during real work
  → note filed under the project, split by cost to fix
  → cheap calibration fix  +  expensive capability fix
  → capability ships
  → does the agent reach for it?
      yes → loop closed
      no  → anti-pattern entry (tool side)
          → contract line + persistent memory (agent side)
```

**Capability generalizes far more readily than attention does.** A shipped capability
works everywhere it applies; the *habit of reaching for it* has to be rebuilt in every
artifact a future reader will encounter. Building the thing is usually the short pole.
Making a future stranger reach for it is the long one, and engineering talent barely
shortens it — because that part is a communication problem wearing an engineering
problem's clothes.

This is why a self-listing namespace (§6) is worth more than it looks: it is the only
mechanism here that makes new capability discoverable **without** a routing pass.

*The dated evidence for the two speeds — why this loop sometimes closes in three hours
and sometimes takes seven weeks — is in
[The Two Speeds of Meta-Engineering](/articles/two-speeds-of-meta-engineering).
Not repeated here.*

---

# Part IV — Doing It

*Tier: **runbook and reference**. Ordered procedures and copyable artifacts. Not read
front to back — entered from the diagnostic index, the question router, or Appendix B.*

## 14. Day One

Ordered. Roughly an afternoon.

```bash
# 1 — The tool half. Adopt or verify one structural retrieval layer.
# Already have a tool meeting §3.1's eight requirements? Validate it and skip
# to step 2. Otherwise:
pip install reveal-cli
reveal help://quick                      # learn the router, not the flags

# 2 — Prove the ladder in your own repo (rungs 3→5)
reveal .
reveal <a-real-source-file>
reveal <a-real-source-file> <a-function-name>
```

**3 — The ledger, by copying.** There's a paradox here: you need a tracker to track
building the tracker. **Appendix A.1 resolves it by arriving pre-filled** — copy it to
`TASKS.md` at your repo root and you have a working ledger in one move, already
seeded with the remaining steps of this manual. Your first tracked work is your own
bootstrap, which means the format proves itself before you've written a task of your
own. Then add one *real* item: something actually unfinished today, with an honest
status. A tracker seeded only with examples never gets used.

**4 — Two documents, authored to be found.** Copy Appendix A.2 to `docs/README.md` as
your router (§7.1), and write one real document with frontmatter (§7.2). Two is
enough to prove the system; twenty is procrastination.

**5 — The contract.** Write `CLAUDE.md` / `AGENTS.md` from the §9 skeleton. Apply the
inclusion test to every line. Expect it to be shorter than feels comfortable — that's
the test working.

**6 — Wire the boot emission.** A script or alias printing the five items in §8.
Identity, docs newest-first, actionable tasks, last handoff, health. Generated, never
typed.

**7 — Run it, then do one real piece of work.** Not a test task. Real work, following
the ladder deliberately.

**8 — Write the handoff.** Use Appendix A.3. Written by the agent that did the work,
from hot context — never delegated to a summarizer, because only that agent knows
which of the day's twenty turns actually mattered.

That's the loop closed. **Part III is what keeps it closed** — if you jumped here
from §2, go back and read it now.

## 15. The Operating Contract

Not a checklist of advice — the terms of every session. Each line is one step of the
loop (§2.1) and one invariant made checkable.

```
EVERY SESSION

  Orient       before acting, not after being wrong           I1
  Retrieve     the cheapest sufficient representation         I1, I2
  Declare      what you could not see                         I3
  Verify       against reality, never against a status report  I1
  Record       open work where someone else will find it      I4, I5
  Generalize   so the lesson outlives the session             §13

  Leave the system more grounded than you found it.
```

The last line is the only one that isn't testable, and it's the one that decides the
others when they conflict. **A session that completes its task and leaves the system
less legible has failed** — it converted a one-time cost into a recurring one, which
is precisely the trade everything here exists to prevent.

**Done when:** you can point at where each of the six lines happened in your last
session. Not whether you agree with them — where they happened.

## 16. Anti-Patterns

An index, not new material — every failure mode named in this document, in one place,
so you can scan for the one you're currently committing.

| Anti-pattern | Stated in |
|---|---|
| **Information dump** — full contents by default | §0 |
| **All-or-nothing** — a summary and a firehose, no navigable middle | §2 |
| **Dead-end output** — a result with no hint of the next move | §6.3 |
| **Hand-maintained truth** — any fact a human re-types to stay current | §9 |
| **A ledger nobody sees** — built, correct, never surfaced at orientation | §8 |
| **Capability with no routing** — it shipped and nothing reaches for it | §13 |
| **Confusing a representation for the system** | *Representation* |

The last row is the root cause of most of the others, and the only one that leaves no
trace when it happens.

## 17. Is This Page Stale?

It is, if any of these are true:

- A command in §5 or §14 fails, or its output no longer matches what's described here
- Your tools now emit something this page still describes as manual
- You've hit a failure class twice that appears nowhere in §16
- Anything here is a fact you've had to re-type to keep true — §12 applies to this
  document as much as to yours

This page is **deliberately bounded, not short.** The install path is a few hundred
lines; the rest is modular reference entered by section. That distinction is the whole
claim — a manual about progressive disclosure has no business being short, but it has
every obligation to be *navigable*. If you find yourself adding a command reference
here, that is the signal to build the tool that emits it instead.

---

## Appendix A — Starter Artifacts

Three files to copy. These are reference material, not reading — they don't count
against §17's length discipline, because you paste them once and then they're yours.

Every one of them is *deliberately minimal*. The failure mode with starter templates
is shipping something so elaborate that filling it in becomes a project; each of these
should take under ten minutes.

### A.1 — `TASKS.md`, seeded with this manual

Copy to your repo root. It is already tracking the rest of your bootstrap.

````markdown
# Tasks

    prefix: BOOT
    next_id: 13

Status: `open` · `in_progress` · `blocked` (name who) · `held` · `future` · `done` · `rejected`
Rule: the counter above is authoritative. Never infer the next ID by scanning for the
highest number — that's a race the moment two sessions file at once.

---

### BOOT-1 · Install and register a structural retrieval layer
```yaml
status: open
priority: high
effort: 30m
owner: bootstrap-owner
resolution: null
```
Must satisfy the eight requirements in §3.1. Register it as first-class agent tools —
structure, element extraction, query, navigation — and omit a raw whole-file read from
the registered set wherever the work allows. → §3.1, §5, §10 day-zero 1

### BOOT-2 · Restrict tools by role
```yaml
status: open
priority: high
effort: 20m
owner: bootstrap-owner
resolution: null
```
Analysis agents get read and query, never edit and write. Be honest about the limit: a
retained shell can still write (§11.1). → §10 day-zero 2

### BOOT-3 · Gate the irreversible
```yaml
status: open
priority: high
effort: 30m
owner: bootstrap-owner
resolution: null
```
Push, production, delete, spend, anything externally visible. Each gate needs a named
approver and an explicit consent lifetime. → §10 day-zero 3, §11

### BOOT-4 · Require truncation and confidence signals in tool output
```yaml
status: open
priority: high
effort: 1h
owner: bootstrap-owner
resolution: null
```
Distinguish "nothing here" from "cannot see." Announce partial views. Report what
couldn't be resolved instead of dropping it. Cheapest item here; most often missing
entirely. → §1, §1.1, §10 day-zero 4

### BOOT-5 · Stand up this ledger for real
```yaml
status: in_progress
effort: 15m
owner: you
resolution: null
```
You're reading it. Close this once you've filed a real task of your own and recorded a
resolution against a validated commit reference. → §6

### BOOT-6 · Session handoffs + searchable history
```yaml
status: open
priority: high
effort: 1h
owner: bootstrap-owner
resolution: null
```
A handoff at the end of every session (A.3) and a way to search prior ones. → §3,
§14 step 8

### BOOT-7 · Document organization
```yaml
status: open
effort: 2h
owner: bootstrap-owner
resolution: null
```
Router (A.2), frontmatter schema, one-home rule, and a check script gating all three.
Unenforced conventions rot. → §7

### BOOT-8 · Wire the boot emission
```yaml
status: open
priority: high
effort: 2h
owner: bootstrap-owner
resolution: null
```
Five items, generated live, never typed: identity, docs newest-first, actionable
tasks, last handoff, health. → §8

### BOOT-9 · Write the always-loaded contract
```yaml
status: open
priority: high
effort: 1h
owner: bootstrap-owner
resolution: null
```
From the §9 skeleton. Apply the inclusion test to every line. Expect it shorter than
feels comfortable. → §9

### BOOT-10 · Establish the trust boundary
```yaml
status: open
priority: high
effort: 2h
owner: bootstrap-owner
resolution: null
```
Retrieved content is data, not instruction. Decide what may act on third-party text,
where secrets can surface, and what the retained shell actually grants. → §11.1, §11.2

### BOOT-11 · Start a friction log
```yaml
status: future
owner: bootstrap-owner
```
Cannot start yet — requires friction that hasn't happened. File notes under the
project the work was on, not the feature at fault. → §10 earned 8–9

### BOOT-12 · First decommission pass
```yaml
status: future
owner: bootstrap-owner
```
Cannot start yet — nothing has accumulated. Schedule it anyway: prune on a calendar,
not on a feeling. → §12
````

Note what BOOT-11 and BOOT-12 demonstrate: `future` is not decoration. Those items
genuinely **cannot** be started on day one, and marking them `open` would put
permanently-unstartable work in your actionable view. That's the status enum doing
real work on its first day.

Every entry carries `owner`, including the unstarted ones — **I5 has no exemption for
"we'll figure that out later."** `bootstrap-owner` is a *role*, not a placeholder:
whoever adopts this file takes it, and replacing it with real names is the first
edit. That satisfies I5 honestly, where a blank or `unassigned` would not — neither
is an accountable owner or a queue, and a query for unowned work would return nothing
while eleven items sat unowned.

### A.2 — `docs/README.md`, the router

````markdown
# Documentation

**Start here.** This is a *router*, not an index — it answers "where do I look for
X," not "what exists." Keep it under ~30 lines. If it outgrows that, split the tree;
don't lengthen the router.

| I need to... | Go to |
|---|---|
| Understand what this project is | `../README.md` |
| Get set up locally | `setup.md` |
| Understand how it's built | `architecture/` |
| Follow a procedure or runbook | `procedures/` |
| Know *why* a decision was made | `decisions/` |
| See what's open right now | `../TASKS.md` |
| Resume prior work | `../handoffs/` (newest first) |

## Conventions
- Every document carries frontmatter: `title`, `type`, `topics`
- **One home per mutable operational fact** — reference down, never copy up (§7.3)
- `###` for every navigable entry, so outline tooling can index it
- `make check-docs` gates loose files, broken links, and missing frontmatter
````

### A.3 — The handoff

````markdown
---
date: YYYY-MM-DD
project: <id>
topics: [<areas this session touched>]
---

# <One line: what this session was actually about>

## Done
- <what shipped> → <commit ref>

## Verified
- <claim> ← <how it was checked: test run, endpoint hit, diff, ancestry check>
- <claim asserted but NOT verified, and why>

## Decided, and why
- <decision> — because <reason>. Rejected <alternative> because <reason>.

## Still open
- <item> → filed as `<PFX-N>`

## Next
<The single most likely next move, named specifically enough to start on.>

## Landmines
<Anything that will mislead the next reader: a doc that's now stale, a test that
fails by design, a tool whose output can't be trusted in this area.>
````

Two rules that make handoffs worth writing:

**If an open item isn't also in the ledger, it isn't open — it's forgotten.** The
handoff is narrative; the ledger is state. Narrative decays, state doesn't.

**`Verified` is what stops `Done` from becoming a status report.** §15 requires
verification against reality rather than against a claim; without a field for it, that
requirement has nowhere to land and "done" silently degrades into "I believe I
finished." An entry naming what was *not* verified is worth more than one that omits
the distinction — same reasoning as `Unverified` in an output contract.

**`Landmines` is the calibration section.** Everything else tells the next session
what you learned. This one tells it what *not to trust* — which is the part it cannot
derive on its own, and the part that would otherwise cost it the same hours it cost
you.

---

## Appendix B — The Self-Audit

§14 is for building from nothing. **This is for improving what you already have.**
Fourteen checks, each independently runnable, each with a fix pointer. Run them
against your own setup; the failures are your backlog.

The point of making these *executable* rather than reflective is §1's own lesson: your
recollection of how you work is the least reliable witness available, and it produces
a flattering account that feels true. Measure.

**"Executable" does not mean "unsupervised."** Several of these run to completion
without a human and still end in a judgment call — classifying a numeric literal,
deciding whether an owner field is a real name or a placeholder. That's not a
weaker check, but an agent running this table alone should know which rows it can
score and close by itself and which need a second pass (yours or a person's) before
the result is trusted. **Type** marks it: **Auto** = script/command settles it,
**Judged** = a script narrows it, a judgment call closes it.

| # | Check | Type | Failing looks like | Fix |
|---|---|---|---|---|
| 1 | Line count of your always-loaded contract | Auto | Over ~150 lines — reference material has crept in | App. C |
| 2 | Grep it for numeric literals, then **classify each**: stable · pinned · generated · drifting | Judged | Only *drifting* is a defect — an unmaintained fact that will silently go wrong | §9 |
| 3 | Diff it against your boot output | Auto | Anything stated in both places is drift waiting to happen | §9, §12 |
| 4 | Does a committed ledger exist in the repo? | Auto | Only issues in an external tracker, or nothing | §6 |
| 5 | **On a project with commits this month:** are closed ledger items carrying validated resolution references? | Judged | Closures recorded as prose, or not at all — a wishlist, not a ledger. (Dormant or long-horizon projects legitimately show zero closures; check the commits first.) | §6.1 |
| 6 | Does boot surface actionable items unprompted? | Auto | The agent has to remember to look | §8 |
| 7 | Is any part of boot output a static file? | Judged | Hand-maintained orientation | §8 |
| 8 | Is a raw whole-file read in the registered tool set? | Judged | The cheap path and the expensive path are equally reachable | §10 day-zero 1 |
| 9 | Point a tool at something it cannot parse | Judged | It returns clean and empty rather than saying it's blind | §1, §0 |
| 10 | Percentage of docs carrying frontmatter; count of docs nothing links to | Auto | Findability is authoring debt you're already carrying | §7 |
| 11 | Age of the oldest untouched entry in your registry or ledger | Auto | Nothing has ever been pruned | §12 |
| 12 | Can you list your own capabilities in one command? | Judged | No rung 0 — capability is tribal knowledge | §2, §6 |
| 13 | Your last three expensive or raw retrievals — does each carry a recorded cheaper attempt that failed, or a documented reason none could suffice? | Judged | No record of either — the expensive call was just the first move | §2, I2 |
| 14 | Every nonterminal ledger item — does it carry exactly one owner (not blank, not a placeholder) and a status from the enum? | Judged | Blank or placeholder owners, or status recorded as free prose instead of the enum | §6.1 |

### B.1 Measure before optimizing

The checks above find structural gaps. They do not tell you where your tokens actually go,
and **you cannot make a system information-efficient by intuition** — the expensive
call is rarely the one that feels expensive.

Your own session history is queryable data, not just a transcript: per-turn token
cost, cache hit rate, tool success rates, which files keep reappearing across
sessions, which commands failed and were retried unchanged. Establish a baseline
before you change anything, then re-measure after. Two numbers worth watching from the
start:

- **Tokens spent before the first substantive action.** This is your orientation cost.
  If it's growing session over session, something in the always-loaded path is bloating.
- **Ratio of structural calls to raw reads.** If raw reads dominate, the ladder is
  advisory rather than enforced — which is check 8, showing up in the data.

A failure followed by the identical command is a loop; a failure followed by a
different, cheaper query is intelligent recovery. Both are visible in the record and
neither is visible in memory.

---

## Appendix C — Refactoring an Existing Contract

The most common real task is not writing an always-loaded file. It's **cutting one
that has grown into a manual.** This is a mechanical procedure; do not do it by taste.

**Extract every rule as its own line, then apply four tests in this order.** The order
matters — each test is cheaper than the one after it, and the early ones delete lines
the later ones would have agonized over.

| Test | Ask | If yes |
|---|---|---|
| **1. Emitted?** | Does a tool already print this at boot or on demand? | **Delete it.** Cite the command instead. |
| **2. Lookup-able?** | Could the agent find this in time, before acting wrongly? | **Make it a pointer.** |
| **3. Scoped?** | Is this true everywhere, or only in one project? | **Move it** to the project block (§4.1). |
| **4. Drifting?** | Is it a number, version, count, or file list? | **Replace it** with the command that emits it. |

What survives all four is your contract. Everything else was reference material
wearing a contract's clothes.

**Expected outcome: a 40–70% cut on a typical contract.** A system carrying many
legitimate hard gates (production, spend, concurrency, a save/handoff ritual) will
land toward or below that range on an honest pass — that's the contract having
earned its length, not evidence the tests were applied too gently. The signal to
distrust yourself is cutting **nothing**, not cutting less than the range. If you
cut more than 90%, check that you haven't deleted a hard gate; those are the lines
that survive by design, because an irreversible action can't wait for a lookup.

Two rules for the cut itself:

**Move, don't delete, on the first pass.** Send removed lines to the project block or
a real document rather than the void. Some of them are load-bearing at a narrower
scope, and you'll find out which within a week.

**Re-run check 3 from Appendix B afterward.** The most common refactoring mistake is
moving a fact out of the contract and into a document while the tool *also* emits it —
you've gone from one stale copy to two.

---

## Deeper Reading

Read these when the corresponding question gets real — not upfront.

| When you're asking | Read |
|---|---|
| Why layer information at all? | [Progressive Disclosure in SIL](/research/progressive-disclosure-guide) |
| How do I get context in cheaply? | [The Hard Part Isn't Reasoning — It's Grounding](/articles/grounding-not-reasoning) |
| What makes a system trustworthy? | [I Didn't Learn to Trust AI. I Learned to Engineer Trust.](/articles/engineering-trust) |
| Where does each property get built? | [The Two Halves of Trust Engineering](/articles/two-halves-of-trust-engineering) |
| How does a lesson become permanent? | [The Two Speeds of Meta-Engineering](/articles/two-speeds-of-meta-engineering) |
| Why contracts instead of permissions? | [Trained to Please, Empowered to Act](/articles/trained-to-please-empowered-to-act) |
| How do I design an analysis subagent? | [Agents That Don't Read Everything](/articles/reveal-subagents) |
| What can I query besides code? | [Your Project Has an API Now](/articles/reveal-project-api) |
| How do I audit an agent's own history? | [Session Archaeology](/articles/claude-session-archaeology) |
