"""Agent definitions for Agent Two - Netanel Systems.

Defines the Lead orchestrator and 5 specialized subagents.
Uses create_deep_agent with the subagents parameter for context isolation.

Verified from docs: https://docs.langchain.com/oss/python/deepagents/subagents
Pattern: subagents inherit the main agent's model unless overridden.
"""

from deepagents import create_deep_agent

from src.config import MODEL
from src.prompts import (
    AGENT_DESIGNER_PROMPT,
    INFRA_PLANNER_PROMPT,
    LEAD_PROMPT,
    RESEARCHER_PROMPT,
    VERIFIER_PROMPT,
    WORKFLOW_DESIGNER_PROMPT,
)
from src.tools import internet_search

# Define the 5 subagents as dictionaries.
# Each gets spawned as an ephemeral agent when Lead calls task().
# Model is inherited from the main agent (Claude Sonnet) unless overridden.

researcher = {
    "name": "researcher",
    "description": "Researches existing solutions, frameworks, and patterns for agentic AI applications. Use this first to understand the landscape before designing.",
    "system_prompt": RESEARCHER_PROMPT,
    "tools": [internet_search],
}

agent_designer = {
    "name": "agent_designer",
    "description": "Designs agents with roles, tools, system prompts, and model recommendations based on research findings.",
    "system_prompt": AGENT_DESIGNER_PROMPT,
    "tools": [],
}

workflow_designer = {
    "name": "workflow_designer",
    "description": "Plans agent communication, data flow, execution order, retry logic, and termination conditions.",
    "system_prompt": WORKFLOW_DESIGNER_PROMPT,
    "tools": [],
}

infra_planner = {
    "name": "infra_planner",
    "description": "Plans memory, evaluation criteria, tracing, deployment, and cost estimation for the system.",
    "system_prompt": INFRA_PLANNER_PROMPT,
    "tools": [],
}

verifier = {
    "name": "verifier",
    "description": "Reviews the complete design for gaps, risks, and improvement suggestions. Returns APPROVED or NEEDS REVISION.",
    "system_prompt": VERIFIER_PROMPT,
    "tools": [],
}

# All subagents in delegation order
subagents = [researcher, agent_designer, workflow_designer, infra_planner, verifier]

# Lead Agent — the orchestrator.
# Has no tools of its own. Delegates via the built-in task() tool.
# Subagents are ephemeral: born, do work, return report, die.
lead_agent = create_deep_agent(
    model=MODEL,
    system_prompt=LEAD_PROMPT,
    subagents=subagents,
)
