import typer
import os
from dotenv import load_dotenv

from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.firecrawl import FirecrawlTools

# Load environment variables
load_dotenv()

app = typer.Typer()

@app.command()
def summarize(url: str = "https://en.wikipedia.org/wiki/MS_Dhoni"):
    """
    Summarize a webpage using Firecrawl and Gemini.
    """
    agent = Agent(
        name="firecrawl_agent",
        model=Gemini(id="gemini-1.5-flash"),
        tools=[FirecrawlTools(scrape=True)],
        show_tool_calls=True,
        markdown=True,
    )

    agent.print_response(f"Summarize this webpage: {url}", stream=True)
    print("\n[DEBUG] Tools used in this response:", agent.last_response.tool_calls)

if __name__ == "__main__":
    app()
