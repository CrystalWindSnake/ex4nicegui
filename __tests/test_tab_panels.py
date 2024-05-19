from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager
from .utils import InputUtils, set_test_id, BaseUiUtils


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        current = to_ref("a")
        rxui.input(value=current).classes("input")

        with rxui.tab_panels(current).classes("panels"):
            with rxui.tab_panel("a"):
                rxui.label("a page")

            with rxui.tab_panel("b"):
                rxui.label("b page")

    page = browser.open(page_path)

    input = page.Input(".input")
    tabs = page.Base(".panels")

    tabs.expect.to_contain_text("a page")

    input.fill_text("b")
    tabs.expect.to_contain_text("b page")
