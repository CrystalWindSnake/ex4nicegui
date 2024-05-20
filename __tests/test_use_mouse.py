from ex4nicegui.reactive import rxui
from nicegui import ui
from .screen import BrowserManager


def test_mouse_move(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_mouse = rxui.use_mouse()

        rxui.label(r_mouse.x).classes("label-x")
        rxui.label(r_mouse.y).classes("label-y")

    page = browser.open(page_path)
    label_x = page.Label(".label-x")
    label_y = page.Label(".label-y")

    page.mouse.move(10, 10)

    label_x.expect_contain_text("10")
    label_y.expect_contain_text("10")
