import re
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import set_test_id, BaseUiUtils, CheckboxUtils


def test_base(page: ScreenPage, page_path: str):
    wrap = to_ref(True)

    @ui.page(page_path)
    def _():
        set_test_id(rxui.checkbox(value=wrap), "checkbox")

        column = rxui.column(wrap=wrap)
        with column:
            for _ in range(5):
                ui.card()
        set_test_id(column, "target")

    page.open(page_path)

    column = BaseUiUtils(page, "target")
    checkbox = CheckboxUtils(page, "checkbox")

    # page.pause()
    column.expect.to_have_class(re.compile(r"wrap"))

    checkbox.click()
    column.expect.not_to_have_class(re.compile(r"wrap"))
