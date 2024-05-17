from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import InputUtils, set_test_id, BaseUiUtils


def test_base(browser: BrowserManager, page_path: str):
    current = to_ref("a")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.label(current), "label")
        with rxui.tabs(current) as tabs:
            rxui.tab("a", "a tab")
            rxui.tab("b", "b tab")
        set_test_id(tabs, "tabs")

    page = browser.open(page_path)

    label = BaseUiUtils(page, "label")
    tabs = BaseUiUtils(page, "tabs")

    tabs.target_locator.get_by_role("tab", name="b tab").click()
    label.expect_to_have_text("b")


def test_should_tab_label_change(browser: BrowserManager, page_path: str):
    current = to_ref("a")
    b_tab_label = to_ref("b tab")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.input(value=b_tab_label), "input")
        with rxui.tabs(current) as tabs:
            rxui.tab("a", "a tab")
            rxui.tab("b", label=b_tab_label)
        set_test_id(tabs, "tabs")

    page = browser.open(page_path)

    input = InputUtils(page, "input")
    tabs = BaseUiUtils(page, "tabs")

    tabs.expect.to_contain_text("b tab")

    input.fill_text("b new tab")
    tabs.expect.not_to_contain_text("b tab")
    tabs.expect.to_contain_text("b new tab")
