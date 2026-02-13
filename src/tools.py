"""Tools for Agent Two - Netanel Systems.

Only the Researcher agent uses tools. All other agents work from text input.

Two search tools:
- internet_search: Broad discovery search (find tool names, patterns, frameworks)
- search_official_site: Targeted search for a specific tool's official homepage
"""

from typing import Literal, Sequence

from tavily import TavilyClient

from src.config import TAVILY_API_KEY

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# Domains that are aggregators/listicles, not official product pages
BLOG_DOMAINS = [
    "medium.com",
    "dev.to",
    "hackernoon.com",
    "towardsdatascience.com",
    "stackoverflow.blog",
    "news.ycombinator.com",
    "reddit.com",
]


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    search_depth: Literal["basic", "advanced"] = "basic",
) -> dict:
    """Search the web for information. Use this for broad discovery searches.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return.
        topic: Category of search - general, news, or finance.
        search_depth: "basic" for fast results, "advanced" for deeper crawling.

    Returns:
        Dictionary containing search results with titles, URLs, and snippets.
    """
    try:
        return tavily_client.search(
            query,
            max_results=max_results,
            search_depth=search_depth,
            topic=topic,
        )
    except Exception as e:
        return {"error": f"Search failed: {e}"}


def search_official_site(
    tool_name: str,
    max_results: int = 3,
) -> dict:
    """Find the official homepage/docs for a specific tool or product.

    Use this AFTER discovering a tool name via internet_search.
    Excludes blog aggregators to find the actual product page.

    Args:
        tool_name: Name of the tool/product to find (e.g., "CodeRabbit", "SonarQube").
        max_results: Maximum number of results to return.

    Returns:
        Dictionary containing search results filtered to official sites.
    """
    try:
        return tavily_client.search(
            f"{tool_name} official site",
            max_results=max_results,
            search_depth="advanced",
            exclude_domains=BLOG_DOMAINS,
        )
    except Exception as e:
        return {"error": f"Search failed: {e}"}
