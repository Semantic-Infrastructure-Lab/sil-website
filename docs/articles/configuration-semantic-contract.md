---
title: "Configuration as Semantic Contract"
subtitle: "Why your config file should declare meaning, not just tune parameters"
author: "Scott Senkeresty"
date: "2025-12-23"
updated: "2026-08-04"
type: "article"
status: "published"
linkedin_posted: false
audience: "developers"
topics: [configuration, reveal, progressive-disclosure, semantic-infrastructure, architecture-validation]
related_projects: [reveal]
related_docs:
  - "CONFIGURATION_AS_SEMANTIC_CONTRACT.md"
  - "PROGRESSIVE_CONFIGURATION_PATTERN.md"
  - "/research/PROGRESSIVE_DISCLOSURE_GUIDE.md"
canonical_url: "https://semanticinfrastructurelab.org/articles/configuration-semantic-contract"
reading_time: "14 minutes"
beth_topics:
  - configuration
  - semantic-contracts
  - progressive-disclosure
  - reveal
  - architecture-validation
session_provenance: "stormy-gale-1223"
---

# Configuration as Semantic Contract

*Why your config file should declare meaning, not just tune parameters*

> **Correction (2026-08-04):** The original version of this article described a `semantic://` adapter and `ast.entry_points` config as shipped Reveal features, and showed Reveal validating its own architecture via `.reveal.yaml`. Neither was true at publication (v0.100.2) or is true today (v0.113.0): `semantic://` was considered and explicitly rejected (see [ROADMAP.md](https://github.com/Semantic-Infrastructure-Lab/reveal/blob/master/ROADMAP.md), "Explicitly Not Planned" — over-engineered, requires ML infrastructure); `entry_points` config was never implemented; and Reveal's own `.reveal.yaml` has never declared an `architecture:` block. This revision corrects those sections and marks what's real, what's proposed ([BACK-952](https://github.com/Semantic-Infrastructure-Lab/reveal)), and what was dropped.

---

## The Webpack Config Problem

You know the moment. Your team says "we need custom build behavior." You open `webpack.config.js` and stare at 300 lines of opaque configuration:

```javascript
module.exports = {
  mode: process.env.NODE_ENV || 'development',
  entry: './src/index.js',
  output: { /* 15 lines of path resolution */ },
  module: {
    rules: [ /* 80 lines of loader chains */ ]
  },
  plugins: [ /* 120 lines of plugin instances */ ],
  optimization: { /* 40 lines of minification settings */ }
}
```

This isn't configuration. It's a second codebase that happens to be written in JavaScript objects instead of functions.

And here's the thing: **none of it says what it means.**

Does `mode: 'production'` enable tree-shaking? Does `optimization.minimize` affect CSS too? What does `output.publicPath` actually control? You don't know. The configuration doesn't say. You have to read the documentation, test in staging, and hope.

This is what configuration has become: **tuning knobs with no semantic meaning.**

---

## The Binary Trap Every Team Hits

Every configuration story starts the same way:

**Week 1:** "This tool is amazing! Zero config, just works!"

**Month 3:** "Okay, we need to customize this one thing. Let me add a config file..."

**Year 1:** "Our configuration file is 500 lines and nobody understands it. Should we just eject?"

The problem isn't the tools. It's a fundamental design pattern failure. Most tools force you to choose:

**Option A: Zero Configuration**
- ✅ Simple to start (literally just run it)
- ✅ Low barrier to entry
- ❌ Breaks down as complexity scales
- ❌ Forces "eject" when you hit limits (hello, Create React App)

**Option B: Configure Everything**
- ✅ Full control over every detail
- ✅ Handles complex enterprise needs
- ❌ Overwhelming for beginners (ESLint's 200+ rules)
- ❌ Configuration becomes harder to maintain than code

**The gap:** No middle path that scales complexity gradually.

This isn't just about convenience. It's about **architectural drift**. Your team decides "we follow clean architecture." Everyone nods. Six months later, someone adds `from repositories import UserRepo` directly to a route handler. Nobody catches it. The architecture document becomes archaeology.

**Why?** Because architecture lived in documentation (static text) instead of configuration (enforced contract).

---

## What If Configuration Declared Meaning?

Here's a different approach. Instead of tuning parameters, what if your configuration **declared what things mean in your system**?

**Traditional configuration** (mechanism-focused):
```yaml
ignore_patterns:
  - "**/tests/**"
  - "**/fixtures/**"
```

What does this mean? Why are we ignoring those paths? Is it for performance? Dead code detection? Linting? You don't know by reading it.

**Semantic configuration** (meaning-focused):
```yaml
architecture:
  layers:
    - name: routes
      paths: [app/routes/**]
      description: "HTTP route handlers"
      deny_imports:
        - repositories      # Routes must go through services

    - name: services
      paths: [app/services/**]
      description: "Business logic layer"
      deny_imports:
        - routes            # Services can't depend on HTTP layer
```

**Notice the difference:**

- **Declares intent**, not just mechanism
- **Documents why**, not just what
- **Tool enforces it** automatically (violations fail CI)
- **Team shares it** (version controlled, everyone sees same rules)

This configuration **IS the architecture**. Not a description of it. Not a promise of it. The actual enforced contract.

---

## The Progressive Configuration Pattern

The best configuration systems don't force you to choose between zero config and total complexity. They follow a **three-level progressive pattern**:

### Level 1: Intelligent Defaults (Zero Config)

The tool works immediately with sensible behavior:

```bash
reveal src/app.py              # Works right away
reveal src/app.py --check      # Quality checks with built-in rules
```

**Design criteria:**
- Cover 80% of common use cases
- Based on industry best practices
- Fail gracefully when defaults don't fit
- Suggest configuration when appropriate

**When to stay here:** Simple projects, standard conventions, solo developer.

### Level 2: Project Overrides (Team Config)

Declare project-specific semantics in version-controlled config:

```yaml
# .reveal.yaml - Your team's architectural rules
architecture:
  layers:
    - name: models
      paths: [app/models/**]
      allow_imports: [typing, pydantic, datetime, enum]
      deny_imports: [services, routes, repositories]

# Rule thresholds — a real, working example from reveal's own .reveal.yaml
rules:
  C901:
    threshold: 21   # Cyclomatic complexity (default: 10)
  E501:
    max_length: 100 # Line length (default: 100, made explicit)
```

**Design criteria:**
- Declarative format (YAML)
- Overrides **extend** defaults (don't replace everything)
- Committed to version control
- Schema-validated (catch errors early)

The `no-god-functions`-style free-form `rules: [{check: "..."}]` block from the original version of this article — an arbitrary expression language for custom checks — was never implemented. What's real is per-rule threshold overrides (`C901.threshold`, `E501.max_length`, etc., keyed by the rule's built-in code) and the `architecture.layers` block above.

**When to move here:** Team projects, custom architecture, domain-specific patterns, enforcement needed.

### Level 3: Custom Extensions (Domain-Specific)

Extend the tool with organization-specific logic when YAML isn't enough:

```python
# ~/.reveal/rules/payment_security.py
# Custom rule: Track all payment code for PCI compliance audits
from reveal.rules.base import BaseRule, Detection, RulePrefix, Severity

class StripeUsage(BaseRule):
    code = "S901"
    message = "Stripe API call detected - ensure PCI DSS compliance"
    category = RulePrefix.S
    severity = Severity.LOW
    file_patterns = [".py"]

    def check(self, file_path, structure, content):
        detections = []
        for i, line in enumerate(content.splitlines(), start=1):
            if "stripe." in line:
                detections.append(self.create_detection(file_path, line=i))
        return detections
```

**Design criteria:**
- Plugin architecture (drop files in directory, auto-discovered)
- Same API as built-in rules
- Full language power (not limited DSL)
- Optional (Level 2 should handle most cases)

**When to move here:** Organization-wide standards, highly domain-specific checks (financial, medical, legal), complex logic that YAML can't express.

---

## Why This Matters: Semantic Infrastructure

This isn't just about making configuration easier. It connects to a deeper principle from the Semantic Infrastructure Lab:

**Principle #2: Meaning Must Be Explicit**

> Semantic infrastructure makes meaning first-class. All meaningful objects are typed, inspectable semantic structures—not implicit conventions or documentation promises.

**Traditional approach:**
- Architecture lives in documentation: "Routes shouldn't call repositories directly"
- Reality lives in code: `from repositories import UserRepo` (oops)
- No automated check catches the violation
- Drift accumulates until architecture is unrecognizable

**Semantic configuration approach:**
- Architecture lives in `.reveal.yaml`: `deny_imports: [repositories]`
- Tool enforces on every commit
- Violations fail CI immediately
- **Architecture cannot drift silently**

Your configuration becomes **executable documentation**—not a promise that might be true, but an enforced contract that's definitely true.

---

## Declaring a Layered Architecture

Here's the pattern applied to a typical routes/services/repositories split:

```yaml
architecture:
  layers:
    - name: routes
      paths: [src/routes/**]
      description: "HTTP route handlers"
      deny_imports: [repositories]

    - name: services
      paths: [src/services/**]
      description: "Business logic layer"
      deny_imports: [routes]

    - name: repositories
      paths: [src/repositories/**]
      description: "Data access layer"
      deny_imports: [routes, services]
```

Running `reveal src/ --check` against this config enforces the layer boundaries as part of the normal quality-check pass.

---

## The URI Adapter Pattern: Composable Queries

Reveal uses a URI scheme pattern (`ast://`, `calls://`, `imports://`, `json://`, 24 adapters total — `reveal --adapters`) that lets you query code like a database, without any config:

```bash
# Find complex functions
reveal 'ast://src?complexity>10'

# Find who calls a function
reveal 'calls://src/?target=validate_item'

# Text/identifier search across a tree
reveal src/ --grep 'stripe\.'
```

Domain-specific knowledge — "what code touches our payment provider?" — becomes a one-line query instead of tribal knowledge ("ask Sarah, she knows where the payment code is"). It's deterministic: a grep pattern or a structural filter, not an embedding search. (A named, saved-pattern `semantic://` adapter was considered and explicitly turned down — see ROADMAP.md's "Explicitly Not Planned" list — as requiring ML infrastructure for too little gain over `--grep`.)

---

## Entry Points and Dead-Code Detection

Modern frameworks use **implicit invocation**—decorators, dependency injection, event handlers. This breaks dead code detection because tools don't understand "framework magic."

Example: a pytest test function

```python
def test_login_flow():
    ...
```

Is `test_login_flow()` dead code? It's never explicitly called anywhere. But pytest discovers and invokes it by convention.

**What Reveal actually does today:** `calls://?uncalled` already recognizes a fixed, built-in set of implicit-invocation patterns and excludes them from dead-code findings — `property`/`classmethod`/`staticmethod` decorators, pytest fixtures and `test_*` functions, `unittest` lifecycle methods (`setUp`, `tearDown`, ...), and C#/Java test attributes (`[Fact]`, `[Test]`, JUnit `@Test`, etc. — added for BACK-446 after this exact false-positive pattern swamped a C# codebase with 1,577 false "dead code" hits).

**What it doesn't cover yet:** web/CLI framework routes — Flask/FastAPI/FastHTML `@app.route`, Click `@click.command`, Django views. Those aren't in the built-in list, so `--uncalled` still false-flags every route handler in a web app today. Letting a project declare additional entry-point patterns per `.reveal.yaml` — closer to the original `ast.entry_points` idea, but as a real, scoped extension of the existing built-in list rather than a fabricated already-shipped feature — is filed as [BACK-952](https://github.com/Semantic-Infrastructure-Lab/reveal) in reveal's backlog, not yet built.

---

## Team Alignment Mechanism

Here's what traditional architecture alignment looks like:

1. Write architecture docs (Confluence, Notion, Google Docs)
2. Explain in team meeting (some people listen)
3. Hope everyone remembers (they don't)
4. Catch drift in code review (sometimes, maybe, if reviewer notices)

**Result:** Architecture drifts. Documentation becomes historical artifact.

Here's what **semantic configuration alignment** looks like:

1. Declare architecture in `.reveal.yaml`
2. Commit to version control
3. Tool enforces on every commit
4. Violations fail CI (can't merge without fixing)

**Result:** Architecture **cannot drift silently**. The config is living documentation.

**Illustrative scenario** (pre-commit hook wired to `reveal src/ --check`; exact output format not verified against current CLI text):

```bash
$ git commit -m "Add quick database access to route"

Running pre-commit hook: reveal src/ --check

✗ Architecture violation detected

File: src/routes/users.py:23
Issue: Routes layer cannot import from repositories layer
Found: from repositories.user import UserRepository

Declared rule: Routes must access data through services layer
Fix: Move database logic to services/user_service.py

Commit blocked. Fix violations and try again.
```

The architecture didn't drift. The config caught it. **Before merge. Before review. Before production.**

---

## Why "Progressive" Matters

Remember the binary trap? Zero config OR configure everything?

Progressive configuration solves this by making **complexity cost opt-in**.

**Bad tool design:**
```bash
$ tool init                       # Generates 200-line config
$ tool run                        # Now you can finally use it
```

You're forced to understand the entire config surface before doing anything.

**Progressive tool design:**
```bash
$ tool src/                       # Works immediately (Level 1)
✓ Analyzed 47 files
  12 functions exceed 100 lines

Tip: Create .tool.yaml to customize rules

$ echo "max_function_lines: 150" > .tool.yaml    # Add config as needed (Level 2)
$ tool src/                       # Override applied
✓ Analyzed 47 files
  3 functions exceed 150 lines
```

You pay complexity cost only when you need customization.

**The principle:** Start simple, add config incrementally, extend with code when YAML isn't enough. Each level is a stable stopping point—you don't *have* to progress.

---

## Beyond Code: The Pattern Generalizes

Configuration as semantic contract isn't specific to code analysis. The pattern applies everywhere:

**Documentation Structure:**
```yaml
# docs.yaml
structure:
  - section: foundations
    audience: [newcomers, researchers]
    reading_time: 30min
    prerequisites: []

  - section: systems
    audience: [developers]
    reading_time: 2hr
    prerequisites: [foundations]
```

**API Contracts:**
```yaml
# api.yaml
endpoints:
  - path: /api/users
    rate_limit: 1000/hour
    auth_required: true
    data_sensitivity: PII
    cannot_call: [/api/admin/**]    # Security boundary
```

**Deployment Rules:**
```yaml
# deployment.yaml
environments:
  - name: production
    branch: main
    auto_deploy: false              # Invariant: prod requires approval
    required_checks:
      - tests
      - security_scan
      - architecture_validation
```

**Common pattern:** Declare semantic constraints → Tools enforce automatically → Version control the contract.

---

## Try It: Reveal v0.113+

Progressive configuration is live in Reveal. Here's how to try it:

```bash
# Install Reveal
pip install reveal-cli

# Start with zero config (Level 1)
reveal src/                       # Works immediately
reveal src/app.py --check         # Quality checks with defaults

# Add project config when needed (Level 2)
cat > .reveal.yaml << EOF
architecture:
  layers:
    - name: routes
      paths: [app/routes/**]
      deny_imports: [repositories]

    - name: services
      paths: [app/services/**]

rules:
  C901:
    threshold: 15   # cyclomatic complexity
EOF

# Now validate architecture + rule thresholds
reveal src/ --check               # Enforces your rules

# Query structural properties directly (no config needed)
reveal 'ast://src?complexity>10'
```

**The progression:**
1. Try it with zero config (30 seconds)
2. Add `.reveal.yaml` for project rules (5 minutes)
3. Write custom rules if needed (optional, when YAML isn't enough)

Each step is valuable. Each step is optional. Complexity scales with your needs.

---

## The Deeper Vision: Semantic OS

Configuration as semantic contract is **Layer 3** of a larger vision we're building at the Semantic Infrastructure Lab.

We call it the **Semantic OS**—a 7-layer stack where meaning is the primary abstraction:

**Layer 0:** Hardware/Substrate (compute, storage)
**Layer 1:** Names (identifiers, symbols)
**Layer 2:** Types & Relationships (AST, type systems)
**Layer 3:** Composition (structure, how things fit together) ← **Configuration lives here**
**Layer 4:** Dynamics (time, simulation, execution)
**Layer 5:** Intent (user goals, constraints)
**Layer 6:** Intelligence (agents, reasoning)

Configuration is part of **Layer 3: Composition**—declaring how your system fits together, what boundaries exist, what patterns have meaning.

When configuration declares composition rules:
- Tools can **validate** architecture automatically
- Agents can **query** semantic patterns
- Teams can **enforce** invariants without manual review
- Knowledge becomes **queryable infrastructure** instead of tribal wisdom

This is what semantic infrastructure means: **making meaning explicit and enforceable**, not implicit and aspirational.

---

## The Bottom Line

Configuration files don't have to be opaque tuning knobs.

They can be **semantic contracts** that:
- Declare what things mean in your system
- Get enforced automatically by tools
- Scale complexity progressively (zero config → project rules → custom extensions)
- Become living documentation that can't drift

**The shift:** From "here are some settings" to "here's what these structures mean."

When configuration declares meaning instead of just tuning behavior, it becomes **infrastructure for maintaining architectural integrity**—exactly the kind of semantic infrastructure that makes AI agents effective and systems maintainable.

Try it. Declare your architecture. Let tools enforce it. Watch configuration become something valuable instead of something to dread.

---

## About the Semantic Infrastructure Lab (SIL)

SIL is building the semantic substrate for intelligent systems—infrastructure where meaning is first-class, reasoning is traceable, and agents build on solid foundations.

**Our work:**
- 12 projects across the 7-layer semantic stack
- Production tools (Reveal, Beth, Scout, Pantheon)
- Research papers on semantic computing foundations
- 25-30x measured efficiency gains in AI workflows

**Progressive disclosure isn't just a pattern. It's proof that semantic infrastructure works.**

---

**Links:**

**Reveal:**
- GitHub: https://github.com/Semantic-Infrastructure-Lab/reveal
- PyPI: https://pypi.org/project/reveal-cli/
- Docs: `reveal help://`

**SIL:**
- Website: https://semanticinfrastructurelab.org
- Research: [Progressive Disclosure Guide](/research/PROGRESSIVE_DISCLOSURE_GUIDE)
- Architecture: [7-Layer Semantic Stack](/foundations/SIL_SEMANTIC_OS_ARCHITECTURE)

---

**Current Version:** Reveal v0.113.0. `architecture: layers:` config and `.reveal/rules/` custom-rule plugins are real and working; `semantic://` and `entry_points` config, described in earlier versions of this article, are not (see correction note above).
**License:** MIT
**Maintained by:** Scott Senkeresty, Semantic Infrastructure Lab

---

*This article was written using Reveal to explore Reveal's own codebase—progressive disclosure in practice. Configuration as semantic contract isn't theory. It's how we build.*
