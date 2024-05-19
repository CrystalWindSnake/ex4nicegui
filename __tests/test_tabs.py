from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    current = to_ref("a")

    @ui.page(page_path)
    def _():
        rxui.label(current).classes("label")
        with rxui.tabs(current).classes("tabs"):
            rxui.tab("a", "a tab")
            rxui.tab("b", "b tab")

    page = browser.open(page_path)

    label = page.Label(".label")
    tabs = page.Base(".tabs")

    tabs.target_locator.get_by_role("tab", name="b tab").click()
    label.expect_to_have_text("b")


def test_should_tab_label_change(browser: BrowserManager, page_path: str):
    current = to_ref("a")
    b_tab_label = to_ref("b tab")

    @ui.page(page_path)
    def _():
        rxui.input(value=b_tab_label).classes("input")
        with rxui.tabs(current).classes("tabs"):
            rxui.tab("a", "a tab")
            rxui.tab("b", label=b_tab_label)

    page = browser.open(page_path)

    input = page.Input(".input")
    tabs = page.Base(".tabs")

    tabs.expect.to_contain_text("b tab")

    input.fill_text("b new tab")
    tabs.expect.not_to_contain_text("b tab")
    tabs.expect.to_contain_text("b new tab")
