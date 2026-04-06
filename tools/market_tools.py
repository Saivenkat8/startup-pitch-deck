from duckduckgo_search import DDGS
from smolagents import tool


@tool
def search_web(query: str) -> list[dict]:
    """
    Searches the web for market research and competitor information.
    
    Args:
        query: The search string to look up.
        
    Returns:
        A list of dictionaries containing 'title', 'snippet', and 'link'.
    """
    results = []
    with DDGS() as ddgs:
        # We grab the top 3 results to give the agent enough context without overwhelming it
        for r in ddgs.text(query, max_results=3):
            results.append({
                "title": r.get("title", ""),
                "snippet": r.get("body", ""),
                "link": r.get("href", "")
            })
    return results