---
title: "SIL Safety Thresholds & HITL Patterns"
subtitle: "Human-in-the-Loop Guidelines for Autonomous Operations"
category: reference
project: SIL
tags: [safety, hitl, automation, thresholds, risk-management]
author: TIA
created: 2025-12-04
beth_topics: [safety, hitl, automation, risk-management, operational-guidelines]
quality:
  completeness: 95
  accuracy: 98
  freshness: 100
  practical_value: 99
related_docs:
  - projects/SIL/docs/SIL_CORE_PRINCIPLES.md
  - templates/CLAUDE.md
---

# SIL Safety Thresholds & HITL Patterns

**Human-in-the-Loop Guidelines for Autonomous Operations**

Version: 1.0
Last Updated: 2025-12-04

---

## Table of Contents

1. [Overview](#overview)
2. [Core Philosophy](#core-philosophy)
3. [Risk Classification Framework](#risk-classification-framework)
4. [Operation Thresholds](#operation-thresholds)
5. [Approval Workflows](#approval-workflows)
6. [Autonomous Agent Guidelines](#autonomous-agent-guidelines)
7. [Audit & Logging](#audit--logging)
8. [Threshold Evolution](#threshold-evolution)

---

## Overview

As SIL builds increasingly autonomous capabilities (Scout, Agent Ether, BrowserBridge), we need clear guidelines on **what requires human approval** and **what can proceed automatically**.

**Key Principle**: High-risk decisions require human approval. Low-risk decisions proceed automatically with logging.

**This Document Defines**:
- Which TIA operations are high-risk vs low-risk
- Approval workflows for autonomous agents
- Cost/impact thresholds that trigger HITL
- Audit requirements for all operations

**Current HITL Implementation**:
TIA already implements excellent HITL patterns for git operations (see templates/CLAUDE.md):

> 🚨 **NEVER PUSH WITHOUT EXPLICIT CONSENT** 🚨
> build → test → commit → tag → **ASK** → push

This document extends that pattern to all SIL operations.

---

## Core Philosophy

### The Trust Gradient

Automation trust should evolve gradually:

```
Phase 1: Conservative (Week 1)
→ Approve: 60-80% of operations
→ Pattern: Everything new requires approval
→ Goal: Build confidence, identify edge cases

Phase 2: Moderate (Weeks 2-4)
→ Approve: 30-50% of operations
→ Pattern: Proven safe operations auto-execute
→ Goal: Reduce friction, maintain safety

Phase 3: Liberal (Month 2+)
→ Approve: 10-20% of operations
→ Pattern: Only high-risk requires approval
→ Goal: Efficient automation with safety net

Phase 4: Autonomous (Month 3+)
→ Approve: <5% of operations
→ Pattern: Rare edge cases only
→ Goal: Full automation with audit trail
```

### Safety Principles

1. **Explicit Over Automatic**: When in doubt, ask
2. **Reversible > Irreversible**: Prefer operations that can be undone
3. **Preview Before Execute**: Show what will happen
4. **Log Everything**: Complete audit trail
5. **Threshold-Based**: Clear, measurable criteria

---

## Risk Classification Framework

### Risk Dimensions

| Dimension | Low Risk | Medium Risk | High Risk |
|-----------|----------|-------------|-----------|
| **Financial** | $0 | $1-$10 | >$10 |
| **Reversibility** | Easily undone | Requires effort | Irreversible |
| **Scope** | Single file | Multiple files | System-wide |
| **External** | Internal only | External APIs | Public-facing |
| **Data** | Read-only | Modify local | Delete/publish |

### Risk Levels

**LOW RISK** (Auto-Execute):
- Read operations (no side effects)
- Local file reads
- Status checks
- Search queries
- Non-destructive analysis

**MEDIUM RISK** (Confirm First):
- Local file modifications
- External API calls (low cost)
- Session management
- Beth index rebuilds
- Configuration changes

**HIGH RISK** (Require Approval):
- Git push operations
- External API calls (high cost)
- Destructive operations (delete)
- Public-facing changes
- System-wide modifications

---

## Operation Thresholds

### Git Operations

| Operation | Risk | Requires Approval | Current Implementation |
|-----------|------|------------------|----------------------|
| `git status` | Low | ❌ No | Auto-execute |
| `git diff` | Low | ❌ No | Auto-execute |
| `git log` | Low | ❌ No | Auto-execute |
| `git add` | Medium | ⚠️ Preview changes | Show diff first |
| `git commit` | Medium | ⚠️ Preview message | Show commit plan |
| `git tag` | Medium | ⚠️ Confirm tag | Show tag details |
| `git push` | **High** | ✅ **Always** | **Explicit consent required** |
| `git push --force` | **High** | ✅ **Always + Warning** | **Strong warning** |
| `git reset --hard` | **High** | ✅ **Always** | Destructive warning |
| `tia git make-clean` | **High** | ✅ **Show 7-phase plan** | Preview all operations |

**Pattern (Already Implemented)**:
```bash
# Claude's git workflow from CLAUDE.md:
1. git status, git diff (auto)
2. git add, git commit (preview first)
3. git push (STOP and ASK user)
```

---

### Search & Discovery Operations

| Operation | Risk | Requires Approval | Notes |
|-----------|------|------------------|-------|
| `tia search all` | Low | ❌ No | Read-only |
| `tia search content` | Low | ❌ No | Read-only |
| `tia beth explore` | Low | ❌ No | Read-only |
| `tia beth rebuild` | Medium | ⚠️ If large | Preview file count |
| `tia read <file>` | Low | ❌ No | Read-only |
| `reveal <file>` | Low | ❌ No | Read-only |

**Pattern**: All read-only discovery operations are low-risk.

---

### Session Operations

| Operation | Risk | Requires Approval | Notes |
|-----------|------|------------------|-------|
| `tia session list` | Low | ❌ No | Read-only |
| `tia session context` | Low | ❌ No | Read-only |
| `tia session read` | Low | ❌ No | Read-only |
| `tia-save` | Low | ❌ No | Creates README only |
| `tia session badge` | Low | ❌ No | Updates metadata |
| Delete session >30d | Low | ❌ No | Automated cleanup |
| Delete session <30d | Medium | ⚠️ Confirm | May be active work |
| Delete session <7d | **High** | ✅ **Confirm** | Likely active |

**Pattern**: Auto-cleanup old sessions, confirm for recent ones.

---

### Project Operations

| Operation | Risk | Requires Approval | Notes |
|-----------|------|------------------|-------|
| `tia project list` | Low | ❌ No | Read-only |
| `tia project show` | Low | ❌ No | Read-only |
| `tia project add` | Medium | ⚠️ Preview | Show project.yaml |
| `tia project edit` | Medium | ⚠️ Confirm changes | Show diff |
| `tia project delete` | **High** | ✅ **Confirm** | Show what's deleted |

---

### AI/Agent Operations

| Operation | Risk | Requires Approval | Cost Threshold |
|-----------|------|------------------|----------------|
| Scout research (small) | Medium | ⚠️ Preview cost | <$2 auto |
| Scout research (large) | **High** | ✅ **Confirm** | >$2 require approval |
| Beth semantic search | Low | ❌ No | No API cost |
| Groqqy query (small) | Low | ❌ No | <$0.10 auto |
| Groqqy query (large) | Medium | ⚠️ Preview | >$0.10 confirm |
| Batch AI operations | **High** | ✅ **Confirm** | Show total cost |

**Cost-Based Thresholds**:
```python
if estimated_cost < 0.10:
    execute_auto()
elif estimated_cost < 2.00:
    preview_and_confirm()
else:
    require_explicit_approval()
```

---

### File Operations

| Operation | Risk | Requires Approval | Notes |
|-----------|------|------------------|-------|
| Read file | Low | ❌ No | No side effects |
| Create new file | Medium | ⚠️ Preview path | Show where |
| Edit existing file | Medium | ⚠️ Show diff | Preview changes |
| Delete file | **High** | ✅ **Confirm** | Show content |
| Batch edit (5+ files) | **High** | ✅ **Show plan** | List all files |
| Batch delete | **High** | ✅ **Strong confirm** | Destructive |

---

### System Operations

| Operation | Risk | Requires Approval | Notes |
|-----------|------|------------------|-------|
| `tia-boot` | Low | ❌ No | Read-only checks |
| Beth S3 sync | Medium | ⚠️ Confirm | External operation |
| Gemma self-healing | Medium | ⚠️ Show plan | Auto-repair |
| Registry auth setup | Medium | ⚠️ Confirm | System config |
| Process cleanup | Low | ❌ No | >1 day old only |

---

## Approval Workflows

### Workflow 1: Preview & Confirm

**Use When**: Medium-risk operations (file edits, config changes)

```bash
# Example: File edit
Operation: Edit config.yaml
Preview:
  File: /home/user/.tia/config.yaml
  Changes:
    - debug: false
    + debug: true

Confirm? [y/N]
```

**Implementation Pattern**:
```python
def edit_file(path, changes):
    # 1. Show diff
    print_diff(current, proposed)

    # 2. Ask confirmation
    if not confirm("Apply these changes?"):
        return "Operation cancelled"

    # 3. Execute
    apply_changes(path, changes)

    # 4. Log
    audit_log("file_edit", path, changes)
```

---

### Workflow 2: Explicit Approval Required

**Use When**: High-risk operations (git push, deletes, costly API calls)

```bash
# Example: Git push
Operation: git push origin master
Risk: HIGH - Publishes code publicly
Impact: Changes will be visible to all users

IMPORTANT: This operation cannot be easily undone.

Branches to push:
  master (3 commits ahead)

Files changed: 12
Additions: +456 lines
Deletions: -123 lines

Type 'CONFIRM PUSH' to proceed:
```

**Implementation Pattern**:
```python
def git_push():
    # 1. Show full context
    print_push_preview()

    # 2. Strong confirmation
    response = input("Type 'CONFIRM PUSH' to proceed: ")
    if response != "CONFIRM PUSH":
        return "Push cancelled"

    # 3. Execute
    subprocess.run(["git", "push"])

    # 4. Log
    audit_log("git_push", branch, commits)
```

---

### Workflow 3: Show Plan, Then Execute

**Use When**: Multi-step operations (tia git make-clean, batch edits)

```bash
# Example: tia git make-clean
Operation: Git repository cleanup (7 phases)

Phase 1: Remove untracked files (23 files)
Phase 2: Reset staging area
Phase 3: Checkout clean working tree
Phase 4: Prune remote branches
Phase 5: Garbage collection
Phase 6: Verify integrity
Phase 7: Final status check

This will:
  ✅ Clean working directory
  ✅ Remove untracked files
  ⚠️  Cannot be undone

Proceed with cleanup? [y/N]
```

**Implementation Pattern**:
```python
def multi_step_operation(phases):
    # 1. Show complete plan
    for i, phase in enumerate(phases):
        print(f"Phase {i+1}: {phase.description}")

    # 2. Confirm entire plan
    if not confirm("Proceed with all phases?"):
        return "Operation cancelled"

    # 3. Execute with progress
    for phase in phases:
        print(f"Executing: {phase.description}")
        phase.execute()

    # 4. Log
    audit_log("multi_step", phases)
```

---

### Workflow 4: Cost-Based Approval

**Use When**: API operations with variable costs (Scout, large queries)

```bash
# Example: Scout research
Operation: Scout research campaign
Topic: "semantic infrastructure patterns"

Estimated Cost: $4.50
  Phase 1 (Discovery): $1.20 (5 queries)
  Phase 2 (Analysis): $2.10 (12 queries)
  Phase 3 (Synthesis): $1.20 (3 queries)

⚠️  Cost exceeds $2 threshold

Proceed? [y/N]
```

**Implementation Pattern**:
```python
def scout_research(topic, config):
    # 1. Estimate cost
    cost = estimate_campaign_cost(config)

    # 2. Check threshold
    if cost > 2.00:
        print(f"Estimated cost: ${cost:.2f}")
        if not confirm("Proceed?"):
            return "Research cancelled"

    # 3. Execute
    result = run_campaign(topic, config)

    # 4. Log actual cost
    audit_log("scout_research", topic, actual_cost)
```

---

## Autonomous Agent Guidelines

### When Building Autonomous Agents

Agents (Scout, Agent Ether, future tools) should implement these patterns:

**1. Cost Tracking**
```python
class Agent:
    def __init__(self, cost_threshold=2.00):
        self.cost_threshold = cost_threshold
        self.total_cost = 0.0

    def make_api_call(self, prompt):
        estimated = estimate_cost(prompt)

        if self.total_cost + estimated > self.cost_threshold:
            if not self.request_approval(estimated):
                raise ApprovalRequired()

        result = api_call(prompt)
        self.total_cost += result.actual_cost
        return result
```

**2. Threshold Checks**
```python
class Agent:
    def perform_action(self, action):
        # Evaluate risk
        risk = self.evaluate_risk(action)

        # Check thresholds
        if risk.level == "high":
            self.require_approval(action, risk)
        elif risk.level == "medium":
            self.preview_and_confirm(action)
        else:
            self.execute_and_log(action)
```

**3. Approval Requests**
```python
def require_approval(self, action, context):
    """Request human approval for high-risk action"""
    print(f"⚠️  Agent requesting approval")
    print(f"Action: {action.description}")
    print(f"Risk: {context.risk_level}")
    print(f"Impact: {context.impact_description}")

    if not confirm("Approve this action?"):
        raise OperationCancelled("User denied approval")
```

---

### Scout-Specific Thresholds

Scout already implements some of these patterns:

```yaml
# scout_config.yaml
cost_thresholds:
  auto_approve: 2.00      # Under $2: auto-execute
  require_confirm: 5.00   # $2-$5: confirm first
  require_approval: 5.00  # Over $5: explicit approval

iteration_limits:
  max_iterations: 50      # Prevent runaway loops
  warn_at: 30            # Warn when approaching limit

quality_thresholds:
  min_confidence: 0.70   # Flag low-confidence results
```

**Recommendation**: Formalize these in Scout's documentation.

---

## Audit & Logging

### What to Log

Every operation should log:

```python
audit_entry = {
    "timestamp": "2025-12-04T14:37:00Z",
    "operation": "git_push",
    "risk_level": "high",
    "approval_required": true,
    "approval_status": "approved",
    "user": "scottsen",
    "session": "xenon-catalyst-1204",
    "details": {
        "branch": "master",
        "commits": 3,
        "files_changed": 12
    },
    "cost": null  # Or actual API cost
}
```

### Audit Log Storage

```bash
# Session-specific logs
.tia/sessions/<session-id>/audit.jsonl

# System-wide logs
.tia/logs/audit/2025-12-04.jsonl
```

### Audit Queries

```bash
# Show all high-risk operations today
tia audit show --risk high --date today

# Show all operations by session
tia audit show --session xenon-catalyst-1204

# Show all git push operations
tia audit show --operation git_push

# Show all operations requiring approval
tia audit show --approval-required
```

---

## Threshold Evolution

### Monitoring & Adjustment

Track approval patterns to optimize thresholds:

```bash
# Metrics to monitor
- Approval rate (% operations requiring approval)
- User denials (operations user rejected)
- False positives (low-risk flagged as high-risk)
- Missed risks (high-risk that should have been flagged)
```

### Quarterly Review

Every quarter, review:

1. **Approval Rate**: Are we asking too often or not enough?
2. **User Feedback**: What's frustrating vs helpful?
3. **Incident Analysis**: Did any approved operations cause issues?
4. **Cost Trends**: Are cost thresholds still appropriate?

### Threshold Tuning

```yaml
# Example: Adjust thresholds based on usage
# Before
cost_thresholds:
  auto_approve: 1.00
  require_confirm: 5.00

# After (based on 3 months data)
cost_thresholds:
  auto_approve: 2.00      # Increased (too many confirmations)
  require_confirm: 10.00  # Increased (user trust built up)
```

---

## Implementation Checklist

When implementing HITL for a new operation:

- [ ] **Classify Risk**: Low/Medium/High using framework
- [ ] **Choose Workflow**: Preview, Approval, Plan, or Cost-based
- [ ] **Implement Preview**: Show what will happen before executing
- [ ] **Add Confirmation**: Appropriate to risk level
- [ ] **Log Operation**: Complete audit trail
- [ ] **Test Edge Cases**: What happens on deny? On error?
- [ ] **Document Threshold**: Update this doc with new operation
- [ ] **Review After 1 Week**: Is threshold appropriate?

---

## Examples from Current TIA

### Example 1: Git Push (High-Risk, Already Implemented)

From CLAUDE.md, Claude's git workflow:

```bash
# Step 1: Gather context (auto)
git status
git diff
git log

# Step 2: Preview commit (confirm)
# Shows: Diff, commit message draft
User approves commit message

# Step 3: Execute safe operations (auto)
git add <files>
git commit -m "message"

# Step 4: STOP AND ASK (high-risk)
# Claude MUST NOT proceed to git push
# User types: "push"
# Claude executes: git push
```

**Why This Works**:
- Low-risk operations (status, diff, log) auto-execute
- Medium-risk (commit) previewed first
- High-risk (push) requires explicit user command

---

### Example 2: Beth Rebuild (Medium-Risk, Should Confirm)

```bash
# Current (no confirmation)
$ tia beth rebuild
Rebuilding Beth index...
Processing 13,549 files...

# Improved (confirm if large)
$ tia beth rebuild
Beth index rebuild requested

Current index: 13,549 files
Estimated time: 2-3 minutes
Estimated cost: $0 (local processing)

This will:
  ✅ Refresh semantic relationships
  ⚠️  Use significant CPU/memory

Proceed? [y/N]
```

---

### Example 3: Scout Research (Cost-Based, Should Implement)

```bash
# Proposed implementation
$ scout research "topic" --config large_campaign.yaml

Scout Research Campaign
Topic: "semantic infrastructure patterns"

Configuration: large_campaign.yaml
  Phases: 3 (Discovery, Analysis, Synthesis)
  Max iterations: 50
  Estimated queries: 35

⚠️  Estimated cost: $6.50 (exceeds $2 threshold)

Cost breakdown:
  Phase 1: $2.00 (12 queries × llama-3.3-70b)
  Phase 2: $3.50 (18 queries × llama-3.3-70b)
  Phase 3: $1.00 (5 queries × llama-3.3-70b)

Proceed with campaign? [y/N]
```

---

## Conclusion

**Human-in-the-Loop is not about blocking automation** - it's about **building trust through transparency**.

**The SIL Way**:
1. **Low-risk**: Auto-execute with logging
2. **Medium-risk**: Preview and confirm
3. **High-risk**: Explicit approval required

**Already Working**:
- Git push workflow (excellent HITL pattern)
- Session cleanup (smart auto-delete old sessions)

**Opportunities**:
- Formalize cost thresholds for Scout
- Add confirmation for Beth rebuild (if large)
- Implement audit logging system
- Build `tia audit` command for querying logs

**Next Steps**:
1. Implement audit logging infrastructure
2. Add cost preview to Scout
3. Create `tia audit` command
4. Monitor approval patterns for 1 month
5. Adjust thresholds based on data

---

## Related Documentation

- [SIL Core Principles](SIL_CORE_PRINCIPLES.md) - HITL as Core Principle #8
- templates/CLAUDE.md - Git workflow HITL implementation
- Scout documentation - Cost tracking patterns

---

**Version History**:
- v1.0 (2025-12-04): Initial formalization of HITL patterns and safety thresholds
