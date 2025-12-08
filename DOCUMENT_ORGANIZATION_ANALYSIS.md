# SIL Website - Document Organization Analysis
**Date**: 2025-12-07
**Purpose**: Identify core "lab founding documents" and reorganize for maximum impact

---

## Current State: 20 Canonical Documents

Total words: 50,328 across 20 documents in `/docs/canonical/`

**Problem**: All documents presented as flat list with no hierarchy or priority signaling.

---

## Proposed Organization: 3-Tier Hierarchy

### **Tier 1: Lab Founding Documents** (The Essence of SIL)
*What every visitor should read to understand SIL*

**Priority**: Highlight these prominently on homepage and docs index

1. **START_HERE** (628 words) - *Entry point for all visitors*
   - Current visibility: Buried alphabetically
   - **Action**: Make this the TOP item, always visible
   - Purpose: Orients visitors and directs to relevant paths

2. **FOUNDERS_LETTER** (604 words) - *The personal story and mission*
   - Current use: Already homepage content ✓
   - Keep as homepage, also feature in docs
   - Purpose: "Why SIL exists" in human terms

3. **SIL_MANIFESTO** (3,084 words) - *The core vision and positioning*
   - Critical document establishing the "wood → steel" thesis
   - Purpose: Problem statement + existence proof + declaration
   - **Action**: Feature after Founder's Letter

4. **SIL_PRINCIPLES** (1,582 words) - *The 14 guiding constraints*
   - Concise statement of what guides all work
   - Purpose: Design constraints that define SIL's approach
   - **Action**: Pair with Manifesto as "vision + principles"

5. **SIL_STEWARDSHIP_MANIFESTO** (2,186 words) - *How we operate and collaborate*
   - Defines the lab's operational philosophy
   - Purpose: Transparency, attribution, human-agent collaboration model
   - **Action**: Include in founding set

6. **FOUNDER_PROFILE** (1,452 words) - *Who leads this lab*
   - Personal background and architectural philosophy
   - Purpose: Establish credibility and perspective
   - **Action**: Link from Founder's Letter

**Subtotal**: ~9,536 words across 6 core documents

**Visual Treatment**:
- Separate section: "Lab Founding Documents"
- Larger cards with descriptions
- Numbered or otherwise emphasized
- Always appear first

---

### **Tier 2: System Architecture** (What SIL Builds)
*The technical foundation - for builders and researchers*

**Priority**: Featured section, but secondary to founding docs

7. **SIL_SEMANTIC_OS_ARCHITECTURE** (3,017 words) - *The 6-layer stack*
   - Core architectural framework
   - Purpose: System overview and layer responsibilities
   - **Highlight**: Diagram-driven, accessible entry point

8. **SIL_TECHNICAL_CHARTER** (3,720 words) - *Formal specification*
   - Detailed technical specification
   - Purpose: Reference doc for implementers
   - **Tag**: "Advanced/Reference"

9. **SIL_DESIGN_PRINCIPLES** (4,038 words) - *How we build*
   - The 5 deep design principles (different from the 14)
   - Purpose: Explains compositional thinking, progressive disclosure, etc.
   - **Position**: After architecture overview

10. **SIL_GLOSSARY** (2,694 words) - *Shared vocabulary (108 terms)*
    - Essential reference
    - Purpose: Canonical definitions
    - **Action**: Always linkable, possibly sidebar

**Subtotal**: ~13,469 words across 4 documents

**Visual Treatment**:
- Section: "System Architecture & Design"
- Medium emphasis
- Include architecture diagram
- Cross-link heavily

---

### **Tier 3: Research Output** (Technical Innovations)
*Published research and technical depth - for specialists*

**Priority**: Available but de-emphasized, organized by theme

**Theme A: Multi-Agent Systems**
11. **HIERARCHICAL_AGENCY_FRAMEWORK** (3,625 words)
12. **MULTI_AGENT_PROTOCOL_PRINCIPLES** (1,785 words)
13. **FOUNDERS_NOTE_MULTISHOT_AGENT_LEARNING** (2,641 words)

**Theme B: Observability & Safety**
14. **SEMANTIC_OBSERVABILITY** (4,293 words)
15. **SEMANTIC_FEEDBACK_LOOPS** (3,574 words)
16. **SIL_SAFETY_THRESHOLDS** (2,621 words)
17. **SIL_TOOL_QUALITY_MONITORING** (2,394 words)

**Theme C: Interface Design**
18. **PROGRESSIVE_DISCLOSURE_GUIDE** (3,119 words)

**Theme D: Roadmap**
19. **SIL_RESEARCH_AGENDA_YEAR1** (2,431 words)

**Overflow**:
20. **README** (840 words) - Likely redundant with START_HERE

**Subtotal**: ~27,323 words across 10 documents

**Visual Treatment**:
- Section: "Research Output & Technical Papers"
- Organized by theme (collapsible sections?)
- Smaller cards
- "For specialists" messaging
- Consider: Only show titles, expand on click

---

## Recommended Homepage Changes

### Current Homepage
- Shows: Founder's Letter (full content)
- Navigation: Sidebar with all 20+ docs

### Proposed Homepage

**Hero Section**:
```
Semantic Infrastructure Lab
Building the semantic substrate for intelligent systems

[Founder's Letter excerpt - first 3 paragraphs]

[Read More] [View Projects →] [Read Founding Documents →]
```

**Featured: Lab Founding Documents** (6 cards):
```
┌─────────────────────────────────────────────────┐
│ 1. START HERE                          628 words│
│ Your entry point to understanding SIL           │
│ [Read →]                                        │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 2. MANIFESTO                         3,084 words│
│ Why explicit meaning matters (15 min)           │
│ [Read →]                                        │
└─────────────────────────────────────────────────┘

[... 4 more cards for other founding docs]
```

**System Architecture** (4 cards, smaller):
- Semantic OS Architecture
- Technical Charter
- Design Principles
- Glossary

**Research Output** (collapsed by default):
```
▶ Multi-Agent Systems (3 papers)
▶ Observability & Safety (4 papers)
▶ Interface Design (1 paper)
▶ Research Roadmap (1 doc)
```

---

## Docs Index Page Changes

### Current: `/docs`
- Flat list of 24 documents
- Alphabetical order
- No hierarchy or priority

### Proposed: `/docs`

**Layout**: 3 clear sections with visual hierarchy

```markdown
# SIL Documentation

## Lab Founding Documents
*Essential reading to understand what SIL is and why it matters*

[Large, prominent cards for 6 founding docs]

---

## System Architecture
*Technical foundation for builders and researchers*

[Medium cards for 4 architecture docs]

---

## Research Output & Technical Papers
*Published research organized by theme*

### Multi-Agent Systems
- Hierarchical Agency Framework (3,625 words)
- Multi-Agent Protocol Principles (1,785 words)
- Founder's Note on Multishot Agent Learning (2,641 words)

### Observability & Safety
- Semantic Observability (4,293 words)
- Semantic Feedback Loops (3,574 words)
- Safety Thresholds & HITL Patterns (2,621 words)
- Tool Quality Monitoring (2,394 words)

### Interface Design
- Progressive Disclosure Guide (3,119 words)

### Research Roadmap
- Year 1 Research Agenda (2,431 words)
```

---

## Sidebar Navigation Changes

### Current Sidebar
7 top-level sections, many items:
- Start Here (3 items)
- The Lab (3 items)
- Research Output (8 items)
- Production Systems (9 items)
- Architecture (3 items)
- Design Philosophy (5 items)
- Acknowledgments (3 items)

### Proposed Sidebar

**Simplified to 4 sections**:

```
┌─────────────────────────────────┐
│ FOUNDING DOCUMENTS              │
│  • Start Here                   │
│  • Founder's Letter             │
│  • Manifesto                    │
│  • Principles (14)              │
│  • Stewardship Manifesto        │
│  • Founder Profile              │
│                                 │
│ SYSTEM ARCHITECTURE             │
│  • Semantic OS (6 layers)       │
│  • Technical Charter            │
│  • Design Principles (5)        │
│  • Glossary (108 terms)         │
│                                 │
│ RESEARCH PAPERS ▼               │
│  [Collapsed by default]         │
│                                 │
│ PROJECTS & TOOLS                │
│  • All Projects                 │
│  • Production Systems (5)       │
│  • Research Projects (7)        │
└─────────────────────────────────┘
```

---

## Priority Recommendations

### P0 - Immediate (Do First)
1. **Reorder `/docs` index** to show founding documents first
2. **Add "Lab Founding Documents" header** with description
3. **Move START_HERE to top** of every list
4. **Group research papers** by theme (collapsible)

### P1 - High Priority (This Week)
5. **Update sidebar navigation** to reflect new hierarchy
6. **Add section descriptions** to each tier
7. **Visual styling**: Larger cards for Tier 1, smaller for Tier 3
8. **Update homepage** to feature founding documents

### P2 - Nice to Have (Next Week)
9. **Reading paths**: "If you're new...", "If you're a researcher...", etc.
10. **Estimated reading times** on all document cards
11. **Dependency hints**: "Read Manifesto before Technical Charter"
12. **Progress tracking**: Check boxes for "I've read this"

---

## Files to Modify

### Code Changes:
1. `src/sil_web/services/content.py` - Add document tier/priority metadata
2. `src/sil_web/routes/pages.py` - Update `/docs` route to group by tier
3. `templates/docs_index.html` - New template with hierarchy
4. `src/sil_web/ui/components.py` - Add `document_tier_section()` component
5. `static/css/style.css` - Styling for tiered document cards

### Content Changes:
None - all markdown files stay as-is, only presentation changes

---

## Success Metrics

**Before**:
- 20 documents, flat list
- No clear entry point
- Research papers same prominence as founding docs
- Visitors don't know where to start

**After**:
- 3-tier hierarchy (6 founding, 4 architecture, 10 research)
- START_HERE always first
- Founding documents prominently featured
- Clear reading paths for different audiences
- Research papers organized by theme, de-emphasized

---

## Next Steps

1. **Review this analysis** - Confirm the 3-tier categorization
2. **Approve founding doc set** - Are these the right 6 documents?
3. **Implement P0 changes** - Reorder docs index
4. **Test on staging** - Verify new organization improves clarity
5. **Deploy to production** - Launch improved site

---

**Questions for Scott**:

1. Do these 6 documents feel like the right "founding set"?
2. Should README.md be merged into START_HERE (seems redundant)?
3. Any research papers that should be promoted to Tier 2?
4. Should Glossary be always-visible (sidebar) or inline with architecture?
5. Timeline for implementing these changes?
