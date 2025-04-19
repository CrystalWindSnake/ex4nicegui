from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        current = to_ref("<p>test1</p>")
        rxui.html(current).classes("target")
        ui.button(
            "change",
            on_click=lambda: current.set_value("<p>test2:<span>inner</span></p>"),
        ).classes("btn-change")

    page = browser.open(page_path)

    target = page.Base(".target")
    btn_change = page.Base(".btn-change")
    target.expect.to_have_text("test1")

    btn_change.click()
    target.expect.to_have_text("test2:inner")
