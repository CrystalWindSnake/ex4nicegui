from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    current = to_ref("<p>test1</p>")

    @ui.page(page_path)
    def _():
        rxui.html(current).classes("target")

    page = browser.open(page_path)

    target = page.Base(".target")
    target.expect.to_have_text("test1")

    current.value = "<p>test2:<span>inner</span></p>"
    target.expect.to_have_text("test2:inner")
