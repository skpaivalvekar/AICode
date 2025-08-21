from pydantic import BaseModel, Field
from typing import List

class Reflection(BaseModel):
    missing : str = Field(description="Critique of what is missing"),
    superfluous : str = Field(description="Critique of what is Superfluous")
    
class AnswerTheQuestion(BaseModel):
    answer: str = Field(description=" 250 Word detailed answer to the question"),
    search_queries : List[str] = Field(description="1-3 search queries for improving the current answer")
    reflection: Reflection = Field(description="instance of type Reflection of what we have asked for")