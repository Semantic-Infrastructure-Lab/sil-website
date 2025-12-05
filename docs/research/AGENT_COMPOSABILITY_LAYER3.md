# Agent Composability for Layer 3: Agent Ether

**Unix Philosophy for LLM Orchestration**

**Document Type:** Technical Specification
**Version:** 1.0
**Date:** 2025-12-03
**Authors:** Scott Senkeresty (Chief Architect, Semantic OS), TIA (Chief Semantic Agent)
**Status:** Design Complete, Ready for Implementation
**Length:** ~25,000 words

---

## Abstract

This specification defines the technical implementation of **Layer 3: Agent Ether** in the SIL Semantic OS Architecture. We extend Unix philosophy (pipes, composition, streams) to multi-agent LLM orchestration, providing standard I/O contracts (`AgentInput`/`AgentOutput`), orchestration patterns (serial, parallel, map-reduce), and aggregation interfaces transparent to both humans and LLMs.

**The Problem:** When TIA launches Scout, or Scout launches Groqqy, and we need to parallelize tasks (e.g., process 5 directories with 3 analysis steps each), how do we make this composable like Unix pipes?

**The Solution:** Standard protocols that transform isolated agents into a composable ecosystem—enabling declarative workflows, reproducible execution, and cross-domain collaboration.

**Key Contributions:**
- `AgentInput`/`AgentOutput` JSON contracts with evolution path to Pantheon IR
- `ComposableAgent` base class with capability discovery
- `AgentWorkflow` orchestrator for serial, parallel, and map-reduce patterns
- Three aggregation interfaces: Streaming (console), JSON (LLM), Markdown (reports)
- Implementation of [Multi-Agent Protocol Principles](MULTI_AGENT_PROTOCOL_PRINCIPLES.md)
- Cross-layer integration with Semantic OS (L0-L5)

**Why this matters:** This is the **glue layer** that makes the Semantic OS vision real. Without this, agents remain isolated. With it, they become a composable ecosystem.

**Related documents:**
- **Principles:** [Multi-Agent Protocol Principles](MULTI_AGENT_PROTOCOL_PRINCIPLES.md) - The philosophical foundation
- **Case Study:** [TIA Unified Workspace](TIA_UNIFIED_WORKSPACE_CASE_STUDY.md) - Working implementation
- **Architecture:** [SIL Semantic OS](../canonical/SIL_SEMANTIC_OS_ARCHITECTURE.md) - Layer 3 context

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Unix Philosophy Applied](#2-unix-philosophy-applied)
3. [Core Design: AgentIO Protocol](#3-core-design-agentio-protocol)
4. [Agent Interface Contract](#4-agent-interface-contract)
5. [Orchestration Layer](#5-orchestration-layer-agentworkflow)
6. [Aggregation Interfaces](#6-aggregation-interfaces)
7. [Mapping to Protocol Principles](#7-mapping-to-protocol-principles)
8. [Cross-Layer Integration](#8-cross-layer-integration)
9. [Example Use Cases](#9-example-use-cases)
10. [Implementation Roadmap](#10-implementation-roadmap)

---

## 1. Problem Statement

### 1.1 The Core Challenge

How do we make agents composable like Unix commands?

**Concrete scenario:**
- TIA needs to review 5 codebases
- Each codebase needs 3 analysis passes (structure, bugs, documentation)
- Results must be aggregated into single report
- Must be transparent to humans watching progress AND LLMs consuming results

**Requirements:**
- ✅ One agent can launch sub-agents (serial or parallel)
- ✅ Standard I/O contracts (JSON in/out)
- ✅ Aggregation interfaces clear to humans and LLMs
- ✅ Provenance tracking (what happened, when, why)
- ✅ Error handling and escalation
- ✅ Resource budgeting (cost, time, tokens)

### 1.2 Why Not "Vibe Coding"?

The naive approach:
```python
# Agent A calls Agent B via natural language
response = agent_b.chat(f"Agent A says: {vague_instruction}")
```

**This fails because:**
- No schema validation (did Agent B understand correctly?)
- No provenance (where did this result come from?)
- No error handling (what if Agent B fails?)
- No composition (how do we chain 5 agents?)
- No aggregation (how do we combine results?)

**See [Multi-Agent Protocol Principles](MULTI_AGENT_PROTOCOL_PRINCIPLES.md) for full failure mode analysis.**

### 1.3 The Unix Inspiration

Unix succeeded because programs communicate through **standard protocols**:

| Unix Concept | Purpose | Agent Equivalent |
|--------------|---------|------------------|
| `stdin/stdout` | Standard I/O | `AgentInput/AgentOutput` |
| Exit codes | Success/failure | `status: success\|error\|partial` |
| Pipes (`\|`) | Sequential composition | Task chains (`→`) |
| `xargs` | Parallel execution | Parallel agents (`∥`) |
| `tee` | Result broadcasting | Multiple consumers |
| `grep -q && cmd` | Conditional execution | Decision flows |

**Our goal:** Agents that compose as naturally as shell commands.

---

## 2. Unix Philosophy Applied

### 2.1 Core Principles

**Principle 1: Do one thing well**
- Each agent has focused capabilities
- `ComposableScout` analyzes code, doesn't manage infrastructure
- Specialization enables reliability

**Principle 2: Standard I/O**
- All agents speak JSON (AgentInput → AgentOutput)
- Schemas are explicit and versioned
- Enables interoperability

**Principle 3: Composability**
- Agents chain via standard interfaces
- No agent-specific plumbing required
- `agent1 | agent2 | agent3` Just Works™

**Principle 4: Text streams (adapted)**
- Unix: text streams
- Agents: JSON streams + semantic types (Pantheon IR)
- Both are parseable, inspectable, debuggable

### 2.2 Mapping Table

| Unix Pattern | Agent Pattern | Example |
|-------------|---------------|---------|
| `cat file \| grep pattern` | Serial chain | Scout.explore() → Scout.analyze() |
| `ls *.txt \| xargs wc -l` | Parallel map | 5 dirs → Scout.explore (parallel) |
| `find . -type f \| tee /tmp/list \| wc -l` | Broadcast | Results → Console + JSON + Beth |
| `cmd1 && cmd2` | Conditional | Success → next_action |
| `cmd 2>&1 \| tee log.txt` | Streaming | Real-time progress to user |

---

## 3. Core Design: AgentIO Protocol

### 3.1 Standard I/O Format

**AgentInput** - The request contract:

```python
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class AgentInput:
    """Standard agent input contract"""
    task_id: str                        # UUID for provenance
    agent: str                          # Which agent to invoke
    action: str                         # What capability to use
    params: Dict[str, Any]             # Action-specific parameters
    context: Optional[Dict[str, Any]] = None  # Parent task, workflow metadata
```

**Example:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "agent": "scout",
  "action": "explore_directory",
  "params": {
    "path": "/workspace/projects/reveal",
    "depth": 2
  },
  "context": {
    "parent_task": "abc-def-123",
    "workflow": "code_review_campaign",
    "budget": {"max_cost": 0.50, "max_time_sec": 300}
  }
}
```

**AgentOutput** - The response contract:

```python
from enum import Enum
from typing import List

class AgentStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"  # Partial success (some tasks failed)

@dataclass
class AgentOutput:
    """Standard agent output contract"""
    task_id: str                              # Links to request
    status: AgentStatus                       # Outcome
    agent: str                                # Who completed it
    data: Dict[str, Any]                      # The actual result
    metadata: Dict[str, Any]                  # Cost, duration, model used
    next_actions: Optional[List[AgentInput]] = None  # Chain continuation
```

**Example:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "agent": "scout",
  "data": {
    "files_found": 42,
    "structure": {"src": 15, "tests": 12, "docs": 8},
    "insights": ["Well-organized codebase", "Good test coverage"]
  },
  "metadata": {
    "cost": 0.0012,
    "duration_ms": 3500,
    "iterations": 8,
    "model": "llama-3.3-70b-versatile",
    "timestamp": "2025-12-03T15:45:00Z"
  },
  "next_actions": [
    {
      "task_id": "new-uuid",
      "agent": "scout",
      "action": "analyze_file",
      "params": {"file": "src/main.py"}
    }
  ]
}
```

### 3.2 Design Rationale

**Why JSON?**
- Immediately implementable (no Pantheon IR dependency)
- Well-typed via Python dataclasses
- Clear migration path: `Dict[str, Any]` → `PantheonIR`
- Human-readable debugging

**Why `next_actions`?**
- Enables **choreography** (agents decide workflow)
- Complements **orchestration** (external coordinator)
- Agents can suggest continuation, supervisor approves

**Why `metadata`?**
- Cost tracking (critical for LLM budgets)
- Performance profiling (optimize slow steps)
- Provenance (which model, when, how long)
- Debugging (replay failed tasks)

---

## 4. Agent Interface Contract

### 4.1 ComposableAgent Base Class

```python
from abc import ABC, abstractmethod
from typing import List

class ComposableAgent(ABC):
    """Base class for composable agents

    All agents must implement:
    - execute(): Standard I/O processing
    - can_handle(): Capability checking
    - capabilities: Advertise what this agent can do
    """

    @abstractmethod
    def execute(self, input: AgentInput) -> AgentOutput:
        """Execute agent task with standard I/O

        Args:
            input: AgentInput with task_id, action, params

        Returns:
            AgentOutput with status, data, metadata

        Raises:
            ValueError: If action not supported
            RuntimeError: If execution fails
        """
        pass

    @abstractmethod
    def can_handle(self, action: str) -> bool:
        """Check if agent can handle this action

        Args:
            action: Action name (e.g., "explore_directory")

        Returns:
            True if agent supports this action
        """
        pass

    @property
    @abstractmethod
    def capabilities(self) -> List[str]:
        """List actions this agent supports

        Returns:
            List of action names (e.g., ["explore", "analyze", "summarize"])
        """
        pass
```

### 4.2 ComposableScout Implementation

```python
import time
import uuid
from typing import Dict, Any

class ComposableScout(ComposableAgent):
    """Scout agent with standard AgentIO interface

    Capabilities:
    - explore_directory: Analyze directory structure
    - analyze_file: Deep-dive into single file
    - search_content: Find patterns in codebase
    - extract_structure: Generate AST/outline
    - summarize_findings: Aggregate results
    """

    def __init__(self, scout_instance=None):
        """Initialize with optional Scout instance"""
        self.scout = scout_instance or Scout()
        self._capabilities = [
            "explore_directory",
            "analyze_file",
            "search_content",
            "extract_structure",
            "summarize_findings"
        ]

    @property
    def capabilities(self) -> List[str]:
        return self._capabilities

    def can_handle(self, action: str) -> bool:
        return action in self._capabilities

    def execute(self, input: AgentInput) -> AgentOutput:
        """Execute with standard I/O"""
        start = time.time()

        # Validate action
        if not self.can_handle(input.action):
            return AgentOutput(
                task_id=input.task_id,
                status=AgentStatus.ERROR,
                agent="scout",
                data={"error": f"Unsupported action: {input.action}"},
                metadata={"duration_ms": 0}
            )

        try:
            # Route to appropriate handler
            handler = getattr(self, f"_handle_{input.action}")
            result = handler(input.params, input.context)

            return AgentOutput(
                task_id=input.task_id,
                status=AgentStatus.SUCCESS,
                agent="scout",
                data=result,
                metadata={
                    "duration_ms": int((time.time() - start) * 1000),
                    "cost": self.scout.bot.total_cost(),
                    "model": self.scout.model,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                }
            )
        except Exception as e:
            return AgentOutput(
                task_id=input.task_id,
                status=AgentStatus.ERROR,
                agent="scout",
                data={"error": str(e), "traceback": traceback.format_exc()},
                metadata={
                    "duration_ms": int((time.time() - start) * 1000),
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                }
            )

    def _handle_explore_directory(self, params: Dict[str, Any], context: Dict) -> Dict:
        """Explore directory structure"""
        path = params["path"]
        depth = params.get("depth", 2)

        # Check budget constraints
        if context and "budget" in context:
            if context["budget"].get("max_cost", float("inf")) < 0.001:
                raise ValueError("Insufficient budget for exploration")

        prompt = f"Explore {path} to depth {depth}. Identify structure, key files, patterns."
        response = self.scout.chat(prompt)

        return {
            "path": path,
            "depth": depth,
            "analysis": response,
            "files": []  # Could enhance with actual file list
        }

    def _handle_analyze_file(self, params: Dict[str, Any], context: Dict) -> Dict:
        """Analyze single file"""
        file_path = params["file"]

        prompt = f"Analyze {file_path}. What does this code do? Any issues?"
        response = self.scout.chat(prompt)

        return {
            "file": file_path,
            "analysis": response
        }

    def _handle_summarize_findings(self, params: Dict[str, Any], context: Dict) -> Dict:
        """Aggregate multiple results"""
        findings = params.get("findings", [])

        prompt = f"Summarize these findings:\n{json.dumps(findings, indent=2)}"
        response = self.scout.chat(prompt)

        return {
            "summary": response,
            "total_findings": len(findings)
        }
```

### 4.3 Capability Discovery

**Pattern: Agents advertise what they can do**

```python
# Query agent capabilities
scout = ComposableScout()
print(scout.capabilities)
# → ["explore_directory", "analyze_file", "search_content", ...]

# Check if agent can handle action
if scout.can_handle("explore_directory"):
    result = scout.execute(AgentInput(...))
```

**Why this matters:**
- Dynamic workflow generation (orchestrator queries capabilities)
- Error prevention (check before execute)
- Self-documenting agents
- Enables agent marketplace (discover agents by capability)

---

## 5. Orchestration Layer: AgentWorkflow

### 5.1 Workflow Definition (YAML DSL)

```yaml
# workflow: code_review_campaign.yaml
name: Code Review Campaign
description: Review multiple directories in parallel

workflow:
  # Stage 1: Discover (parallel)
  - stage: discover
    agent: scout
    action: explore_directory
    parallel: true
    inputs:
      - path: /workspace/projects/groqqy
      - path: /workspace/projects/scout
      - path: /workspace/projects/reveal

  # Stage 2: Analyze (serial, uses stage 1 output)
  - stage: analyze
    agent: scout
    action: analyze_structure
    input_from: discover.data.files
    parallel: true
    map: each_file

  # Stage 3: Summarize (reduce)
  - stage: summarize
    agent: scout
    action: aggregate_findings
    input_from: analyze.data
    reduce: all

output:
  format: markdown
  destination: report.md
  template: code_review_summary.md.j2
```

### 5.2 Workflow Executor Implementation

```python
import concurrent.futures
from typing import Dict, List, Any

class AgentWorkflow:
    """Execute multi-agent workflows from YAML specs

    Supports:
    - Serial execution (stages run sequentially)
    - Parallel execution (tasks within stage run concurrently)
    - Stage dependencies (input_from previous stage)
    - Map-reduce patterns
    """

    def __init__(self, agents: Dict[str, ComposableAgent]):
        """Initialize with agent registry

        Args:
            agents: Dict mapping agent name → ComposableAgent instance
        """
        self.agents = agents
        self.results = {}  # stage_name → List[AgentOutput]

    def run(self, workflow_spec: Dict) -> Dict[str, List[AgentOutput]]:
        """Execute workflow from specification

        Args:
            workflow_spec: Workflow definition (from YAML)

        Returns:
            Dict mapping stage_name → results
        """
        for stage in workflow_spec["workflow"]:
            stage_name = stage["stage"]
            agent_name = stage["agent"]
            action = stage["action"]

            # Validate agent exists and can handle action
            agent = self.agents.get(agent_name)
            if not agent:
                raise ValueError(f"Unknown agent: {agent_name}")
            if not agent.can_handle(action):
                raise ValueError(f"{agent_name} cannot handle {action}")

            # Prepare inputs (from previous stage or spec)
            if "input_from" in stage:
                inputs = self._resolve_inputs(stage["input_from"], stage)
            else:
                inputs = stage.get("inputs", [{}])

            # Execute (parallel or serial)
            if stage.get("parallel", False):
                results = self._execute_parallel(agent, action, inputs)
            else:
                results = [self._execute_serial(agent, action, inp) for inp in inputs]

            # Store results for next stage
            self.results[stage_name] = results

        return self.results

    def _resolve_inputs(self, input_from: str, stage: Dict) -> List[Dict]:
        """Extract inputs from previous stage output

        Args:
            input_from: "stage_name.data.field_path"
            stage: Current stage spec

        Returns:
            List of inputs for current stage
        """
        # Parse: "discover.data.files" → stage="discover", path="data.files"
        parts = input_from.split(".", 1)
        prev_stage = parts[0]
        data_path = parts[1] if len(parts) > 1 else "data"

        prev_results = self.results.get(prev_stage, [])

        # Extract data from each result
        inputs = []
        for result in prev_results:
            data = self._extract_path(result, data_path)
            if isinstance(data, list):
                inputs.extend(data)
            else:
                inputs.append(data)

        return inputs

    def _extract_path(self, obj: Any, path: str) -> Any:
        """Extract nested field from object

        Args:
            obj: Object (dict or dataclass)
            path: Dot-separated path (e.g., "data.files")

        Returns:
            Value at path
        """
        for part in path.split("."):
            if hasattr(obj, part):
                obj = getattr(obj, part)
            elif isinstance(obj, dict):
                obj = obj[part]
            else:
                raise ValueError(f"Cannot extract {path} from {obj}")
        return obj

    def _execute_parallel(
        self,
        agent: ComposableAgent,
        action: str,
        inputs: List[Dict]
    ) -> List[AgentOutput]:
        """Execute agent tasks in parallel

        Args:
            agent: ComposableAgent instance
            action: Action to perform
            inputs: List of parameter dicts

        Returns:
            List of AgentOutput results
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            tasks = [
                executor.submit(
                    agent.execute,
                    AgentInput(
                        task_id=str(uuid.uuid4()),
                        agent=agent.__class__.__name__,
                        action=action,
                        params=inp
                    )
                )
                for inp in inputs
            ]
            return [task.result() for task in tasks]

    def _execute_serial(
        self,
        agent: ComposableAgent,
        action: str,
        input_data: Dict
    ) -> AgentOutput:
        """Execute single agent task

        Args:
            agent: ComposableAgent instance
            action: Action to perform
            input_data: Parameter dict

        Returns:
            AgentOutput result
        """
        return agent.execute(
            AgentInput(
                task_id=str(uuid.uuid4()),
                agent=agent.__class__.__name__,
                action=action,
                params=input_data
            )
        )
```

### 5.3 Orchestration Patterns

**A. Serial Chain (→)**
```yaml
workflow:
  - stage: step1
    agent: scout
    action: explore

  - stage: step2
    agent: scout
    action: analyze
    input_from: step1.data

  - stage: step3
    agent: scout
    action: summarize
    input_from: step2.data
```

**B. Parallel Fan-Out (∥)**
```yaml
workflow:
  - stage: parallel_explore
    agent: scout
    action: explore_directory
    parallel: true
    inputs:
      - path: /dir1
      - path: /dir2
      - path: /dir3
```

**C. Map-Reduce**
```yaml
workflow:
  - stage: map
    agent: scout
    action: analyze
    parallel: true
    input_from: discover.data.files

  - stage: reduce
    agent: scout
    action: aggregate
    input_from: map.data
```

---

## 6. Aggregation Interfaces

### 6.1 Streaming Aggregator (Human-Readable Console)

**Purpose:** Real-time progress updates for humans monitoring workflows

```python
class StreamingAggregator:
    """Real-time progress updates to console

    Shows:
    - Task start/complete events
    - Progress bars (if task reports progress)
    - Success/failure indicators
    - Cost and duration tracking
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.start_times = {}

    def on_task_start(self, task_id: str, agent: str, action: str):
        """Called when task starts"""
        self.start_times[task_id] = time.time()
        if self.verbose:
            print(f"[{task_id[:8]}] ▶ {agent}.{action} starting...")

    def on_task_progress(self, task_id: str, progress: float, message: str = ""):
        """Called during task execution"""
        if self.verbose:
            bar = "█" * int(progress * 20)
            print(f"[{task_id[:8]}] {bar:<20} {progress*100:.0f}% {message}")

    def on_task_complete(self, task_id: str, output: AgentOutput):
        """Called when task completes"""
        elapsed = time.time() - self.start_times.get(task_id, 0)
        status_icon = {
            AgentStatus.SUCCESS: "✅",
            AgentStatus.ERROR: "❌",
            AgentStatus.PARTIAL: "⚠️"
        }[output.status]

        print(f"[{task_id[:8]}] {status_icon} {output.agent} complete")
        print(f"  └─ Cost: ${output.metadata.get('cost', 0):.4f}")
        print(f"  └─ Time: {output.metadata.get('duration_ms', 0)}ms")

        if output.status == AgentStatus.ERROR:
            print(f"  └─ Error: {output.data.get('error', 'Unknown')}")
```

**Example output:**
```
[550e8400] ▶ scout.explore_directory starting...
[550e8400] ████████████████████ 100%
[550e8400] ✅ scout complete
  └─ Cost: $0.0012
  └─ Time: 3500ms
```

### 6.2 JSON Aggregator (LLM-Readable Structured Data)

**Purpose:** Structured output for LLM consumption and programmatic processing

```python
class JSONAggregator:
    """Structured output for LLM consumption

    Produces:
    - Summary statistics
    - Complete task results
    - Provenance metadata
    - Error details
    """

    def aggregate(self, results: List[AgentOutput]) -> Dict[str, Any]:
        """Combine results into single JSON structure

        Args:
            results: List of AgentOutput from workflow

        Returns:
            Structured dict with summary + details
        """
        successful = [r for r in results if r.status == AgentStatus.SUCCESS]
        failed = [r for r in results if r.status == AgentStatus.ERROR]
        partial = [r for r in results if r.status == AgentStatus.PARTIAL]

        return {
            "summary": {
                "total_tasks": len(results),
                "successful": len(successful),
                "failed": len(failed),
                "partial": len(partial),
                "total_cost": sum(r.metadata.get("cost", 0) for r in results),
                "total_time_ms": sum(r.metadata.get("duration_ms", 0) for r in results),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            },
            "tasks": [
                {
                    "task_id": r.task_id,
                    "agent": r.agent,
                    "status": r.status.value,
                    "data": r.data,
                    "metadata": r.metadata
                }
                for r in results
            ],
            "errors": [
                {
                    "task_id": r.task_id,
                    "agent": r.agent,
                    "error": r.data.get("error"),
                    "traceback": r.data.get("traceback")
                }
                for r in failed
            ]
        }
```

**Example output:**
```json
{
  "summary": {
    "total_tasks": 5,
    "successful": 4,
    "failed": 1,
    "total_cost": 0.0056,
    "total_time_ms": 12500
  },
  "tasks": [...],
  "errors": [...]
}
```

### 6.3 Markdown Aggregator (Human + LLM Reports)

**Purpose:** Human-readable reports that LLMs can also parse

```python
class MarkdownAggregator:
    """Generate markdown summary reports

    Produces:
    - Executive summary table
    - Detailed task results
    - Error analysis
    - Recommendations
    """

    def aggregate(self, results: List[AgentOutput], template: str = None) -> str:
        """Create markdown report

        Args:
            results: List of AgentOutput
            template: Optional Jinja2 template path

        Returns:
            Markdown string
        """
        md = ["# Agent Workflow Results\n"]
        md.append(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Summary table
        md.append("## Summary\n")
        md.append("| Metric | Value |")
        md.append("|--------|-------|")
        md.append(f"| Total Tasks | {len(results)} |")
        md.append(f"| Successful | {len([r for r in results if r.status == AgentStatus.SUCCESS])} |")
        md.append(f"| Failed | {len([r for r in results if r.status == AgentStatus.ERROR])} |")
        md.append(f"| Total Cost | ${sum(r.metadata.get('cost', 0) for r in results):.4f} |")
        md.append(f"| Total Time | {sum(r.metadata.get('duration_ms', 0) for r in results)/1000:.1f}s |\n")

        # Task details
        md.append("## Task Details\n")
        for result in results:
            status_icon = {
                AgentStatus.SUCCESS: "✅",
                AgentStatus.ERROR: "❌",
                AgentStatus.PARTIAL: "⚠️"
            }[result.status]

            md.append(f"### {status_icon} {result.agent} - Task {result.task_id[:8]}\n")
            md.append(f"**Status:** {result.status.value}  ")
            md.append(f"**Cost:** ${result.metadata.get('cost', 0):.4f}  ")
            md.append(f"**Duration:** {result.metadata.get('duration_ms', 0)}ms\n")

            # Data preview
            md.append("**Output:**")
            md.append("```json")
            md.append(json.dumps(result.data, indent=2))
            md.append("```\n")

        return "\n".join(md)
```

**Example output:**
```markdown
# Agent Workflow Results

**Generated:** 2025-12-03 15:45:00

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 5 |
| Successful | 4 |
| Failed | 1 |
| Total Cost | $0.0056 |
| Total Time | 12.5s |

## Task Details

### ✅ scout - Task 550e8400

**Status:** success
**Cost:** $0.0012
**Duration:** 3500ms

**Output:**
```json
{
  "files_found": 42,
  "structure": {...}
}
```
```

---

## 7. Mapping to Protocol Principles

This specification implements the seven principles from [Multi-Agent Protocol Principles](MULTI_AGENT_PROTOCOL_PRINCIPLES.md):

| Principle | Implementation in AgentIO | Location |
|-----------|---------------------------|----------|
| **1. Communicate Intent** | `AgentInput.params` includes goals + constraints | §3.1 |
| **2. Typed Communication** | JSON schemas → Pantheon IR migration path | §3.1, §8.2 |
| **3. Explicit Roles** | `ComposableAgent.capabilities` + role metadata | §4.1 |
| **4. Bounded Autonomy** | Context includes budgets, permission boundaries | §3.1, §4.2 |
| **5. Escalate on Uncertainty** | `AgentStatus.PARTIAL` + error handling | §3.1, §4.2 |
| **6. Provenance** | `metadata` includes full execution trace | §3.1 |
| **7. Synthesis** | Aggregators combine parallel results | §6 |

**Example: Principle 4 (Bounded Autonomy) in Practice**

```python
# Context includes resource bounds
input = AgentInput(
    task_id="...",
    agent="scout",
    action="explore_directory",
    params={"path": "/workspace"},
    context={
        "budget": {
            "max_cost": 0.50,      # Stop if cost exceeds $0.50
            "max_time_sec": 300,   # Timeout after 5 minutes
            "max_iterations": 20   # Prevent runaway loops
        },
        "permissions": {
            "can_modify_files": False,  # Read-only
            "can_access_network": False  # No external calls
        }
    }
)

# Agent checks bounds before executing
def _handle_explore_directory(self, params, context):
    budget = context.get("budget", {})
    if self.scout.bot.total_cost() > budget.get("max_cost", float("inf")):
        raise ValueError("Budget exceeded")
    # ... proceed with exploration
```

---

## 8. Cross-Layer Integration

### 8.1 Layer 0: Semantic Memory (Agent Knowledge)

**Integration:** Agents persist learned knowledge across executions

```python
class ComposableScoutWithMemory(ComposableAgent):
    """Scout with persistent semantic memory"""

    def __init__(self):
        self.scout = Scout()
        self.memory = SemanticMemory()  # Layer 0

    def execute(self, input: AgentInput) -> AgentOutput:
        # Check if we've seen this before
        cache_key = f"{input.action}:{input.params}"
        cached = self.memory.query(cache_key)

        if cached and not input.context.get("force_refresh"):
            return AgentOutput(
                task_id=input.task_id,
                status=AgentStatus.SUCCESS,
                agent="scout",
                data=cached["result"],
                metadata={"cached": True, "cost": 0}
            )

        # Execute fresh
        result = super().execute(input)

        # Store for future
        self.memory.store(cache_key, {
            "result": result.data,
            "timestamp": time.time(),
            "provenance": result.metadata
        })

        return result
```

**Benefits:**
- Avoid redundant work
- Learn from past executions
- Knowledge accumulation over time

### 8.2 Layer 1: Pantheon IR (Semantic Messaging)

**Evolution path:** JSON → Pantheon IR for type-safe cross-domain messaging

**Current (MVP):**
```python
params: Dict[str, Any]  # Generic dict
```

**Future (Pantheon Integration):**
```python
from pantheon import PantheonIR, Entity, TimeRange

params: PantheonIR  # Typed semantic graph

# Example: Water network analysis
params = PantheonIR({
    "type": "water_network_analysis",
    "network": Entity(id="network-sf-001", type="WaterNetwork"),
    "time_range": TimeRange(start="2025-01-01", end="2025-12-31"),
    "sensors": [
        Sensor(id="sensor-001", location=GeoPoint(37.7749, -122.4194)),
        Sensor(id="sensor-002", location=GeoPoint(37.7849, -122.4094))
    ]
})
```

**Cross-domain example:**
```python
# Water agent detects anomaly
water_result = water_agent.execute(AgentInput(
    action="detect_anomalies",
    params=PantheonIR({...})  # Water domain semantics
))

# Healthcare agent consumes water agent output (type-safe!)
health_agent.execute(AgentInput(
    action="correlate_illnesses",
    params=water_result.data  # Still PantheonIR, different domain
))
```

**Benefits:**
- Type-safe inter-agent communication
- Cross-domain interoperability
- Formal semantics, verification

### 8.3 Layer 4: Morphogen (Deterministic Workflows)

**Integration:** Agent workflows as reproducible Morphogen derivations

```python
# Agent workflow wrapped as Morphogen derivation
derivation = {
    "name": "code_review_workflow",
    "version": "1.0",
    "inputs": {
        "codebase": "sha256:abc123...",  # Content-addressed
        "config": "sha256:def456..."
    },
    "workflow": {
        "discover": {
            "agent": "scout",
            "action": "explore_directory",
            "hermetic": True  # No network, reproducible
        },
        "analyze": {
            "agent": "scout",
            "action": "analyze_structure",
            "depends_on": ["discover"]
        },
        "summarize": {
            "agent": "scout",
            "action": "aggregate",
            "depends_on": ["analyze"]
        }
    },
    "output": "sha256:..."  # Deterministic output hash
}

# Execute via Morphogen
result = morphogen.build(derivation)

# Result is reproducible: same inputs → same output
# Can verify: morphogen.verify(derivation, result)
```

**Benefits:**
- Reproducible multi-agent workflows
- Cryptographic verification
- Audit trails for compliance

### 8.4 Layer 5: Human Interfaces (CLI, API)

**Integration:** Expose agent workflows via CLI and REST API

**CLI:**
```bash
# Run workflow from YAML spec
tia agent workflow run code_review_campaign.yaml

# Output:
# [550e8400] ▶ scout.explore_directory starting...
# [550e8400] ✅ scout complete (Cost: $0.0012, Time: 3500ms)
# ...
# Workflow complete. Report saved to report.md

# Query agent capabilities
tia agent capabilities scout
# → explore_directory, analyze_file, search_content, ...

# Execute single action
tia agent exec scout explore_directory --path /workspace/projects/reveal
```

**REST API:**
```python
# POST /api/v1/workflows
{
  "workflow_spec": {...},
  "async": true
}
# → Returns: {"job_id": "abc-123", "status": "running"}

# GET /api/v1/workflows/abc-123
# → Returns: {"status": "complete", "results": [...]}
```

---

## 9. Example Use Cases

### 9.1 Process 5 Directories in Parallel

**Scenario:** Review 5 codebases simultaneously, aggregate findings

```python
# Setup
scout = ComposableScout()
workflow = AgentWorkflow({"scout": scout})

# Define workflow
spec = {
    "workflow": [
        {
            "stage": "explore",
            "agent": "scout",
            "action": "explore_directory",
            "parallel": True,
            "inputs": [
                {"path": "/workspace/projects/groqqy"},
                {"path": "/workspace/projects/scout"},
                {"path": "/workspace/projects/reveal"},
                {"path": "/workspace/tia/commands"},
                {"path": "/workspace/tia/lib"}
            ]
        },
        {
            "stage": "summarize",
            "agent": "scout",
            "action": "aggregate_findings",
            "input_from": "explore.data"
        }
    ]
}

# Execute
results = workflow.run(spec)

# Generate report
aggregator = MarkdownAggregator()
report = aggregator.aggregate(results["explore"])
with open("code_review.md", "w") as f:
    f.write(report)
```

**Output:**
- 5 directories explored in parallel (~3.5s total vs 17.5s serial)
- Aggregated report with summary + per-directory findings
- Total cost tracked, errors isolated

### 9.2 Serial Task Chain (Deep Analysis)

**Scenario:** Explore → Identify Issues → Prioritize → Create Tasks

```python
spec = {
    "workflow": [
        {
            "stage": "explore",
            "agent": "scout",
            "action": "explore_directory",
            "inputs": [{"path": "/workspace/projects/foo"}]
        },
        {
            "stage": "analyze",
            "agent": "scout",
            "action": "identify_issues",
            "input_from": "explore.data.files"
        },
        {
            "stage": "prioritize",
            "agent": "scout",
            "action": "prioritize_issues",
            "input_from": "analyze.data.issues"
        },
        {
            "stage": "create_tasks",
            "agent": "tia",
            "action": "create_tasks",
            "input_from": "prioritize.data.prioritized"
        }
    ]
}

# Each stage feeds into next
# Output: TIA tasks created for top-priority issues
```

### 9.3 Map-Reduce (5 Analysis Types per Directory)

**Scenario:** Run multiple analysis passes, then aggregate

```python
spec = {
    "workflow": [
        {
            "stage": "discover",
            "agent": "scout",
            "action": "explore_directory",
            "inputs": [{"path": dir} for dir in directories]
        },
        {
            "stage": "map_analysis",
            "agent": "scout",
            "action": "analyze",
            "parallel": True,
            "map": [
                "structure_analysis",
                "bug_detection",
                "complexity_metrics",
                "documentation_check",
                "security_scan"
            ],
            "input_from": "discover.data.files"
        },
        {
            "stage": "reduce",
            "agent": "scout",
            "action": "aggregate_findings",
            "input_from": "map_analysis.data"
        }
    ]
}

# 5 directories × 5 analyses = 25 parallel tasks
# Reduced to single comprehensive report
```

---

## 10. Implementation Roadmap

### Phase 1: Core Protocol (2 weeks)

**Goal:** Validate AgentIO design with working prototype

**Deliverables:**
- [x] Define `AgentInput`/`AgentOutput` dataclasses
- [x] Create `ComposableAgent` base class
- [ ] Implement `ComposableScout` with 3 basic actions
  - `explore_directory`
  - `analyze_file`
  - `summarize_findings`
- [ ] Test basic execute() with JSON I/O
- [ ] Unit tests for contract validation

**Success Criteria:**
- Can execute single agent task with standard I/O
- Error handling works (invalid action, execution failure)
- Metadata tracking (cost, duration, model)

**Files:**
- `lib/agent_composability/io.py` - AgentInput/AgentOutput
- `lib/agent_composability/base.py` - ComposableAgent
- `projects/scout/composable_scout.py` - ComposableScout
- `tests/agent_composability/test_io.py` - Tests

---

### Phase 2: Orchestration (4 weeks)

**Goal:** Multi-agent workflow execution (serial + parallel)

**Deliverables:**
- [ ] Build `AgentWorkflow` executor
- [ ] Support serial execution (stage chains)
- [ ] Support parallel execution (ThreadPoolExecutor)
- [ ] Stage dependency resolution (`input_from`)
- [ ] YAML workflow spec parser
- [ ] Error propagation and partial success handling

**Success Criteria:**
- Can run workflow with 3 stages (serial)
- Can run workflow with parallel fan-out (5 tasks)
- Can chain stages (output → input)
- Failures isolated, don't crash workflow

**Files:**
- `lib/agent_composability/workflow.py` - AgentWorkflow
- `lib/agent_composability/yaml_parser.py` - YAML → workflow spec
- `tests/agent_composability/test_workflow.py` - Tests

---

### Phase 3: Aggregation (2 weeks)

**Goal:** Human + LLM readable output interfaces

**Deliverables:**
- [ ] Implement `StreamingAggregator` (console output)
- [ ] Implement `JSONAggregator` (structured data)
- [ ] Implement `MarkdownAggregator` (reports)
- [ ] Progress tracking (real-time updates)
- [ ] Cost/time/error summaries

**Success Criteria:**
- Streaming output shows real-time progress
- JSON output parseable by LLMs
- Markdown reports human-readable
- All three formats show same underlying data

**Files:**
- `lib/agent_composability/aggregators.py` - All three aggregators
- `templates/workflow_report.md.j2` - Markdown template
- `tests/agent_composability/test_aggregators.py` - Tests

---

### Phase 4: Pantheon IR Integration (6 weeks)

**Goal:** Type-safe semantic messaging between agents

**Deliverables:**
- [ ] Replace `Dict[str, Any]` with `PantheonIR` types
- [ ] Cross-domain agent test (water + healthcare)
- [ ] Schema validation and type checking
- [ ] Migration guide (JSON → PantheonIR)

**Success Criteria:**
- Agents use PantheonIR for params/data
- Type errors caught before execution
- Cross-domain messaging works

**Files:**
- `lib/agent_composability/pantheon_integration.py`
- `examples/cross_domain_workflow.yaml`

---

### Phase 5: Production (8 weeks)

**Goal:** Full CLI, templates, documentation

**Deliverables:**
- [ ] CLI: `tia agent workflow run <spec.yaml>`
- [ ] CLI: `tia agent capabilities <agent>`
- [ ] CLI: `tia agent exec <agent> <action> <params>`
- [ ] Workflow templates (code review, analysis campaigns)
- [ ] Full documentation + examples
- [ ] Integration tests (end-to-end workflows)

**Success Criteria:**
- Users can run workflows via CLI
- Templates cover common use cases
- Documentation clear and complete

**Files:**
- `commands/agent/workflow.py` - CLI commands
- `workflows/templates/*.yaml` - Workflow templates
- `docs/AGENT_COMPOSABILITY_GUIDE.md` - User guide

---

## Conclusion

This specification provides the complete technical foundation for **Layer 3: Agent Ether** implementation. Key achievements:

✅ **Standard protocols** - AgentInput/AgentOutput contracts
✅ **Composability** - Agents chain like Unix commands
✅ **Orchestration** - Serial, parallel, map-reduce patterns
✅ **Transparency** - Three aggregation interfaces (human + LLM)
✅ **Cross-layer integration** - Semantic Memory, Pantheon IR, Morphogen
✅ **Implementation plan** - 5 phases, 22 weeks total

**Next Steps:**
1. Begin Phase 1 implementation (ComposableScout prototype)
2. Validate design with real use case (5 directory review)
3. Iterate based on learnings

**This is how you build semantic infrastructure - not with vibes, but with principled engineering.**

---

## Related Reading

**For philosophical foundation:**
- [Multi-Agent Protocol Principles](MULTI_AGENT_PROTOCOL_PRINCIPLES.md) - The seven principles

**For working example:**
- [TIA Unified Workspace Case Study](TIA_UNIFIED_WORKSPACE_CASE_STUDY.md) - Real implementation

**For architectural context:**
- [SIL Semantic OS Architecture](../canonical/SIL_SEMANTIC_OS_ARCHITECTURE.md) - The six-layer stack
- [SIL Principles](../canonical/SIL_PRINCIPLES.md) - Design philosophy

---

**License:** CC BY 4.0 (documentation)
**Version:** 1.0
**Last Updated:** 2025-12-03
**Implementation Status:** Design complete, Phase 1 ready to begin
