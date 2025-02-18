from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool

def get_search_tool():
    """Initialize and return the DuckDuckGo search tool."""
    search = DuckDuckGoSearchRun()
    return Tool(
        name="web_search",
        func=search.run,
        description="Useful for searching the web for current information. Use this when you need to find up-to-date information about a topic."
    )

def get_tools():
    """Get all available tools."""
    return [get_search_tool()] 