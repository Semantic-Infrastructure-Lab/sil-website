---
title: "Configuration as Semantic Contract"
subtitle: "Why your config file should declare meaning, not just tune parameters"
author: "Scott Senkeresty"
date: "2025-12-23"
type: "article"
status: "published"
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
ast:
  entry_points:
    - pattern: "def test_"
      description: "Pytest test functions invoked by test runner"
      languages: [python]

    - pattern: "@app\\.(route|get|post)"
      description: "FastHTML route handlers (framework invocation)"
      languages: [python]

architecture:
  layers:
    - name: routes
      path: app/routes/**
      description: "HTTP route handlers"
      cannot_import:
        - repositories/**      # Routes must go through services

    - name: services
      path: app/services/**
      description: "Business logic layer"
      cannot_import:
        - routes/**            # Services can't depend on HTTP layer
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
imports:
  ignore_unused:
    - "**/tests/fixtures/**"     # Test fixtures import for side effects

architecture:
  layers:
    - name: models
      path: app/models/**
      can_import: [typing, pydantic, datetime, enum]
      cannot_import: ["**/!(typing|pydantic|datetime|enum)"]

  rules:
    - name: no-god-functions
      pattern: "app/services/**"
      check: function_lines <= 100
      severity: error
      message: "Service functions should be focused and under 100 lines"
```

**Design criteria:**
- Declarative format (YAML/TOML/JSON)
- Overrides **extend** defaults (don't replace everything)
- Committed to version control
- Schema-validated (catch errors early)

**When to move here:** Team projects, custom architecture, domain-specific patterns, enforcement needed.

### Level 3: Custom Extensions (Domain-Specific)

Extend the tool with organization-specific logic when YAML isn't enough:

```python
# ~/.reveal/rules/payment_security.py
# Custom rule: Track all payment code for PCI compliance audits
from reveal.rules import Rule

class StripeUsageRule(Rule):
    name = "track-stripe-usage"
    description = "Log all Stripe API calls for security audit trail"

    def check(self, node):
        if self.matches_pattern(node, r"stripe\\..*\\("):
            return self.info(
                node,
                "Stripe API call detected - ensure PCI DSS compliance"
            )
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
- Architecture lives in `.reveal.yaml`: `cannot_import: [repositories/**]`
- Tool enforces on every commit
- Violations fail CI immediately
- **Architecture cannot drift silently**

Your configuration becomes **executable documentation**—not a promise that might be true, but an enforced contract that's definitely true.

---

## Real-World Example: Reveal's Architecture Validation

Let me show you what this looks like in practice.

**The problem:** I was building Reveal's new pattern detection system. The architecture was clear in my head:

- **Adapters** fetch data (files, environment, AST)
- **Renderers** display data (text, JSON, tree format)
- **Rules** validate code quality
- **Core** orchestrates everything

But code has a way of violating architecture when you're moving fast. Without enforcement, I'd inevitably add "just one quick import" that breaks the layering.

**The solution:** Declare the architecture in `.reveal.yaml`:

```yaml
architecture:
  layers:
    - name: core
      path: src/reveal/core/**
      description: "Orchestration and coordination"
      can_import:
        - adapters/**
        - renderers/**
        - rules/**

    - name: adapters
      path: src/reveal/adapters/**
      description: "Data fetching (AST, files, environment)"
      cannot_import:
        - renderers/**    # Adapters don't display
        - rules/**        # Adapters don't validate

    - name: renderers
      path: src/reveal/renderers/**
      description: "Data display logic"
      cannot_import:
        - adapters/**     # Renderers don't fetch
        - rules/**        # Renderers don't validate
```

Now when I run `reveal . --check`, the tool validates its own architecture:

```bash
$ reveal src/ --check

✓ Architecture validation passed
  - All layers respect import boundaries
  - 0 violations detected

Core: 12 files, 2,847 lines
Adapters: 8 files, 1,923 lines
Renderers: 6 files, 1,456 lines
Rules: 14 files, 2,103 lines
```

**The meta moment:** A tool that checks code architecture, checking its own architecture, using configuration as semantic contract.

If it violates the architecture I declared, **it fails its own quality check**. The configuration isn't documentation. It's proof.

---

## The URI Adapter Pattern: Composable Semantics

Configuration becomes even more powerful when combined with **queryable domain knowledge**.

Reveal uses a URI scheme pattern (`python://`, `ast://`, `json://`) that lets you query code like a database. Configuration extends this with project-specific semantics:

```yaml
semantic:
  custom_patterns:
    - name: uses_stripe_api
      description: "Functions that call Stripe payment API"
      patterns:
        - "stripe\\..*\\("
        - "StripeClient"

    - name: sends_email
      description: "Functions that send email"
      patterns:
        - "send.*email"
        - "EmailMessage"
        - "smtp\\."
```

**Now these become first-class queryable semantics:**

```bash
# Find all code that touches payments
reveal 'semantic://app?uses_stripe_api'

# Find all email-sending code
reveal 'semantic://app?sends_email'
```

**The power:** Domain-specific knowledge that was tribal ("ask Sarah, she knows where payment code is") becomes **explicit, queryable infrastructure**.

This is what "semantic contract" means. You're not just configuring behavior. You're **declaring what patterns mean in your domain**, and tools can query that meaning.

---

## Entry Points as First-Class Concept

Modern frameworks use **implicit invocation**—decorators, dependency injection, event handlers. This breaks dead code detection because tools don't understand "framework magic."

Example: FastHTML route handlers

```python
@app.route("/login")
def login_page():
    return Form(...)
```

Is `login_page()` dead code? It's never explicitly called in the codebase. But the framework invokes it via the `@app.route` decorator.

**Traditional tools see:** Unused function (false positive)
**Reveal with semantic config sees:** Entry point (framework invocation)

```yaml
ast:
  entry_points:
    - pattern: "@app\\.(route|get|post)"
      description: "FastHTML route handlers"
      languages: [python]

    - pattern: "@click\\.command"
      description: "Click CLI commands"
      languages: [python]

    - pattern: "def test_"
      description: "Pytest test functions"
      languages: [python]
```

Now the tool understands your framework. What was "magic" becomes **declared semantic contract**.

**Generalization:** Any implicit invocation pattern can be declared:
- React hooks (`useEffect`, `useState`)
- Event handlers (`addEventListener`, Vue lifecycle)
- Dependency injection (`@Injectable`, Spring beans)
- Plugin systems (Jupyter kernels, VSCode extensions)

You teach the tool your domain. The tool validates using your semantics.

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

**Example from a real code review:**

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

## Try It: Reveal v0.26+

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
      path: app/routes/**
      cannot_import: [repositories/**]

    - name: services
      path: app/services/**

quality:
  max_function_lines: 100
EOF

# Now validate architecture
reveal src/ --check               # Enforces your rules

# Query custom semantics
reveal 'semantic://app?complexity>10'
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

**Current Version:** Reveal v0.24.0 (v0.26+ with full configuration support coming soon)
**License:** MIT
**Maintained by:** Scott Senkeresty, Semantic Infrastructure Lab

---

*This article was written using Reveal to explore Reveal's own codebase—progressive disclosure in practice. Configuration as semantic contract isn't theory. It's how we build.*
