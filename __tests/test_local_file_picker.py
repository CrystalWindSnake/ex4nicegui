from pathlib import Path
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager
from .utils import LabelUtils, set_test_id, ButtonUtils


def test_base(browser: BrowserManager, page_path: str):
    cur_file = Path(__file__)

    @ui.page(page_path)
    def _():
        select = to_ref("")
        fp = rxui.local_file_picker(dir=cur_file.parent, mode="dir")
        fp.bind_ref(select)

        set_test_id(rxui.label(select), "label")

        set_test_id(ui.button("choose file", on_click=fp.open), "btn")

    page = browser.open(page_path)
    page_utils = page._page

    label = LabelUtils(page, "label")
    btn = ButtonUtils(page, "btn")

    btn.click()

    first_cell = page_utils.locator(".ag-cell-value").first
    path_text = first_cell.text_content()
    assert path_text
    first_cell.click()

    page_utils.get_by_role("button", name="ok").click()
    label.expect_contain_text(str(cur_file.parent / path_text))
