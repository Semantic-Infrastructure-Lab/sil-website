---
title: "Reveal: The Surprising Recipes"
subtitle: "Clever combinations and unexpected capabilities — the ones people forward to each other"
author: "Scott Senkeresty"
date: "2026-03-18"
type: "article"
status: "published"
linkedin_posted: false
audience: "developers, ai-agent-builders, devops"
beth_topics:
  - reveal
  - progressive-disclosure
  - calls-adapter
  - pipelines
  - composability
  - infrastructure
  - ai-agent
  - session-archaeology
  - code-quality
related_docs:
  - "reveal-what-it-makes-possible.md"
  - "reveal-call-graphs.md"
  - "systems/reveal.md"
---

# Reveal: The Surprising Recipes

**The basics are in [the main article](reveal-what-it-makes-possible.md).** This is the rest — the combinations nobody sat down to design, the capabilities that show up unexpectedly, the things that make you stop and say "wait, that works?"

Almost all of these are just two adapters composing, or a filter combination nobody thought to try. That's the point.

---

## Adapters Composing Into Each Other

The URI model means adapters don't know about each other — they just consume and emit structured data. These pipelines emerge naturally from that.

### Your nginx config is a source of SSL targets

```bash
# Extract every domain from a config, check every cert
reveal /etc/nginx/conf.d/app.conf --extract domains | reveal --stdin --check
```

Parse nginx, pull every `server_name`, pipe directly to SSL check. `--extract domains` outputs one `ssl://domain` URI per line — reveal routes each to the SSL adapter automatically.

Show only failures (useful when you have dozens of vhosts):
```bash
reveal /etc/nginx/sites-enabled/ --extract domains | reveal --stdin --check --only-failures
```

### An entire hosting environment, one pipeline

```bash
# Audit every domain under a cPanel user for SSL health
reveal cpanel://USERNAME/domains --format=json | \
  jq -r '.domains[].domain' | sed 's/^/ssl:\/\//' | reveal --stdin --check
```

Or start from the cPanel SSL view directly — only probe the ones that aren't already healthy:
```bash
reveal cpanel://USERNAME/ssl --format=json | \
  jq -r '.certs[] | select(.status != "ok") | .domain' | \
  sed 's/^/ssl:\/\//' | reveal --stdin --check-live
```

### Schema drift between live databases

```bash
reveal diff://mysql://localhost/users:mysql://staging/users
reveal diff://sqlite://./dev.db:sqlite://./prod.db
```

The same `diff://` adapter that compares git branches compares live database schemas. Production vs staging, caught in one command. Nobody thinks of diff as something you run against databases — until it obviously should work, and does.

### Mix anything in a single stdin batch

```bash
echo -e "config.yaml\nssl://prod.example.com\nenv://DATABASE_URL" | reveal --stdin
```

Files, URIs, and environment variable lookups — all processed in one pass, all with the same output format. Reveal accepts anything on stdin and routes each line to the right adapter automatically.

---

## The Self-Reference

Reveal uses its own interface to document and explain itself.

```bash
# How does the hardcoded-secrets rule work?
reveal reveal://rules/security/S001.py

# How does the Python analyzer parse files?
reveal reveal://analyzers/python.py

# How is the calls adapter structured?
reveal reveal://adapters/calls

# Extract a specific method from a rule
reveal reveal://rules/links/L001.py _extract_anchors_from_markdown
```

`reveal://` is a real adapter. When you want to understand how any capability works — or contribute a new one — you use the same tool and the same syntax you use on your own code. The interface is complete.

---

## Code Smell Detectors Nobody Thinks to Write

### Code golf detection

```bash
reveal 'ast://src?complexity>10&lines<50'
```

High complexity, suspiciously short. Usually means over-compressed list comprehensions, chained ternaries, or regex abuse masquerading as logic. Neither filter alone is the smell — the combination is.

### Simple but huge

```bash
reveal 'ast://src?complexity<5&lines>50'
```

Long functions that do nothing difficult. These are usually config dumps, dead feature flags, or data that should be in a file. `complexity < 5` and `lines > 50` together surface the ones worth questioning.

### The danger zone

```bash
reveal 'ast://src?complexity>20'           # needs refactoring now
reveal 'ast://src?complexity>30&lines>150' # god functions
```

### Audit what a function actually calls — including dangerous builtins

```bash
reveal 'calls://src/?callees=process_request&builtins=true'
```

Default behavior hides builtins (noise). `builtins=true` surfaces calls to `eval`, `exec`, `open`, `__import__` — security-relevant primitives hidden inside otherwise normal-looking functions. A fast security smell check before a code review.

### Wildcard decorator matching across the whole codebase

```bash
reveal 'ast://.?decorator=*cache*'         # every cached function — @lru_cache, @cached_property, @cache
reveal 'ast://.?decorator=*auth*'          # every auth-gated function
reveal 'ast://.?decorator=property&lines>10'  # properties with side effects (code smell)
reveal 'ast://.?decorator=abstractmethod'  # every interface definition
```

You don't need to know the exact decorator name. `*cache*` catches every caching pattern regardless of library or vintage.

---

## CI Gates Nobody Else Ships

### Block PRs that make code *more* complex — per function

```bash
reveal diff://git://origin/main/.:git://HEAD/. --format json | \
  jq '.diff.functions[] | select(.complexity_delta > 5)'
```

Not "are there complex functions." **Did this PR make any specific function harder to maintain than it was before?** Every changed function carries `complexity_before`, `complexity_after`, and `complexity_delta`. The gate is the delta — catching the moment complexity accumulates, not after it's already entrenched.

As a GitHub Actions step:
```yaml
- name: Complexity gate
  run: |
    REGRESSIONS=$(reveal diff://git://origin/${{ github.base_ref }}/.:git://HEAD/. \
      --format json | jq '[.diff.functions[] | select(.complexity_delta > 5)] | length')
    if [ "$REGRESSIONS" -gt 0 ]; then
      echo "Complexity increased in $REGRESSIONS function(s)"
      exit 1
    fi
```

### Dead code introduced by this PR

```yaml
- name: Dead code check
  run: |
    UNCALLED=$(reveal 'calls://src/?uncalled' --format json | \
      jq '.entries | length')
    echo "Uncalled functions: $UNCALLED"
    # Advisory — change exit 0 to exit 1 to enforce
```

### SSL cert health from nginx — in CI

```yaml
- name: SSL cert check
  run: |
    reveal /etc/nginx/sites-enabled/ --extract domains | reveal --stdin --check
    # exit 2 if any cert is expired or expiring within 7 days
```

### Quality score over time — one shell loop, no external tool

```bash
git log --oneline | head -10 | while read commit _; do
  git checkout $commit 2>/dev/null
  score=$(reveal stats://src/ --format json | jq '.summary.avg_quality_score')
  echo "$commit: $score"
done
```

Trend tracking across your git history. Reveal runs on each checkout. The score history tells you when quality started declining — before it became a crisis.

---

## Refactoring Verification

### Did the rename actually propagate?

```bash
# After renaming parse_config → load_config:
reveal 'calls://src/?target=parse_config'   # should return 0 callers
reveal 'calls://src/?target=load_config'    # should have inherited them
```

Two commands confirm the rename worked. Faster and more reliable than grep, which matches strings in comments, docstrings, and variable names.

### Understand what a function delegates to *before* reading it

```bash
reveal 'calls://src/?callees=initialize_app'
reveal 'calls://src/?callees=process_request'
```

See the collaboration pattern — what it orchestrates, what it depends on — without reading the implementation. For unfamiliar functions, this is often the right level of detail.

### Full impact radius before touching anything

```bash
reveal 'calls://src/?target=parse_config&depth=3'  # callers-of-callers, 3 levels deep
```

Everything that will break if `parse_config` changes its signature. Run this before you move it, rename it, or change what it returns. Then extract the files for review:
```bash
reveal 'calls://src/?target=parse_config' --format=json | \
  jq -r '.levels[0].callers[].file' | sort -u
```

### Visual architecture documentation from code

```bash
reveal 'calls://src/?target=main&depth=3&format=dot' | \
  dot -Tsvg -Grankdir=TB > architecture.svg
```

Generate a call graph diagram from live code. Not a diagram you maintain — one that stays current because it's derived from the actual function calls.

---

## AI Session Archaeology

### Git blame for AI interactions

```bash
reveal 'claude://files/auth.py'
reveal 'claude://files/operations.py?since=today'
```

Every Claude Code session that touched a file — with Read/Write/Edit counts and timestamps. Not "who committed this" but "which agent sessions changed it and when." `git log` doesn't capture what an AI agent read or how many times it tried something.

### Session crash recovery

```bash
reveal 'claude://my-session?last'     # last assistant message
reveal 'claude://my-session?tail=5'   # last 5 turns
```

Session died mid-task? Recover the last output without re-opening a 50MB JSONL file.

### Audit what an agent actually did

```bash
reveal 'claude://session/my-session/workflow'  # tool call sequence, collapsed duplicates
reveal 'claude://my-session?errors'            # every error encountered, with context
reveal 'claude://session/my-session/files'     # every file touched, with operation counts
```

Post-session forensics. The workflow view shows the pattern of what the agent did — where it looped, where it got stuck, what it tried before succeeding.

### Find past work by topic

```bash
reveal 'claude://?search=authentication&since=2026-03-01'
reveal 'claude://?filter=reveal'   # sessions in the reveal project
```

With 2,000+ sessions, manual search doesn't scale. `?search=` pre-filters with parallel byte-scan (~0.7s for 2,700 files).

---

## Documentation Graph Tricks

### Find orphaned docs — written but unreachable

```bash
# Which docs have the most backlinks?
reveal 'markdown://docs/?link-graph' | grep "linked by" | sort -t'(' -k2 -rn | head -20

# Docs nobody links to (isolated = no "(linked by N)" annotation)
reveal 'markdown://docs/?link-graph' | grep -v "linked by\|→\|files\|edges\|isolated"
```

Most link checkers tell you if a link is broken. This tells you which docs are stranded — technically valid, but unreachable from everything else. Those are the ones that get stale.

### Your doc taxonomy, as data

```bash
reveal 'markdown://docs/?aggregate=beth_topics'
reveal 'markdown://docs/?aggregate=type'
reveal 'markdown://docs/?aggregate=status'
```

Frequency tables: how many docs cover each topic, what types exist, how many are drafts. Understand what your knowledge base actually covers — and where the gaps are — in one command.

### Full-text AND frontmatter in one query

```bash
reveal 'markdown://docs/?topics=authentication&body-contains=oauth'
reveal 'markdown://docs/?body-contains=retry&type=procedure'
reveal 'markdown://?!topics'    # docs missing the topics field entirely
```

Structured metadata filter combined with full-text body search. The `!` operator finds docs where a frontmatter field is absent — useful for finding docs that need tagging.

### Extract all code blocks from a doc

```bash
reveal README.md --code                    # all code blocks
reveal README.md --code --language=python  # only Python examples
```

Pull every code sample from documentation. Useful for testing that all examples actually run, or for generating a tutorial's example set.

---

## The One That Reads Certs Without a Network

```bash
reveal ssl://file:///etc/letsencrypt/live/example.com/fullchain.pem
reveal ssl://file:///var/cpanel/ssl/apache_tls/example.com/combined
```

Same output as a live SSL probe — expiry, SANs, chain count, health score — but reading directly from the PEM file on disk. Combined PEM files (leaf + chain concatenated) split automatically. Works air-gapped, works before a domain goes live, works when the server is down.

---

## The Meta-Point

None of these were explicitly designed as features. They emerged from two constraints:

1. **Everything is a URI with the same query syntax.** New adapters inherit all existing operators and output formats automatically. When someone added `diff://`, it worked against databases immediately because databases were already URIs.

2. **Outputs are structured data that pipes.** Every adapter's output can feed another adapter's input. Composability isn't a feature — it's what happens when the interface is consistent.

This is why the surprising recipes keep appearing. They're not surprises in the codebase — they're surprises in the discovery process. Once you internalize "everything composes," you start seeing pipelines everywhere.

---

**← [Back to the main article](/articles/reveal-what-it-makes-possible)** · **[Full documentation](/systems/reveal)** · **[All recipes](https://github.com/Semantic-Infrastructure-Lab/reveal/blob/main/docs/RECIPES.md)**
