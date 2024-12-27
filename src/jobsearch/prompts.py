from enum import Enum

class AIPrompts(Enum):
    JOB_Title = "Get the job title"
    SALARY = "What's the salary for this jobs?"
    REMOTE = "Is this job remote, hybride or in person?"
    LOCATION = "What's the location for this job?"
    YEARS_EXPERIENCE = "How many years of experiece are required for this role?"
    CLOSING_DATE = "What is the closing date for this job?"
    SKILLS = "List the requiesd skills for the job."
    PERMANENT = "Is this job permenant, temporary, full-time, part-time, contract or casual?"


def prompt_composer(details: str):
    prefix = "Analysis this job description, respond to those questions and return in a json format key: response. The questions are:"
    suffix = f"The job description: {details}"
    questions = '\n'.join([f'[{n.name}]: {n.value}' for n in AIPrompts])
    return '\n'.join([prefix, questions, suffix])
    

if __name__ == '__main__':
    print(prompt_composer(''))
