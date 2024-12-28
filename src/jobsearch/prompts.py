from enum import Enum

class AIPrompts(Enum):
    JOB_Title = "Get the job title"
    COMPANY = "What's the name of company?"
    JOB_REFERENCE_CODE = "What the job reference code?"
    SALARY = "What's the salary for this jobs?"
    REMOTE = "Is this job remote, hybride or in person?"
    LOCATION = "What's the location for this job?"
    EDUCATION_REQUIREMENT = "What's the minimal educational degree required?"
    YEARS_EXPERIENCE = "How many years of experiece are required for this role?"# Specify them as MIN and MAX values."
    POSTED_DATE = "When was this job posted?"
    CLOSING_DATE = "What is the closing date for this job?"
    STARTING_DATE = "What is the starting date for this job?"
    PERMANENT = "Is this job permenant, temporary, full-time, part-time, contract or casual?"
    PERSON_OF_CONTACT = "Is there a person of contact mentionend? Get their NAME and EMAIL"
    SKILLS = "List the requiesd skills by scanning all jobs sections for the job under two categories TECHNICAL_SKILLS And SOFT_SKILLS."


class DataFormatingRules(Enum):
    Date = "Format dates in this format YYYY-MM-DD"
    MULTIPLE_NUMBER_VALUES = "Specify multiple numeric values as MIN and MAX fields"
    NOT_FOUND_VALUES = "Not found values are specified as 'NULL'",


def merge_enums(en: Enum, sep: str='\n') -> str:
    return sep.join([f'[{n.name}]: {n.value}' for n in en])


def prompt_composer(details: str):
    questions = merge_enums(AIPrompts)
    formating_rules = merge_enums(DataFormatingRules)
    message  = [
        "Analysis this job description, respond to those questions and return in a json format key: response.",
        "The questions are:",
        questions,
        "The formating rules are as follow",
        formating_rules,
        f"The job description: {details}",
    ]
    return '\n'.join(message)
    

if __name__ == '__main__':
    print(prompt_composer(''))
