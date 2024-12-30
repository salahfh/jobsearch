# Python demo
# https://github.com/google-gemini/cookbook/blob/main/quickstarts/Prompting.ipynb
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import NewType, Callable
import json
import os

from dotenv import load_dotenv
import google.generativeai as genai

from jobsearch.ai.prompts import prompt_composer
from jobsearch.ai.schema import JobDetails


load_dotenv()


AIResponse = NewType("AIResponse", str)
AIQuery = NewType("AIQuery", str)


@dataclass
class Response:
    _reponse: dict

    def as_dict(self):
        return json.loads(self._reponse)
    
    def as_str(self):
        return json.dumps(self._reponse, separators=(',', ':'))



class AI(ABC):
    def __init__(self, API_KEY: str):
        self.api_key = API_KEY

    @abstractmethod
    def query_ai(self, query: AIQuery) -> AIResponse:
        pass

    # Implement query counter - To remain within Quota
    # Implement query caching


class Gemini(AI):
    def __init__(self, tools: list[Callable] = None):
        self.API_KEY = os.environ.get("GEMINI_API_KEY")
        self.tools = tools
        self.model = self.configure()
        super().__init__(self.API_KEY)

    def configure(self) -> genai.GenerativeModel:
        genai.configure(api_key=self.API_KEY)
        return genai.GenerativeModel("gemini-1.5-flash", tools=self.tools)

    def query_ai(self, query):
        response = self.model.generate_content(query)
        return response.text

    def ask_ai_about_job(self, job_description: str) -> str:
        # query = prompt_composer(job_description)
        # return self.query_ai(query)
        query = prompt_composer(job_description)
        result = self.model.generate_content(
            query,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=JobDetails
            ),
        )
        return Response(result.text)
