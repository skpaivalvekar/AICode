import os
import openai
from dotenv import find_dotenv, load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

""" import langchain
import getpass
from dotenv import find_dotenv, load_dotenv
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community import adapters """


load_dotenv(find_dotenv())

 
openai_api_key = os.environ["OPENAI_API_KEY"]

print("API Key Loaded:", os.environ.get("OPENAI_API_KEY"))


humanprompt = "What is the capital of India?"
sysprompt = "You are a polite helpful assistant! Your name is Sai."

""" messages = [
    SystemMessage(
        content=sysprompt
    ),
    HumanMessage(
        content=humanprompt
    )
] """

customer_review = """Pathetic. Irritating. Highly pathetic product. How you were able to make it to market. Utterly disaapointed"""
tone = """Proper English in a nice, warm and respectable tone"""
language ="""Hindi"""

custprompt = f"""Rewrite the following {customer_review} in a {tone} and translate the new review message to {language}"""



def get_completion(prompt, llm_model = "gpt-3.5-turbo"):
    messages_prompt = [    
                    {"role":"user", 
                    "content": prompt
                    }
                ]
    response =  openai.chat.completions.create(model=llm_model, messages=messages_prompt)
    return response.choices[0].message.content
    
rewrite = get_completion(prompt=custprompt)

print("Full Response:")
print(rewrite)

rewrite_parts = rewrite.split("\n")

# Print polite English version
print("\nPolite English Version:\n")
print(rewrite_parts[0].strip())  # English version of the review
print(f"\nTranslated {language} Version:\n")
print(rewrite_parts[-1].strip())  # Telugu translation of the review

print("============================")
print(rewrite_parts)

""" llm_model = "gpt-3.5-turbo"
llms = OpenAI()
model = ChatOpenAI(
    model_name=llm_model,
    openai_api_key=openai_api_key
) """

#print(llms.invoke("What is the time now in CST"))

#print(model.invoke(messages))


