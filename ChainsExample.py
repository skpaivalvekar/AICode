import os
import openai
from dotenv import find_dotenv, load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser


load_dotenv(find_dotenv())

 
openai_api_key = os.environ["OPENAI_API_KEY"]

print("API Key Loaded:", os.environ.get("OPENAI_API_KEY"))

llm_model = "gpt-3.5-turbo"
model = ChatOpenAI(
    model_name=llm_model,
    openai_api_key=openai_api_key
) 

messages =[
    ("system", "You are a facts expert who know about {country}" ),
    ("human", "Tell me {fact_count} facts.")
]

translation_messages =[
    ("system", "You are a office assistant and compose an email" ),
    ("human", "Compose message to {mailID}: {message}")
]


parser = StrOutputParser() 
prompt_template = ChatPromptTemplate.from_messages(messages)

translation_template = ChatPromptTemplate.from_messages(translation_messages)

facts_chain = prompt_template | model | parser

facts_result = facts_chain.invoke({"country":"India", "fact_count": 3})

translation_chain = translation_template | model | parser

result = translation_chain.invoke({"mailID":"Ravi", "message": facts_result})

print(result)

