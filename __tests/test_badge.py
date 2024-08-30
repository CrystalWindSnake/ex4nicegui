from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_badge(browser: BrowserManager, page_path: str):
    text = to_ref("badge")

    @ui.page(page_path)
    def _():
        rxui.input(value=text).classes("input")
        rxui.badge(text).classes("target")

    page = browser.open(page_path)

    badge = page.Badge(".target")
    input = page.Input(".input")
    badge.expect_equal_text("badge")

    input.fill_text("new badge")
    badge.expect_equal_text("new badge")
