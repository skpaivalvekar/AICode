import os
import datetime
from dotenv import find_dotenv, load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from schema import AnswerTheQuestion, Reflection
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.messages import HumanMessage
from langsmith import traceable


load_dotenv(find_dotenv())
#openai_api_key = os.environ["GOOGLE_API_KEY"]



#print("API Key Loaded:", os.environ.get("GOOGLE_API_KEY"))

#google_llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
openai_llm = ChatOpenAI(model="gpt-4o-mini")

pydantic_parser = PydanticToolsParser(tools=[AnswerTheQuestion])

actor_prompt_template = ChatPromptTemplate.from_messages(
                                                            [   ("system", """You are an expert AI Researcher.
                                                                        CurrentTime : {now}
                                                                        1.{firstInstruction}
                                                                        2. Reflect and critique your answer. Be Severe to maximize improvement.
                                                                        3. After the reflection, **list 1-3 search queries seperately** for 
                                                                           researching improvements. Do not include them inside reflection.
                                                                        """
                                                                 ),
                                                                MessagesPlaceholder(variable_name = "humanmessages"),
                                                                ("system", "Answer the user query using the required format")
                                                            ]
                                                            ).partial(now = lambda: datetime.datetime.now().isoformat()
                                                        )
                                                        
first_actor_prompt_template = actor_prompt_template.partial(firstInstruction ="Provide me a 250 word answer")



first_actor_chain = (first_actor_prompt_template | openai_llm.bind_tools(tools = [AnswerTheQuestion], tool_choice='AnswerTheQuestion') | pydantic_parser)



response = first_actor_chain.invoke(
                                        {
                                        "humanmessages" : [HumanMessage(content="Write a blog about how AI impacts education industry")]
                                        }

                                    )


lang_api_key = os.environ["LANGSMITH_API_KEY"]

print("Lang API Key Loaded:", os.environ.get("LANGSMITH_API_KEY"))

lng_key_project = os.environ["LANGSMITH_PROJECT"]
print("Lang API Project Loaded:", os.environ.get("LANGSMITH_PROJECT"))