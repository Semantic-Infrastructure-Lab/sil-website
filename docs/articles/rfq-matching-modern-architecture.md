---
title: "The Too-Many-Sausages Problem"
subtitle: "A practitioner's guide to RFQ matching at scale — from exact match to agentic retrieval"
author: "Scott Senkeresty"
date: "2026-03-23"
type: "article"
status: "published"
audience: "ML engineers, software engineers, technical leaders in manufacturing and distribution"
reading_time: "25 minutes"
canonical_url: "https://semanticinfrastructurelab.org/articles/rfq-matching-modern-architecture"
topics: [information-retrieval, rfq, semantic-search, embeddings, agentic-ai, manufacturing, enterprise, contrastive-learning]
beth_topics:
  - information-retrieval
  - rfq
  - semantic-search
  - embeddings
  - agentic-ai
  - manufacturing
  - enterprise
  - contrastive-learning
related_projects: [patmatch-v2, SIL]
session_provenance: "expanding-meteorite-0322"
---

# The Too-Many-Sausages Problem: A Practitioner's Guide to RFQ Matching at Scale

*State of the art, 2026*

---

## The Input Is Already Broken

Every industrial distributor has a version of this story.

A customer sends an RFQ — a request for quote — with 200,000 line items. Each line is a part they need: a bearing, a fuse, a sprocket, a hydraulic seal. Each part is described in the customer's local notation: their manufacturer codes, their part number formats, their shorthand. The distributor has a catalog of 14 million products. The job is to match every line on the RFQ to a product in the catalog, price it, and respond in two weeks.

This is, at its core, an **information retrieval problem**.

It's also one of the hardest information retrieval problems in industry: the queries are short and cryptic, the catalog is enormous, the domain semantics are highly specific, the cost of a wrong match ranges from "annoyed customer" to "electrical fire," and the throughput requirements are brutal. 200,000 queries, each searching 14 million candidates, is 2.8 trillion comparisons — before you add any intelligence.

This article explains what the state of the art looks like in 2026 — from the naive approaches that fail in predictable ways, through the pipeline architecture that handles most volume, to the agentic systems that handle what pipelines can't — and the non-obvious training strategy that makes all of it work.

---

## Part I: The Naive Approaches (And Why They Fail)

### The Query Is Also a Problem

Before discussing catalog matching at all, there's an upstream step that production systems spend significant effort on: the customer's line items are often not clean part numbers.

They arrive as free-text blobs:

```
"FLANGE BLOCK, 2-1/2 BORE DODGE 126220"
"SKF BEARING 6203-2RS1/C3 SEALED"
"SPACER, CPLG ATRA-FLEX M4 8-1/2"
"60BS15 X 1-7/16"
```

The matching system needs `(manufacturer_code, part_number)` before it can do anything. Getting there from these strings is its own problem: brand names are embedded in noise, part numbers are mixed with descriptions and measurements, fractions appear in non-standard notation, word order is inconsistent.

First-generation systems handle this with exclusion lists (strip known noise words: "BEARING", "BLOCK", "BORE"), brand dictionaries (scan for known manufacturer names), and heuristics ("the part number is probably the longest token with digits in it"). The result is brittle in the exact way you'd expect: word-order sensitive, word-boundary dependent, and fragile on measurement notation like `1-7/16` or `33.5 QD`.

A small LLM call (Haiku, $0.025/1K) transforms this step completely:

```
Input: "FLANGE BLOCK, 2-1/2 BORE DODGE 126220"

→ { manufacturer: "Dodge",
    part_number: "126220",
    description: "flange block, 2.5\" bore" }
```

Zero regex. Word-order independent. Contextually aware of what "BORE" qualifies vs. what the part number is. The LLM understands that "DODGE" here is a manufacturer, not a verb; that "2-1/2" describes the bore dimension, not the part number; that "126220" is the catalog item being requested.

This is the first place in the RFQ pipeline where modern AI moves the needle — before any vector search or catalog matching is involved. The downstream cascade only works if the upstream parsing gives it something to work with.

With clean `(manufacturer, part_number)` pairs available, the question becomes what to do with them — and here, too, the naive approaches fail in predictable ways.

### Approach 1: Exact Match

The first generation of RFQ matching is essentially exact match with hand-crafted normalization rules.

```
Query:  "SKF 6208-2RS"
Lookup: UPPER(STRIP(query)) → catalog
Result: found / not found
```

It works — for parts it has seen before. Production systems built this way routinely achieve 70% auto-match, which is real value: millions of dollars annually in manual lookup labor saved. But the brittleness is structural: a typo, a different spacing convention, a new manufacturer abbreviation — all return "no match" and route to manual review.

The deeper problem is maintenance. Fifty-plus hand-crafted brand-specific regex patterns. Every new manufacturer requires a new rule. Every rule has edge cases. The maintenance burden grows with the catalog, and the system fails silently on anything it hasn't been explicitly taught.

### Approach 2: "1 Massive Semantic Search"

The natural response to brittle exact matching is: use AI embeddings. Train a model on your catalog, embed everything, embed the query, find nearest neighbors. No more brittle rules — the model generalizes.

To understand why this is powerful and where it breaks down, it helps to understand what semantic search actually is.

**What semantic search is.** Over the last decade, researchers trained neural networks on enormous amounts of human-generated text. What those networks learned — remarkably — is how to plot words and concepts in a high-dimensional space such that meaning is encoded as geometry. Things with similar meaning land near each other. You can do arithmetic on the geometry: *king − man + woman ≈ queen*. More practically: *hot + dog ≈ sausage*. The model learned that "hot dog" and "sausage" are semantic neighbors because humans use them in the same contexts.

This is genuinely powerful. A semantic search for "hot dog" will surface sausages, bratwursts, frankfurters, and buns — the whole neighborhood of meaning. For discovery problems — e-commerce, knowledge bases, document search — this is exactly right.

**The too-many-sausages problem.** RFQ matching is not a discovery problem. It's a *substitution* problem. You don't want something like a `6208-2RS` bearing. You want a `6208-2RS` bearing — or something **certified interchangeable** by a human who has validated it in production. And the semantic neighborhood of `6208-2RS` is full of sausages:

```
6208-2RS   ←→   6208-ZZ      different seal type — often interchangeable, sometimes not
6208-2RS   ←→   6208-C3      extra clearance — usually NOT interchangeable
6208-2RS   ←→   6308-2RS     similar notation, different bore series — wrong bore, won't fit
6208-2RS   ←→   62082RS      same part, different formatting — IS interchangeable
6208-2RS   ←→   SKF 6208     same part, no seal code specified — ambiguous
```

All of these are sausage. Most are wrong. The semantic similarity score doesn't tell you which one to trust because the model correctly learned that they're all close — they *are* all close, in meaning-space. The problem is that "semantically close" is not the same as "safe to substitute."

Worse: the embedding space doesn't know about standards. A 30A Class CC fuse and a 15A Class CC fuse are semantic neighbors — both are fuses, same class, same mounting. They are not interchangeable. In a circuit designed for 30A protection, substituting a 15A fuse means it blows immediately, possibly causing an outage or a fire. The model learned fuse-ness but not the physical meaning of the amperage rating.

Fine-tuned embedding models on industrial interchange data can reach 82-86% accuracy. A real achievement — but production deployments surface three problems that are hard to escape at scale:

**Problem 1: Performance at scale.** A 200,000-item RFQ searching 14 million products is 2.8 trillion comparisons. Even with approximate nearest neighbor search, this becomes problematic at large customer volumes.

**Problem 2: No per-category reporting.** When accuracy is 84% overall, which categories are hitting 95% and which are at 60%? A monolithic model gives you one number. You can't improve what you can't measure.

**Problem 3: Confidence scores don't mean anything.** A 0.87 similarity score on a fuse query and a 0.87 on a bearing query mean completely different things. Without knowing which category you're in and what the ground truth distribution looks like for that category, the number is uninterpretable — and acting on it is guessing.

The monolithic semantic search approach is powerful but missing the structural insight that makes it trustworthy at scale.

---

## Part II: The Structural Insight — Category-First Architecture

The breakthrough isn't a better model. It's recognizing that **this is not one retrieval problem — it's eleven** — and that the "too many sausages" problem is different for every category.

Industrial MRO parts fall into distinct categories: bearings, sprockets, fuses, motors, belts, valves, chains, seals, hydraulics, pneumatics, fasteners. Each category has:
- Its own semantic rules (bearings match on base number; sprockets match on teeth count and bore)
- Its own catalog size (~1M products each vs 14M total)
- Its own definition of "interchangeable" (and its own hard negatives)
- Its own accuracy requirements (fuses: safety-critical; commodity hardware: permissive)
- Its own training signal (bearing interchange data doesn't teach sprocket matching)

The architecture that falls out of this insight is **category-based routing + progressive cascade**:

```
RFQ Item
    │
    ▼
[Category Classifier]    ← "Is this a bearing, sprocket, fuse...?"
    │
    ▼ (routed to correct category)
[Verified Data Layer]    ← exact match, fuzzy, interchange — 70% coverage
    │ miss
    ▼
[Semantic Pattern Layer] ← domain-specific extraction (bearing base numbers, sprocket teeth)
    │ miss
    ▼
[Hybrid Search Layer]    ← category-tuned model + Qdrant filtered HNSW + SPLADE
    │ low confidence
    ▼
[LLM Validation Layer]   ← category-specific compatibility reasoning (Corrective RAG)
    │ uncertain or miss
    ▼
[Agentic Research]       ← iterative tool use for genuine unknowns
```

The key metrics from category routing alone:
- Search space: 14M → ~1M per category (**14× reduction**)
- Parallelization: all categories searched simultaneously
- 200K-item RFQ: ~8 minutes instead of an hour
- Cross-category errors: prevented by architecture, not by model accuracy

But the deeper value of category routing is semantic, not just computational. Each category gets a model trained specifically to understand *its* sausage problem — to know which differences matter and which don't. A bearing model learns that seal codes are sometimes noise and sometimes signal. A fuse model learns that amperage is always a hard constraint. A fasteners model learns that grade is load-bearing in structural applications.

This is the PageRank insight applied to enterprise search: **structure in the problem** yields more than a better algorithm on an unstructured problem.

---

## Part III: Building Each Pipeline Layer Right

### Layer 0: The Category Classifier

Start with a learned model, not regex. A small fine-tuned BERT with 50-200 examples per category achieves 95%+ classification accuracy and generalizes to new manufacturer formats automatically. Regex classifiers have the same brittleness problem as the original exact matcher.

For parts that don't confidently classify — genuinely ambiguous formats, multi-category components — a cheap LLM call (Haiku, $0.025/1K) handles the edge cases before routing.

Getting classification right is critical: a misrouted part either misses the correct pool entirely or generates cross-category false positives. The classifier is the gating function for everything downstream. A fuse routed to the bearing index is a fire hazard waiting to happen.

### Layer 1: Verified Data First

The most important architectural principle in this system: **evidence beats inference**.

Production interchange data — matches validated by human experts over years of operation — is 100% accurate by definition. It should be the first thing searched, not the last. The cascade within this layer:

- **Strategy 0**: Exact match (confidence 1.0)
- **Strategy 1**: Interchange database lookup (confidence 0.95)
- **Strategy 2**: Fuzzy normalized match — strip `*`, `+`, `-`, spaces (confidence 0.90)
- **Strategy 3**: Prefix match for truncated part numbers (confidence 0.85)

In production systems built on years of interchange data, this layer covers ~70% of RFQ volume. Seventy percent of the hardest retrieval problem in the building gets solved before any ML model is involved. The certified sausages come first.

### Layer 2: Domain-Specific Semantic Patterns

Before reaching for AI, extract what the domain actually tells you.

Bearing part numbers encode their own identity: `6208-2RS` breaks down as base number `6208` (deep groove ball bearing, 40mm bore, 80mm OD, 18mm width) plus seal code `2RS` (rubber sealed). A `6208-ZZ` (metal shielded) is interchangeable for most applications. A `6208-C3` (extra clearance) may or may not be, depending on application.

```python
def extract_bearing_base(part_number):
    # "6208-2RS" → base="6208", suffix="2RS"
    cleaned = re.sub(r'[\s\-]', '', part_number.upper())
    match = re.match(r'^(6[0-9]{3})', cleaned)
    ...
```

Similarly: sprocket teeth count and bore size. Fuse amperage rating and voltage class. Motor HP and frame code. These are the features that actually determine interchangeability — extractable from part number structure without any ML.

This layer adds ~15% coverage at near-zero computational cost.

### Layer 3: Fine-Tuned Embeddings + Hybrid Search

By the time a part reaches this layer, it's been through verified data and domain pattern extraction. The embedding layer handles genuine semantic uncertainty: parts that are *probably* interchangeable but where no explicit rule applies.

**Model choice**: BGE-M3, fine-tuned on domain-specific interchange pairs. BGE-M3 is no longer the top scorer on general MTEB benchmarks — NV-Embed-v2 and BGE-en-ICL now score higher there — but it remains the strongest practical choice for pipelines that need all three retrieval modes from a single checkpoint: dense vector search, learned sparse retrieval, and late interaction (ColBERT-style). That tri-functional architecture is genuinely distinctive; no widely-adopted alternative provides all three from one model. One model for all three modes simplifies the pipeline considerably. If your pipeline uses only dense retrieval, NV-Embed-v2 or BGE-en-ICL are worth evaluating as alternatives.

The fine-tuning is essential — a general-purpose embedder doesn't know that `6208-2RS` and `62082Z` are semantically adjacent. Training on verified interchange pairs teaches the model the part-number geometry of industrial components. Plan for 5,000–10,000 high-quality query-document pairs for technical nomenclature; domain-specific fine-tuning typically yields +10–30% gains over a general baseline.

The embedding quality is only as good as the training strategy that produced it. That's the subject of Part IV.

**Hybrid search.**

Dense-only search has a known failure mode: it misses exact token matches. Part number `6208-2RS` queried against a catalog containing `SKF-6208-2RS` should be a slam dunk — but the manufacturer prefix can shift the embedding enough to drop the ranking. The fix is **hybrid search**: run sparse and dense retrieval in parallel, then fuse:

```
Query: "6208-2RS"
→ Sparse: [SKF-6208-2RS: rank 1, NSK-6208-2RS: rank 2, ...]  (exact token match)
→ Dense:  [SKF-6208-2Z: rank 1, NSK-6208ZZ: rank 3, ...]     (semantic similarity)
→ Fused:  merge → comprehensive candidate list
```

For the sparse component, **SPLADE** outperforms raw BM25 on technical vocabularies. BM25 operates on raw term frequency; SPLADE learns sparse representations that capture domain expansion — it learns that `2RS` and `2Z` are related seal codes, that `SKF` and `NSK` occupy the same manufacturer neighborhood. BM25 is the right starting point; SPLADE is better once you have fine-tuning data.

For fusion, **RRF (Reciprocal Rank Fusion)** is the zero-configuration default — it operates only on rank position, not raw scores, which makes it robust without normalization tuning. If your system shows variable score distributions between retrievers (common in technical catalogs), **DBSF (Distribution-Based Score Fusion)** normalizes per-query before fusing and can outperform RRF on those cases.

**Scale**: At 14 million products, brute-force FAISS is unusable. Use **HNSW**. Important caveat: naive HNSW degrades significantly under high-selectivity filters. Since every parts query includes a category filter, use **Qdrant's filtered HNSW** — it includes an adaptive query planner that switches to brute-force scan when filters are highly selective, plus ACORN-style graph traversal for multi-filter scenarios. Raw FAISS supports only coarser bitset masking without this adaptive layer, and degrades under high-selectivity filters as a result.

**Reranking — three tiers**:

1. **HNSW + sparse fusion** → top-50 candidates (~5ms)
2. **ColBERT late interaction** → top-50 to top-10. ColBERT encodes query and document independently but computes a fine-grained MaxSim token interaction at rerank time — near cross-encoder accuracy at ~100× fewer FLOPs. The tradeoff: ColBERT stores per-token embeddings for every document, which is 10–100× the storage of single-vector dense retrieval. Budget for it. Usually the right production operating point.
3. **Cross-encoder** → top-5 for safety-critical or low-confidence parts only. Full joint encoding; the highest-accuracy option at the highest cost. Reserve it for cases where the stakes warrant it.

### Layer 4: LLM Validation (Corrective RAG)

A cosine score of 0.87 means "these vectors are close." It doesn't mean "these parts are interchangeable." The LLM layer converts similarity scores into compatibility judgments:

```
Retrieved: {query: "LP-CC-30", match: "KTK-30", similarity: 0.91}

Prompt: "Are these industrial fuses interchangeable?
  Query: LP-CC-30 (Bussmann, 30A, 600VAC, Class CC)
  Match: KTK-30 (Littelfuse, 30A, 600VAC, Class CC)
  Verdict: [INTERCHANGEABLE / NOT_INTERCHANGEABLE / UNCERTAIN]"

→ INTERCHANGEABLE, 0.94, "Identical 30A/600VAC/Class CC — manufacturer difference only"
```

This is the **Corrective RAG** pattern applied to parts matching: a lightweight evaluator assesses whether the retrieved result is good enough before the system commits. If the verdict is UNCERTAIN or the reasoning reveals a spec mismatch, the result doesn't pass forward — it escalates to the agent layer with context attached.

The distinction from simple thresholding is important: a 0.85 score on a fuse query and a 0.85 on a bearing query mean completely different things. The LLM evaluator reasons in context — voltage class, form factor, regulatory certification — in a way that a score threshold cannot.

**For safety-critical categories, the prompt changes:**

```
Prompt: "Are these fuses interchangeable in a safety context?
  Check explicitly:
  • Amperage rating: [match / mismatch]
  • Voltage rating: [match / mismatch]
  • Interrupt rating: [match / mismatch]
  • UL class: [match / mismatch]
  • Response speed: [match / mismatch]
  Verdict: SAFE_INTERCHANGE / UNSAFE / UNCERTAIN"
```

A fuse prompt must ask about regulatory dimensions explicitly. A general "are these interchangeable?" prompt isn't sufficient — the model needs to be directed to check the specific attributes that govern safety compliance.

Cost: Claude Haiku at $0.025/1K validations. On a 200K-item RFQ where 85% is handled by prior layers, ~30K items reach this layer. Under $1 for the entire RFQ.

---

## Part IV: Teaching the Model Which Sausage Is Which

The pipeline is only as good as its model's ability to distinguish the right sausage from the wrong one. That's a training problem.

A fine-tuned model at 84% overall accuracy sounds like progress. But if fuses are at 60% and bearings at 95%, the overall number is hiding a safety problem. The training strategy is what determines where the model's discrimination actually lands — whether it learns the distinctions that matter in the real world, or just produces a neighborhood of similar-smelling sausage.

### The Core Technique: Contrastive Learning with Hard Negatives

Embedding models are trained by showing them pairs of items and teaching them which pairs should be close in the embedding space and which should be far apart.

The obvious approach — train on positive pairs (interchangeable parts) and random negatives (random non-matching parts) — produces a model that gets the easy cases right. The catalog-density problem remains: the model places `6208-2RS` and `6208-C3` close together because they're both bearings, both 6208-series, both from the same family. Random negatives don't include `6208-C3` as a negative example because it's too similar — the training process never draws it.

**Hard negatives** are the fix. A hard negative is a part that *looks* like it should be interchangeable but isn't:

```
Part:          6208-2RS  (deep groove ball bearing, 40mm bore, rubber sealed, standard clearance)

Easy negative: LP-CC-30  (30A Class CC fuse — completely different domain)
Hard negative: 6208-C3   (same base, extra clearance — usually NOT interchangeable)
Hard negative: 6308-2RS  (similar notation, different bore series — wrong bore, won't fit)
Hard negative: 6209-2RS  (adjacent in the series — close in number, different bore)
```

Hard negatives teach the model the distinctions that matter for interchangeability — exactly the discrimination that a general model gets wrong.

### ANCE: The Model Mines Its Own Mistakes

The challenge is finding good hard negatives. Hand-crafting them is expensive and incomplete. **ANCE (Approximate Nearest Neighbor Negative Contrastive Estimation)** solves this automatically: use the *current model's own embeddings* to find the parts it currently gets confused about, then use those as training negatives.

The loop:
1. Embed the catalog with the current model
2. For each positive pair (A, B), find the parts closest to A that are NOT valid interchanges for A
3. Those are your hard negatives for the next training round
4. Retrain, re-embed, repeat

The model progressively learns the distinctions it currently gets wrong. The harder it becomes to confuse it, the harder the negatives it generates for itself. It's self-correcting toward exactly the discriminations that matter in production.

**One caveat**: ANCE's mined negatives can include false positives — parts that are actually valid interchanges but aren't in your labeled interchange database. Research estimates that a significant fraction of ANN-retrieved "negatives" may be true positives misclassified due to labeling gaps. **RocketQA** and **SimANS** address this by using a cross-encoder to filter likely false negatives before training. For production systems where interchange data is incomplete — which is most of them — adding this filtering step is worth the additional complexity.

### Different Categories, Different Hard Negatives

What counts as a dangerous confusion is fundamentally category-specific. You need different hard negative sets — and different positive pair definitions — for each category:

**Bearings**: The base number is the identity; the manufacturer prefix is noise. But suffix codes matter in ways that vary by application:
- `6208-2RS` vs `6208-ZZ`: different seal types, usually interchangeable → *soft positive* (interchangeable in most applications)
- `6208-2RS` vs `6208-C3`: different clearance, usually NOT interchangeable → *hard negative*
- `6208-2RS` vs `6308-2RS`: adjacent series, different bore → *hard negative*
- `SKF-6208-2RS` vs `NSK-6208-2RS`: different manufacturer, identical part → *positive*

**Fasteners**: Grade is load-bearing in structural applications.
- `M8×1.25 Grade 8.8` vs `M8×1.25 Grade 10.9`: same thread, different tensile strength → *hard negative* in structural joints, *soft positive* for non-structural use
- `M8×1.25` vs `M8×1.0`: same diameter, different thread pitch — physically incompatible → *hard negative*
- `M8×1.25 hex head` vs `M8×1.25 socket head`: different head type, same thread → application-dependent

**Motors**: Frame code is the physical mounting standard.
- `5HP NEMA 56C` vs `5HP NEMA 145T`: same power, incompatible mounting → *hard negative*
- `5HP TEFC` vs `5HP ODP`: same power, different enclosure — interchangeable unless environment matters → *soft positive*
- `5HP 1750RPM` vs `5HP 3450RPM`: same power, different speed — almost never interchangeable → *hard negative*

**Fuses**: Every electrical specification is a hard constraint, no exceptions.
- `LP-CC-30 (30A Class CC)` vs `LP-CC-15 (15A Class CC)`: same class, different amperage → *hard negative* (a 15A in a 30A circuit blows immediately)
- `LP-CC-30 (Class CC)` vs `KTK-30 (Class CC)`: different manufacturer, identical spec → *positive*
- `LP-CC-30 (600VAC)` vs `FNM-30 (250VAC)`: different voltage rating → *hard negative*

### Safety Equipment Is Categorically Different

Fuses, circuit breakers, pressure relief valves, safety harnesses, fall protection — these categories follow different training and deployment rules.

**Why**: The cost of a wrong match isn't "annoyed customer." It's a tripped circuit, a burst pipe, a dropped worker. The embedding model doesn't know about regulatory standards: a UL-listed safety harness and a non-UL harness with identical physical dimensions are semantic neighbors. Interchanging them may violate installation codes or void certification.

**Three changes for safety categories:**

1. **Stricter hard negative definitions.** Any spec mismatch is a hard negative. There are no soft positives. The training data should be heavily weighted toward examples that look similar but aren't — because that's the failure mode that injures people.

2. **Higher auto-match threshold.** For commodity fasteners, 0.82 confidence might be acceptable. For fuses and safety equipment, require 0.95+ before auto-matching — and mandate LLM validation regardless of confidence.

3. **Safety-specific validation prompts.** The LLM evaluator must be explicitly directed to check regulatory attributes (amperage, voltage, UL class, interrupt rating, certification standard) — not just asked whether the parts are similar.

### The Training Pipeline

These principles translate into a three-phase training architecture:

**Phase 1: Domain base fine-tuning (shared across all categories)**

Train BGE-M3 on all available interchange pairs, mixed across categories. The goal is domain adaptation: teach the model that part numbers are addresses (not descriptions), that manufacturer prefixes like `SKF-` and `NSK-` are noise, that part-number arithmetic matters. Use **GISTEmbedLoss** with in-batch negatives — it extends the standard Multiple Negatives Ranking loss by using a guide model to score and filter out semantically positive in-batch samples before computing the loss, which addresses the false-negative contamination problem inherent in vanilla MNR. ~10,000 pairs across all categories is enough to start.

**Phase 2: Per-category LoRA adapters**

Fine-tune a lightweight LoRA adapter for each category, starting from the Phase 1 checkpoint. Each adapter trains on category-specific interchange pairs with category-specific hard negatives. LoRA adapters are a few to ~30MB depending on rank and target modules — vs. ~1.1GB for BGE-M3 full weights — so you get per-category specialization without maintaining 11 full models. Use ANCE for hard negative mining in this phase.

```
BGE-M3 base (Phase 1 fine-tuned)
    ├── bearings_lora.adapter   ← learns clearance codes, series distinctions
    ├── fuses_lora.adapter      ← learns electrical spec constraints
    ├── fasteners_lora.adapter  ← learns grade, thread pitch, head type
    ├── motors_lora.adapter     ← learns frame codes, enclosure types
    └── ...
```

The category classifier routes each query to the correct adapter at inference time. The HNSW index for each category was built using embeddings from that category's adapter — ensuring the index geometry matches the query-time embedding geometry.

**Phase 3: Safety-critical specialization**

For fuses, safety equipment, and pressure components: additional fine-tuning on a hard-negative-heavy dataset of "physically similar but electrically/mechanically incompatible" pairs. Increase the margin in the contrastive loss. The goal is to push dangerous near-matches further apart in embedding space — so that a 30A fuse and a 15A fuse land far enough apart that the model is not confused even at high similarity scores.

### Ongoing Learning from Production

Every production outcome is a training signal that compounds over time:

- Accepted match at low confidence → soft positive pair → add to next training cycle
- Customer rejection ("wrong part delivered") → hard negative pair → high-priority training signal
- Safety incident or near-miss → critical hard negative → immediate retraining trigger

Active learning makes the feedback loop explicit: route low-confidence predictions to human review, feed the outcomes back into training. The model continuously learns the distinctions it currently gets wrong. The system gets better the longer it runs — not because the algorithm improves, but because its hard negative coverage expands with every production mistake.

---

## Part V: The Agent Layer — When the Pipeline Isn't Enough

The pipeline handles 85-90% of volume. Fast, parallelizable, cheap. The remaining 10-15% is where the architecture shifts from pipeline to agent.

### What Changes When You Add Agency

A pipeline asks: "did this layer find a match?"

An agent asks: "what do I know so far, what should I try next, and what does the result tell me?"

An agent with the right tools can try a semantic search, see that it returned low confidence, decide to look up the manufacturer first, discover an acquisition renaming, find the superseded part number, and confirm the match — in a single reasoning loop. No pipeline can do this because no pipeline can decide mid-execution to change strategies based on what it found.

This is **Corrective RAG** taken to its logical conclusion. Standard RAG retrieves once and generates. Corrective RAG evaluates whether the retrieved result is good enough and, if not, triggers a different strategy. An agent that can call a full tool palette and reason about *why* a search failed before deciding what to try next is Corrective RAG with real teeth.

### Adaptive Routing: Deciding How Much Work to Do

Before the cascade runs, there's a decision worth making: how hard is this query?

**Adaptive RAG** classifies query complexity upfront:

```
Query complexity classifier
    │
    ├─→ Simple (known format, major manufacturer): Layer 1-2 only → done
    ├─→ Medium (minor mfr, partial info): Full cascade → done or agent
    └─→ Hard (unknown format, OEM code, no description): Agent-first
```

A 200K-item RFQ is not uniformly difficult. Perhaps 40% are commodity parts from major manufacturers — they'll hit in Layer 1 regardless. Running those through the full cascade wastes compute. Part number format is itself a strong signal of difficulty — a classifier that reads the format and routes accordingly saves meaningful latency without sacrificing accuracy.

### The Catalog as a Navigable Artifact

Most catalog deployments are built as flat vector indexes: embed every product description, query with nearest neighbor search. This is correct as far as it goes — Layer 3 of this architecture does exactly that. But the agent layer requires something more intentional: **a catalog you can navigate, not just search**.

The distinction matters. A flat index answers one question: *what's closest to this query?* It cannot answer: *does this manufacturer exist in our catalog? What product families do they make? Has this part number been superseded?* These questions aren't about similarity — they're about structure, provenance, and existence. An agent that can only search fails silently when the right answer is "this manufacturer was acquired and their part numbers changed." An agent that can navigate finds that fact in a single `manufacturer_lookup` call before wasting tool calls searching for something that no longer exists under the original name.

The tool palette below is only possible if you've made an explicit investment in catalog structure:

```
Flat index (what most teams build):
    14M products → embed descriptions → HNSW index
    Agent can ask: "what's close to this query?"

Navigable catalog (what the agent layer requires):
    Manufacturer taxonomy        → catalog_browse works
    Product family hierarchy     → catalog_browse(mfr, family) works
    Per-category spec schemas    → specs_parse works
    Supersession chain data      → supersession_chain works
    Cross-reference tables       → cross_reference works
    Validated interchange groups → interchange_lookup works
```

This is a data engineering investment, not an ML investment — and it compounds. Every supersession chain entry, every manufacturer acquisition record, every cross-reference table you add makes the agent more capable without retraining anything. The ML gets smarter with more training data; the navigation layer gets smarter with structure.

The analogy holds across any structured knowledge system: a well-organized codebase is explorable by directory structure and function signatures before you read a single implementation. An agent exploring a well-structured catalog is qualitatively more capable than one searching a flat index — not because the search algorithm is better, but because it can ask fundamentally different questions before committing to expensive retrieval.

**Practical implication**: before building the agent layer, audit what's navigable in your catalog. Manufacturer and product family taxonomies are usually accessible via the ERP. Supersession data lives in procurement history. Cross-reference tables exist — often as spreadsheets that have never been imported anywhere useful. The bottleneck to a capable agent is rarely the LLM or the retrieval stack. It's whether someone has done the data work to make the catalog structurally explorable.

### The Tool Palette

```
SEARCH TOOLS              (fast — the first moves)
  semantic_search(query, category)
      Dense + sparse BGE-M3, filtered HNSW index, ColBERT rerank
  spec_search(specs_dict)
      Search by parsed specs: {bore: "40mm", type: "deep-groove", seals: "2RS"}
  hyde_search(query)
      Generate hypothetical catalog entry, embed, search — for sparse queries

CATALOG NAVIGATION        (orient before committing)
  catalog_browse(manufacturer?)
      → what manufacturers and product families exist?
  catalog_browse(manufacturer, family)
      → all products in a family
  part_lookup(part_number)
      → full spec sheet for a specific part
  specs_parse(part_number)
      → extract specs encoded in part number structure
  supersession_chain(part_number)
      → follow replacement history forward and back

CROSS-REFERENCE TOOLS     (provenance and history)
  interchange_lookup(part_number)
      → validated interchanges from production history
  cross_reference(part, from_brand, to_brand)
      → manufacturer cross-reference (SKF→NSK, Bussmann→Littelfuse)
  manufacturer_lookup(name)
      → who makes this? acquired by whom? renamed when?
  web_search(query)
      → external research for discontinued or obscure parts

VALIDATION TOOLS          (commit or reject)
  compare_specs(part_a, part_b)
      → are these parts interchangeable?
  compatibility_check(part, application_context)
      → is this safe for the described application?
```

`part_lookup` is cheap — a single record fetch — but gives the agent the full spec sheet: voltage class, mounting dimensions, temperature rating, regulatory certifications. Once the agent has specs for both query and candidate, it reasons directly about compatibility rather than using embedding proximity as a proxy.

`catalog_browse` lets the agent orient before committing to a search. If a manufacturer is unknown, browse first — does it exist in the catalog at all? If a product family is ambiguous, browse the family before fetching individual specs. Cheap navigation saves expensive retrieval.

### How the Loop Works

The agent runs a ReAct loop — Thought, Action, Observation, repeat — and its power comes from changing strategy mid-execution based on what each action reveals. When retrieval returns nothing useful, the agent doesn't rephrase the same query. It reasons about *why* the search failed and picks a structurally different approach.

**Case 1: Confident hit, validated with specs**

```
Query: "LP-CC-30"

Thought: Class CC fuse format. Try semantic search.
Action:  semantic_search("LP-CC-30", category="fuse")
Obs:     [KTK-30: 0.94, FNQ-R-30: 0.91, LPN-RK-30: 0.87] — tight cluster

Thought: Tight cluster — all 30A Class CC candidates. Pull specs on top two to
         verify amperage and voltage match before committing.
Action:  part_lookup("LP-CC-30") + part_lookup("KTK-30")
Obs:     Both: 30A, 600VAC, Class CC, fast-acting. Manufacturer difference only.

Answer:  KTK-30, confidence 0.97, "Identical 30A/600VAC/Class CC profile"
Audit:   [semantic_search → part_lookup × 2] → 3 tool calls, ~150ms
```

Fast, cheap, auditable. And it validated with actual specs rather than trusting the score alone.

**Case 2: Search fails → pivot to provenance**

```
Query: "ACME-7X50-AB" (no description, unknown manufacturer)

Thought: Unknown format. Semantic search first.
Action:  semantic_search("ACME-7X50-AB", category="conveyor")
Obs:     [RXN-7050-AB: 0.71, CNV-7X50: 0.68] — low confidence, different prefix

Thought: Low confidence and the top result has a completely different manufacturer prefix.
         Before trying another search, understand why ACME is unknown.
Action:  manufacturer_lookup("ACME")
Obs:     ACME Power Products — conveyor drives — acquired by Rexnord 2018,
         product line renumbered under RXN- prefix post-acquisition.

Thought: That explains RXN-7050-AB appearing in the original search. Confirm with
         a direct cross-reference.
Action:  cross_reference("ACME-7X50-AB", from_brand="ACME", to_brand="Rexnord")
Obs:     "ACME-7X50-AB superseded by RXN-7050-AB, effective 2018-06"

Thought: Direct supersession confirmed. Validate specs before committing.
Action:  part_lookup("RXN-7050-AB")
Obs:     Rexnord conveyor drive, 7" width, 50mm bore, AB mounting — consistent.

Answer:  RXN-7050-AB, confidence 0.95, "Confirmed supersession: ACME→Rexnord 2018"
Audit:   [semantic_search → manufacturer_lookup → cross_reference → part_lookup]
         → 4 tool calls, ~400ms
```

This case is impossible for any single-pass pipeline. The agent needed to understand *why* the search returned a different prefix before it could find the right angle. No amount of fine-tuning teaches a search index to reason about corporate acquisitions.

**Case 3: Spec disambiguation**

```
Query: "GE30ES-2RS"

Thought: Bearing format. Semantic search.
Action:  semantic_search("GE30ES-2RS", category="bearing")
Obs:     [GE30ES-2RS/SKF: 0.96, GE30TXE-2LS: 0.74, GE40ES-2RS: 0.71]
         Top hit strong but GE40ES is in the candidates — different bore would be wrong.

Thought: Parse the part number to confirm series before committing.
Action:  specs_parse("GE30ES-2RS")
Obs:     Type: spherical plain bearing, bore=30mm, seal=2RS, series=ES

Thought: Spherical plain, 30mm bore. GE40ES is 40mm — wrong bore, eliminated.
Action:  compare_specs("GE30ES-2RS", "GE30ES-2RS/SKF")
Obs:     Identical: spherical plain, 30mm bore, rubber sealed.

Answer:  GE30ES-2RS/SKF, confidence 0.98, "Identical part, manufacturer only"
Audit:   [semantic_search → specs_parse → compare_specs] → 3 tool calls, ~200ms
```

The agent used spec parsing to eliminate a false candidate that was close in embedding space but wrong on a critical dimension. A cosine threshold wouldn't reliably catch this — `0.71` might pass or fail depending on where you set it. The agent caught it because it looked at what the scores meant.

### HyPE and HyDE: Solving Sparse Queries

Some parts are hard at the query layer: OEM part numbers with no description, competitor codes, discontinued parts. The query is too sparse to embed well.

**HyDE (Hypothetical Document Embeddings)**: instead of embedding the sparse query, generate a hypothetical catalog entry that *would* match it, then embed that:

```
Query: "OEM-4719-B" (no description)

Action: hyde_search("OEM-4719-B")
  → LLM generates: "B-section drive belt, 47\" outside circumference, OEM application..."
  → Embed the generated description
  → HNSW finds: [B47: 0.89, 4L470: 0.85, BX47: 0.81]
```

The generated description is semantically richer than the raw part number. The vector index doesn't care it was hypothetical — it retrieves by semantic shape, and "B-section belt, 47-inch" has the right shape.

**HyPE (Hypothetical Prompt Embeddings)** flips the approach: precompute hypothetical queries at index time for each catalog entry, then match real queries against those at search time — zero query-time generation cost. A 2025 study (Vake et al.) found HyPE yielding up to +42 percentage points improvement in retrieval precision across six standard benchmarks. Worth evaluating if you control index construction, since the LLM cost is paid once at index time rather than per query.

One caution on HyDE: it can leak LLM training knowledge into retrieval, inflating recall on common parts but hurting on truly novel or obscure ones. Apply it conditionally — when query confidence is low and the query is genuinely sparse.

### Hardening Against Retrieval Failure

The known failure mode of ReAct agents is getting stuck: retrieval returns nothing useful and the agent keeps rephrasing the same query without improving. This isn't a prompting problem — it requires explicit fallback logic in the orchestration.

A robust agent implements **structured Corrective RAG escalation**:

```
if retrieval_confidence < threshold:
    if manufacturer_unknown:
        → manufacturer_lookup first, then retry
    elif format_unrecognized:
        → specs_parse first, then spec_search
    elif supersession_possible:
        → supersession_chain, then cross_reference
    elif all_structured_tools_exhausted:
        → web_search
    else:
        → escalate to manual review with full research log
```

Each branch is a structured pivot, not a rephrasing. When the agent exhausts all branches, it escalates with everything it learned. The manual reviewer gets a pre-researched part with the full tool call log attached — not a raw part number with no context.

### The Audit Trail Is a Product Feature

A pipeline returns: `KTK-30, confidence 0.94`

An agent returns:
```
Match:      KTK-30
Confidence: 0.97
Reasoning:  "Semantic search returned tight cluster of Class CC fuses.
             Spec validation confirmed identical 30A/600VAC/Class CC ratings.
             Manufacturer difference only (Bussmann → Littelfuse)."
Strategy:   semantic_search → part_lookup × 2
Tool calls: 3 | Latency: ~150ms
```

When a customer disputes a match, you pull the audit log. For safety-critical parts — fuses, pressure relief valves, circuit breakers — the reasoning trace isn't a nice-to-have. It's the documentation that makes the system defensible in a compliance or liability context.

### When to Use Agent vs Pipeline

| Scenario | Right approach |
|---|---|
| 200K-item RFQ, standard catalog parts | Pipeline (400 items/sec, batch) |
| High-value contract, 50 line items | Agent-first (thoroughness > throughput) |
| Pipeline returns low confidence | Corrective RAG escalation to agent |
| Unknown manufacturer or format | Agent (provenance research before search) |
| Safety-critical part | Agent (audit trail required) |
| Discontinued or acquisition-renamed part | Agent (supersession chain) |
| Sparse OEM/competitor codes | Agent with HyDE/HyPE |

A practical deployment runs the pipeline on everything first, routes the low-confidence tail (~10-15%) to the agent, and runs agent-first on high-value contracts where every line matters.

---

## Part VI: The Full Architecture

```
RFQ Input (50–200,000 items)
    │
    ▼
┌────────────────────────────────────────────────────────────────┐
│ ADAPTIVE COMPLEXITY ROUTER                                      │
│ Simple (known format, major mfr) → Layer 1 direct              │
│ Medium (minor mfr, partial info) → full cascade                │
│ Hard (unknown format, OEM code)  → Agent-first                 │
└────────────────────────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────────────────────────┐
│ CATEGORY CLASSIFIER                                             │
│ Fine-tuned BERT (~0.1ms, 95%+ accuracy)                        │
│ + LLM fallback for ambiguous parts (Haiku, $0.025/K)           │
│ Routes to: bearing / sprocket / fuse / motor / belt /          │
│           valve / chain / seal / hydraulic / pneumatic /       │
│           fastener                                             │
└────────────────────────────────────────────────────────────────┘
    │ (per-category, parallelized)
    ▼
┌────────────────────────────────────────────────────────┐
│ LAYER 1: VERIFIED DATA                  ~70% coverage   │
│ Exact (1.0) → interchange DB (0.95) →                   │
│ fuzzy normalized (0.90) → prefix (0.85)                 │
└────────────────────────────────────────────────────────┘
    │ miss
    ▼
┌────────────────────────────────────────────────────────┐
│ LAYER 2: DOMAIN SEMANTIC PATTERNS       +15% coverage   │
│ Bearings: base number + seal code                       │
│ Sprockets: teeth count + bore size                      │
│ Fuses: amperage + voltage + class                       │
│ Motors: HP + frame + RPM                                │
└────────────────────────────────────────────────────────┘
    │ miss
    ▼
┌────────────────────────────────────────────────────────┐
│ LAYER 3: HYBRID SEARCH + RERANKER       +8-15% coverage │
│ BGE-M3 + category LoRA adapter                         │
│ SPLADE sparse + dense HNSW → RRF fusion                 │
│ Qdrant filtered HNSW (per-category index)               │
│ ColBERT rerank top-50 → top-10                          │
│ Cross-encoder top-5 (safety-critical only)              │
└────────────────────────────────────────────────────────┘
    │ low confidence
    ▼
┌────────────────────────────────────────────────────────┐
│ LAYER 4: LLM VALIDATION (Corrective RAG)                │
│ Category-specific compatibility prompt                  │
│ Safety categories: explicit regulatory attribute check  │
│ Accept / Reject / Uncertain + reasoning                 │
│ Cost: ~$0.75 per 200K RFQ                               │
│ Uncertain → escalate to agent with context              │
└────────────────────────────────────────────────────────┘
    │ uncertain or miss
    ▼
┌────────────────────────────────────────────────────────────────┐
│ LAYER 5: AGENTIC RESEARCH (Corrective + Adaptive RAG)          │
│                                                                 │
│ SEARCH:    semantic_search · spec_search · hyde_search          │
│ NAVIGATE:  catalog_browse · part_lookup · specs_parse          │
│            supersession_chain                                  │
│ CROSS-REF: interchange_lookup · cross_reference                │
│            manufacturer_lookup · web_search                    │
│ VALIDATE:  compare_specs · compatibility_check                 │
│                                                                 │
│ ReAct loop with explicit structured escalation branches        │
│ Full audit trail on every tool call                            │
│ Agent-first for safety-critical and high-value contracts       │
│ Cost: $0.50-2.00 per part                                      │
└────────────────────────────────────────────────────────────────┘
    │ all strategies exhausted
    ▼
Manual Review Queue — agent's research log attached (target: <5%)
```

**Expected performance:**

| Layer | Coverage | Confidence | Latency |
|---|---|---|---|
| Verified data | ~70% | 0.90–1.00 | <1ms |
| Domain patterns | +15% | 0.80–0.90 | 1–5ms |
| Hybrid search + rerank | +8-15% | 0.75–0.90 | 5–25ms |
| LLM validation (Corrective RAG) | gates above | calibrated | +50ms |
| Agentic research | +3-8% | 0.75–0.95 | 0.5–30 sec |
| **Total auto-match** | **~85-95%** | — | — |
| **200K RFQ batch** | — | — | **~8-12 min** |

---

## Part VII: The Business Case

**The cost of the status quo.** A 200K-item RFQ at 70% auto-match leaves 60,000 lines requiring manual lookup. At 3–5 minutes per line — finding the part, confirming the match, pricing — that's 3,000–5,000 analyst-hours per RFQ. At a fully-loaded cost of $40–60/hour, that's $120K–$300K in labor per large RFQ, before accounting for opportunity cost. More importantly: those analysts can only process so many lines per day. A two-week turnaround is the industry norm. Customers notice. Speed of response is a competitive differentiator at this scale — a distributor that quotes in two days wins business that a two-week distributor never sees.

**What 85-90% auto-match actually means.** Moving from 70% to 85-90% reduces the manual review queue from 60,000 to 20,000 lines — a 67% reduction in analyst time for that tail. The lines that remain get pre-researched agent logs attached, reducing per-line review time further. At scale, the increment from 70% to 85-90% is worth roughly 30-40% of the original system's savings — before accounting for improved match confidence, auditability, and response speed.

**The AI cost is negligible relative to the value.** On a 200K-item RFQ:
- LLM validation (Haiku): ~$0.75
- HyDE expansion: ~$1.50
- Agentic research (10-15% of parts, Sonnet): ~$200-500
- Total: **under $500 per RFQ**

Against $120K–$300K in labor cost per RFQ, the operational AI cost is approximately 0.2–0.4% of the value it creates.

**Realistic build timeline.** A focused team of 3–4 engineers — one data engineer for interchange data extraction and catalog structure, two ML engineers for fine-tuning and pipeline, one infra engineer for serving — can reach Layer 1–3 production coverage in 8 weeks and a full agentic layer by Month 4. The bottleneck is almost always data access: getting interchange history out of legacy ERP systems and into a training-ready format takes longer than the ML work. Budget for it.

**The cost of wrong matches is asymmetric.** A 30-amp fuse returned instead of the correct fuse is a safety incident — potential liability, potential injury. The category-first architecture prevents cross-category errors at the routing layer, not by improving model accuracy on an unsafe baseline but by making the mistake structurally impossible. The category-specific training ensures the model can distinguish dangerous near-matches within a category. The LLM validation layer rejects matches where the reasoning produces uncertainty. The agent's audit trail makes every decision traceable.

The architecture is not just more accurate. It's more defensible.

**The competitive risk of waiting.** For early movers, the systems they're building today create a compounding advantage: every accepted match becomes a training pair, every production rejection a hard negative. The model gets better the longer it runs. A competitor who starts this work two years from now won't just be two years behind — they'll be millions of training examples behind, with a knowledge base of interchange data they haven't accumulated. Data moats in this domain are real and they widen over time.

---

## Part VIII: Principles for Building RFQ Systems

These emerged from building and rebuilding production systems. Most generalize beyond RFQ to any high-stakes enterprise retrieval problem.

### 1. Structure before embeddings

Before reaching for a model, ask: does the problem have structure you can exploit? In industrial parts matching, category structure reduces the search space 14×. In legal document retrieval, jurisdiction and document type are analogous separators. The structure is usually there — the monolithic approach just ignores it.

### 2. Evidence before inference

Verified interchange data — matches confirmed by humans over years of production use — is more reliable than any model. Put it first in the cascade. Let the model handle only what the evidence layer can't. The model's job is to extend the system's reach, not replace its foundation.

### 3. Semantic search is a discovery tool, not a substitution tool

"Hot + dog ≈ sausage" is the feature of semantic search in consumer applications. In parts matching, it's the problem. Every category has a neighborhood of semantically-similar parts that are physically incompatible. The architecture exists to answer the substitution question — "is this candidate certified interchangeable?" — not just the similarity question.

### 4. Hard negatives are the training investment that pays off

A model trained on random negatives produces a neighborhood of similar-smelling sausage. A model trained with category-specific hard negatives — parts that look substitutable but aren't — learns to discriminate where discrimination matters. ANCE automates hard negative mining from the model's own current confusion. This is where the accuracy gains come from.

### 5. Safety-critical categories need their own rules

Fuses, circuit breakers, pressure relief valves, safety equipment — these follow different training, validation, and deployment rules. Stricter hard negatives. Higher auto-match thresholds. Category-specific LLM prompts that explicitly check regulatory attributes. The architecture that works for commodity bearings is insufficient for electrical safety components.

### 6. Confidence requires provenance

A confidence score without provenance is noise. "0.87 similarity" is meaningless. "Interchange database, validated interchange group, confirmed by 12 production transactions" is a confidence score. "Spec validation: 30A ✓, 600VAC ✓, Class CC ✓, manufacturer only difference" is a confidence score. Design your system to know *why* it's confident, not just *that* it's confident.

### 7. Hybrid search beats pure dense

For short, specific queries — part numbers, product codes, SKUs — sparse token matching outperforms dense-only embedding search. The two are complementary: dense captures semantic generalization, sparse captures exact token matches. Always hybrid. RRF as the zero-config default; SPLADE over raw BM25 once you have fine-tuning data.

### 8. Classify complexity before you retrieve

Not all queries need the full pipeline. A complexity classifier that routes easy parts directly to verified data saves meaningful compute. Adaptive RAG applied to parts matching: the format of a part number is itself a signal about how hard the query will be.

### 9. LLMs validate; agents investigate; indexes retrieve

Each component does what it's actually good at. Fast bi-encoders for candidate generation at scale. ColBERT for efficient reranking. LLMs for reasoning about retrieved candidates (Corrective RAG). Agents for multi-step investigation when the answer isn't in a single search — especially when you need to understand *why* a search failed before trying a different angle.

### 10. The data blocker is real

A world-class retrieval architecture covering only bearings — the highest-volume category at roughly 20-25% of typical RFQ volume — achieves at best a 25% match rate on the full RFQ. A mediocre architecture covering all 11 categories achieves 70%. Data coverage beats algorithmic sophistication, every time. The good news: production interchange data — years of validated interchange pairs — is a FAISS index waiting to be built and a hard-negative training set waiting to be mined.

### 11. Build the catalog as a navigable artifact, not just a searchable index

A flat vector index can only answer "what's closest to this query?" An agent needs to ask "does this manufacturer exist in the catalog?", "has this part been superseded?", "what's the full spec sheet for this candidate?" — questions about structure and provenance that nearest-neighbor search can't answer. The navigation tools that make agents powerful (catalog browse, supersession chain, cross-reference lookup) require intentional data investment: manufacturer taxonomies, product family hierarchies, cross-reference tables, supersession records. This work is unglamorous and precedes the ML work by months. It also compounds without bound: every new supersession chain entry, every acquisition record, every imported cross-reference table makes the agent more capable without any retraining.

### 12. The audit trail is part of the product

In safety-critical or high-value applications, the reasoning trace — every tool call, every observation, every decision — is a deliverable alongside the match result. Design the agent to produce it from the start. Customers, procurement officers, and regulators want to know not just *what* the system matched, but *why*.

---

## Part IX: What This Looks Like to an Engineering Team Starting Today

**Week 1–2: Foundation**
- Extract and normalize your existing match history into interchange groups
- Stand up PostgreSQL with verified interchange data
- Implement exact/fuzzy/prefix cascade (Layer 1)
- Build category classifier — fine-tuned BERT if you have 50+ examples per category, regex if you don't yet
- Measure baseline: what % does the verified layer cover?
- **Begin catalog structure work** — this is unglamorous data engineering that must start now to be ready in Month 3:
  - Import manufacturer taxonomy and product family hierarchy from ERP
  - Gather supersession data from procurement history
  - Locate cross-reference spreadsheets and get them into a database
  - Document known acquisition/renaming events for major manufacturers

**Week 3–4: Hybrid search**
- Fine-tune BGE-M3 on your interchange pairs with basic hard negatives (4,000 pairs is enough to start)
- Build Qdrant filtered HNSW index per category
- Add SPLADE sparse retrieval with RRF fusion
- Measure: how much does hybrid beat dense-only?

**Week 5–6: Reranking + LLM validation**
- Add ColBERT reranker on top-50 candidates
- Add cross-encoder for safety-critical categories
- Add Haiku validation for matches in the 0.70-0.90 band, with category-specific prompts
- Build per-category reporting (fill rate, accuracy by category)

**Week 7–8: Hard negative mining + coverage expansion**
- Run ANCE: embed your catalog with the current model, mine hard negatives
- Retrain category LoRA adapters on hard-negative-enriched data
- Identify weakest categories via per-category reporting
- Acquire or generate training data for the bottom categories

**Month 3+: Agentic layer + production hardening**
- Stand up tool palette: catalog navigation, manufacturer lookup, cross-reference, supersession chain
- Implement ReAct loop with Sonnet for the low-confidence tail
- Wire up HyDE/HyPE for sparse queries
- Build audit trail logging from the start
- Route high-value contracts to agent-first mode
- Feedback loop: accept/reject outcomes from production feed back into ANCE hard negative mining
- Production deployment: FastAPI, Celery batch, Prometheus monitoring

### Building Your Evaluation Set

Before the Week 3-4 accuracy numbers mean anything, you need a trustworthy eval set. This is harder than it sounds and most teams get it wrong.

**The sampling trap**: if you sample your eval set from historical auto-matched parts, you're evaluating on what your current system already handles well. Accuracy looks excellent. The system is silently failing on everything it escalates to manual review — which is exactly the population you need to improve. That's not an eval set; it's a self-congratulation set.

**What a good eval set looks like:**

- **Verified interchange positives**: random sample of confirmed-good matches across all categories. Ground truth.
- **Production rejections**: parts your system matched and customers rejected. The model was confident and wrong. These are your most valuable examples.
- **Manual review history**: parts that reached human review, with reviewer decisions. Your current knowledge boundary.
- **Seeded adversarials**: for each category, include your known hard negative patterns explicitly (6208-C3 as a negative when querying 6208-2RS; 15A fuse when 30A is the query). If you don't seed these, your eval set won't surface the failure modes that actually matter.
- **Category balance**: ensure at least 200 examples per category. An eval set that's 80% bearings will mask failures everywhere else.

**What to measure**: fill rate (% matched at each confidence tier), precision per tier (of auto-matched parts, how many were correct), and both broken down per category. A system with 90% overall precision but 60% fuse precision is a safety problem, not a success. The per-category breakdown is the metric that drives decisions.

**Production monitoring**: offline eval tells you how you're doing on historical data. Production monitoring tells you how you're doing *now*. Track customer rejection rate per category, escalation rate per category, and agent tool call count distribution (spikes signal new hard patterns emerging). Alert on week-over-week changes of more than 2 percentage points in any category — that's the signal that something in the catalog or the query distribution has shifted.

---

## Part X: What Will Break in Production

The architecture described in this article works. These are the things that will hurt you anyway — not because the design is flawed, but because production environments are dynamic and every system eventually encounters conditions the lab didn't anticipate. Build for these from the start.

### Catalog Drift

Your catalog changes constantly: new manufacturers added, parts discontinued, product lines renumbered, OEM relationships established. Each change degrades the system in ways that don't announce themselves. The HNSW index becomes stale — new parts aren't indexed, superseded parts still return as top hits. Interchange data ages — a valid interchange in 2022 may not be in 2026 if a manufacturer changed a spec.

**Signs**: fill rate gradually declining on categories where it was previously stable; manual review queue growing without obvious cause; customer complaints concentrated on recently-added manufacturers.

**Fix**: index freshness monitoring (track stale vs. current embeddings per category); automated re-indexing on catalog update events; supersession record validation as part of interchange data maintenance. Treat catalog updates as deployment events, not background jobs.

### Category Classifier Degradation

The classifier was trained on your historical part number formats. New manufacturers, OEM relationships, and market consolidation introduce formats it hasn't seen. A new supplier with an unfamiliar format gets misclassified — routed to the wrong category index, returning high-confidence wrong results that look correct until a customer rejects the shipment.

This is more dangerous than low confidence. A misclassified part that finds a plausible hit in the wrong category produces a *confident wrong answer*.

**Signs**: per-category fill rate is stable but overall wrong-match rate rising; customer rejections concentrated on recently-added manufacturers or product lines.

**Fix**: monitor classifier confidence distribution by manufacturer; route anything below the confidence threshold to the LLM fallback rather than taking the argmax; add misclassified examples to classifier training data within days, not quarters.

### Confidence Score Miscalibration

After catalog updates, large interchange data additions, or retraining events, score distributions shift. Thresholds calibrated at 0.82 for auto-accept may now correspond to a lower actual accuracy level. The system continues auto-accepting at 0.82 but the true precision at that threshold has dropped.

**Signs**: auto-match rate is stable but manual review team reports elevated error rate on escalated parts; customer rejection rate creeping up without obvious cause.

**Fix**: hold out a calibration set from each training cycle and re-run threshold calibration after every retraining event. Monitor precision per confidence band per category — not just overall accuracy. A score threshold is a bet on a distribution; when the distribution shifts, the bet changes.

### Hard Negative Coverage Gaps

ANCE mines hard negatives from the model's current confusion — it finds what the *current model* gets wrong. As the catalog grows, new hard negative cases emerge that training hasn't encountered. Parts that were rare when the model was trained become common in customer RFQs. The model stays confident on these cases because it has never been trained to be uncertain about them.

**Signs**: newly-onboarded product categories show lower accuracy than established ones; specific sub-families have high auto-match rate but elevated customer rejection rate.

**Fix**: run ANCE continuously on a rolling basis rather than as a batch step; weight hard negative mining toward recently-added catalog entries; treat every customer rejection as an immediate ANCE seed for the next training cycle.

### Agent Loop Instability

Agents get stuck. The structured escalation branches in Part V prevent most infinite loops, but novel failure patterns emerge in production: a `manufacturer_lookup` that returns ambiguous results (two companies named "ACME"); a supersession chain that loops (A superseded by B, B superseded by A — a real occurrence in some interchange databases); a `web_search` that returns authoritative-looking but wrong information.

**Signs**: agent latency spikes on specific part formats; manual review queue accumulating parts with very long tool call logs and no answer.

**Fix**: hard cap on tool calls per part (15–20 is usually sufficient); detect supersession loops explicitly and escalate immediately; log every case where `web_search` is the last resort and audit them manually each week; never auto-accept a web_search result — route to human validation with the full research log attached.

### The Measurement Blindspot

The most insidious failure mode isn't operational — it's measurement. If your offline test set is sampled only from historical successful matches, it's biased toward parts your current system already handles. Accuracy metrics look stable while the system silently fails on the long tail. This is why the eval methodology in Part IX matters: if your test set doesn't include production rejections and manual review cases, your accuracy numbers are telling you a story about your best-case performance, not your actual performance.

**Fix**: actively maintain the hard-case portion of your eval set. Every batch of production rejections is new ground truth. Treat eval set maintenance as a first-class engineering task, not a one-time setup step.

---

## Coda: Why This Problem Matters

Every supply chain runs on RFQs. Every distributor, every manufacturer, every procurement operation has a version of the matching problem. The vocabulary is different — SKUs, BOMs, catalog IDs, part numbers — but the structure is the same: a short query against a large catalog, domain-specific semantics, high cost of error, massive throughput requirements.

Semantic search taught machines that "hot + dog ≈ sausage." That's remarkable, and it's genuinely useful. But a catalog of 14 million industrial parts is a catalog of 14 million sausages, and most of them are wrong for any given application. The too-many-sausages problem is the core challenge of RFQ matching — and the architecture in this article is a systematic answer to it.

The architecture answers the too-many-sausages problem at each layer: category routing narrows the pool before any model runs; verified data serves only certified matches; hard-negative training teaches each model the dangerous near-misses in its own domain; agents investigate what the pipeline couldn't resolve, with a full audit trail attached.

What's changed in 2026 is not that these techniques exist. BM25 has been around since the 1970s. BERT fine-tuning since 2018. FAISS since 2019. Contrastive learning since before that. ReAct agents since 2022. What's changed is that all of it is commodity infrastructure — and the research literature has given names (Corrective RAG, Adaptive RAG, Agentic RAG, ANCE, HyDE) to patterns that practitioners have been building toward for years.

A small fraction of procurement operations have deployed AI matching at scale — industry surveys put the figure in the low single digits. That number says more about the difficulty of the organizational and data problems than the technology. The technology is ready. The architecture is understood. The main remaining work is the disciplined accumulation of verified interchange data, category-specific hard negative mining, and the engineering to make all of it run reliably at production volume.

That work is tractable. And the systems it produces are, by any honest measure, a different category of thing than what came before.

---

*Written in sessions lingering-ice-0322, mountain-whirlwind-0322, oceanic-sea-0322, and expanding-meteorite-0322 | March 2026*
*See also: [From Filing Cabinets to Agentic Minds](/articles/information-retrieval-history-and-agentic-future) — a companion overview of how IR evolved from inverted indexes to RAG to agentic systems*
