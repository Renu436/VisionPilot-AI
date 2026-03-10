
import os
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

class BrowserController:

    def __init__(self):
        self.playwright = sync_playwright().start()
        headless = os.getenv("BROWSER_HEADLESS", "true").lower() == "true"
        try:
            self.browser = self.playwright.chromium.launch(headless=headless)
        except PlaywrightError as exc:
            self.playwright.stop()
            raise RuntimeError(
                "Failed to launch Chromium. Install it with: playwright install chromium"
            ) from exc
        self.page = self.browser.new_page()

    def open_site(self, url):
        self.page.goto(url, wait_until="domcontentloaded", timeout=60000)

    def screenshot(self):
        path = "screen.png"
        self.page.screenshot(path=path, full_page=True)
        return path

    def click_search(self):
        try:
            self.page.click("#twotabsearchtextbox")
        except Exception as exc:
            print(f"click_search failed: {exc}")

    def type_search(self, text):
        try:
            self.page.fill("#twotabsearchtextbox", text)
            self.page.press("#twotabsearchtextbox", "Enter")
        except Exception as exc:
            print(f"type_search failed: {exc}")

    def scroll(self):
        try:
            self.page.mouse.wheel(0, 1000)
        except Exception as exc:
            print(f"scroll failed: {exc}")

    def close(self):
        try:
            self.browser.close()
        finally:
            self.playwright.stop()
