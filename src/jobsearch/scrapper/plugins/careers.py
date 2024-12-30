import re
from abc import ABC

from jobsearch.scrapper.browser import (
    PageClickElement,
    BrowserPage,
    PageSteps,
    SelectorType,
)


class CareersWebsite(ABC):
    def __init__(
        self,
        start_url: str,
        next_page_selector: PageClickElement,
        job_links_pattern: str,
        unique_job_url: bool,
    ) -> None:
        self.start_url = start_url
        self.next_page_selector = next_page_selector
        self.job_links_pattern = job_links_pattern
        self.unique_job_url = unique_job_url

    @property
    def search_filter(self) -> None:
        return self.search_filter_steps

    def search_filter_steps(self, page: BrowserPage) -> list[PageSteps]:
        return None


class Manulife(CareersWebsite):
    def __init__(self):
        self.start_url = "https://careers.manulife.com/global/en/c/technology-jobs"
        self.next_page_selector = PageClickElement(
            value="Next", type=SelectorType.LABEL
        )
        self.job_links_pattern = r".*/global/en/job/.*"
        self.unique_job_url = True

    def search_filter_steps(self, page):
        page.get_by_label("Country", exact=True).click()
        page.get_by_label(re.compile(r"Canada\(.*\)", re.IGNORECASE)).check()
        page.wait_for_load_state("networkidle")


class Citylitics(CareersWebsite):
    def __init__(self):
        self.start_url = "https://apply.workable.com/citylitics/#jobs"
        self.next_page_selector = PageClickElement(type=SelectorType.NONE)
        self.job_links_pattern = r".*/j/.*"
        self.unique_job_url = True


class WinnipegCity(CareersWebsite):
    """
    Single page application with no clear job links.
    """

    def __init__(self):
        self.start_url = "https://careers.winnipeg.ca/psc/cgext/EMPLOYEE/HRMS/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?Page=HRS_APP_SCHJOB_FL&Action=U"
        self.next_page_selector = PageClickElement(
            value="", type=SelectorType.CSS_SELECTOR
        )
        self.job_links_pattern = r"javascript:submitAction_win0.*;"
        self.unique_job_url = True


class CanadaPost(CareersWebsite):
    """
    Next page has a page number navigation rather than next button.
    """

    def __init__(self):
        self.start_url = "https://jobs.canadapost.ca/go/Canada-Post-All-Current-Opportunities/2319117/"
        self.next_page_selector = PageClickElement(SelectorType.NONE)
        self.job_links_pattern = r".*"
        self.unique_job_url = False


class Wave(CareersWebsite):
    def __init__(self):
        self.start_url = "https://jobs.lever.co/waveapps"
        self.next_page_selector = PageClickElement(SelectorType.NONE)
        self.job_links_pattern = r"^https://jobs.lever.co/waveapps/[\w\d-]+"
        self.unique_job_url = True


class StackAdapt(CareersWebsite):
    def __init__(self):
        self.start_url = "https://jobs.lever.co/stackadapt"
        self.next_page_selector = PageClickElement(SelectorType.NONE)
        self.job_links_pattern = r"^https://jobs.lever.co/stackadapt/[\w\d-]+"
        self.unique_job_url = True

    def search_filter_steps(self, page):
        page.get_by_label("Filter by Location: All").click()
        page.get_by_role("link", name="Canada", exact=True).click()


class ShakePay(CareersWebsite):
    def __init__(self):
        self.start_url = "https://shakepay.com/careers?lang=en"
        self.next_page_selector = PageClickElement(SelectorType.NONE)
        self.job_links_pattern = r".*/shakepay/jobs/.*"
        self.unique_job_url = True


class DeloitCanada(CareersWebsite):
    # TODO: Build support for multi page with number and no next button
    # Also add support for click by role
    def __init__(self):
        self.start_url = "https://careers.deloitte.ca/go/Experienced-professionals-opportunities/9604300/"
        # self.next_page_selector = PageClickElement(SelectorType.ROLE, value='')
        # page.get_by_role("link", name="Last Page").first.click()
        self.next_page_selector = PageClickElement(
            SelectorType.ROLE, value="link", name="2"
        )
        self.job_links_pattern = r".*/job/.*"
        self.unique_job_url = True

    def search_filter_steps(self, page):
        page.wait_for_load_state("networkidle")
