from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import BaseUiUtils, set_test_id


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        set_test_id(rxui.element("p").props('innerHTML="test"'), "target")

    page = browser.open(page_path)

    target = BaseUiUtils(page, "target")
    target.expect_to_have_text("test")
