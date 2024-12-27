# Python demo
# https://github.com/google-gemini/cookbook/blob/main/quickstarts/Prompting.ipynb
from abc import ABC, abstractmethod
from typing import NewType
import os

from dotenv import load_dotenv
import google.generativeai as genai

from jobsearch.prompts import prompt_composer


load_dotenv() 


AIResponse = NewType("AIResponse", str)
AIQuery = NewType("AIQuery", str)



class AI(ABC):
    def __init__(self, API_KEY: str):
        self.api_key = API_KEY
    
    @abstractmethod
    def query_ai(self, query: AIQuery) -> AIResponse:
        pass

    # Implement query counter - To remain within Quota
    # Implement query caching


class Gemini(AI):

    def __init__(self):
        self.API_KEY = os.environ.get('GEMINI_API_KEY')
        self.model = self.configure()
        super().__init__(self.API_KEY)
    
    def configure(self) -> genai.GenerativeModel:
        genai.configure(api_key=self.API_KEY)
        return genai.GenerativeModel('gemini-1.5-flash')
    
    def query_ai(self, query):
        response = self.model.generate_content(query)
        return response.text

    def ask_ai_about_job(self, job_description: str) -> str:
        query = prompt_composer(job_description)
        return self.query_ai(query)



if __name__ == '__main__':
    gemini = Gemini()
    gemini.query_ai('Tell me about yourself')