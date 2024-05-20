from ex4nicegui.reactive import rxui
from nicegui import ui
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.element("p").props('innerHTML="test"').classes("target")

    page = browser.open(page_path)

    target = page.Base(".target")
    target.expect_to_have_text("test")
