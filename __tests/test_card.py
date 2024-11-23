from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    align_items = to_ref("start")

    @ui.page(page_path)
    def _():
        rxui.select(["start", "center", "end"], value=align_items).classes("select")
        rxui.card(align_items=align_items).classes("target")  # type: ignore

    page = browser.open(page_path)

    card = page.Base(".target")
    select = page.Select(".select")

    card.expect_to_contain_class("items-start")
    select.click_and_select("center")
    card.expect_to_contain_class("items-center")
