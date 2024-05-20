from nicegui import ui
from ex4nicegui import to_ref, effect, on
from .screen import BrowserManager
from .utils import fn


def test_effect_cleanup_when_page_close(browser: BrowserManager, page_path: str):
    other_page_path = f"{page_path}/other"
    value = to_ref("org")

    @fn
    def call():
        value.value

    @ui.page(page_path)
    def _():
        ui.link("to other page", other_page_path)
        effect(call)

    @ui.page(other_page_path)
    def _():
        ui.link("back to main", page_path)

    page = browser.open(page_path)

    assert call.calledTimes == 1

    page.get_by_role("link", name="to other page").click()

    # must wait for background execution to clean up
    page.wait(4000)
    value.value = "new"

    assert call.calledTimes == 1


def test_on_cleanup_when_page_close(browser: BrowserManager, page_path: str):
    other_page_path = f"{page_path}/other"
    value = to_ref("org")

    @fn
    def call_fn_times():
        pass

    def call():
        value.value
        call_fn_times()

    @ui.page(page_path)
    def _():
        ui.link("to other page", other_page_path)
        on(value)(call)

    @ui.page(other_page_path)
    def _():
        ui.link("back to main", page_path)

    page = browser.open(page_path)

    assert call_fn_times.calledTimes == 1
    page._page.get_by_role("link", name="to other page").click()

    # must wait for background execution to clean up
    page.wait(4000)
    value.value = "new"
    assert call_fn_times.calledTimes == 1
