import typer
import os

from typing import List, Optional
from dotenv import load_dotenv

from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector
from phi.storage.agent.postgres import PgAgentStorage
from phi.agent import Agent, RunResponse
from phi.assistant import assistant
from phi.agent import Agent
#from phi.model.google import Gemini

load_dotenv()
#os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

def setup_knowledge_base(pdf_url: str):
    return PDFUrlKnowledgeBase(
        urls=[pdf_url],
        vector_db=PgVector(
            table_name="pdf_documents",
            db_url=db_url
        )
    )

def pdf_assistant(pdf_url: str = "https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf", user: str = "user"):
    run_id: Optional[str] = None
    
    knowledge_base = setup_knowledge_base(pdf_url)
    agent = Agent(
        storage=PgAgentStorage(
            table_name="pdf_agent", 
            db_url=db_url
        ),
        knowledge=knowledge_base,
        show_tool_calls=True,
        search_knowledge=True,
        read_chat_history=True
    )
    
    # Load knowledge base (comment out after first run)
    agent.knowledge.load(recreate=False)
    
    if run_id is None:
        run_id = agent.run_id
        print(f"Started Run: {run_id}\n")
    else:
        print(f"Continuing Run: {run_id}\n")

    # Start CLI loop
    while True:
        try:
            agent.cli_app(markdown=True)
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    typer.run(pdf_assistant)

