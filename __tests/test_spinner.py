from ex4nicegui.reactive import rxui
from nicegui import ui
from .screen import BrowserManager
from playwright.sync_api import expect


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.spinner().classes("target")

    page = browser.open(page_path)

    expect(page.locator("svg.q-spinner")).to_be_visible()
