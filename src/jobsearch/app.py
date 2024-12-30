from pathlib import Path

from jobsearch.scrapper.manager import ScrappingManager
from jobsearch.scrapper.plugins import Manulife
from jobsearch.ai.gemini import Gemini
from jobsearch.storage.repo import FileRepository, DataIntegrityException


def query_ai(job_description: str):
    gemini = Gemini()
    return gemini.ask_ai_about_job(job_description)


def collect_urls(urls_file: Path):
    sm = ScrappingManager()
    career_website = Manulife()
    repo1 = FileRepository(connection={"filepath": urls_file, "key": "url"})

    urls = sm.get_job_urls(career_website)
    for url in urls:
        data = {"url": url}
        repo1.write(data)
    return urls

def get_job_description_and_save_it(url: str, job_description_file: Path):
    sm = ScrappingManager()
    repo2 = FileRepository(connection={"filepath": job_description_file, "key": "url"})

    job_description = sm.get_one_job_details(url)
    data = {
        'url': url,
        'job': job_description
    }
    try:
        repo2.write(data)
    except DataIntegrityException:
        print(f'Already added, {url}')
    return data


if __name__ == "__main__":
    output_folder = Path.home() / "jobsearch"
    urls_file = output_folder / "urls.json"
    job_description_file = output_folder / 'job_descriptions.json'

    repo = FileRepository(connection={"filepath": urls_file, "key": "url"})
    repo2 = FileRepository(connection={"filepath": job_description_file, "key": "url"})
    urls = repo.read_all()
    for url in urls:
        url = url.get('url')
        if repo2.read(url) != {}:
            print("Job already extacted")
        else:
            get_job_description_and_save_it(url, job_description_file)

    # ai_response = query_ai(job_description)
    # pprint(ai_response)
