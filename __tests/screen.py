import threading
from playwright.sync_api import Browser
from nicegui import ui, app
from nicegui.server import Server

PORT = 3392


class ServerManager:
    def __init__(self, browser: Browser) -> None:
        self.server_thread = None
        self.browser = browser

        self._context = browser.new_context()
        self._context.set_default_timeout(10000)
        self.ui_run_kwargs = {"port": PORT, "show": False, "reload": False}
        self.connected = threading.Event()

        app.on_startup(self.connected.set)

    def start_server(self) -> None:
        """Start the webserver in a separate thread. This is the equivalent of `ui.run()` in a normal script."""
        self.server_thread = threading.Thread(target=ui.run, kwargs=self.ui_run_kwargs)
        self.server_thread.start()

    def stop_server(self) -> None:
        """Stop the webserver."""
        self.browser.close()
        Server.instance.should_exit = True

        if self.server_thread:
            self.server_thread.join()

    def new_page(self):
        if self.server_thread is None:
            self.start_server()

        self.connected.clear()

        return BrowserManager(self, self.connected)


class BrowserManager:
    def __init__(self, server: ServerManager, connect_event: threading.Event) -> None:
        self.__server = server
        self._page = self.__server._context.new_page()
        self.connected = connect_event

    def open(self, path: str):
        # self._page.wait_for_selector("body", timeout=10000)

        # wait for server to be ready
        is_connected = self.connected.wait(5)
        if not is_connected:
            raise TimeoutError("Failed to connect to server")

        self._page.goto(
            f"http://localhost:{PORT}{path}",
            timeout=5000,
            wait_until="domcontentloaded",
        )

        self._page.wait_for_timeout(600)
        return self._page

    def close(self):
        self._page.close()

    @property
    def pw_page(self):
        return self._page
