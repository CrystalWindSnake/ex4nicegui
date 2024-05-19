from pathlib import Path
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    cur_file = Path(__file__)

    @ui.page(page_path)
    def _():
        select = to_ref("")
        fp = rxui.local_file_picker(dir=cur_file.parent, mode="dir")
        fp.bind_ref(select)

        rxui.label(select).classes("label")
        ui.button("choose file", on_click=fp.open).classes("btn")

    page = browser.open(page_path)
    page_utils = page._page

    label = page.Label(".label")
    btn = page.Button(".btn")

    btn.click()

    first_cell = page_utils.locator(".ag-cell-value").first
    path_text = first_cell.text_content()
    assert path_text
    first_cell.click()

    page_utils.get_by_role("button", name="ok").click()
    label.expect_contain_text(str(cur_file.parent / path_text))
