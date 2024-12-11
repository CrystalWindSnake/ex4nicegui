from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_chip(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_text = to_ref("chip")
        rxui.input(value=r_text).classes("input")
        rxui.chip(r_text).classes("chip")

    page = browser.open(page_path)

    chip = page.Chip(".chip")
    input = page.Input(".input")
    chip.expect_equal_text("chip")

    input.fill_text("new chip")
    chip.expect_equal_text("new chip")
