import json
from pathlib import Path
from typing import Self, Optional
from datetime import datetime

from pydantic import BaseModel


class SALARY(BaseModel):
    MIN: float
    MAX: float
    CURRENCY: str


class YEARSEXPERIENCE(BaseModel):
    MIN: Optional[int]
    MAX: Optional[int]


class PERSONOFCONTACT(BaseModel):
    NAME: Optional[str]
    EMAIL: str


class SKILLS(BaseModel):
    TECHNICAL_SKILLS: list[str]
    SOFT_SKILLS: list[str]


class Response(BaseModel):
    JOB_Title: str
    COMPANY: str
    JOB_REFERENCE_CODE: str
    SALARY: SALARY
    REMOTE: str
    LOCATION: str
    EDUCATION_REQUIREMENT: str
    YEARS_EXPERIENCE: YEARSEXPERIENCE
    POSTED_DATE: str
    CLOSING_DATE: str
    STARTING_DATE: str
    PERMANENT: str
    PERSON_OF_CONTACT: PERSONOFCONTACT
    SKILLS: SKILLS


class AIJobResponse:
    def __init__(self, raw_response: str):
        self.raw_response = json.loads(self.__strip_ticks(raw_response))["response"]

    def __strip_ticks(self, raw: str):
        return raw.replace("```json", "").replace("```", "")

    @property
    def as_json(self):
        return self.raw_response

    @property
    def as_str(self):
        return json.dumps(self.raw_response, separators=(",", ":"))

    @property
    def as_model(self):
        return Response.model_validate(self.raw_response)


if __name__ == "__main__":
    file = Path.home() / "data.txt"
    responses = []
    with open(file) as f:
        for line in f:
            response = line.strip()
            res = AIJobResponse(raw_response=response)
            print(res.as_model)
            # print(res.as_model.response)
            break
