from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    value = to_ref(0.3)

    @ui.page(page_path)
    def _():
        rxui.circular_progress(value, show_value=True, size="100px").classes("cp")
        rxui.number(value=value).classes("number")

    page = browser.open(page_path)

    cp = page.Base(".cp")

    cp.expect.to_contain_text("0.3")

    value.value = 0.9

    cp.expect.to_contain_text("0.9")
