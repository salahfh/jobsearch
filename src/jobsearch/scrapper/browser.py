import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import Callable, NewType, TypeAlias, Self

from playwright.sync_api import sync_playwright, Page, Locator, expect

from jobsearch.patterns import SingletonMeta


Url = NewType("Url", str)
BrowserPage = NewType("BrowserPage", Page)
PageContent = NewType("PageContent", str)
PageSteps: TypeAlias = Callable[[BrowserPage], None]


class SelectorType(Enum):
    CSS_SELECTOR = auto()
    LABEL = auto()
    ROLE = auto()
    TEXT = auto()
    NONE = auto()


@dataclass
class PageClickElement:
    type: SelectorType
    value: str = None
    name: str = None

    def __post_init__(self):
        if self.value is None and self.type != SelectorType.NONE:
            raise ValueError(
                '"PageClickElement.value" cannot be empty when type is not "NONE"'
            )

        if self.type is SelectorType.ROLE and self.name is None:
            raise ValueError(
                '"PageClickElement.name" cannot be empty when type is not "ROLE"'
            )


class Browser(metaclass=SingletonMeta):
    def __init__(self):
        self.browser = None
        self.pages: list[Page] = []

    def start_dev_mode(self, url: Url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)
            page.pause()
            browser.close()

    def new_page(self) -> BrowserPage:
        if self.browser is None:
            self.start_browser()
        if len(self.pages) > 3:
            for page in self.pages:
                page.close()
        page = self.browser.new_page()
        self.pages.append(page)
        return page

    def start_browser(self):
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(
            headless=False, args=["--start-fullscreen"]
        )
        self.browser = browser

    def close_browser(self):
        self.browser.close()

    @staticmethod
    def pick_locator_function(
        page: Page, selector: PageClickElement
    ) -> Callable[[str], Locator] | None:
        match selector.type:
            case SelectorType.CSS_SELECTOR:
                return page.query_selector
            case SelectorType.LABEL:
                return page.get_by_label
            case SelectorType.ROLE:
                # Test it with deloit
                # return lambda role: page.get_by_role(role=role, name=selector.name).first()
                return page.get_by_role
            case SelectorType.TEXT:
                return page.get_by_text
            case SelectorType.NONE:
                return None


class WebPage:
    EMPTY = None

    def __init__(self, page: BrowserPage):
        self.page: BrowserPage = page

    # def new_page(self, browser: Browser) -> Self:
    #     # Rewrite this one to use the Browser Class
    #     return WebPage(browser.new_page())

    def go_next_page(self, selector: PageClickElement) -> Self | None:
        select_func = Browser.pick_locator_function(self.page, selector)

        if select_func is None:
            return WebPage.EMPTY
        try:
            expect(select_func(selector.value)).to_be_visible()
            select_func(selector.value).click()
            self.page.wait_for_load_state("networkidle")
            return self
        except AssertionError:
            return WebPage.EMPTY

    def goto_page(self, url: Url) -> Self:
        self.page.goto(url)
        return self

    def run_on_page(self, steps: PageSteps) -> Self:
        steps(self.page)
        return self

    def get_content(self) -> PageContent:
        return self.page.query_selector("body").inner_text()

    def get_urls(self, pattern: str = r"\w+") -> set[Url]:
        url_pattern = rf"{pattern}"
        links = self.page.locator("a").all()
        hrefs = [link.get_attribute("href") for link in links]
        urls = {str(href) for href in hrefs if re.search(url_pattern, href or "")}
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
    
    def close_page(self) -> None:
        self.page.close()
        return WebPage.EMPTY
