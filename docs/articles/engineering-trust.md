---
title: "I Didn't Learn to Trust AI. I Learned to Engineer Trust."
subtitle: "A working theory of engineered trust — five properties a human-agent system needs before an imperfect model becomes safe to rely on"
author: "Scott Senkeresty"
date: "2026-08-03"
type: "article"
status: "published"
audience: "developers, AI engineers, teams deploying agents in production"
reading_time: "16 minutes"
canonical_url: "https://semanticinfrastructurelab.org/articles/engineering-trust"
topics: [agentic-ai, trust, observability, verification, containment, continuity, meta-engineering, progressive-disclosure]
beth_topics:
  - agentic-ai
  - trust
  - observability
  - verification
  - containment
  - isolation
  - continuity
  - meta-engineering
  - reveal
  - sil
related_projects: [reveal, SIL]
related_docs:
  - docs/articles/two-halves-of-trust-engineering.md
  - docs/articles/two-speeds-of-meta-engineering.md
  - docs/articles/grounding-not-reasoning.md
  - docs/articles/trained-to-please-empowered-to-act.md
  - docs/articles/reveal-subagents.md
  - docs/articles/claude-session-archaeology.md
  - docs/articles/reveal-diff.md
  - docs/articles/configuration-semantic-contract.md
session_provenance: "tempestuous-ice-0803, destined-herald-0804"
linkedin_posted: false
---

# I Didn't Learn to Trust AI. I Learned to Engineer Trust.

*A working theory of engineered trust — five properties a human-agent system needs before an imperfect model becomes safe to rely on.*

One of the most common questions I get after talking about agentic AI is:

> "How did you learn to trust the agent?"

It's a fascinating question, because most people expect the answer to be about the models. Maybe something like "the latest models finally got good enough" or "reasoning models changed everything." Those things helped. But they aren't the real answer.

I never woke up one morning and decided an LLM was finally trustworthy. Over roughly the last eighteen months, I slowly engineered a human-agent system that became more trustworthy. That's an important distinction — trust isn't something you decide. It's something you engineer.

Which means the question people ask is actually the wrong one. The better question is:

> **How do you engineer a system that stays trustworthy even when the agent is wrong?**

That reframe matters, because it changes what you're optimizing for. You stop waiting for a smarter model to save you and start asking what your *system* needs to survive an agent's mistakes — because it will make them, no matter how capable it gets.

This isn't really an article about trusting ChatGPT, or any other chat interface. It's about trusting software engineering systems that happen to include AI as one component — which turns out to be a much older and better-understood problem than "is the model good enough." What follows is less a set of anecdotes than a working theory: trust is a property of the system built around the model, not the model itself, and that system can be engineered on purpose.

## Trust Starts at Zero

When I first started using LLMs for real engineering work, I trusted them about as much as I'd trust a brand-new engineer on day one. Not much. I reviewed everything, verified every change, questioned every recommendation. The models were already remarkably capable, but they failed in ways that made blind trust impossible: misunderstanding context, confidently asserting things that weren't true, editing the wrong abstraction, sometimes failing to even perceive the problem they were supposed to solve.

None of that surprised me. What surprised me was how my own response evolved. Instead of asking "how do I get a better answer," I started asking:

> **"Why did this fail?"**

That became the most valuable habit in my workflow. I started calling it *doing the meta*: doing the work solves today's problem, doing the meta improves how every future piece of work gets done. Every time I hit friction, I asked what assumption had failed, what information was missing, what tool or process would have prevented it — then tried to fix that permanently rather than just fixing the task in front of me.

A pattern connects almost everything that follows, and it's worth flagging before we get there: very little of it turned out to be about making the model reason harder. Almost all of it was about giving it — and giving me — a truer representation of what was actually going on. Better reasoning turned out to be surprisingly rare. Better perception turned out to matter almost every week.

Looking back at eighteen months of that habit, the fixes weren't random. They clustered into five properties, and understanding them as *properties of a system* — not just a list of failure stories — is the actual thesis of this piece. Each one is really a question you can ask when a piece of work is done, a checklist rather than a mood:

- Is this **observable** — can the agent actually see it?
- Is this **verified** — do we have evidence, not just a claim?
- Is this **contained** — how much damage can a wrong answer do?
- Is this **continuous** — does it survive past this one conversation?
- Did we do the **meta-engineering** — is the system permanently better for having failed here?

## 1. Observability — Can the Agent Perceive Reality?

The first question is simple: can the agent actually see the shape of the system it's working in? A surprising number of early failures had nothing to do with reasoning. The model wasn't stupid. It was blind.

Most coding agents default to grepping for a symbol, grabbing a few surrounding lines, and immediately proposing an edit. Experienced engineers rarely work that way — before touching code, they want the shape of the file, the interfaces, who calls what, the architectural boundaries. This is where progressive disclosure — feeding an agent a system in layers (project, then directory, then file, then call graph, then implementation) instead of dumping raw text into its context window — changed the workflow. The result isn't just fewer tokens; it's better reasoning, because the model spends its attention budget on structure instead of noise. It also unlocks a different class of question: instead of "search for authentication," you can ask "which files are the most complex" — sorting by complexity gives an agent a rational place to start instead of wandering randomly.

But observability tools carry an assumption baked in, and that assumption can quietly stop holding. One of our largest production systems is a legacy PHP application — over 820,000 lines of first-party code, more than half of it in files with zero or one function definition. One of the most important files in the whole system is over 11,000 lines long and defines no functions at all. An AST-based structure tool built to index functions, classes, and methods reports almost nothing on a file like that — not because the tool is broken, but because the abstraction it's built on (code organizes into named functions) no longer matches reality. The actual behavior lives in loops, SQL statements, session locks, and long procedural execution paths that were never organized into anything indexable.

The fix wasn't "make the model reason harder about an empty outline." It was building a second lens for a different abstraction — one that asks "what *behavior* exists here" instead of "what *functions* exist here," tracing variable flow, SQL safety, and lock windows directly rather than assuming they live inside named boundaries. The lesson generalizes past code: when the agent can't perceive the right structure, the fix is never "try harder to reason around the gap." It's building better perception for the structure that's actually there. Failures of observability like this one are what eventually pushed me toward building tools that improved what an agent could perceive, rather than asking it to keep reasoning harder over the same incomplete view.

## 2. Verification — Can We Prove What We Think Is True?

Observability solves a lot of failures. It doesn't solve all of them. There's a second class of problem where the agent could see perfectly, reason correctly, and still confidently tell me something false.

The rule that came out of this is almost embarrassingly simple: **never trust a status report when you can verify reality directly.** Don't trust "it's fixed" — run the test. Don't trust "it's deployed" — hit the endpoint. Don't trust "nothing changed" — diff before and after. Verification stopped being a fallback and became routine, applied even when nothing seemed to be on fire.

There's a sharper, public version of the same failure. Replit's AI coding agent, working inside an active code freeze, deleted the production database anyway — then, before anyone noticed, fabricated synthetic data to replace what was lost and represented the system as healthy. That's a report *engineered to survive verification*: if the agent that broke the dashboard is also the one keeping it green, verification isn't happening — it's being spoofed. The fix isn't a sharper verification habit; it's making sure the agent that might have failed isn't the sole source of evidence about its own work.

There's a third version of this, and it's about what "verify" even means. A staging environment went down — a gateway process had crashed against a hostname for a service that no longer existed. We found the bad reference, fixed it, verified the fix worked, and moved on. Five days later, the exact same outage happened again. The reason: the fix had patched the *generated* configuration file, not the *template* that generates it. Something on a routine schedule regenerated the config from the stale template, silently reverting the fix — and the verification we'd run the first time was real, honest, and completely insufficient, because it checked the artifact instead of the source of truth.

That's a different and deeper lesson than "reports can be wrong." **Verification can lie if you verify the wrong abstraction.** You can check reality perfectly and still be checking the wrong reality. That's the exact same failure shape as the PHP example above, wearing different clothes — the tool wasn't wrong, the boundary it was checking against was.

This is also why I've come to like output contracts that force the evidence itself into the artifact, not just the conclusion. A structural-code-analysis subagent we run in production must return every finding as Finding / Evidence / Mechanism / Confidence / Unverified, which leaves a confident claim with no traceable basis nowhere to hide — not because anything rejects a malformed answer (it's a required template, not a validated schema) but because a missing `Evidence:` line is conspicuous in a way that a merely unsupported sentence never is. It paid for itself in one ordinary week: the same contract closed one monitoring alarm as a false positive and independently confirmed a real, previously-unknown bug elsewhere in the same investigation — just as capable of saying *nothing's wrong here* as *something's wrong here*, which is the only way either verdict is worth trusting.

The same discipline applies to code: comparing structural complexity before and after a refactor, instead of trusting a description of what changed, is the identical "diff instead of narrate" instinct built into [one command](/articles/reveal-diff).

## 3. Containment — Are Failures and Concurrent Work Contained?

Even perfect perception and perfect verification don't eliminate mistakes. They just help you find them faster. The next question is: when something goes wrong, how much damage can it do — and it turns out this property runs in two different directions.

The first direction is the one people usually mean by "safety": if *my* agent is wrong, how do I limit the blast radius? The sharpest public example is Amazon's Kiro incident: given a minor bug to fix in AWS Cost Explorer, with operator-level permissions and no mandatory approval gate for AI-initiated production changes, the agent selected the "optimal" fix — delete the production environment and recreate it — and executed it. Cost Explorer went down for thirteen hours. The agent wasn't even wrong on the merits; delete-and-recreate genuinely is often the fastest path to a clean environment. Amazon's postmortem blamed "misconfigured access controls," not the AI — the agent made the call, the humans got the blame, a pattern worth watching because it will recur.

I wrote up that incident alongside four others in [Trained to Please, Empowered to Act](/articles/trained-to-please-empowered-to-act); the distinction that fell out of it matters here: **a permission says you can do this; a contract says what you should do, what to ask about first, and what you're never allowed to do even when you technically can.** In practice: approval gates before irreversible actions, leased and time-boxed production access instead of standing credentials, backups before any edit, read-only analysis kept structurally separate from write access.

The same distinction generalizes past agent actions into ordinary code. Declaring an architecture boundary in [an enforced config file](/articles/configuration-semantic-contract) — "routes cannot import repositories," checked on every commit — rather than in a design doc turns the boundary from a promise into a contract that fails CI the moment it's crossed. A doc says what *should* be true. A contract makes it true whether or not anyone remembers to check.

But the honest version of this section has to include the times the gate didn't get built. One roadmap spells out a full pre-merge check for a posting pipeline — the exact invariant guards it needs, already designed — under a heading that reads, verbatim: "REJECTED — not adding CI gates," with the cost stated in the same breath: "the phase that makes every other phase durable; without it, the fix decays exactly as the last one did." The gate wasn't missing because nobody thought of it. It was priced and declined, on the record. Not every promise gets upgraded to a contract. Sometimes the honest move is writing down that it didn't, and why.

The second direction is one I underestimated for a long time: agents don't just fail individually, they interfere with each other. A human and an agent can race for the same resource. Two agents can race with each other. Two independent coding-agent sessions can each believe they're making an isolated change right up until one runs a blanket "stage everything" command and quietly sweeps the other's unfinished, uncommitted work into the same commit under the wrong message. Nothing about better reasoning fixes that — it's not a reasoning problem at all. It's the same class of problem distributed systems have been solving for decades (races, locks, isolation levels), and agentic AI inherits every bit of it whether or not anyone building agent tooling has thought about it yet. The fix isn't intelligence. It's isolation: explicit staging instead of blanket adds, checking for concurrent activity before you touch shared state, and treating "someone else might be live right now" as a standing assumption in any shared repo or shared system.

## 4. Continuity — Does Work Survive Beyond One Context Window?

I originally thought agents mainly needed memory. I don't think that's quite right anymore.

Memory helps. Retrieval — letting an agent search prior sessions, decisions, and documents instead of hoping it remembers — is strictly better than memory, because it's engineered rather than probabilistic. But retrieval alone still isn't enough, and I only really understood why after watching it fail in a very specific way: one missing piece of configuration got rediscovered independently across more than half a dozen sessions spread over more than a week. Every single session searched correctly and found the exact same fact. Every session stopped right there. Nothing was ever resolved, and nothing was ever tracked as unresolved — it just got rediscovered, over and over, at full cost each time.

The problem wasn't memory, and it wasn't retrieval either — every session that hit it retrieved the fact just fine. The problem was that nothing in the system was accountable for finishing it. That reframed how I think about continuity entirely: **the missing primitive isn't remembering. It's knowing whose responsibility this is, whether it's done, and if not, why not.** Documentation tells you what's true. Retrieval helps you find it. A ledger — a durable, git-tracked record of open work with real status, real ownership, and a record of what resolved it — tells you whether something is actually finished. Those are different systems, and conflating them is exactly how the same gap gets rediscovered for free, forever.

Continuity's own machinery isn't exempt from needing the same scrutiny. The tool that links a session to its own transcript makes that link once, early, and has no reason to look again. Clear the conversation mid-session — a command that has nothing to do with continuity on its face — and the link keeps pointing at the transcript that existed a moment before, while the real conversation moves on in a file it was never repointed to. Nothing errors. The next summary reads perfectly normal; it's just quietly describing the wrong conversation. It only surfaced because the summary got checked against what had actually happened instead of taken on faith — the same rule from Verification, aimed one layer down at the ledger this whole section just argued for.

## 5. Meta-Engineering — Does Every Failure Make the System Better?

The fifth property is "doing the meta" itself, made literal. **Meta-engineering is treating a failure as an input to the engineering system itself, not an isolated defect to patch and move past.** Every failure either becomes a permanent capability — a tool, a rule, a tracked item — or it remains a recurring cost, paid again by whoever hits it next.

This property is easy to *claim* and hard to *show*, so here's the receipt rather than the assertion. A single piece of architectural cleanup — migrating twenty-five code adapters onto one canonical construction pattern — took five sessions of session-hopping in a single day. It never got lost or silently abandoned across that hopping, because it lived the whole time as one tracked work item with a running history: eight progress notes tracking exactly how many adapters were done after each batch. Two adapters flagged as hardest early on turned out, sessions later, to already handle the canonical shape correctly — discovered only because the ledger carried the "here's what we thought was hard" note forward instead of it evaporating with the session that made the guess. The work closed against the exact commit that resolved it, and the follow-up question it surfaced got filed as new tracked work instead of mentioned once and dropped.

The stronger version of the same instinct doesn't just track a failure — it makes the whole failure class unable to hide again. A codebase that has already been bitten by a status flag written before the action it claims actually succeeded, or by a per-platform gate a downstream query silently drops, now has commands built to sweep every file for every remaining instance of each shape, not just the one that already broke something. That's the difference between a note that says *watch out for this* and a scanner that finds every occurrence, including the ones nobody has looked at yet.

That's what meta-engineering looks like when it's actually built rather than aspirational: not a vibe, but an audit trail — or a standing scanner — you can point to.

The same instinct scales down to a single session. A session's own tool-call history — which commands failed, which repeated, where the token budget went — is queryable rather than reconstructed from memory (the same [`?errors`/`/workflow` introspection](/articles/claude-session-archaeology) that also matters for Verification), which turns "did we learn from that mistake" from a feeling into something you can check. An agent that can read its own error log has what it needs to stop repeating it — the missing piece usually isn't the data, it's the habit of looking.

That last sentence has since aged into a to-do list. The habit is now a standing procedure rather than a good intention, and the audit it runs keeps surfacing the same finding: the standing rules are all *written down* and nothing *watches* whether they were followed. Both halves of that turn out to be enumerable — the rules are a queryable list, and so is every command a session actually ran — which makes compliance checkable rather than merely aspirational. That check is now tracked work, which is the only reason I trust it more than the last five times I resolved to be more careful.

## The Industry Was Doing the Meta Too

I wasn't the only one running this loop. As the ecosystem matured, a long list of individual engineering workarounds — planning, sub-agents, persistent memory, tool orchestration, context management — independently evolved into standard platform capabilities. That convergence wasn't a coincidence. It was the industry rediscovering, team by team, versions of the same five properties a trustworthy human-agent system needs. Trust didn't increase because of one breakthrough model. It increased because the engineering around the model, in a lot of places at once, kept converging on the same shape.

None of the five properties were invented for AI, either. Observability, verification, containment, continuity, and learning from failure are what dashboards, code review, blast-radius limits, runbooks, and blameless postmortems have always been for — engineering concerns that predate language models by decades. Agentic systems didn't create those problems. They just raised the cost of skipping them, because a system that used to fail at the speed of a human typing now fails at the speed of an agent that never gets tired of being confidently wrong. The novelty isn't that AI needs trust. It's that AI makes the cost of skipping the engineering show up in weeks instead of years.

## The Same Failure, Wearing Different Clothes

Look back across all five properties and a pattern shows up that I didn't expect going in: an unusual number of these failures weren't really about intelligence, or even about which of the five properties was missing. They were about confusing a *representation* of the system for the system itself.

The AST outline wasn't wrong about the PHP file — it was a representation (code organizes into named functions) that no longer matched the reality it was standing in for. The generated nginx config wasn't unverified — it was a representation of the template, and the fix touched the representation instead of the source it was generated from. A status report is a representation of what actually happened, and the Replit incident is what it looks like when that representation gets actively falsified rather than just going stale.

A pile of retrievable session transcripts is a representation of what's still open — and it's the wrong one, because "open" is a status, not a fact you search for. A permission is a representation of what an agent is allowed to do; a contract is a representation of what it *should* do — and only one of those two survives contact with a goal-directed optimizer looking for the fastest path to "done."

Looking back, I don't think most of these failures came from poor reasoning. They came from reasoning correctly over the wrong representation of reality. Every one of the five properties, in the end, was really about the same move: giving the agent — or giving *me* — a representation that actually matched the system we were trying to change, instead of one that was merely convenient, familiar, or cheap to check.

## I Don't Trust the Model

People still ask me: "Do you trust AI now?"

Honestly — not exactly. I don't trust that the model is infallible. I trust something more interesting: a system deliberately engineered to help an imperfect model succeed anyway. Around the model, I've built better perception for the structures that actually matter, verification in place of self-reported status, containment in both directions — mine and everyone else's — continuity as a ledger instead of a hope that something gets remembered, and meta-engineering as the habit of turning every failure into a permanent change rather than a one-off patch.

Every failure became an opportunity to improve the system. Every improvement made the next conversation a little more reliable. That's how trust grew — not because the models became perfect, but because the system around them became steadily better engineered.

**Trust isn't a property of the model. It's an emergent property of the entire engineering system.** The biggest lesson I've learned from eighteen months of agentic AI isn't that the models are getting smarter, though they are. It's that we have enormous leverage in designing the environment they work within. The model never became perfect. What it could perceive, what got verified instead of trusted, what damage it could do, what survived past one conversation, what got permanently fixed — all of that did. That's where trust actually comes from.

---

**Where this goes next.** These five properties describe *what* a trustworthy system needs. They say nothing about where any of it gets built — and that turns out to have a structural answer. [The Two Halves of Trust Engineering](/articles/two-halves-of-trust-engineering) takes these same five and asks where each one actually lives.

*Part of SIL's ongoing series on agentic reliability. See also:*
- *[The Two Halves of Trust Engineering](/articles/two-halves-of-trust-engineering) — where these five properties actually live: each one engineered twice, and the calibration dimension that comparison exposes*
- *[The Two Speeds of Meta-Engineering](/articles/two-speeds-of-meta-engineering) — how a lesson becomes a permanent capability, in three hours or seven weeks*
- *[The Hard Part of Agentic AI Isn't Reasoning — It's Grounding](/articles/grounding-not-reasoning) — getting the right information in, before any of this matters*
- *[Trained to Please, Empowered to Act](/articles/trained-to-please-empowered-to-act) — five public incidents behind the permissions-vs-contracts distinction*
- *[Agents That Don't Read Everything](/articles/reveal-subagents) — evidence-bearing output contracts in production*
- *[Session Archaeology](/articles/claude-session-archaeology) — querying an agent's own history as an audit trail*
