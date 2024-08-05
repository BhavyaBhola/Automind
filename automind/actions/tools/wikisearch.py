from automind.actions.base import BaseAction
import wikipedia
from pydantic import Field

class WikiSearch(BaseAction):
    """
    This function searches wikipedia for a topic .
    """
    query: str = Field(
        ... , description="The search string. be simple"
        )
    
    def execute(self) -> str:
      search_res = wikipedia.search(self.query)
      print(search_res)
      if not search_res:
        return 'No results found.'
      article = wikipedia.page(search_res[0])
      return article.title + '\n' + article.content