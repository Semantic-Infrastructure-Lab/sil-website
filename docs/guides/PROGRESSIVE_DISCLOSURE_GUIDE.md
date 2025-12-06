---
title: "Progressive Disclosure in SIL"
subtitle: "Orient → Navigate → Focus: Managing Complexity Through Layered Revelation"
category: guide
project: SIL
tags: [progressive-disclosure, design-pattern, user-experience, architecture]
author: TIA
created: 2025-12-04
beth_topics: [progressive-disclosure, reveal, beth, architecture, user-experience]
quality:
  completeness: 98
  accuracy: 99
  freshness: 100
  practical_value: 99
related_docs:
  - projects/SIL/docs/SIL_CORE_PRINCIPLES.md
  - projects/SIL/docs/KNOWLEDGE_MESH_QUALITY_IMPERATIVE.md
---

# Progressive Disclosure in SIL

**The art of showing just enough, just when it's needed**

Version: 1.0
Last Updated: 2025-12-04

---

## Table of Contents

1. [What is Progressive Disclosure?](#what-is-progressive-disclosure)
2. [Why It's SIL's #1 Principle](#why-its-sils-1-principle)
3. [The Three Levels](#the-three-levels)
4. [Implementation Across SIL](#implementation-across-sil)
5. [Design Patterns](#design-patterns)
6. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
7. [Measuring Success](#measuring-success)
8. [Building Progressive Disclosure Into New Tools](#building-progressive-disclosure-into-new-tools)

---

## What is Progressive Disclosure?

**Definition**: Progressive Disclosure is the practice of presenting information in layers, from high-level overview to detailed specifics. Users and agents only see what they need, when they need it.

**Core Insight**: Human and AI agents can only process so much information at once. By revealing information progressively, we:
- Reduce cognitive load
- Improve comprehension
- Enable faster navigation
- Support both quick scans and deep dives

**The Metaphor**: Like zooming a map:
- **Zoom out**: See continents and countries (orientation)
- **Zoom in**: See cities and roads (navigation)
- **Zoom close**: See buildings and details (focus)

---

## Why It's SIL's #1 Principle

### The Scale Problem

SIL's knowledge mesh indexes **13,549 files** with **33,752 keywords**. Without Progressive Disclosure:

```
User asks: "How does deployment work?"

System could return:
- 47 deployment documents (complete text)
- 320KB of content
- 85,000 tokens
- Overwhelming, unusable
```

With Progressive Disclosure:

```
User asks: "How does deployment work?"

LEVEL 1: Top 10 most relevant documents (titles + summaries)
→ 2KB, 500 tokens, scannable in 15 seconds

User picks one:
LEVEL 2: Document outline (sections, key points)
→ 5KB, 1,200 tokens, scannable in 30 seconds

User finds relevant section:
LEVEL 3: Full section content
→ 15KB, 4,000 tokens, complete information
```

**Result**:
- 85,000 tokens → 5,700 tokens (15x reduction)
- User found answer in <2 minutes instead of overwhelming dump

### The Discovery Problem

Progressive Disclosure enables **exploration without drowning**:

```
User doesn't know: "I need to understand error handling patterns"

LEVEL 1: reveal file.py
→ Shows: 15 functions exist, 3 relate to errors

LEVEL 2: reveal file.py --outline
→ Shows: handle_error(), log_error(), retry_on_failure()

LEVEL 3: reveal file.py handle_error
→ Shows: Complete implementation of handle_error()
```

**Without Progressive Disclosure**: User gets all 500 lines, must manually parse.

**With Progressive Disclosure**: User navigates naturally from overview → specifics.

---

## The Three Levels

### LEVEL 1: ORIENT
**"Where am I? What exists?"**

**Purpose**: Establish context, show landscape, provide entry points

**Characteristics**:
- High-level summaries
- Breadth over depth
- Quick scan (5-15 seconds)
- Minimal details

**Examples**:
```bash
# Code structure
reveal app.py
# Output: Classes, functions, imports (no implementations)

# Project overview
tia project list
# Output: All projects with one-line summaries

# Knowledge search
tia beth explore "authentication"
# Output: Top 10 results, titles + one-line summaries

# File search
tia search all "pytest"
# Output: File paths that match, no content
```

**Design Pattern**:
- Show **what exists**, not **what it contains**
- Provide **landmarks**, not **details**
- Enable **quick scanning**, not **deep reading**

---

### LEVEL 2: NAVIGATE
**"What's relevant to my goal?"**

**Purpose**: Follow breadcrumbs, narrow focus, identify targets

**Characteristics**:
- Structure and organization
- Section headers, signatures
- Moderate detail
- Drill-down hints

**Examples**:
```bash
# Code hierarchy
reveal app.py --outline
# Output: Hierarchical structure, function signatures

# Project details
tia project show SIL
# Output: Metadata, directory structure, key files

# Knowledge clusters
tia beth explore "authentication" --depth 2
# Output: + Related topics, knowledge clusters

# File content structure
tia search content "authentication" --outline
# Output: Files + section headers where pattern appears
```

**Design Pattern**:
- Show **structure**, not **implementation**
- Provide **organization**, not **full content**
- Enable **navigation**, not **reading**

---

### LEVEL 3: FOCUS
**"Get the specific details I need"**

**Purpose**: Deep dive on target, complete context on narrow scope

**Characteristics**:
- Full implementation
- Complete details
- Narrow focus
- Maximum depth

**Examples**:
```bash
# Specific function
reveal app.py authenticate_user
# Output: Complete function implementation

# Full document
tia read docs/DEPLOYMENT_GUIDE.md
# Output: Complete file content

# Specific search results
tia search content "def authenticate" --context 10
# Output: Matching lines + 10 lines before/after

# Deep knowledge exploration
tia session read <session-id>
# Output: Complete session transcript
```

**Design Pattern**:
- Show **everything** about **one thing**
- Provide **complete context** on **narrow scope**
- Enable **deep understanding**, not **broad scanning**

---

## Implementation Across SIL

### reveal (Code Structure)

**The Gold Standard** - reveal perfectly implements Progressive Disclosure:

**LEVEL 1: Orient**
```bash
$ reveal src/scout.py

File: src/scout.py

Classes: Scout, ScoutConfig, ResearchResult
Functions: main(), run_research(), validate_config()
Imports: groqqy, anthropic, json, yaml

Lines: 487 | Complexity: Medium
```
→ User learns: Structure exists, what components are present
→ Tokens: ~50 vs 7,500 for full file

**LEVEL 2: Navigate**
```bash
$ reveal src/scout.py --outline

File: src/scout.py

Classes (3):
  Scout (src/scout.py:45)
    ├─ __init__(self, config)
    ├─ run_research(self, topic)
    ├─ _validate_phase(self, phase)
    └─ _save_results(self, results)

  ScoutConfig (src/scout.py:12)
    └─ from_yaml(cls, path)

  ResearchResult (src/scout.py:156)
    └─ to_dict(self)

Functions (3):
  main() (src/scout.py:420)
  run_research(topic, config_path) (src/scout.py:385)
  validate_config(config) (src/scout.py:350)
```
→ User learns: Hierarchy, relationships, organization
→ Tokens: ~200 vs 7,500

**LEVEL 3: Focus**
```bash
$ reveal src/scout.py run_research

def run_research(topic: str, config_path: str = "scout_config.yaml") -> ResearchResult:
    """
    Execute a Scout research campaign on the given topic.

    Args:
        topic: Research topic to investigate
        config_path: Path to Scout configuration file

    Returns:
        ResearchResult containing findings and artifacts
    """
    config = ScoutConfig.from_yaml(config_path)
    scout = Scout(config)
    return scout.run_research(topic)
```
→ User learns: Exact implementation of this function
→ Tokens: ~150 (just what's needed)

**Progressive Flow**:
```
User journey: "How does Scout work?"
1. reveal src/scout.py → See overall structure
2. reveal src/scout.py --outline → See Scout class methods
3. reveal src/scout.py Scout.run_research → See implementation
4. Now understands Scout architecture in 3 steps
```

---

### Beth (Knowledge Mesh)

**LEVEL 1: Orient**
```bash
$ tia beth explore "deployment"

🔍 Beth Topic Explorer
Topic: deployment

Strongest Matches (10):
  19.5  projects/tia-server/DEPLOYMENT_GUIDE.md
        "Complete deployment guide for TIA server"
  15.3  sessions/blazing-ghost-1202/nginx-patterns.md
        "Nginx configuration patterns for production"
  [8 more results...]

Related Topics: docker, systemd, nginx
```
→ User learns: What deployment docs exist
→ Tokens: ~300

**LEVEL 2: Navigate**
```bash
$ tia beth explore "deployment" --depth 2

Topic: deployment (47 docs, 2 hops)

Knowledge Clusters:
  projects (12 docs, 45 connections)
    ├─ tia-server deployment
    ├─ squaroids deployment
    └─ sil-website deployment

  sessions (35 docs, 78 connections)
    ├─ Nginx configurations
    ├─ Systemd services
    └─ Docker patterns

Related Topics (depth 2):
  deployment → docker → containers → orchestration
  deployment → systemd → process-management
  deployment → nginx → reverse-proxy → ssl
```
→ User learns: How deployment topics relate
→ Tokens: ~800

**LEVEL 3: Focus**
```bash
$ tia read projects/tia-server/DEPLOYMENT_GUIDE.md
# (Full document content)
```
→ User learns: Complete deployment guide
→ Tokens: 4,000-8,000

---

### tia search (Content Discovery)

**LEVEL 1: Orient**
```bash
$ tia search all "authentication"

Beth Results (5):
  docs/AUTH_GUIDE.md
  src/auth/manager.py
  [3 more...]

Path Results (8):
  src/auth/
  tests/auth/
  [6 more...]
```
→ User learns: Where authentication code/docs exist
→ Tokens: ~200

**LEVEL 2: Navigate**
```bash
$ tia search content "def authenticate"

src/auth/manager.py:45
src/auth/oauth.py:89
src/auth/session.py:112
tests/auth/test_manager.py:23
```
→ User learns: Specific locations of authenticate functions
→ Tokens: ~100

**LEVEL 3: Focus**
```bash
$ tia search content "def authenticate" --context 10

src/auth/manager.py:45
    35  class AuthManager:
    36      """Manages authentication and authorization"""
    ...
    45      def authenticate(self, username: str, password: str) -> User:
    46          """Authenticate user with credentials"""
    47          hashed = self._hash_password(password)
    48          user = self.db.get_user(username)
    ...
    55          return user
```
→ User learns: Complete context around authenticate function
→ Tokens: ~500 per match

---

### Examples Demonstrate Progressive Disclosure

**Key Insight**: Examples themselves follow progressive disclosure - they show patterns at increasing detail levels.

**Connection to SIL Core Principles #9**: "Examples as Multi-Shot Reasoning Anchors"

**LEVEL 1: Simple Example (Orient)**
```bash
# Show the pattern
reveal app.py  # Structure only
```
→ User learns: What the tool does in simplest form

**LEVEL 2: Workflow Example (Navigate)**
```bash
# Show the progression
Step 1: reveal app.py              → See structure (50 tokens)
Step 2: reveal app.py --outline    → Hierarchical view
Step 3: reveal app.py func_name    → Extract specific function
```
→ User learns: How to navigate through detail levels

**LEVEL 3: Detailed Example (Focus)**
```bash
# Show concrete use case
$ reveal src/scout.py Scout.run_research

def run_research(topic: str, config_path: str = "scout_config.yaml") -> ResearchResult:
    """Execute a Scout research campaign on the given topic."""
    config = ScoutConfig.from_yaml(config_path)
    scout = Scout(config)
    return scout.run_research(topic)
```
→ User learns: Exact implementation with full context

**Why This Works**:
- Examples follow the same progressive pattern as the tools they demonstrate
- Each level adds detail without repeating previous levels
- Users can stop at any level where they have enough information
- Concrete examples ground understanding better than abstract descriptions

**Application**: When documenting SIL tools, structure examples progressively:
1. **Quick example** - One-liner showing basic usage
2. **Workflow example** - Multi-step showing typical patterns
3. **Complete example** - Full context with edge cases

See: [SIL Core Principles #9: Examples as Multi-Shot Reasoning Anchors](SIL_CORE_PRINCIPLES.md#9-examples-as-multi-shot-reasoning-anchors)

---

### Documentation Hierarchy

**LEVEL 1: Orient (README)**
```markdown
# SIL - Semantic Infrastructure Lab

Core semantic layer for cognitive architecture

## Quick Links
- [Documentation Index](docs/INDEX.md)
- [Getting Started](docs/GETTING_STARTED.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
```
→ User learns: What SIL is, where to go next
→ Read time: 30 seconds

**LEVEL 2: Navigate (Index)**
```markdown
# Documentation Index

## Core Concepts
- [SIL Core Principles](docs/SIL_CORE_PRINCIPLES.md)
- [Progressive Disclosure](docs/PROGRESSIVE_DISCLOSURE.md)

## Guides
- [Deployment Guide](docs/guides/DEPLOYMENT.md)
- [Development Setup](docs/guides/SETUP.md)

## Reference
- [API Documentation](docs/reference/API.md)
```
→ User learns: Documentation structure, picks relevant guide
→ Read time: 2 minutes

**LEVEL 3: Focus (Detailed Guide)**
```markdown
# Complete Deployment Guide

(Full detailed content with examples, commands, troubleshooting...)
```
→ User learns: Complete deployment process
→ Read time: 15-30 minutes

---

## Design Patterns

### Pattern 1: Default to Summary, Opt-In to Detail

```bash
# Default = compact
tia project list
# Shows: Project names + one-line summaries

# Opt-in = detail
tia project show <name>
# Shows: Full project metadata

# Opt-in = maximum detail
cd /path/to/project
# Shows: Everything in context
```

**Rule**: Never dump everything by default. Make detail opt-in.

---

### Pattern 2: Breadcrumbs to Next Level

Every Level 1/2 output should hint at how to reach Level 3:

```bash
$ reveal app.py

File: app.py
Functions: authenticate(), validate(), process()

Next: reveal app.py <function>    # Extract specific element
      reveal app.py --outline     # Hierarchical view
      reveal app.py --code        # Extract all code blocks
```

**Rule**: Guide users toward deeper exploration.

---

### Pattern 3: Consistent Flags Across Tools

```bash
# Consistent pattern
<tool> <target>              # Level 1: Summary
<tool> <target> --outline    # Level 2: Structure
<tool> <target> --full       # Level 3: Everything
```

**Current SIL Tools**:
- `reveal file.py` → `reveal file.py --outline`
- `tia beth explore` → `tia beth explore --depth 2`
- `tia search all` → `tia search content` → `tia read`

**Opportunity**: Standardize `--outline`, `--summary`, `--full` flags across all tools.

---

### Pattern 4: Context-Aware Detail Level

Adjust detail based on context:

```python
# Few results = more detail per result
if len(results) <= 5:
    show_expanded_summaries(results)

# Many results = less detail per result
elif len(results) > 20:
    show_compact_list(results)
```

**Example**:
```bash
$ tia search all "xyzabc123"  # Rare term
# Result: 2 files found
# Shows: Detailed context for each

$ tia search all "def"         # Common term
# Result: 847 files found
# Shows: File paths only (avoid overwhelming)
```

---

### Pattern 5: Progressive Context in Errors

Even error messages use Progressive Disclosure:

```bash
# Level 1: What went wrong
Error: Failed to connect to database

# Level 2: Why it went wrong (with --verbose)
Error: Failed to connect to database
Cause: Connection timeout after 30s
Host: localhost:5432

# Level 3: How to fix it (with --debug)
Error: Failed to connect to database
Cause: Connection timeout after 30s
Host: localhost:5432
Config: /home/user/.tia/config.yaml
Suggestion: Check if PostgreSQL is running: systemctl status postgresql
Debug log: /tmp/tia-debug-12345.log
```

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Information Dump

```bash
# BAD: Dumps everything by default
$ show-code app.py
# (Prints all 500 lines to terminal)
```

**Why it's bad**: Overwhelming, unusable, no context

**Fix**:
```bash
# GOOD: Summary first, detail on demand
$ reveal app.py          # Structure only
$ reveal app.py func     # Specific function
```

---

### ❌ Anti-Pattern 2: No Navigation Path

```bash
# BAD: Dead-end output
$ find-docs "topic"
Here are 47 documents about topic.
# (No guidance on what to do next)
```

**Why it's bad**: User doesn't know how to proceed

**Fix**:
```bash
# GOOD: Provide next steps
$ tia beth explore "topic"
Found 47 documents.

Top 10 matches: (shows list)

Next:
  tia read <file>               # Read specific document
  tia beth explore "topic" --depth 2    # Explore related topics
```

---

### ❌ Anti-Pattern 3: All-or-Nothing

```bash
# BAD: Only two modes exist
$ tool query
# (Shows 1-line summary, not enough info)

$ tool query --verbose
# (Shows everything, too much info)
```

**Why it's bad**: No middle ground for navigation

**Fix**:
```bash
# GOOD: Three levels
$ tool query              # Summary
$ tool query --outline    # Structure
$ tool query --full       # Everything
```

---

### ❌ Anti-Pattern 4: Inconsistent Levels

```bash
# BAD: Different tools use different patterns
$ tool-a summary          # Level 1
$ tool-b --compact        # Level 1 (different flag)
$ tool-c list             # Level 1 (different command)
```

**Why it's bad**: Users must learn each tool separately

**Fix**:
```bash
# GOOD: Consistent patterns
$ tool-a <target>              # Level 1
$ tool-b <target>              # Level 1
$ tool-c <target>              # Level 1

$ tool-a <target> --outline    # Level 2
$ tool-b <target> --outline    # Level 2
$ tool-c <target> --outline    # Level 2
```

---

### ❌ Anti-Pattern 5: No Context Awareness

```bash
# BAD: Same output regardless of result count
$ search "rare-term"
# 2 results found
# Shows: Just file paths (user needs more context!)

$ search "common-term"
# 847 results found
# Shows: Full content for all (overwhelming!)
```

**Fix**:
```bash
# GOOD: Adjust detail based on count
$ search "rare-term"
# 2 results found (showing full context for each)

$ search "common-term"
# 847 results found (showing paths only)
# Use --limit or refine query
```

---

## Measuring Success

### Quantitative Metrics

**Context Reduction**:
- Target: 20x-30x reduction from full dump
- Measure: Avg tokens in Level 1 vs Level 3
- SIL Achievement: 25x average reduction

**Navigation Efficiency**:
- Target: 80% of users find answer in <3 steps
- Measure: User actions from query → answer
- Steps: Level 1 → Level 2 → Level 3 → Done

**Response Time**:
- Target: Level 1 responses <2 seconds
- Measure: Time from command → output
- SIL Achievement: <1s for most Level 1 queries

**Drill-Down Depth**:
- Target: Max 3 levels to reach any detail
- Measure: Longest path from overview → specifics
- SIL Achievement: 3 levels max (Orient → Navigate → Focus)

### Qualitative Metrics

**User Feedback Signals**:
- ✅ "I found it immediately"
- ✅ "Didn't need to read everything"
- ✅ "The outline showed me exactly where to look"
- ❌ "I had to read through tons of output"
- ❌ "I couldn't find where to go next"

**Developer Experience**:
- New users productive quickly (good Level 1 summaries)
- Power users access details efficiently (good Level 3 extraction)
- AI agents use outline modes naturally (good structure)

**Documentation Quality**:
- README → Index → Guide structure is clear
- Users can navigate without asking
- Breadcrumbs work (users follow suggested paths)

---

## Building Progressive Disclosure Into New Tools

### Checklist for New Tool Development

When building a new SIL tool:

- [ ] **Level 1 (Orient)**: Does it show summary/structure by default?
- [ ] **Level 2 (Navigate)**: Is there an `--outline` or intermediate mode?
- [ ] **Level 3 (Focus)**: Can users extract specific elements?
- [ ] **Breadcrumbs**: Does output hint at next steps?
- [ ] **Consistency**: Does it match patterns of other SIL tools?
- [ ] **Context-Aware**: Does detail level adjust based on result count?
- [ ] **Performance**: Is Level 1 fast (<2s)?
- [ ] **Testing**: Do you have tests for all three levels?

### Template Pattern

```python
class NewTool:
    def execute(self, target: str, level: str = "summary"):
        """Progressive Disclosure template"""

        if level == "summary":  # LEVEL 1
            return self._summarize(target)

        elif level == "outline":  # LEVEL 2
            return self._outline(target)

        elif level == "full":  # LEVEL 3
            return self._full_detail(target)

    def _summarize(self, target):
        """High-level overview - fast, compact"""
        # Show: What exists, key metrics
        # Omit: Implementation details
        pass

    def _outline(self, target):
        """Structure and organization - navigable"""
        # Show: Headers, signatures, hierarchy
        # Omit: Full implementations
        pass

    def _full_detail(self, target):
        """Complete information - focused scope"""
        # Show: Everything about this specific target
        # Omit: Unrelated details
        pass
```

### CLI Interface Pattern

```bash
# Command structure
tool <target>                # Level 1: Summary (default)
tool <target> --outline      # Level 2: Structure
tool <target> --full         # Level 3: Everything

# Optional: Element extraction
tool <target> <element>      # Level 3: Specific element

# Optional: Depth control
tool <target> --depth 2      # Control navigation depth
```

### Documentation Pattern

```markdown
# Project README (Level 1)
- What it is (1-2 sentences)
- Quick links to docs

## docs/INDEX.md (Level 2)
- Categories of documentation
- Brief description of each guide
- Links to detailed docs

### docs/guides/TOPIC.md (Level 3)
- Complete detailed guide
- Examples, commands, troubleshooting
```

---

## Conclusion

Progressive Disclosure is not just a UI pattern - it's a **cognitive architecture principle** that enables humans and AI agents to navigate complexity at scale.

**The SIL Way**:
1. **Orient first**: Show the landscape before the details
2. **Navigate efficiently**: Provide structure, not raw dumps
3. **Focus precisely**: Drill down to exactly what's needed

**Why it works**:
- Reduces cognitive load (manageable chunks)
- Improves comprehension (context before details)
- Enables exploration (breadcrumbs guide discovery)
- Scales beautifully (works for 10 files or 10,000)

**Tools that nail it**:
- **reveal**: The gold standard for code exploration
- **Beth**: Semantic search that doesn't overwhelm
- **tia search**: Layered discovery from paths → content

**Next tool you build**: Ask yourself at every step:
> "Am I showing too much, too soon?"

If yes, add Progressive Disclosure.

---

## Related Documentation

- [SIL Core Principles](SIL_CORE_PRINCIPLES.md) - Full principle hierarchy
- [Knowledge Mesh Quality Imperative](KNOWLEDGE_MESH_QUALITY_IMPERATIVE.md) - Context management
- reveal: `reveal --agent-help-full` - See Progressive Disclosure in action

---

**Version History**:
- v1.0 (2025-12-04): Initial deep-dive on Progressive Disclosure as SIL's #1 principle
