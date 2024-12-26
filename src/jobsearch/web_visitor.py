# import logging
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)

from playwright.sync_api import sync_playwright

from jobsearch.ai import Gemini

URL = 'https://careers.manulife.com/global/en/job/JR24070803/Lead-Data-Engineer'

gemini = Gemini()

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False
    )
    page = browser.new_page()
    page.goto(URL)
    page.wait_for_load_state('networkidle')
    description = page.query_selector('._job-description-block_izt6j_3')
    # print(page.title())
    query = f"Tell me what are the roles for this jobs print them a list of keywords seperated by ','.\n{description.inner_text()}"
    print(gemini.query_ai(query))

    browser.close()