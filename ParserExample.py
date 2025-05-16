import os
import json
import openai
from dotenv import find_dotenv, load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from langchain.output_parsers.structured import ResponseSchema
from langchain.output_parsers.structured import StructuredOutputParser




load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

print("API Key Loaded:", os.environ.get("OPENAI_API_KEY"))

Orig_email_list = [
    """Would be leaving at 8 AM CST from Chicago to Hyderabad for vacation. Will reach Delhi around 6 PM IST. 
    Will have breakfast and have a 3 hrs nap. 
    Then go to visit Hyderabad, Shirdi, Pune and Tirupati""",
    
""" 
Would be leaving at 8 AM CST from Amstredam to Mumbai for vacation. Will reach Chennai around 8 PM IST. 
Will have breakfast and have a 3 hrs nap. 
Then go to visit Mumbai, Shirdi, Pune and Tirupati""",

"""Would be leaving from Duabi to Hyderabad for vacation. Will reach Kolkatta. 
Will have breakfast and have a 3 hrs nap. 
Then go to visit Chennai, Shirdi, Pune and Tirupati"""]

 

email_template=""" 
From the following email extract the below Information.
leave_time: when they are leaving for vacation from Hyderabad. If the time provided use it. If not provided write unknown.
leave_from: where are they leaving from, the aiport or City and State if available
cities_to_visit:extract cities they are going to visit. If there are more than one put them in square brackets like ["CityOne", "CityTwo"]

Format the output as JSON with follwoing keys:
leave_time
leave_from
cities_to_visit

email: {email}
{format_output_instructions}
"""


leave_time_schema = ResponseSchema(name="leave_time", description="Leaving time")
leave_from_schema = ResponseSchema(name="leave_from", description="Leaving from")
cities_schema = ResponseSchema(name="cities_to_visit", description="Cities to Visit")

response_schema_list = [leave_time_schema,leave_from_schema,cities_schema]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas=response_schema_list)

format_output_instructions = output_parser.get_format_instructions()

print(format_output_instructions)


prompt_template = ChatPromptTemplate.from_template(email_template)
print(prompt_template)

llm_model = "gpt-3.5-turbo"
chat = ChatOpenAI(
    model_name=llm_model,
    openai_api_key=openai_api_key
) 

def parse_email_and_produce_json(email_from_list):
    messages_prompt = prompt_template.format_messages(email=email_from_list, format_output_instructions=format_output_instructions)
    response =  chat.invoke(messages_prompt)
    return response.content

""" json_list = list(map(parse_email_and_produce_json, Orig_email_list))

parsed_list = [json.loads(item) for item in json_list]

parsed = json.dumps(parsed_list,indent=4)

print(parsed) """

json_list = list(map(parse_email_and_produce_json, Orig_email_list))
output_dict = [output_parser.parse(item) for item in json_list]

#print(output_dict)

pretty_json = json.dumps(output_dict,indent=4)

print(pretty_json)