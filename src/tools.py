"""Tools for Agent Two - Netanel Systems.

Only the Researcher agent uses tools. All other agents work from text input.
"""

from typing import Literal

from tavily import TavilyClient

from src.config import TAVILY_API_KEY

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
) -> dict:
    """Search the web for information.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return.
        topic: Category of search - general, news, or finance.
        include_raw_content: Whether to include full page content.

    Returns:
        Dictionary containing search results with titles, URLs, and snippets.
    """
    try:
        return tavily_client.search(
            query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic=topic,
        )
    except Exception as e:
        return {"error": f"Search failed: {e}"}
