from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    wrap = to_ref(True)

    @ui.page(page_path)
    def _():
        rxui.checkbox(value=wrap).classes("checkbox")

        with rxui.column(wrap=wrap).classes("target"):
            for _ in range(5):
                ui.card()

    page = browser.open(page_path)

    column = page.Base(".target")
    checkbox = page.Checkbox(".checkbox")

    column.expect_to_have_style("flex-wrap", "wrap")

    checkbox.click()
    column.expect_to_have_style("flex-wrap", "nowrap")
