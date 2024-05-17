import re
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import set_test_id, BaseUiUtils, CheckboxUtils


def test_base(browser: BrowserManager, page_path: str):
    wrap = to_ref(True)

    @ui.page(page_path)
    def _():
        set_test_id(rxui.checkbox(value=wrap), "checkbox")

        row = rxui.row(wrap=wrap)
        with row:
            for _ in range(5):
                ui.card()
        set_test_id(row, "target")

    page = browser.open(page_path)

    row = BaseUiUtils(page, "target")
    checkbox = CheckboxUtils(page, "checkbox")

    # page.pause()
    row.expect.to_have_class(re.compile(r"wrap"))

    checkbox.click()
    row.expect.not_to_have_class(re.compile(r"wrap"))
