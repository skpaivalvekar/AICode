import os
import json
import openai
from dotenv import find_dotenv, load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from langchain.output_parsers.structured import ResponseSchema
from langchain.output_parsers.structured import StructuredOutputParser
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from pydantic import BaseModel, Field, field_validator

class VacationInfo(BaseModel):
    leave_time : str = Field(description="Leave Time")
    leave_from : str = Field(description="Leave From")
    cities_to_visit : list = Field(description="List of cities")
    num_people: int = Field(description="Number of people")
    
    @field_validator('num_people')
    def check_num_people(cls,value):
        if value <= 0:
            raise ValueError("Number must be positive")
        return value

load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

print("API Key Loaded:", os.environ.get("OPENAI_API_KEY"))

llm_model = "gpt-3.5-turbo"
chat = ChatOpenAI(
    model_name=llm_model,
    openai_api_key=openai_api_key
) 



Orig_email_list = [
    """We are grouof 5 people and Would be leaving at 8 AM CST from Chicago to Hyderabad for vacation. Will reach Delhi around 6 PM IST. 
    Will have breakfast and have a 3 hrs nap. 
    Then go to visit Hyderabad, Shirdi, Pune and Tirupati""",
    
""" 
Would be leaving at 8 AM CST from Amstredam to Mumbai for vacation. Will reach Chennai around 8 PM IST. 
Will have breakfast and have a 3 hrs nap. 
Then go to visit Mumbai, Shirdi, Pune and Tirupati""",

"""We are grouof 15 people and Would be leaving from Duabi to Hyderabad for vacation. Will reach Kolkatta. 
Will have breakfast and have a 3 hrs nap. 
Then go to visit Chennai, Shirdi, Pune and Tirupati"""]

 

email_template=""" 
From the following email extract the below Information.
leave_time: when they are leaving for vacation from Hyderabad. If the time provided use it. If not provided write unknown.
leave_from: where are they leaving from, the aiport or City and State if available
cities_to_visit:extract cities they are going to visit. If there are more than one put them in square brackets like ["CityOne", "CityTwo"]
num_people: Number of people travelliing. If not available, set it to 0.

Format the output as JSON with follwoing keys:
leave_time
leave_from
cities_to_visit
num_people

email: {email}
{format_output_instructions}
"""


email_template_pydantic=""" 
From the following email extract the below Information.

email: {email}
{format_output_instructions}
"""

prompt_template = ChatPromptTemplate.from_template(email_template_pydantic)
print(prompt_template)

pydantic_parser = PydanticOutputParser(pydantic_object=VacationInfo)
format_output_instructions = pydantic_parser.get_format_instructions()

def parse_email_and_produce_json(email_from_list):
    messages_prompt = prompt_template.format_messages(email=email_from_list, format_output_instructions=format_output_instructions)
    response =  chat.invoke(messages_prompt)
    return response.content

json_list = list(map(parse_email_and_produce_json, Orig_email_list))
output_dict = [pydantic_parser.parse(item) for item in json_list]

print(output_dict)