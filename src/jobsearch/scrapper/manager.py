# Build a web scarapping manger with simple interface 
# It should work on a general plugin interface, extensible to different websites
# 1. It should work concurently 
# 2. Have a rate limitter
# 3. Optionaly implement caching
# 4. Have a retry option

import re
from enum import Enum, auto
from typing import Callable, NewType, TypeAlias, Generator, Self
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from playwright.sync_api import sync_playwright, Page, expect, Locator
# from playwright._impl._errors import TimeoutError


Url = NewType("Url", str)
BrowserPage = NewType("BrowserPage", Page)
PageContent = NewType("PageContent", str)
PageSteps: TypeAlias = Callable[[BrowserPage], None]


class SelectorType(Enum):
    CSS_SELECTOR = auto()
    LABEL = auto()
    ROLE = auto()
    TEXT = auto()


@dataclass
class PageClickElement:
    value: str
    type: SelectorType


class CareersWebsite(ABC):
    def __init__(self) -> None:
        self.start_url: str
        self.next_page_selector: PageClickElement
        self.job_links_pattern: str
        self.unique_job_url: bool

    @property
    def search_filter(self) -> None:
        return self.search_filter_steps

    @abstractmethod
    def search_filter_steps(self, page: BrowserPage) -> list[PageSteps]:
        pass


class Browser:
    def start_dev_mode(self, url: Url):
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False
            )
            page = browser.new_page()
            page.goto(url)
            page.pause()
            browser.close()
        
    def run_on_browser(self, steps: PageSteps): 
        # TODO: Make it async later
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False
            )
            page = browser.new_page()
            steps(page)
            browser.close()

    def new_page(self) -> BrowserPage:
        # run browser and return page.
        # or open new tab if brower is open
        try:
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch(
                headless=False,
                args=["--start-fullscreen"]
                )
            page = browser.new_page()
            return page
        finally:
            # browser.close()
            pass
 
    @staticmethod
    def pick_locator_function(page: Page, selector: PageClickElement) -> Callable[[str], Locator]:
        match selector.type:
            case SelectorType.CSS_SELECTOR:
                return page.query_selector
            case SelectorType.LABEL:
                return page.get_by_label
            case SelectorType.ROLE:
                return page.get_by_role
            case SelectorType.TEXT:
                return page.get_by_text           


class WebPage:
    EMPTY = None

    def __init__(self, page: BrowserPage):
        self.page: BrowserPage = page
    
    # def new_page(self, browser: Browser) -> Self:
    #     # Rewrite this one to use the Browser Class
    #     return WebPage(browser.new_page())

        
    def go_next_page(self, selector: PageClickElement) -> Self|None:
        select_func = Browser.pick_locator_function(self.page, selector)
        try:
            expect(select_func(selector.value)).to_be_visible()
        except AssertionError:
            return WebPage.EMPTY
        select_func(selector.value).click()
        self.page.wait_for_load_state('networkidle')
        return self

    def goto_page(self, url: Url) -> Self:
        self.page.goto(url)
        return self

    def run_on_page(self, steps: PageSteps) -> Self:
        steps(self.page)
        return self

    def parse_page(self) -> PageContent:
        return self.page.query_selector('body').inner_text()
    
    def get_urls(self, pattern: str=r'\w+') -> list[Url]:
        # url_pattern = fr'https?://{pattern}'
        url_pattern = fr'{pattern}'
        links = self.page.locator("a").all()
        hrefs = [link.get_attribute("href") for link in links]
        urls = [href for href in hrefs if re.search(url_pattern, href or '')]
        return urls
    
    def print_title(self) -> Self:
        print(self.page.title())
        return self

    def print_url(self) -> Self:
        print(self.page.url)
        return self
    
    def page_scroll_to_btm(self) -> Self:
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        return self

    def wait_page(self, time=1000) -> Self:
        # self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(time)
        return self


class ScrappingManager:
    '''
    Take a plug carrier page definition, extract all jobs, apply data extracts to each.
    With cache pages return saved result.

    Caching can be done through job reference
    '''
    def __init__(self):
        self.page = WebPage(Browser().new_page())

    def get_job_urls(self, website: CareersWebsite) -> list[Url]:
        urls = []
        self.page \
            .goto_page(website.start_url) \
            .run_on_page(website.search_filter) 
        while self.page:
                self.page.print_title() \
                    .print_url() \
                    .wait_page()
                content = self.page.get_urls(website.job_links_pattern)
                self.page = self.page.go_next_page(website.next_page_selector)
                urls.extend(content)

        return urls
        # self.browser.go_next_page(website.next_page_selector) or self.goto_page("next_page")
    
    def get_job_urls_multipage(self):
        pass

    def get_one_job_details(self, url: Url) -> PageContent:
        pass

    def goto_page(self):
        self.page\
            .goto_page("http://playwright.dev") \
            .print_title() \


@dataclass
class JobList:
    current: int
    next: Url|None = None
    result: list[Url] = field(default_factory=[])


class Manulife(CareersWebsite):
    def __init__(self):
        self.start_url='https://careers.manulife.com/global/en/c/technology-jobs'
        self.next_page_selector=PageClickElement(value='Next', type=SelectorType.LABEL)
        self.job_links_pattern=r'.*/global/en/job/.*'
        self.unique_job_url=True

    def search_filter_steps(self, page):
        page.get_by_label("Country", exact=True).click()
        page.get_by_label("Canada(25jobs)").check()
        page.wait_for_load_state('networkidle')


        # TODO: Add regex to those matches
        # page.get_by_label(r"Canada.*").check()


class Citylitics(CareersWebsite):
    def __init__(self):
        self.start_url='https://apply.workable.com/citylitics/#jobs'
        self.next_page_selector=PageClickElement(value='', type=SelectorType.CSS_SELECTOR)
        self.job_links_pattern=r'.*/j/.*'
        self.unique_job_url=True

    def search_filter_steps(self, page):
        None


class WinnipegCity(CareersWebsite):
    def __init__(self):
        self.start_url='https://careers.winnipeg.ca/psc/cgext/EMPLOYEE/HRMS/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?Page=HRS_APP_SCHJOB_FL&Action=U'
        self.next_page_selector=PageClickElement(value='', type=SelectorType.CSS_SELECTOR)
        self.job_links_pattern=r"javascript:submitAction_win0.*;"
        self.unique_job_url=True

    def search_filter_steps(self, page):
        None


class CanadaPost(CareersWebsite):
    def __init__(self):
        self.start_url='https://jobs.canadapost.ca/go/Canada-Post-All-Current-Opportunities/2319117/'
        self.next_page_selector=''
        self.job_links_pattern=r"javascript:submitAction_win0.*;"
        self.unique_job_url=True

    def search_filter_steps(self, page):
        None

    

def test_manager():
    m = ScrappingManager()
    

if __name__ == '__main__':
    carriersweb = Manulife()
    # b = Browser()
    # b.start_dev_mode(carriersweb.start_url)
    sm = ScrappingManager()
    urls = sm.get_job_urls(carriersweb)
    for i, url in enumerate(urls):
        print(i, url)