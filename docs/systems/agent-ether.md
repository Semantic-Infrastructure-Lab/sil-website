# Agent Ether: Tool Behavior Contracts for Multi-Agent Systems

> *Universal tool orchestration layer for agentic AI*

## The Problem

**The Fragmented Tool Landscape**

AI agents today face unpredictable chaos when using tools:

- **No standard interface:** Every tool has different calling conventions
  - Sync vs async? Blocking vs streaming? No way to know without trying
  - Agent wastes tokens guessing execution model

- **Unpredictable behavior:** Agents don't know what to expect
  - Does this tool return immediately or run for hours?
  - Will it report progress or go silent?
  - Can I monitor it or is it a black box?

- **Hidden side effects:** No visibility into internal state
  - Progress unknown → Agent polls blindly or timeouts
  - Logs inaccessible → Can't diagnose failures
  - State invisible → Can't resume after interruption

- **Security blind spots:** Unclear what tools can do
  - What files can it read?
  - Can it access the network?
  - What's the blast radius if it fails?

- **Poor composability:** Can't reliably chain tools
  - Tool A outputs format incompatible with Tool B input
  - Agent writes brittle glue code per tool pair
  - Multi-step workflows fragile to tool updates

- **Multi-agent chaos:** Agents can't coordinate
  - Agent A doesn't know how to invoke Agent B
  - No shared protocol for delegation
  - Duplicate work, conflicting actions

**Result:** Agents waste tokens on trial-and-error, make wrong assumptions about tool behavior, and produce brittle workflows that break when tools change.

---

## The Innovation

**Tool Behavior Contract (TBC): Unified Metadata-Driven Interface**

Agent Ether introduces a specification where every tool declares exactly how it behaves:

### The Contract: 5 Questions Every Tool Answers

**1. How does it execute?**
```json
{
  "execution": {
    "mode": "job"  // sync, async, job, or session
  }
}
```

**2. What channels does it use?**
```json
{
  "io": {
    "stdin": "structured",   // JSON input
    "stdout": "structured",  // JSON output
    "progress": "events"     // Progress via event stream
  }
}
```

**3. How do you track progress?**
```json
{
  "progress_model": {
    "type": "percent",       // percent, steps, or indeterminate
    "channel": "events"      // Where to read progress from
  }
}
```

**4. What permissions does it need?**
```json
{
  "security": {
    "permissions": ["filesystem-read", "network-access"],
    "audit_level": "full",
    "rate_limits": {"max_per_minute": 30}
  }
}
```

**5. How do you invoke and monitor it?**
```json
{
  "devices": {
    "invoke": "/dev/agent-ether/tools/fs.search/invoke",
    "events": "/dev/agent-ether/tools/fs.search/jobs/{id}/events",
    "result": "/dev/agent-ether/tools/fs.search/jobs/{id}/result"
  }
}
```

**Agents read the metadata once and know exactly how to use ANY tool.**

### Four Execution Modes Unified

**🟩 Sync** (Request → Response)
- Simple queries, calculations, validations
- Blocking call, single request/response
- Example: `tool.invoke(input) → output`

**🟦 Async** (Fire and Monitor)
- Background tasks, API calls
- Returns operation ID immediately, produces events asynchronously
- Example: `op_id = tool.invoke(input); poll events until done`

**🟪 Job** (Long-Running with Progress)
- Builds, compilations, large searches
- Returns job ID, reports progress via events
- Example: `job_id = tool.invoke(input); monitor progress; get result`

**🟧 Session** (Interactive/Stateful)
- REPLs, browsers, debuggers, terminals
- Persistent bidirectional streams, stateful conversation
- Example: `session_id = tool.create_session(); write/read loop`

**One interface. Four modes. Infinite tools.**

---

## Quick Example: Filesystem Search

**Tool declares its behavior** (`/sys/agent-ether/registry/tools.d/fs.search.json`):

```json
{
  "id": "fs.search",
  "version": "1.2.0",
  "execution": { "mode": "job" },
  "io": {
    "stdin": "structured",
    "stdout": "structured",
    "progress": "events"
  },
  "progress_model": {
    "type": "percent",
    "channel": "events"
  },
  "security": {
    "permissions": ["filesystem-read"],
    "audit_level": "full"
  },
  "devices": {
    "invoke": "/dev/agent-ether/tools/fs.search/invoke",
    "events": "/dev/agent-ether/tools/fs.search/jobs/{id}/events",
    "result": "/dev/agent-ether/tools/fs.search/jobs/{id}/result"
  }
}
```

**Agent uses metadata to invoke correctly:**

```python
from agent_ether import ToolRegistry, ToolInvoker

# 1. Discover tool
registry = ToolRegistry()
tool = registry.get_tool("fs.search")

# 2. Agent reads metadata and knows:
#    - It's a job (long-running)
#    - It reports percent progress via events
#    - It needs filesystem-read permission
#    - Input/output is structured JSON

# 3. Invoke with correct pattern
invoker = ToolInvoker(tool)
job_id = invoker.invoke({
    "pattern": "*.py",
    "path": "/home/user/project"
})

# 4. Monitor progress (metadata told us how)
for event in invoker.stream_events(job_id):
    if event["event"] == "progress":
        print(f"Progress: {event['data']['percent']}%")
    elif event["event"] == "done":
        results = event["data"]["result"]
        break
```

**No guessing. No hardcoded assumptions. Just metadata-driven orchestration.**

---

## Status & Adoption

**Current Version:** v0.1.0-alpha (Design Phase with Complete Specification)

**Production Metrics:**
- ✅ **Complete TBC specification** defined
- ✅ **Architecture designed** (registry, executor, device filesystem, security, tracing)
- ✅ **Four execution modes** specified (sync, async, job, session)
- ✅ **Virtual device filesystem** designed (`/dev/agent-ether/*` paths)
- ✅ **Security model** complete (permissions, audit levels, rate limits)
- 🔄 **Reference implementation** in progress (Python SDK)

**Novel Research Contributions:**

1. **Tool Behavior Contract (TBC) Specification**
   - Declarative metadata describes tool execution model
   - Agents discover tools, read contracts, invoke correctly
   - No trial-and-error, no hardcoded tool logic
   - **Industry first:** Unified interface spanning sync/async/job/session modes

2. **Virtual Device Filesystem (`/dev/agent-ether/*`)**
   - Unix-like device paths for tool interaction
   - Agents write to `/dev/agent-ether/tools/{id}/invoke`
   - Read progress from `/dev/agent-ether/tools/{id}/jobs/{job_id}/events`
   - Familiar interface, universal access pattern

3. **Four Execution Modes Unified**
   - **Sync:** Simple request/response
   - **Async:** Fire-and-forget with event monitoring
   - **Job:** Long-running with progress tracking
   - **Session:** Interactive bidirectional streams
   - Same discovery/invocation pattern, different execution models

4. **Metadata-Driven Security**
   - Every tool declares permissions upfront
   - Agent runtime enforces constraints
   - Audit logging for all invocations
   - Rate limiting prevents abuse

**What This Unlocks:**
- **Predictable agent behavior** - No more token waste guessing tool interfaces
- **Multi-agent orchestration** - Agents can delegate to other agents using same TBC protocol
- **Tool composability** - Chain tools reliably (metadata guarantees compatibility)
- **Security transparency** - Know permissions before invocation, not after breach

**v1.0 Release Timeline:** Active design phase
- Reference implementation (Python SDK)
- Tool adapter SDK (wrap existing tools in TBC metadata)
- Multi-agent coordination protocols
- Integration with Pantheon IR (tool graphs as semantic IR)

---

## Technical Deep Dive

**Full Documentation:**
- [Agent Ether GitHub Repository](https://github.com/Semantic-Infrastructure-Lab/agent-ether)
- [TBC Specification](https://github.com/Semantic-Infrastructure-Lab/agent-ether/blob/main/docs/specifications/tool-behavior-contract.md)
- [Architecture Guide](https://github.com/Semantic-Infrastructure-Lab/agent-ether/blob/main/docs/architecture/)
- [Multi-Agent Coordination](https://github.com/Semantic-Infrastructure-Lab/agent-ether/blob/main/docs/architecture/MULTI_AGENT_COORDINATION.md)

**Example Gallery:**
- [Filesystem Search Tool](https://github.com/Semantic-Infrastructure-Lab/agent-ether/tree/main/examples/fs-search) - Job execution mode
- [REPL Session Tool](https://github.com/Semantic-Infrastructure-Lab/agent-ether/tree/main/examples/repl) - Interactive session mode
- [API Call Tool](https://github.com/Semantic-Infrastructure-Lab/agent-ether/tree/main/examples/api-call) - Async execution mode

**Getting Started:**
```bash
git clone https://github.com/Semantic-Infrastructure-Lab/agent-ether.git
cd agent-ether
# Design docs available, implementation in progress
```

---

## Part of SIL's Semantic OS Vision

**Agent Ether's Role in the 7-Layer Semantic OS:**

- **Layer 6 (Intelligence):** Agent orchestration, tool discovery, multi-agent coordination
  - **Tool registry:** Discover available tools and read TBC metadata
  - **Tool executor:** Invoke tools using metadata-driven patterns
  - **Multi-agent protocols:** Agents orchestrate other agents using same TBC interface
  - **Planning & reasoning:** Agents compose tool calls into workflows

**Composes With:**
- **Pantheon (Layer 3/5):** Tool graphs as Pantheon IR
  - Workflow planning compiles to Pantheon semantic graphs
  - Validation framework ensures tool composition is semantically valid
  - Constraint solving optimizes tool execution order

- **BrowserBridge (Layer 6):** Human-AI collaboration layer
  - Agents observe browser state, invoke browser tools
  - Same TBC interface for browser automation as any other tool

- **All Layers (0-5):** Universal tool interface
  - Layer 0 (Substrate): Hardware control tools (Philbrick modules)
  - Layer 1 (Primitives): Domain operation tools (Morphogen operators)
  - Layer 2 (Structures): Data structure manipulation tools (TiaCAD geometry)
  - Layer 3 (Composition): Graph operation tools (Pantheon transformations)
  - Layer 4 (Dynamics): Temporal execution tools (schedulers, timers)
  - Layer 5 (Intent): Constraint solving tools (validators, optimizers)

**Architectural Principle:** *Intelligence Scales with Coordination, Not Opacity*

Agent Ether proves that multi-agent systems don't need black-box communication. When agents share a predictable protocol (TBC), coordination becomes natural instead of heroic.

**The Key Insight:**
Most agent frameworks treat tools as afterthoughts (wrap existing tools, hope for best). Agent Ether makes tool contracts the foundation:
- **Discoverable:** Agents list tools, read metadata
- **Predictable:** Execution model declared upfront
- **Safe:** Permissions checked before invocation
- **Traceable:** Every action logged and auditable

This transforms multi-agent systems from "pray it works" to "provably correct orchestration."

---

## Impact: Real-World Use Cases

**Before Agent Ether:**
- Agent guesses tool is sync → Calls blocking tool → Hangs for hours
- Agent assumes JSON output → Tool returns YAML → Parse error
- Multi-agent system: Agent A doesn't know how to delegate to Agent B → Hardcoded per-agent logic
- Security: Agent uses tool → Later discovers it wrote to filesystem unexpectedly

**With Agent Ether:**
- Agent reads TBC metadata → Knows tool is job with progress → Monitors correctly
- Agent sees "output: structured" → Parses JSON confidently
- Multi-agent: Agent A reads Agent B's TBC → Delegates using same protocol as any tool
- Security: Agent checks permissions upfront → Filesystem write blocked before invocation

**Use Cases Enabled:**

1. **Multi-Agent Orchestration**
   - Research agents delegate to specialist agents (code, writing, analysis)
   - Hierarchical task decomposition with agent-to-agent coordination
   - Transparent handoffs (full audit trail of delegations)

2. **Tool Marketplace**
   - Third-party tools publish TBC metadata
   - Agents discover and integrate new tools dynamically
   - No code changes to agent, just metadata registration

3. **Safe Autonomous Systems**
   - Agents declare required permissions upfront
   - Runtime enforces constraints (filesystem, network, rate limits)
   - Audit logs capture all tool invocations for compliance

4. **LLM-Optimized Workflows**
   - Agents read TBC metadata once, cache knowledge
   - No token waste on "how does this tool work?"
   - Correct invocation patterns guaranteed by metadata

**Adoption Path (v1.0 Goals):**
- 20+ tools with TBC metadata (filesystem, network, browsers, REPLs)
- Reference implementation (Python SDK)
- Multi-agent coordination framework
- Integration with major agent frameworks (LangChain, AutoGPT, etc.)

---

**Version:** 0.1.0-alpha → 1.0 (Active Design Phase)
**License:** Apache 2.0
**Status:** Complete specification, architecture designed, implementation in progress

**Patron Saint:** Marvin Minsky (1927-2016)
*"The Society of Mind" - Intelligence emerges from coordination of simple agents*

**Learn More:**
- [GitHub Repository](https://github.com/Semantic-Infrastructure-Lab/agent-ether)
- [Tool Behavior Contract Spec](https://github.com/Semantic-Infrastructure-Lab/agent-ether/blob/main/docs/specifications/tool-behavior-contract.md)
- [Architecture](https://github.com/Semantic-Infrastructure-Lab/agent-ether/blob/main/docs/architecture/)
