from automind.actions.base import BaseAction
from typing import str
from pydantic import Field
from duckduckgo_search import DDGS

class DuckDuckGoSearch(BaseAction):
    """
    This function searches DuckDuckGo search engine for a topic .
    """
    query: str = Field(
        ... , description="The search string. be simple"
        )
    
    def execute(self) -> str:
      results = DDGS().text(self.query, max_results=2)
      return results