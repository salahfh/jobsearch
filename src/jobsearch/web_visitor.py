# import logging

from playwright.sync_api import sync_playwright

from jobsearch.ai import Gemini


# logging.basicConfig()
# logging.getLogger().setLevel(logging.ERROR)


# URL = 'https://careers.manulife.com/global/en/job/JR24070803/Lead-Data-Engineer'
# URL = 'https://apply.workable.com/citylitics/j/2993E0AA9A/'
URL = 'https://www.jobbank.gc.ca/jobsearch/jobposting/42840079'

gemini = Gemini()

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False
    )
    page = browser.new_page()
    page.goto(URL)
    page.wait_for_load_state('networkidle')
    # description = page.query_selector('._job-description-block_izt6j_3')
    description = page.query_selector('body')
    # print(page.title())
    # query = f"What's the salary for this position.\n{description.inner_text()}"
    print(gemini.ask_ai_about_job(description.inner_text()))

    browser.close()