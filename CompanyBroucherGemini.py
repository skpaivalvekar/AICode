import os
import requests
from typing import List
import json
from bs4 import BeautifulSoup
from IPython.display import HTML, Markdown, display, update_display
from google import genai
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")



client = genai.Client(api_key="GEMINI_API_KEY")


class Website:
    url : str
    title : str
    body : str
    text : str
    links : list[str]

    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.body = response.content
        soup = BeautifulSoup(self.body, "html.parser")
        self.title = soup.title.string if soup.title else " No Title Found"

        if soup.body:
            for irrelvant_tag in soup.body(['script', 'style', 'header', 'footer', 'nav']):
                irrelvant_tag.decompose()

            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.title = ""

        

        links = [link.get("href") for link in soup.find_all("a")]
        self.links = [link for link in links if link ]  

    def get_contents(self):
        return f"""
                Title: {self.title}
                Text: {self.text}
                Links: {self.links}
            """
ed = Website("https://www.infosys.com/")
#print(ed.get_content())

link_system_prompt = "You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
link_system_prompt += "You should respond in JSON as in this example:"
link_system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page": "url": "https://another.full.url/careers"}
    ]
}
"""

#print(link_system_prompt)


def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt

def get_links_response(url):
    website = Website(url)
    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[
                                    {"type": "text", "text": link_system_prompt},
                                    {"type": "text", "text": get_links_user_prompt(website)}
                                ],
                        
                             
    )
    result = response.choices[0].message.content
    return json.loads(result)

def get_all_details(url):
    result = "Landing Page Details:\n"
    result += Website(url).get_contents()
    links = get_links_response(url)
    print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    return result

print(get_all_details("https://www.infosys.com/"))

system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."

def get_brochure_user_prompt(company_name, website_url):
    user_prompt = f"Company Name: {company_name}\n"     
    user_prompt += f"Website URL: {website_url}\n"
    user_prompt += "Please create a brochure about the company for prospective customers, investors and recruits. \
Include details of company culture, customers and careers/jobs if you have the information."
    return user_prompt

def get_brochure_response(company_name, website_url):
    user_prompt = get_brochure_user_prompt(company_name, website_url)
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "text"}
    )
    return response.choices[0].message.content  

print(get_brochure_response("Infosys", "https://www.infosys.com/"))






#response = client.models.generate_content(
#    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
#)
#print(response.text)















