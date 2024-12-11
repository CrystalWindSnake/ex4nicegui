from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_value = to_ref(0.1)
        rxui.linear_progress(value=r_value)
        ui.button(
            "change",
            on_click=lambda: r_value.set_value(0.5),
        ).classes("btn-change")

    page = browser.open(page_path)
    btn = page.Button(".btn-change")
    page.should_contain("0.1")

    btn.click()
    page.should_contain("0.5")
