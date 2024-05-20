from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_display(browser: BrowserManager, page_path: str):
    r_color = to_ref("red")

    @ui.page(page_path)
    def _():
        rxui.color_picker(r_color).classes("target")
        rxui.label(r_color).classes("label")

    page = browser.open(page_path)

    target = page.ColorPicker(".target")
    label = page.Label(".label")

    target.expect_has_button()
    label.expect_contain_text("red")

    target.click_button()
    target.click_color_panel()

    label.expect_contain_text("rgba")
