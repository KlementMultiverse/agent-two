"""Agent Two: Multi-Agent Spec Generator by Netanel Systems.

Takes an agentic app idea and produces a complete, buildable specification
through 6 specialized agents:
  Lead → Researcher → Agent Designer → Workflow Designer → Infra Planner → Verifier

Usage:
    python -m src.agent "Build a code review agent that reviews PRs"

Output saved to: output/YYYY-MM-DD-idea-slug.md
"""

import os
import re
import sys
import time
from datetime import datetime

from src.agents import lead_agent

# Map subagent names to step number + description for progress display.
# Order matches the sequential execution flow defined in the Lead prompt.
AGENT_STEPS = {
    "researcher": (1, "Researcher", "Researching solutions and patterns"),
    "agent_designer": (2, "Agent Designer", "Designing agents, roles, and tools"),
    "workflow_designer": (3, "Workflow Designer", "Planning communication and data flow"),
    "infra_planner": (4, "Infra Planner", "Planning memory, evals, and deployment"),
    "verifier": (5, "Verifier", "Reviewing design for gaps and risks"),
}
TOTAL_STEPS = 5


def slugify(text: str, max_length: int = 50) -> str:
    """Convert text to a filename-safe slug."""
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    return slug[:max_length].rstrip("-")


def format_duration(seconds: float) -> str:
    """Format seconds into human-readable duration."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"


def main() -> None:
    """Run agent-two with streaming progress indicators."""
    if len(sys.argv) < 2:
        print("Usage: python -m src.agent 'your agentic app idea'")
        print()
        print("Example:")
        print("  python -m src.agent 'Build a code review agent that reviews PRs'")
        print("  python -m src.agent 'Build a customer support agent with memory'")
        sys.exit(1)

    idea = " ".join(sys.argv[1:])

    print(f"\n  Generating specification for: {idea}")
    print("=" * 60)
    print(f"  Pipeline: Lead (Sonnet) → {TOTAL_STEPS} subagents (Haiku)")
    print("=" * 60)

    current_agent = None
    agent_start_time = None
    overall_start = time.time()
    last_root_state = None

    for namespace, stream_mode, data in lead_agent.stream(
        {"messages": [{"role": "user", "content": idea}]},
        config={"configurable": {"thread_id": "1"}},
        stream_mode=["messages", "values"],
        subgraphs=True,
    ):
        # --- Progress tracking via message metadata ---
        if stream_mode == "messages":
            token, metadata = data
            agent_name = metadata.get("lc_agent_name", "")

            if agent_name and agent_name != current_agent:
                # Print completion time for previous agent
                if current_agent and agent_start_time:
                    elapsed = time.time() - agent_start_time
                    if current_agent in AGENT_STEPS:
                        print(f"  Done ({format_duration(elapsed)})")

                current_agent = agent_name
                agent_start_time = time.time()

                # Print new agent status
                if agent_name in AGENT_STEPS:
                    step_num, display_name, description = AGENT_STEPS[agent_name]
                    total_elapsed = time.time() - overall_start
                    print(
                        f"\n  [{step_num}/{TOTAL_STEPS}] {display_name}"
                        f"  ({format_duration(total_elapsed)} elapsed)"
                    )
                    print(f"  {description}...")
                elif agent_name == "lead":
                    total_elapsed = time.time() - overall_start
                    print(
                        f"\n  [Lead] Orchestrating..."
                        f"  ({format_duration(total_elapsed)} elapsed)"
                    )

        # --- Capture final state from root graph ---
        if stream_mode == "values":
            # Root graph namespace is an empty tuple
            if namespace == ():
                last_root_state = data

    # Print completion for last agent
    if current_agent and agent_start_time:
        elapsed = time.time() - agent_start_time
        if current_agent in AGENT_STEPS:
            print(f"  Done ({format_duration(elapsed)})")

    total_time = time.time() - overall_start
    print(f"\n{'=' * 60}")
    print(f"  Completed in {format_duration(total_time)}")
    print("=" * 60)

    # Extract final output from last root state
    if last_root_state and "messages" in last_root_state:
        output = last_root_state["messages"][-1].content
    else:
        print("\nError: No output captured. The pipeline may have failed.")
        sys.exit(1)

    # Save to file
    os.makedirs("output", exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(idea)
    filename = f"output/{date_str}-{slug}.md"

    with open(filename, "w") as f:
        f.write(output)

    print(f"\n{output}")
    print(f"\n{'=' * 60}")
    print(f"  Saved to: {filename}")
    print(f"  Length: {len(output):,} characters")


if __name__ == "__main__":
    main()
