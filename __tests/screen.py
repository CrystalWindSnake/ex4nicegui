import threading
from playwright.sync_api import Page, expect, Browser
from nicegui import context, ui
from nicegui.server import Server

PORT = 3392


class Screen:
    def __init__(self, browser: Browser) -> None:
        self.server_thread = None
        self.browser = browser
        self.ui_run_kwargs = {"port": PORT, "show": False, "reload": False}

    def start_server(self) -> None:
        """Start the webserver in a separate thread. This is the equivalent of `ui.run()` in a normal script."""
        self.server_thread = threading.Thread(target=ui.run, kwargs=self.ui_run_kwargs)
        self.server_thread.start()

    def stop_server(self) -> None:
        """Stop the webserver."""
        # self.close()
        # self.caplog.clear()
        self.browser.close()
        Server.instance.should_exit = True

        if self.server_thread:
            self.server_thread.join()

    def new_page(self):
        if self.server_thread is None:
            self.start_server()

        return ScreenPage(self)


class ScreenPage:
    def __init__(self, screen: Screen) -> None:
        self.__screen = screen
        self._page = self.__screen.browser.new_page()

    def open(self, path: str):
        self._page.wait_for_selector("body", timeout=10000)
        self._page.goto(f"http://localhost:{PORT}{path}")

    def is_checked_by_label(self, target_test_id: str, label: str):
        assert self.get_by_test_id(target_test_id).get_by_label(label).is_checked()

    def get_by_test_id(self, testid: str):
        return self._page.get_by_test_id(testid)

    def radio_check_by_label(self, label: str):
        self._page.click(f"text={label}")
        self.wait()

    def should_contain(self, text: str) -> None:
        expect(self._page.get_by_text(text).first).to_be_visible()

    def should_not_contain(self, text: str) -> None:
        expect(self._page.get_by_text(text)).not_to_be_visible()

    def should_contain_text(self, testid: str, text: str) -> None:
        assert self._page.get_by_test_id(testid).evaluate("node=>node.value") == text

    def click(self, text: str) -> None:
        self._page.get_by_text(text).click()

    def fill(self, test_id: str, type_str: str):
        self._page.get_by_test_id(test_id).fill(type_str)

    def enter(self, test_id: str):
        self._page.get_by_test_id(test_id).press("Enter")

    def wait(self, timeout=500) -> None:
        self._page.wait_for_timeout(timeout=timeout)

    def get_ele(self, text: str):
        return self._page.get_by_text(text)

    def pause(self):
        self._page.pause()

    def close(self):
        self._page.close()
