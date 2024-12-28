import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import Callable, NewType, TypeAlias, Self

from playwright.sync_api import sync_playwright, Page, Locator, expect


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


class Browser:
    def start_dev_mode(self, url: Url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)
            page.pause()
            browser.close()

    def run_on_browser(self, steps: PageSteps):
        # TODO: Make it async later
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            steps(page)
            browser.close()

    def new_page(self) -> BrowserPage:
        # run browser and return page.
        # or open new tab if brower is open
        try:
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch(
                headless=False, args=["--start-fullscreen"]
            )
            page = browser.new_page()
            return page
        finally:
            # browser.close()
            pass

    @staticmethod
    def pick_locator_function(
        page: Page, selector: PageClickElement
    ) -> Callable[[str], Locator]:
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

    def go_next_page(self, selector: PageClickElement) -> Self | None:
        select_func = Browser.pick_locator_function(self.page, selector)
        try:
            expect(select_func(selector.value)).to_be_visible()
        except AssertionError:
            return WebPage.EMPTY
        select_func(selector.value).click()
        self.page.wait_for_load_state("networkidle")
        return self

    def goto_page(self, url: Url) -> Self:
        self.page.goto(url)
        return self

    def run_on_page(self, steps: PageSteps) -> Self:
        steps(self.page)
        return self

    def parse_page(self) -> PageContent:
        return self.page.query_selector("body").inner_text()

    def get_urls(self, pattern: str = r"\w+") -> list[Url]:
        # url_pattern = fr'https?://{pattern}'
        url_pattern = rf"{pattern}"
        links = self.page.locator("a").all()
        hrefs = [link.get_attribute("href") for link in links]
        urls = [href for href in hrefs if re.search(url_pattern, href or "")]
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
