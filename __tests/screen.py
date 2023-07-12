import threading
from playwright.sync_api import Page, expect, Browser
from nicegui import globals, ui


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
        globals.server.should_exit = True

        if self.server_thread:
            self.server_thread.join()

    def new_page(self):
        if self.server_thread is None:
            self.start_server()

        return TestPage(self)


class TestPage:
    def __init__(self, screen: Screen) -> None:
        self.__screen = screen
        self.__page = self.__screen.browser.new_page()

    def open(self, path: str):
        self.__page.wait_for_selector("body", timeout=10000)
        self.__page.goto(f"http://localhost:{PORT}{path}")

    def should_contain(self, text: str) -> None:
        expect(self.__page.get_by_text(text)).to_be_visible()

    def click(self, text: str) -> None:
        self.__page.get_by_text(text).click()

    def wait(self, timeout=500) -> None:
        self.__page.wait_for_timeout(timeout=timeout)

    def get_ele(self, text: str):
        return self.__page.get_by_text(text)

    def pause(self):
        self.__page.pause()

    def close(self):
        self.__page.close()
