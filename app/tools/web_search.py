from langchain_core.tools import tool
from ddgs import DDGS

@tool
def web_search(query: str) -> str:
    """Searches the web for information using DuckDuckGo.
    
    Args:
        query: The search query string.
    """
    try:
        with DDGS() as ddgs:
            # We fetch up to 3 results to keep context small
            results = list(ddgs.text(query, max_results=3))
            
        if not results:
            return "No results found."
            
        formatted_results = []
        for r in results:
            formatted_results.append(f"Title: {r['title']}\nSummary: {r['body']}\nURL: {r['href']}")
            
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Error performing web search: {e}"
