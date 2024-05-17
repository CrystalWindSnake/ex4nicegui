from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager
from .utils import set_test_id, BaseUiUtils


def test_base(browser: BrowserManager, page_path: str):
    current = to_ref("<p>test1</p>")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.html(current), "target")

    page = browser.open(page_path)

    target = BaseUiUtils(page, "target")
    target.expect.to_have_text("test1")

    current.value = "<p>test2:<span>inner</span></p>"
    target.expect.to_have_text("test2:inner")
