from dataclasses import dataclass
from typing import Literal


@dataclass
class Salary:
    max_salary: float
    min_salary: float
    currency: str
    unit: str


@dataclass
class YearsOfExperience:
    min_years: float
    max_years: float


@dataclass
class Dates:
    posting_date: str
    closing_date: str
    starting_date: str


@dataclass
class PersonOfContact:
    name: str
    email: str
    address: str


@dataclass
class Skills:
    technical_skills: list[str]
    soft_skills: list[str]


@dataclass
class JobDetails:
    company_name: str
    job_reference_code: str
    position_title: str
    is_it_IT_job: bool
    salary: Salary
    job_type: Literal["remote", "in-person", "hybrid", "other"]
    address: str
    educational_requirements: list[str]
    years_of_experience: YearsOfExperience
    dates: Dates
    permenante: Literal["permanant", "temporary", "contract", "casual"]
    shift_type: Literal["full-time", "part-time"]
    person_of_contact: PersonOfContact
    skills: Skills
