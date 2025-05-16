from openai import OpenAI
from langsmith import traceable
from langsmith.wrappers import wrap_openai
from dotenv import find_dotenv, load_dotenv
import os


load_dotenv(find_dotenv())
openai_client = wrap_openai(OpenAI())

from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
llm.invoke("Hello, world!")


lang_api_key = os.environ["LANGSMITH_API_KEY"]

print("Lang API Key Loaded:", os.environ.get("LANGSMITH_API_KEY"))

lng_key_project = os.environ["LANGSMITH_PROJECT"]
print("Lang API Project Loaded:", os.environ.get("LANGSMITH_PROJECT"))