from pathlib import Path
from pprint import pprint

from jobsearch.scrapper.manager import ScrappingManager
from jobsearch.scrapper.plugins import Manulife, ShakePay
from jobsearch.ai.gemini import Gemini
from jobsearch.storage.repo import FileRepository, DataIntegrityException


def query_ai(job_description: str):
    gemini = Gemini()
    return gemini.ask_ai_about_job(job_description)


def collect_urls(urls_file: Path, career_website):
    sm = ScrappingManager()
    repo1 = FileRepository(connection={"filepath": urls_file, "key": "url"})

    urls = sm.get_job_urls(career_website)
    for url in urls:
        data = {"url": url}
        try:
            repo1.write(data)
        except DataIntegrityException:
            print("Link already added.")
    return urls


def get_job_description_and_save_it(url: str, job_description_file: Path):
    sm = ScrappingManager()
    repo2 = FileRepository(connection={"filepath": job_description_file, "key": "url"})

    job_description = sm.get_one_job_details(url)
    data = {"url": url, "job": job_description}
    try:
        repo2.write(data)
    except DataIntegrityException:
        print(f"Job Already added, {url}")
    return data


if __name__ == "__main__":
    output_folder = Path.home() / "jobsearch"
    urls_file = output_folder / "urls.json"
    job_description_file = output_folder / "job_descriptions.json"
    ai_answers_file = output_folder / "ai_answers.json"
    career_website = ShakePay()

    # urls = collect_urls(urls_file, career_website)

    repo = FileRepository(connection={"filepath": urls_file, "key": "url"})
    repo2 = FileRepository(connection={"filepath": job_description_file, "key": "url"})
    urls = repo.read_all()
    for url in urls:
        url = url.get("url")
        if repo2.read(url) != {}:
            # print("Job already extacted")
            pass
        else:
            get_job_description_and_save_it(url, job_description_file)

    urls_with_desc = repo2.read_all()
    repo3 = FileRepository(connection={"filepath": ai_answers_file, "key": "url"})
    for url_desc in urls_with_desc:
        url = url_desc.get('url')
        description = url_desc.get("job")
        if repo3.read(url) == {}:
            response = query_ai(description)
            data = {
                'url': url,
                'job': description,
                "response": response.as_str()
                }
            repo3.write(data)
            pprint(response.as_dict())
        # break

    # ai_response = query_ai(job_description)
    # pprint(ai_response)
