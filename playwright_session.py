from typing import Optional

from playwright.sync_api import Playwright, Page, BrowserContext, Browser


class PlaywrightSession:
    def __init__(self, url: str, proxy: str = None):
        """
        Saves list of dicts into jsonl file.

        :param url: url of the page we are navigating to,
        :param proxy: the proxy string should consist of login credentials and proxy url,
                    according to the following scheme: login:password@www.proxy.com:8080
        """
        self.page: Optional[Page] = None
        self.context: Optional[BrowserContext] = None
        self.browser: Optional[Browser] = None
        self.url = url
        self.proxy = proxy

    def setup_playwright(self, playwright: Playwright, wait_selector: str = None) -> None:
        """Set up playwright."""

        if self.proxy is not None:
            credentials, url = self.proxy.split("@")
            username, password = credentials.split(":")
            self.browser = playwright.chromium.launch(
                headless=False,
                slow_mo=1000,
                proxy={
                    "server": url,
                    "username": username,
                    "password": password
                },
            )
        else:
            self.browser = playwright.chromium.launch(
                headless=False,
                slow_mo=1000,
            )

        self.context = self.browser.new_context(viewport={"width": 1920, "height": 1080})
        self.page = self.context.new_page()
        self.page.goto(self.url)
        if wait_selector is not None:
            self.wait_for_content(wait_selector)  # wait for the selector to load

    def teardown_playwright(self) -> None:
        """Tear down playwright."""

        self.context.close()
        self.browser.close()

    def scroll_to_last_element(self, selector: str, child_selector: str = "div") -> None:
        """Scroll to the last child element in given selector."""

        while True:
            elements = self.page.locator(selector + ">" + child_selector)
            elements.element_handles()[-1].scroll_into_view_if_needed()
            elements = self.page.locator(selector)
            items_on_page = len(elements.element_handles())
            # self.page.wait_for_timeout(2_000)  # give some time for new items to load
            items_on_page_after_scroll = len(elements.element_handles())
            if items_on_page_after_scroll > items_on_page:
                continue  # more items loaded - keep scrolling
            else:
                break  # no more items - break scrolling loop

    def click_button(self, button: str) -> None:
        self.page.locator(button).click(delay=2000)

    def wait_for_content(self, wait_selector: str) -> None:
        """Wait for the selector to load."""
        self.page.wait_for_selector(wait_selector)
