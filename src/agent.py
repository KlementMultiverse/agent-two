"""Agent Two: Multi-Agent Spec Generator by Netanel Systems.

Takes an agentic app idea and produces a complete, buildable specification
through 6 specialized agents:
  Lead → Researcher → Agent Designer → Workflow Designer → Infra Planner → Verifier

Usage:
    python -m src.agent "Build a code review agent that reviews PRs"
"""

import sys

from src.agents import lead_agent


def main() -> None:
    """Run agent-two from command line."""
    if len(sys.argv) < 2:
        print("Usage: python -m src.agent 'your agentic app idea'")
        print()
        print("Example:")
        print("  python -m src.agent 'Build a code review agent that reviews PRs'")
        print("  python -m src.agent 'Build a customer support agent with memory'")
        sys.exit(1)

    idea = " ".join(sys.argv[1:])

    print(f"\nGenerating specification for: {idea}")
    print("=" * 60)
    print("Running 5 subagents sequentially. This may take a few minutes.\n")

    response = lead_agent.invoke(
        {"messages": [{"role": "user", "content": idea}]},
        config={"configurable": {"thread_id": "1"}},
    )

    print(response["messages"][-1].content)


if __name__ == "__main__":
    main()
