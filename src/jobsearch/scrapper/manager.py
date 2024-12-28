# Build a web scarapping manger with simple interface
# It should work on a general plugin interface, extensible to different websites
# 1. It should work concurently
# 2. Have a rate limitter
# 3. Optionaly implement caching
# 4. Have a retry option

from jobsearch.scrapper.plugins import Manulife, CareersWebsite
from jobsearch.scrapper.browser import WebPage, Url, Browser, PageContent


class ScrappingManager:
    """
    Take a plug carrier page definition, extract all jobs, apply data extracts to each.
    With cache pages return saved result.

    Caching can be done through job reference
    """

    def __init__(self):
        self.page = WebPage(Browser().new_page())

    def get_job_urls(self, website: CareersWebsite) -> list[Url]:
        urls = []
        self.page.goto_page(website.start_url).run_on_page(website.search_filter)
        while self.page:
            self.page.print_title().print_url().wait_page()
            content = self.page.get_urls(website.job_links_pattern)
            self.page = self.page.go_next_page(website.next_page_selector)
            urls.extend(content)

        return urls

    def get_one_job_details(self, url: Url) -> PageContent:
        pass


def test_manager():
    m = ScrappingManager()


if __name__ == "__main__":
    carriersweb = Manulife()
    # b = Browser()
    # b.start_dev_mode(carriersweb.start_url)
    sm = ScrappingManager()
    urls = sm.get_job_urls(carriersweb)
    for i, url in enumerate(urls):
        print(i, url)
