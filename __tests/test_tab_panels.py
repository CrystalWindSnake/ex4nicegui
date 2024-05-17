from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import InputUtils, set_test_id, BaseUiUtils


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        current = to_ref("a")

        set_test_id(rxui.input(value=current), "input")

        with rxui.tab_panels(current) as panels:
            with rxui.tab_panel("a"):
                rxui.label("a page")

            with rxui.tab_panel("b"):
                rxui.label("b page")

        set_test_id(panels, "panels")

    page = browser.open(page_path)

    input = InputUtils(page, "input")
    tabs = BaseUiUtils(page, "panels")

    tabs.expect.to_contain_text("a page")

    input.fill_text("b")
    tabs.expect.to_contain_text("b page")
