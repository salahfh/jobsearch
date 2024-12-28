import re
from abc import ABC, abstractmethod

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
        self.next_page_selector = PageClickElement(
            value="", type=SelectorType.CSS_SELECTOR
        )
        self.job_links_pattern = r".*/j/.*"
        self.unique_job_url = True


class WinnipegCity(CareersWebsite):
    def __init__(self):
        self.start_url = "https://careers.winnipeg.ca/psc/cgext/EMPLOYEE/HRMS/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?Page=HRS_APP_SCHJOB_FL&Action=U"
        self.next_page_selector = PageClickElement(
            value="", type=SelectorType.CSS_SELECTOR
        )
        self.job_links_pattern = r"javascript:submitAction_win0.*;"
        self.unique_job_url = True


class CanadaPost(CareersWebsite):
    def __init__(self):
        self.start_url = "https://jobs.canadapost.ca/go/Canada-Post-All-Current-Opportunities/2319117/"
        self.next_page_selector = ""
        self.job_links_pattern = r"javascript:submitAction_win0.*;"
        self.unique_job_url = True
