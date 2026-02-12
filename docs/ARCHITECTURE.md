# Agent-Two: Architecture Design

## Overview

Multi-agent system that takes an agentic app idea and produces a complete, buildable specification.

Specialized for agentic AI applications. Not a generic task decomposer.

## Input / Output

**Input:** Plain text idea
Example: "Build a code review agent that reviews PRs for bugs and security issues"

**Output:** Complete agentic app specification containing:
- Researched existing solutions and frameworks
- Agent roles, tools, prompts, model choices
- Workflow design (agent communication, data flow, retry logic)
- Infrastructure plan (memory, evals, tracing, deployment, cost)
- Verification report (gaps, risks, suggestions)

## Agent Architecture

```
                    ┌──────────────┐
    User Idea ───►  │  LEAD AGENT  │  ───► Final Spec
                    └──────┬───────┘
                           │ delegates via task() tool
          ┌────────────────┼────────────────────┐
          │                │                    │
          ▼                ▼                    ▼
   ┌─────────────┐ ┌──────────────┐ ┌───────────────────┐
   │ RESEARCHER  │ │AGENT DESIGNER│ │ WORKFLOW DESIGNER  │
   │             │ │              │ │                    │
   │ Finds       │ │ Designs      │ │ Plans agent        │
   │ existing    │ │ agents,      │ │ communication,     │
   │ solutions   │ │ roles,       │ │ data flow,         │
   │ & patterns  │ │ tools,       │ │ sequential vs      │
   │             │ │ prompts      │ │ parallel, retries  │
   └─────────────┘ └──────────────┘ └───────────────────┘
          │                │                    │
          └────────────────┼────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                                 ▼
   ┌──────────────┐                ┌──────────────┐
   │INFRA PLANNER │                │   VERIFIER   │
   │              │                │              │
   │ Memory,      │                │ Reviews full │
   │ evals,       │                │ design for   │
   │ tracing,     │                │ gaps, risks, │
   │ deployment,  │                │ improvements │
   │ cost         │                │              │
   └──────────────┘                └──────────────┘
```

## Agent Specifications

### 1. Lead Agent (Orchestrator)

- **Role:** Receives user idea, delegates to subagents in order, combines final output
- **Tools:** task() (built-in Deep Agents subagent tool)
- **Model:** claude-sonnet-4-5-20250929 (via ChatAnthropic)

### 2. Researcher

- **Role:** Search for existing implementations, frameworks, and patterns relevant to the idea
- **Tools:** internet_search (Tavily)
- **Model:** claude-sonnet-4-5-20250929 (via ChatAnthropic)
- **Output:**
  - Existing solutions found
  - Relevant frameworks/libraries
  - Patterns from similar systems
  - Gaps in existing solutions (what we can do better)

### 3. Agent Designer

- **Role:** Design the agents needed for the agentic app
- **Tools:** none (works from research output)
- **Model:** claude-sonnet-4-5-20250929 (via ChatAnthropic)
- **Output per agent:**
  - Name and role
  - Responsibility (what it does, what it does NOT do)
  - Tools needed
  - System prompt draft
  - Model recommendation with reasoning

### 4. Workflow Designer

- **Role:** Plan how agents communicate and coordinate
- **Tools:** none
- **Model:** claude-sonnet-4-5-20250929 (via ChatAnthropic)
- **Output:**
  - Execution order (sequential, parallel, or mixed)
  - Data flow between agents (what passes from A to B)
  - Retry logic (what happens on failure)
  - Human-in-the-loop points (where human approval is needed)
  - Termination conditions

### 5. Infrastructure Planner

- **Role:** Plan the non-agent infrastructure
- **Tools:** none
- **Model:** claude-sonnet-4-5-20250929 (via ChatAnthropic)
- **Output:**
  - Memory strategy (short-term, long-term, what to persist)
  - Evaluation criteria (how to measure agent output quality)
  - Tracing/observability setup (LangSmith config)
  - Deployment plan (local, cloud, API)
  - Cost estimate (tokens per run, monthly projection)

### 6. Verifier

- **Role:** Review the complete design and flag issues
- **Tools:** none (read-only review)
- **Model:** claude-sonnet-4-5-20250929 (via ChatAnthropic)
- **Output:**
  - Gaps found (missing agents, tools, or flows)
  - Risks identified (single points of failure, cost risks)
  - Suggestions for improvement
  - Final verdict: APPROVED or NEEDS REVISION

## Execution Flow

```
1. Lead receives idea
2. Lead → Researcher: "Find existing solutions for: {idea}"
3. Lead → Agent Designer: "Design agents based on: {idea} + {research}"
4. Lead → Workflow Designer: "Design workflow for: {agents}"
5. Lead → Infra Planner: "Plan infrastructure for: {agents} + {workflow}"
6. Lead → Verifier: "Review this design: {research} + {agents} + {workflow} + {infra}"
7. Lead combines all outputs into final structured document
```

Sequential execution for v1. Each agent's output feeds into the next.

## Tech Stack

- Deep Agents SDK (create_deep_agent + subagents)
- LangChain (ChatAnthropic from langchain-anthropic)
- Tavily (web search for Researcher)
- LangSmith (tracing)
- Python 3.11+

## Scope

**v1 (now):**
- Sequential execution
- Text output to terminal
- Specialized for agentic apps

**v2 (later):**
- Streaming output
- Save to file
- Auto-create GitHub issues from output

**v3 (future):**
- Self-evolving prompts based on past outputs
- Parallel subagent execution
- Multiple domain specializations
