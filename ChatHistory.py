import os
import openai
from dotenv import find_dotenv, load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


load_dotenv(find_dotenv())

 
openai_api_key = os.environ["OPENAI_API_KEY"]

print("API Key Loaded:", os.environ.get("OPENAI_API_KEY"))

llm_model = "gpt-3.5-turbo"
model = ChatOpenAI(
    model_name=llm_model,
    openai_api_key=openai_api_key
) 

chat_history=[]

system_message = SystemMessage(content ="You are a Chat Model and your name is SKPAI. Your creator's name is Boss SKP")
chat_history.append(system_message)

while True:
    query = input("You :")
    if (query.lower() == "quit"):
        break
    
    chat_history.append(HumanMessage(content=query))
    result = model.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))
    
    print(f"AI : {response}")
                        
    




