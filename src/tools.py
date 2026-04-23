from tavily import TavilyClient
from langchain_tavily import TavilySearch


def get_agent_tools():
    tavily = TavilyClient()
    tavily_search_tool = TavilySearch (
        max_results=3,
        search_depth="advanced"
    )
    return [tavily_search_tool]