from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage


def test_base(browser: BrowserManager, page_path: str):
    r_value = to_ref(0.1)

    @ui.page(page_path)
    def _():
        rxui.linear_progress(value=r_value)

    page = browser.open(page_path)
    page.should_contain("0.1")

    r_value.value = 0.5
    page.should_contain("0.5")
