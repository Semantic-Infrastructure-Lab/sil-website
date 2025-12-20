# Beth Front Matter Guide (Internal Technical Reference)

**Audience**: TIA sessions, internal contributors
**Purpose**: Ensure documents index correctly in Beth
**Version**: 1.0
**Last Updated**: 2025-12-10

---

## Quick Reference

**Minimum viable front matter** for Beth indexing:

```yaml
---
title: Document Title
beth_topics:
  - topic1
  - topic2
---
```

**Recommended for session READMEs**:

```yaml
---
session_id: fierce-altar-1210
date: 2025-12-10
badge: "Session description [saved]"
beth_topics:
  - topic1
  - topic2
  - topic3
tags: [tag1, tag2]
related_docs:
  - path/to/related.md
project: SIL
type: documentation
---
```

---

## Field Names Beth Recognizes

**CRITICAL**: Use exact field names below. Beth's indexer is case-sensitive and field-specific.

### Tier 1: Highest Priority (3.0x weight)

#### `session_id`
**Weight**: 3.0x (highest)
**Type**: String
**Purpose**: Cross-session linking, provenance tracking

```yaml
session_id: fierce-altar-1210  # Correct
session_id: "fierce-altar-1210"  # Also correct (quotes optional)
```

**Best practices**:
- Use actual session name (from `tia session badge`)
- Lowercase, hyphen-separated
- Enables precise queries like "work from fierce-altar-1210"

---

### Tier 2: High Priority (2.5x weight)

#### `beth_topics`
**Weight**: 2.5x
**Type**: List
**Purpose**: Semantic clustering, knowledge graph topics

**⚠️ IMPORTANT**: Field name is `beth_topics` (NOT `topics`)

```yaml
# CORRECT
beth_topics:
  - beth-architecture
  - knowledge-graphs
  - front-matter-patterns

# WRONG - Beth won't index these
topics:  # ❌ Wrong field name
  - something

# WRONG - Not a list
beth_topics: single-topic  # ❌ Must be a list
```

**Best practices**:
- 3-7 topics per document
- Lowercase, hyphen-separated
- Consistent vocabulary across sessions
- Specific over general ("oauth2" > "auth")

---

### Tier 3: Medium Priority (2.0x weight)

#### `tags`
**Weight**: 2.0x
**Type**: List
**Purpose**: User-defined categorization, filtering

```yaml
tags:
  - architecture
  - production
  - reviewed
```

**Common tag categories**:
- **Type**: architecture, guide, reference, api, research
- **Status**: draft, reviewed, production, deprecated
- **Domain**: infrastructure, semantic, search, ai
- **Audience**: internal, public, advanced

**Best practices**:
- 2-4 tags per document
- Lowercase, hyphen-separated
- Use for categorical metadata (not semantic concepts)

---

### Other Important Fields

#### `related_docs`
**Weight**: N/A (affects authority scoring, not keyword matching)
**Type**: List
**Purpose**: Explicit relationship edges (knowledge graph construction)

```yaml
related_docs:
  - path/to/related.md
  - path/to/another.md
  - ../projects/SIL/docs/canonical/REVEAL_BETH_PROGRESSIVE_KNOWLEDGE_SYSTEM.md
```

**Best practices**:
- Relative or absolute paths from TIA root
- 2-10 related docs (too many dilutes authority)
- Creates bidirectional connections when both docs link to each other
- **Critical for summaries/indexes** (boosts PageRank authority)

---

#### `title`
**Weight**: 1.5x
**Type**: String
**Purpose**: Document display name (shown in search results)

```yaml
title: Beth Front Matter Guide
# OR
title: "Beth Front Matter Guide: Internal Reference"
```

**Best practices**:
- Clear, descriptive (not just filename)
- 3-10 words
- Unique across project

---

#### `summary`
**Weight**: N/A (not indexed, but displayed in results)
**Type**: String
**Purpose**: One-sentence description for search results

```yaml
summary: Technical reference for ensuring documents index correctly in Beth
```

---

#### `project`
**Weight**: N/A
**Type**: String
**Purpose**: Project affiliation (for filtering)

```yaml
project: SIL
```

Common values: `SIL`, `TIA`, `reveal`, `beth`, `infrastructure`

---

## Field Weights Hierarchy (From Code)

**Source**: `lib/beth/beth_search.py:573-667`

```python
# Relevance calculation weights:
session_id:    3.0x  # Precise cross-session linking
beth_topics:   2.5x  # Semantic topics
tags:          2.0x  # User categorization
filename:      2.0x  # File name words
title:         1.5x  # Document title (# heading)
heading:       1.0x  # Section headings (## headings)
content:       0.3x  # Word frequency in body text
```

**Quality score multiplier**:
```python
base = 0.5
if has_frontmatter: base = 0.7  # +40% for having front matter
if len(content) > 1000: base += 0.2  # +40% for substantial content
# Applied as: relevance *= (0.5 + quality_score)
```

**Authority boost** (from `related_docs` relationships):
```python
relationship_count = len(outbound_links) + len(inbound_links)
authority_boost = 0.5 + min(0.5, log10(relationship_count + 1) * 0.2)
final_score = base_relevance * authority_boost  # Up to 30% improvement
```

---

## Session README Templates

### Standard Session README

```yaml
---
session_id: session-name-1210
date: 2025-12-10
badge: "Brief description of session work [saved]"
beth_topics:
  - primary-topic
  - secondary-topic
  - related-concept
tags: [documentation, infrastructure]
related_docs:
  - ../previous-session/README.md
  - /projects/SIL/docs/relevant-doc.md
project: SIL
type: documentation
files_created: 3
previous_session: cafuno-1210
---

# Session Title

**Session**: session-name-1210
**Date**: 2025-12-10
**Duration**: ~2 hours
**Type**: [research | implementation | documentation | planning]

---

## Executive Summary

[1-2 paragraphs: what was accomplished, key deliverables]

---

## [Additional sections as needed]
```

---

### Research Gem README (High-Value Outputs)

```yaml
---
title: "Research Title: Descriptive Subtitle"
subtitle: "Context and purpose"
category: research-gems
project: SIL
tags: [research, architecture, analysis]
session_id: session-name-1204
created: 2025-12-04
author: Claude (TIA)
beth_topics:
  - search-systems
  - beth-architecture
  - knowledge-graphs
  - discovery-patterns
quality:
  completeness: 98
  accuracy: 95
  freshness: 100
  practical_value: 98
related_docs:
  - ../other-research/DOC.md
  - /projects/SIL/docs/canonical/RELATED.md
---
```

---

### Summary/Index Documents (Maximize Authority)

```yaml
---
title: Topic Overview or Documentation Index
subtitle: "Complete guide to [topic]"
category: documentation
project: SIL
beth_topics:
  - topic1
  - topic2
  - topic3
  - topic4
  - topic5
  # 5-10 topics (broad coverage)
tags: [index, overview, navigation]
related_docs:
  - doc1.md
  - doc2.md
  - doc3.md
  # ... 10-30 docs (high connection count)
summary: Complete guide to [topic] with links to all resources
---
```

**Why this works**: High topic count + high relationship count = **high authority** → ranks first in searches.

---

## Anti-Patterns (Common Mistakes)

### ❌ Wrong Field Name: `topics` instead of `beth_topics`

```yaml
# WRONG - Beth won't index this
topics:
  - something

# CORRECT
beth_topics:
  - something
```

**Impact**: Topics not indexed, semantic clustering fails, authority drops.

---

### ❌ Not a List: Single value instead of list

```yaml
# WRONG
beth_topics: single-topic

# CORRECT
beth_topics:
  - single-topic
```

**Impact**: Beth's YAML parser expects list, may skip field entirely.

---

### ❌ Malformed YAML

```yaml
---
beth_topics:
  - topic1
  - topic2
tags: [tag1, tag2  # ← Missing closing bracket
---
```

**Impact**: Entire front matter ignored (graceful degradation, but zero indexing).

**Fix**: Validate YAML before committing (use `yamllint` or `yq`).

---

###  ❌ Duplicate Front Matter

```yaml
---
title: Doc Title
---

# Some content

---
title: Another Title  # ← Second front matter block
---
```

**Impact**: Beth only parses first `---` block. Second block ignored.

---

### ❌ Front Matter Not at File Start

```markdown
# Document Title

---
beth_topics:  # ← Too late, must be at line 1
  - something
---
```

**Impact**: Beth only recognizes front matter if it **starts on line 1**.

**Fix**: Front matter must be first thing in file.

---

### ❌ Inconsistent Vocabulary

```yaml
# Session A
beth_topics: [auth, authentication, oauth]

# Session B
beth_topics: [authentication, security, login]

# Session C
beth_topics: [auth, user-auth, oauth2]
```

**Impact**: Should be one topic cluster, but fragments across 6 different terms.

**Solution**: Establish vocabulary guide, use consistent terms:
- `authentication` (canonical)
- `oauth2` (specific protocol)
- `security` (broader category)

---

## Vocabulary Guide (Common Topics)

**Standardized topics for TIA/SIL projects**:

### Search & Discovery
- `beth-architecture`
- `knowledge-graphs`
- `search-systems`
- `semantic-search`
- `discovery-patterns`

### Documentation & Tooling
- `documentation-standards`
- `front-matter-patterns`
- `progressive-disclosure`
- `agent-help-standard`
- `ai-documentation`

### Infrastructure & Systems
- `infrastructure`
- `deployment`
- `nginx-config`
- `service-registry`
- `port-management`

### AI & Agents
- `agent-orchestration`
- `multi-agent-systems`
- `tool-behavior-contracts`
- `agent-ether`
- `pantheon`

### SIL Projects
- `reveal`
- `beth`
- `morphogen`
- `genesisgraph`
- `prism`
- `pantheon`

---

## Validation Checklist

**Before committing session README**:

- [ ] Front matter starts at line 1
- [ ] Used `beth_topics` (not `topics`)
- [ ] beth_topics is a list (not single value)
- [ ] session_id matches actual session name
- [ ] 3-7 beth_topics chosen (not too few, not too many)
- [ ] Topics use consistent vocabulary
- [ ] YAML is valid (no syntax errors)
- [ ] related_docs uses valid paths
- [ ] title is descriptive and unique

**Test indexing**:
```bash
# After committing, verify Beth indexed it:
tia beth explore "[your-topic]"
# Should see your doc in results
```

---

## Debugging Beth Indexing

### Doc Not Appearing in Search?

**Check 1**: Front matter syntax
```bash
# Validate YAML
head -20 path/to/doc.md | yq eval -
# Should parse without errors
```

**Check 2**: Field names correct?
```bash
grep -A 5 "^---" path/to/doc.md | grep beth_topics
# Should see beth_topics (not "topics")
```

**Check 3**: Beth index fresh?
```bash
tia beth rebuild
# Forces full reindex
```

**Check 4**: File in Beth's search paths?
```bash
# Beth searches:
# - /home/scottsen/src/tia/docs
# - /home/scottsen/src/tia/sessions
# - /home/scottsen/src/tia/projects
# - /home/scottsen/src/projects  # All projects including SIL

# Verify file is under one of these paths
```

---

## Quality Metrics

**Beth index health** (from `tia-boot`):
```
✅ Beth index healthy (15,263 files, 38,070 keywords)
```

**Good indicators**:
- File count growing (new sessions indexed)
- Keyword count proportional to files (avg ~2.5 keywords/file)
- <400ms search latency (P95)

**Warning signs**:
- ⚠️ Stale index (run `tia beth rebuild`)
- ⚠️ File count shrinking unexpectedly
- ⚠️ Keyword count drops dramatically

---

## Advanced: Relationship Graph Analysis

**Check backlinks** (what references this doc):
```python
from lib.beth.beth_search import BethSearch

beth = BethSearch()
backlinks = beth.get_reverse_references('/path/to/doc.md')
# Returns: [{'source': 'other-doc.md', 'strength': 0.8, 'type': 'markdown_link'}, ...]
```

**Authority calculation** (conceptual):
```python
outbound = len(doc.related_docs)  # Explicit links
inbound = len(beth.get_reverse_references(doc.path))  # Backlinks
relationship_count = outbound + inbound
authority = 0.5 + min(0.5, log10(relationship_count + 1) * 0.2)
# Range: 0.5 (no relationships) to 1.0 (30+ relationships)
```

---

## Future: Automatic Front Matter Validation

**Proposed**: Pre-commit hook to validate front matter

```bash
#!/bin/bash
# .git/hooks/pre-commit

# For all modified .md files in sessions/
for file in $(git diff --cached --name-only --diff-filter=AM | grep "sessions/.*\.md$"); do
  # Check front matter starts at line 1
  if ! head -1 "$file" | grep -q "^---"; then
    echo "ERROR: $file missing front matter at line 1"
    exit 1
  fi

  # Validate YAML
  if ! head -50 "$file" | sed -n '/^---$/,/^---$/p' | yq eval - >/dev/null 2>&1; then
    echo "ERROR: $file has malformed YAML front matter"
    exit 1
  fi

  # Check for beth_topics (not topics)
  if grep -q "^topics:" "$file" && ! grep -q "^beth_topics:" "$file"; then
    echo "WARNING: $file uses 'topics:' - should be 'beth_topics:'"
  fi
done
```

---

## Related Documentation

- [Documentation Front Matter Standard](/projects/sil-website/docs/research/DOCUMENTATION_FRONT_MATTER_STANDARD) - Public specification
- [Reveal + Beth System](/projects/SIL/docs/canonical/REVEAL_BETH_PROGRESSIVE_KNOWLEDGE_SYSTEM) - Architecture overview
- [TIA Search Ecosystem](../research-gems/TIA_SEARCH_ECOSYSTEM_RESEARCH) - Beth deep dive

---

**Version History**:
- v1.0 (2025-12-10): Initial technical reference based on beth_search.py implementation
