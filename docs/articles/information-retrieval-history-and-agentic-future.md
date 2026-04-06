---
title: "From Filing Cabinets to Agentic Minds"
subtitle: "The long arc of information retrieval — from Luhn's inverted index to agentic systems that reason about what they find"
author: "Scott Senkeresty"
date: "2026-03-22"
type: "article"
status: "published"
linkedin_posted: true
audience: "developers, AI practitioners, technical leaders"
reading_time: "12 minutes"
canonical_url: "https://semanticinfrastructurelab.org/articles/information-retrieval-history-and-agentic-future"
topics: [information-retrieval, semantic-search, rag, agentic-ai, embeddings, search, history]
beth_topics:
  - sil
  - information-retrieval
  - semantic-search
  - rag
  - agentic-ai
  - beth
  - search
  - embeddings
---

# From Filing Cabinets to Agentic Minds: The Long Arc of Information Retrieval

*How humanity learned to find what it knows — and what comes next*

---

## The Problem Is as Old as Writing

The moment humans began accumulating more knowledge than any one person could hold, they had an information retrieval problem. Ancient Mesopotamian scribes organized clay tablets by topic. The Library of Alexandria had cataloguers. Medieval monasteries developed cross-reference systems. The Dewey Decimal Classification was invented in 1876 — a brilliant attempt to impose a universal tree structure on all human knowledge.

The tree structure was the foundational mental model: everything has one canonical home. You navigate to it. If you know the taxonomy, you find the thing.

It worked reasonably well — until the taxonomy decayed, things belonged in multiple places at once, and classifiers disagreed. The deeper problem: **the tree assumes knowledge is stable and classifiable in advance**. Reality is neither.

When computers arrived, we brought the tree model with us. Directories. File systems. EDGAR filing categories. Oracle schemas. For decades, digital information organization was essentially Dewey Decimal with faster lookups.

Then Hans Peter Luhn changed the game.

---

## The Inverted Index: The Insight That Built Modern Search

In 1957, IBM researcher Hans Peter Luhn published "A Statistical Approach to Mechanized Encoding and Searching of Literary Information." His key insight: **you don't need to classify documents by topic — you can index the words inside them**.

Luhn proposed treating text as a statistical distribution of terms. Words that appeared frequently within a document, but rarely across the corpus as a whole, were diagnostically significant. This was the intellectual seed that would eventually become TF-IDF.

The mechanism that made it practical was the **inverted index** — a data structure that inverts the natural document-centric view:

```
Instead of:  doc_17 → [contains: "oauth", "authentication", "bearer", ...]
Build:        "authentication" → [doc_3, doc_17, doc_42, ...]
              "oauth"          → [doc_17, doc_89, ...]
```

The inverted index made term lookup O(1) instead of O(n). Rather than scanning every document for a matching word, you look up the word and get the list of documents containing it. At the scale of the early web — billions of pages — this wasn't an engineering optimization. It was the precondition for search existing at all.

Gerard Salton, working at Harvard and Cornell through the 1960s–1980s, formalized this into the **Vector Space Model**: represent both documents and queries as vectors in a high-dimensional term space, measure relevance by cosine similarity. His SMART system was one of the first complete experimental information retrieval systems, and the Vector Space Model remains conceptually active fifty years later.

In 1972, Karen Spärck Jones added the other half of the equation. She published "A statistical interpretation of term specificity and its application in retrieval" — introducing **Inverse Document Frequency (IDF)**. A word appearing in 90% of documents (like "the") is useless for retrieval. A word appearing in 0.1% of documents (like "eigenvalue") is highly diagnostic. The specificity of a term is an inverse function of how many documents contain it.

Combined with term frequency, this became **TF-IDF**: the workhorse of information retrieval for the next three decades, and still the baseline most new systems are benchmarked against.

Later refinements — most notably **Okapi BM25**, developed by Stephen Robertson and Spärck Jones through the 1970s–90s — added term frequency saturation (diminishing returns for repeated words) and document length normalization. BM25 remains the dominant sparse retrieval baseline in production systems today, **forty years after its invention**.

**Beth** — SIL's document discovery index, built over 14,000+ files across projects — is a direct descendant of this lineage. Topic tags in document front matter, term weighting, and the index-first architecture all trace back to Luhn and Spärck Jones.

---

## PageRank: When Links Became Votes

The inverted index solves retrieval. It doesn't solve *ranking*.

If 10,000 documents contain the word "authentication," how do you decide which ones to show first? Early search engines used TF-IDF signals, document length, and metadata. Then Larry Page and Sergey Brin proposed **PageRank** in 1998: rank documents by the graph authority of the links pointing to them.

The key insight was that a hyperlink is an implicit endorsement. If a highly-linked document links to your document, that's a stronger signal than if a nobody links to you. Authority propagates through the graph.

This was a profound epistemological shift: **relevance as a social consensus, not just a linguistic match**. The web's link structure was a massively distributed voting system, and PageRank was how you counted the votes. It worked extraordinarily well — because it was hard to fake. You couldn't easily manufacture thousands of authoritative links.

Google's dominance for twenty years was built on this: a combination of BM25-style lexical matching (does this document contain the right words?) with PageRank-style graph authority (does the web think this document matters?).

Beth uses cross-links as an authority signal in exactly this way. Widely-linked docs rise organically — not through explicit weight annotations, but because other documents point to them. The design is explicit PageRank thinking applied to a private knowledge base.

---

## The Semantic Revolution: From Words to Meaning

Keyword search has a fundamental limitation. A query for "how do I log in?" doesn't match a document that explains "OAuth 2.0 authentication flow" — even though that document likely answers the question. Synonyms, paraphrases, domain jargon: the lexical gap between how people ask and how experts write is enormous.

The first serious crack in this problem came in 2013.

**Word2Vec** (Mikolov et al., Google) trained neural networks to predict words from their context, producing dense 300-dimensional vectors for every word. The emergent property was stunning: arithmetic worked on meaning.

```
vector("king") − vector("man") + vector("woman") ≈ vector("queen")
vector("Paris") − vector("France") + vector("Germany") ≈ vector("Berlin")
```

Words with similar meanings clustered in the vector space. You could compute semantic similarity as a distance metric. For the first time, "authentication" and "login" were *close* in a machine-representable sense — not because someone said so, but because they appeared in similar contexts across billions of words of text.

But Word2Vec had a critical limitation: **static representations**. Every word got one vector, regardless of context. "Bank" — financial institution or river bank — had the same vector always.

**BERT** (Devlin et al., Google, 2018) fixed this with bidirectional transformers. Now every word's representation depended on every other word in the sentence. Context-sensitive, deeply relational, genuinely semantic. The representation of "bank" in "I deposited money at the bank" differs from "bank" in "we sat on the river bank."

**Sentence-BERT** (Reimers & Gurevych, 2019) made it practical. A cross-encoder BERT comparing 10,000 sentence pairs took *65 hours*. SBERT, using a siamese network to produce fixed-size sentence embeddings, did it in *5 seconds* — a 47,000× speedup. Dense semantic retrieval at scale became feasible overnight.

**Dense Passage Retrieval** (Karpukhin et al., Facebook AI, 2020) brought this to IR proper: separate BERT encoders for queries and passages, both projecting into a shared vector space, similarity via dot product, approximate nearest-neighbor (ANN) search for speed at scale. On open-domain QA benchmarks, it outperformed strong BM25 baselines by 9–19% absolute on top-20 retrieval accuracy.

The vector database industry was born: Pinecone, Weaviate, Chroma, Qdrant, pgvector. Every major cloud provider now offers managed vector search. Embedding dimensionality arc: 100-dimensional Word2Vec in 2013 → 768-dimensional BERT in 2018 → 4,096-dimensional models with 128K context windows by 2026.

**Semantic search changed the world** not by replacing keyword search, but by addressing its fundamental blind spot. The question "does this document contain these words?" became "is this document semantically relevant to this query?" — a qualitatively different operation.

---

## RAG: Connecting LLMs to External Knowledge

Language models know a lot. They also have a hard cutoff date, no citations, no access to private knowledge, and a tendency to hallucinate when pushed past what they know. The question became: how do you give an LLM access to a corpus of documents it wasn't trained on?

The answer, formalized in the original RAG paper (Lewis et al., Meta AI, NeurIPS 2020), is conceptually simple:

```
Query
  → embed query
  → ANN search corpus
  → retrieve top-K chunks
  → inject chunks into LLM context
  → LLM synthesizes answer from retrieved text
```

RAG converts the retrieval problem into a **context injection problem**. The LLM doesn't "know" your documents — it reads retrieved excerpts at inference time. No fine-tuning required. The knowledge base is separate from the model and can be updated independently.

The original paper combined DPR retrieval with a sequence-to-sequence language model. It set state-of-the-art on multiple open-domain QA benchmarks and described the generated language as "more specific, diverse, and factual" than parameter-only models. It launched an industry.

By 2024, over **1,200 RAG-related papers appeared on arXiv** — compared to fewer than 100 the year before. 12× growth in one year.

### Where RAG Breaks

Naive RAG is fragile. The failure modes are predictable and well-documented:

**Chunking is brutal.** Documents are split at fixed token boundaries — 256 or 512 tokens, wherever a paragraph falls. A passage that requires context from three pages earlier to be understood is retrieved without that context. The semantic coherence of the original document is destroyed.

**Retrieval failure is silent.** If the top-K chunks don't contain the relevant information, the LLM doesn't know that. It synthesizes from what it has — often producing plausible, fluent, confident hallucination. The system has no mechanism to say "I didn't find anything useful."

**Embedding ≠ relevance.** Semantic similarity is not the same as "answers this question." A document titled "Why OAuth Can Fail" might embed close to "How does OAuth work?" but the former is about failure modes and the latter wants a tutorial. Vector distance captures topic, not intent.

**Multi-hop reasoning.** Complex questions require chaining evidence across multiple documents. Naive RAG retrieves once; if the answer requires combining information from three separate sources, a single retrieval pass can't capture it.

**Adversarial context.** If retrieved documents contain wrong information, the LLM often reproduces it confidently. Attackers can inject manipulated documents into a corpus to systematically bias outputs.

Advanced RAG addressed some of these with query rewriting, reranking, context compression, and iterative refinement. But the deeper architectural limitations remained.

---

## Agentic AI: When Retrieval Becomes Reasoning

The shift from RAG to agentic retrieval is a shift from **pipeline** to **loop**. Instead of retrieve-once-then-generate, the system can reason about what it found, decide it's insufficient, and try again.

### MRKL and ReAct: The Foundational Papers

**MRKL Systems** (Karpas et al., AI21 Labs, 2022) established the conceptual architecture: an LLM router plus a set of discrete modules — calculator, search API, database, weather service. The LLM interprets the intent and dispatches to the appropriate tool. Simple, but it made retrieval a *decision* rather than a fixed pipeline step.

**ReAct** (Yao et al., Google Brain, 2022/ICLR 2023) was the key advance. The LLM interleaves **Thought** (chain-of-thought reasoning), **Action** (tool call, e.g. Wikipedia lookup), and **Observation** (what came back), in iterative cycles:

```
Thought: I need to find when the Eiffel Tower was built
Action: Search[Eiffel Tower construction date]
Observation: The Eiffel Tower was built between 1887 and 1889
Thought: Now I can answer the question
Answer: 1889
```

The reasoning trace isn't just for explanation — it actively updates the plan. Each observation can change what the agent searches for next. Retrieval becomes a *conversation with the corpus*.

### The Techniques That Make It Work

**HyDE (Hypothetical Document Embeddings)** addresses the cold-start problem: a short query embeds poorly because it's sparse. Instead, prompt the LLM to generate a hypothetical document that *would* answer the query, then embed that. The resulting embedding is much richer, and the dense encoder's bottleneck filters out hallucinations — only the semantic gist reaches retrieval. On zero-shot benchmarks, HyDE approaches the quality of fine-tuned retrievers.

**FLARE (Forward-Looking Active Retrieval)** addresses the timing problem: when should retrieval happen? FLARE generates tentatively, monitors the model's confidence in what it's generating, and triggers retrieval when that confidence drops — using its own tentative output as the query. Retrieval happens *when and where* it's needed, not once at the start.

**Self-RAG** adds a critique loop: the model reflects on whether retrieval was even needed, and whether its output is grounded in what was retrieved. It can reject its own answers and regenerate with different context.

### The Five Capabilities That Change Everything

Taken together, these techniques unlock five capabilities that classic RAG fundamentally cannot have:

**1. Iterative query refinement.** The agent uses first-pass results to reformulate. If "authentication best practices" returns generic content, the agent notices and searches for "OAuth 2.0 refresh token rotation." Humans do this constantly. Classic RAG cannot.

**2. Multi-strategy fusion.** An agent can run semantic search, BM25 keyword search, structured database queries, and API calls in parallel, then synthesize across all of them. Different strategies surface different evidence; the agent decides which to trust.

**3. Multi-hop reasoning.** A complex question — "What's the current best practice for handling expired OAuth tokens in a microservices architecture?" — requires chaining across multiple documents. The agent can retrieve, read, identify a gap, retrieve again from a different angle, and build up an answer incrementally.

**4. Source verification and triangulation.** Rather than trusting retrieved chunks, an agent can read the full source, follow links, check cross-references, and notice when two retrieved documents contradict each other. It can go upstream to resolve the conflict rather than synthesizing over a contradiction it doesn't know exists.

**5. The query as a task.** The deepest change: instead of query → retrieve → answer, you have task → decompose → research plan → parallel retrieval → synthesis → verify → iterate. Retrieval is no longer the operation — it's a sub-operation within a reasoning process. The unit of work is a goal, not a question.

---

## The Architectural Tension at the Center

This evolution surfaces a genuine architectural question that doesn't have a settled answer:

> **How much should live in the index, and how much in the agent?**

The classical bet was: pay the indexing cost upfront (crawl, chunk, embed, weight, cross-link), answer queries cheaply (millisecond ANN search). This works well when the query distribution is predictable and the corpus is stable.

Agentic retrieval shifts the calculus: if the agent can reason at query time — read docs, follow links, cross-check, reformulate — you need *less* perfect indexing. The cost moves from index time to inference time. You can handle queries the index never anticipated.

The tradeoff is real. ANN search is O(log n) and returns in milliseconds. An agentic retrieval loop might take ten seconds and cost a hundred API calls. For high-volume consumer search, that's prohibitive. For enterprise knowledge work — a researcher, a lawyer, an engineer — the quality difference may justify the cost entirely.

The likely equilibrium is layered:

- **Fast lexical/vector search** as the first pass: cheap, broad, milliseconds
- **Reranking** as the second pass: cross-encoder accuracy, hundreds of milliseconds
- **Agentic verification** as the third pass: reasoning over the best candidates, seconds
- **Agentic research mode** for complex tasks: full loop with multi-hop and synthesis, minutes

Each layer handles the queries the previous layer can't answer well.

This maps directly onto TIA's architecture. Beth (fast lexical index) + dense semantic search covers the first two layers. Claude reasoning over retrieved results is the third and fourth. The layers already exist; the question is when to invoke which.

---

## The Numbers Behind the Stakes

The scale of what these systems must handle is difficult to fully grasp:

- **149 zettabytes** of data exist in the global datasphere as of 2024 — roughly 250 billion DVDs worth of information
- **402 million terabytes** of data are created, captured, copied, and consumed *every day*
- **8–14 billion searches** are performed on Google alone *every day*
- The gap between data generated and data meaningfully indexed and retrievable has been widening for decades

We have never had more information. The retrieval problem has never been harder. And for the first time, the systems working on it can reason about what they find.

---

## What This Means for Knowledge Work

We are living through a phase transition in how information becomes accessible.

For the last seventy years, the retrieval contract was: **humans ask, systems match**. The quality of the answer depended almost entirely on the quality of the query. Power users learned to write precise Boolean queries. Everyone else got whatever TF-IDF or PageRank surfaced in the first ten results.

Semantic search weakened the dependency on exact phrasing. You could ask in natural language and get semantically relevant results. But you still got a list of documents to read.

RAG went further: you could ask in natural language and get a synthesized answer derived from a corpus. But the synthesis was only as good as the single retrieval pass.

Agentic retrieval changes the contract: **you describe a problem, the system researches it**. The retrieval, synthesis, verification, and follow-up happen in a reasoning loop. The work shifts from "find the right document" to "state the right goal."

This is not science fiction. Deep Research agents from multiple major labs are already doing this for general web search. Enterprise implementations are doing it over private knowledge bases. The tools exist; the engineering is happening now.

---

## Coda: The Shape of the Next Era

The inverted index was an insight about text structure. TF-IDF was an insight about statistical significance. PageRank was an insight about social consensus. Dense retrieval was an insight about semantic geometry. RAG was an insight about context injection.

Agentic retrieval is an insight about something different in kind: **information access as goal-directed behavior**. Not "find the document that matches" but "pursue the answer until you have it."

The scholars who built these systems — Luhn, Salton, Spärck Jones, Robertson, Mikolov, the DPR team, the ReAct team — each shifted what it meant for a machine to "find" something. Each shift made more of human knowledge practically accessible.

We're at another inflection point. The question now is not whether agentic systems will transform information retrieval — they already are. The question is how we design knowledge bases, indexes, and organizational structures to make the most of systems that can actually reason about what they find.

The filing cabinet era is over. The library era is over. The search box era is nearly over.

What comes next is a system that reads.

---

*March 2026*
*See also: [RFQ Matching at Scale](/articles/rfq-matching-modern-architecture) — the architecture in this article applied to a concrete production problem | [Reveal](/articles/reveal-introduction) — what agent-native information access looks like for codebases: structured, queryable, and built around progressive disclosure*
