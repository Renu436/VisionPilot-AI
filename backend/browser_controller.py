
import os
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

class BrowserController:

    def __init__(self):
        self.playwright = sync_playwright().start()
        headless = os.getenv("BROWSER_HEADLESS", "true").lower() == "true"
        executable_path = os.getenv("CHROME_EXECUTABLE_PATH")
        chrome_channel = os.getenv("BROWSER_CHANNEL", "chrome")

        launch_attempts = []
        if executable_path:
            launch_attempts.append({"headless": headless, "executable_path": executable_path})
        launch_attempts.append({"headless": headless})
        launch_attempts.append({"headless": headless, "channel": chrome_channel})

        last_error = None
        try:
            for launch_kwargs in launch_attempts:
                try:
                    self.browser = self.playwright.chromium.launch(**launch_kwargs)
                    break
                except PlaywrightError as exc:
                    last_error = exc
                    continue
            else:
                raise last_error if last_error else RuntimeError("Failed to launch browser")
        except Exception as exc:
            self.playwright.stop()
            raise RuntimeError(
                "Failed to launch browser. Install Chromium with: playwright install chromium "
                "or set CHROME_EXECUTABLE_PATH to your local Chrome binary."
            ) from exc
        self.page = self.browser.new_page(viewport={"width": 1366, "height": 900})

    def open_site(self, url):
        try:
            self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception as exc:
            raise RuntimeError(f"Failed to open {url}: {exc}") from exc

    def screenshot(self):
        path = "screen.png"
        # Viewport snapshots are more stable for action planning than giant full-page captures.
        self.page.wait_for_timeout(400)
        self.page.screenshot(path=path, full_page=False)
        return path

    def _try_click(self, selectors):
        for selector in selectors:
            try:
                self.page.click(selector, timeout=3000)
                return True
            except Exception:
                continue
        return False

    def _try_fill_and_submit(self, selectors, text):
        for selector in selectors:
            try:
                self.page.fill(selector, text, timeout=3000)
                self.page.press(selector, "Enter")
                return True
            except Exception:
                continue
        return False

    def click_search(self, selectors=None):
        selectors = selectors or ["#twotabsearchtextbox", "input[type='search']", "input[name='q']"]
        success = self._try_click(selectors)
        if not success:
            print(f"click_search failed for selectors: {selectors}")
        return success

    def type_search(self, text, selectors=None):
        selectors = selectors or ["#twotabsearchtextbox", "input[type='search']", "input[name='q']"]
        success = self._try_fill_and_submit(selectors, text)
        if not success:
            print(f"type_search failed for selectors: {selectors}")
        return success

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
