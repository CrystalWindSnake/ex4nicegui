import re
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    wrap = to_ref(True)

    @ui.page(page_path)
    def _():
        rxui.checkbox(value=wrap).classes("checkbox")

        with rxui.row(wrap=wrap).classes("target"):
            for _ in range(5):
                ui.card()

    page = browser.open(page_path)

    row = page.Base(".target")
    checkbox = page.Checkbox(".checkbox")

    row.expect.to_have_class(re.compile(r"wrap"))

    checkbox.click()
    row.expect.not_to_have_class(re.compile(r"wrap"))
