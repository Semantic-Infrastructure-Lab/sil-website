---
title: "The Diff That Shows What Actually Changed"
subtitle: "reveal diff://: semantic structural diffs for code review, CI gates, and pre-commit sanity checks"
author: "Scott Senkeresty"
date: "2026-04-06"
type: "article"
status: "published"
linkedin_posted: true
audience: "developers"
topics: ["reveal", "diff", "code-review", "ci-cd", "refactoring", "complexity", "ast"]
beth_topics:
  - reveal
  - diff-adapter
  - code-review
  - ci-cd
  - complexity
  - ast-adapter
  - refactoring
related_docs:
  - "reveal-call-graphs.md"
  - "reveal-pack-and-review.md"
  - "reveal-nav-flags.md"
canonical_url: "https://semanticinfrastructurelab.org/articles/reveal-diff"
reading_time: "6 minutes"
session_id: "celestial-moon-0406"
---

# The Diff That Shows What Actually Changed

**`reveal diff://` — semantic structural diffs that answer the questions `git diff` can't**

---

`git diff` shows you what lines changed.

That's useful — but it's not what you actually want to know before merging a PR. What you want is:

- Which functions were added, removed, or modified?
- Did complexity go up — or did that refactor actually make things simpler?
- Did a signature change in a way that affects callers?
- Were new dependencies pulled in, or dead imports finally cleaned up?

Line diffs show *syntax*. Structural diffs show *impact*.

`git diff` is a line counter. `reveal diff://` is a question answerer.

```bash
reveal diff://git://main/.:git://HEAD/.
```

```
======================================================================
Structure Diff: git://main/. → git://HEAD/.
======================================================================

📊 Summary:

  Functions:  +3 -1 ~7

🔧 Functions:

  + process_refund
      Line 234
      (self, order_id: str, amount: float) -> bool
      [NEW - 28 lines, complexity 6]

  - legacy_sync_handler
      Was: line 180, 45 lines, complexity 12
      [REMOVED]

  ~ validate_payment
      Signature:
        - (self, amount: float) -> bool
        + (self, amount: float, currency: str = 'USD') -> bool
      Complexity: 8 → 14 (+6)
      Lines: 32 → 51 (+19)
```

Three functions added, one removed, seven modified — and for each modified function, exactly what changed: signature, complexity, line count, line number. It also tracks imports: new dependencies added, dead imports removed.

---

## What makes it different from `git diff`

A line diff of `validate_payment` looks like this:

```diff
@@ -45,8 +45,27 @@ def validate_payment(self, amount: float) -> bool:
-    if amount <= 0:
+    if amount <= 0 or currency not in SUPPORTED_CURRENCIES:
         return False
+    if self.fraud_check_enabled:
+        score = self._get_fraud_score(amount, currency)
+        if score > self.fraud_threshold:
+            log.warning(...)
+            return False
+    if currency != 'USD':
+        amount = self._convert(amount, currency)
+        if amount is None:
+            raise ValueError(...)
     ...19 more lines
```

That's what `git diff` gives you: a wall of syntax. You have to read it, hold it in your head, and mentally simulate what it means.

The structural diff answers the question you were actually trying to answer:

```
~ validate_payment
    Complexity: 8 → 14 (+6)
```

**Complexity jumped from 8 to 14. That's a +75% increase.** Whatever those 19 lines do, they added 6 decision points to a function that previously had 8. That's worth a careful read — and now you know that *before* you start reading.

Complexity here approximates decision points — branches, loops, conditionals. Higher means harder to reason about and harder to test.

Code review has always been semantic: you were reading text to understand *behavior*. Structural diff makes that explicit.

---

## Four workflows

### 1. Pre-commit sanity check

Before you commit, see exactly what you changed structurally:

```bash
reveal diff://git://HEAD/src/:src/
```

This compares your working tree against the last commit. Output:

```
📊 Summary:

  Functions:  +0 -0 ~1

🔧 Functions:

  ~ handle_checkout
      Complexity: 6 → 11 (+5)
      Lines: 24 → 38 (+14)
      Line: 67 → 67
```

You added 14 lines to `handle_checkout` and complexity went up by 5. Is that intentional? Is the function getting too complex? This is the question to answer before committing, not after code review.

---

### 2. PR review — the full picture before you start reading

Before reading any code in a PR, get the structural summary:

```bash
reveal diff://git://main/.:git://HEAD/.
```

This tells you:
- How many functions changed (scope of the PR)
- Which ones got more complex (where to focus review attention)
- Which signatures changed (potential breaking changes for callers)
- What was added or removed (the net change)
- Which imports were added or dropped (new dependencies, dead code cleanup)

You're not replacing code review — you're orienting yourself before you start. A PR with 12 modified functions and 3 complexity increases is a different review than a PR with 2 modified functions and no complexity change.

---

### 3. CI gate — block PRs that make code harder to maintain

The `diff://` output is machine-readable JSON. That makes it a scriptable CI gate:

```bash
reveal diff://git://main/.:git://HEAD/. --format json | \
  jq '[.diff.functions[] | select(.complexity_delta > 5)] | length'
```

If that returns anything greater than 0, the PR increased at least one function's complexity by more than 5. Your CI step fails, the author is told which function and by how much.

Full gate:

```bash
#!/bin/bash
VIOLATIONS=$(reveal diff://git://main/.:git://HEAD/. --format json | \
  jq '[.diff.functions[] | select(.complexity_delta > 5)] | length')

if [ "$VIOLATIONS" -gt 0 ]; then
  echo "❌ Complexity gate failed: $VIOLATIONS function(s) increased complexity by >5"
  reveal diff://git://main/.:git://HEAD/. --format json | \
    jq -r '.diff.functions[] | select(.complexity_delta > 5) |
           "  \(.name): \(.complexity_before) → \(.complexity_after) (+\(.complexity_delta))"'
  exit 1
fi
echo "✅ Complexity gate passed"
```

The threshold is yours to set. `> 5` is a reasonable starting point for "this change meaningfully increased complexity." `> 10` catches only egregious cases. `> 0` enforces no complexity increases at all — useful for critical modules.

---

### 4. Refactor validation — prove the cleanup worked

The same tool that catches regressions validates improvements. After a refactor, run the diff to confirm complexity actually went down:

```bash
reveal diff://git://HEAD~1/src/payments.py:src/payments.py
```

```
  ~ execute
      Complexity: 61 → 54 (-7)
      Lines: 183 → 160 (-23)

  ~ _extract_frontmatter
      Complexity: 9 → 1 (-8)
      Lines: 44 → 12 (-32)
```

Complexity went down by 7 and 8 respectively. The refactor did what it claimed. This is the diff direction most tools ignore — negative delta is signal too.

---

## Per-file commit diffs

Branch comparison is the PR review workflow. File-level commit diffs are for reviewing your own work:

```bash
reveal diff://git://HEAD~1/src/auth.py:src/auth.py
```

Output:

```
======================================================================
Structure Diff: git://HEAD~1/src/auth.py → src/auth.py
======================================================================

📊 Summary:

  Functions:  +0 -0 ~2

🔧 Functions:

  ~ validate_token
      Signature:
        - (token: str) -> bool
        + (token: str, strict: bool = False) -> bool
      Complexity: 5 → 8 (+3)
      Lines: 18 → 26 (+8)
      Line: 34 → 34

  ~ refresh_session
      Complexity: 4 → 4 (unchanged)
      Lines: 22 → 24 (+2)
      Line: 61 → 63
```

You added a `strict` parameter to `validate_token` and complexity went up by 3. `refresh_session` got two lines longer but complexity didn't change — probably a comment or minor adjustment. One function worth reviewing, one that's fine.

This is the "did I actually mean to do that?" check — run it before every commit.

---

## Connecting diff to impact

The structural diff tells you *what* changed. Pairing it with `calls://` tells you *who's affected*:

```bash
# Step 1: What functions changed?
reveal diff://git://main/.:git://HEAD/. --format json | \
  jq -r '.diff.functions[] | select(.type == "modified") | .name'

# Step 2: For each changed function, who calls it?
reveal 'calls://src/?target=validate_token'
```

A signature change to a function with 12 callers is a different risk profile than the same change to a function with 1 caller. The combination answers both questions.

---

## What the JSON contains

This isn't just output — it's a programmable surface. Every field is queryable:

```json
{
  "name": "validate_payment",
  "type": "modified",
  "complexity_before": 8,
  "complexity_after": 14,
  "complexity_delta": 6,
  "changes": {
    "signature": {
      "old": "(self, amount: float) -> bool",
      "new": "(self, amount: float, currency: str = 'USD') -> bool"
    },
    "complexity": { "old": 8, "new": 14, "delta": 6 },
    "line_count": { "old": 32, "new": 51, "delta": 19 }
  }
}
```

Added functions include full signature and complexity. Removed functions include where they were. Modified functions include before/after for every dimension that changed.

This is the basis for any automated analysis — complexity gates, signature change detection, line budget enforcement, documentation generation.

---

## Getting started

```bash
pip install reveal-cli

# Branch diff (PR review)
reveal diff://git://main/.:git://HEAD/.

# Commit diff for a specific file
reveal diff://git://HEAD~1/src/module.py:src/module.py

# Working tree vs last commit
reveal diff://git://HEAD/src/:src/

# Machine-readable for CI
reveal diff://git://main/.:git://HEAD/. --format json | \
  jq '.diff.functions[] | select(.complexity_delta > 5)'

# Validate a refactor reduced complexity
reveal diff://git://HEAD~1/src/module.py:src/module.py
```

Full reference: `reveal help://diff`.

---

You don't review code by reading lines — you review it by understanding change. Which functions got riskier, which signatures broke, what the net structural change is: those are the questions that matter. Now you can answer them before the review starts.

---

*Part of the Reveal documentation series. See also:*
- *[Find Every Caller in Your Codebase With One Command](/articles/reveal-call-graphs) — impact analysis before refactoring*
- *[Two Commands That Change How You Work With Code](/articles/reveal-pack-and-review) — automated PR review*
- *[Stop Scrolling. Start Navigating.](/articles/reveal-nav-flags) — navigating complex functions*
