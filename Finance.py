
import os
import openai
from dotenv import find_dotenv, load_dotenv
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.model.google import Gemini




load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

finance_agent = Agent(
    name="Finance Agent",
    model=Gemini(model="gemini-1.5-flash"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)
while True:
    finance_agent.print_response("show latest NVDA stock price in table format", stream=True)
    
