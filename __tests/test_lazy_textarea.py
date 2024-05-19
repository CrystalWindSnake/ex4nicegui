from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager
from .utils import TextareaUtils, LabelUtils, set_test_id


def test_display(browser: BrowserManager, page_path: str):
    r_str = to_ref("ref value")

    @ui.page(page_path)
    def _():
        rxui.lazy_textarea(value="const value").classes("const-input")
        rxui.lazy_textarea(value=r_str).classes("ref-input")

    page = browser.open(page_path)
    target_const = page.Textarea(".const-input")
    target_const.expect_to_have_text("const value")

    target_ref = page.Textarea(".ref-input")
    target_ref.expect_to_have_text("ref value")

    r_str.value = "new"
    target_ref.expect_to_have_text("new")


def test_input_change_value_when_enter(browser: BrowserManager, page_path: str):
    r_str = to_ref("old")

    @ui.page(page_path)
    def _():
        rxui.lazy_textarea(value=r_str).classes("target")
        rxui.label(r_str).classes("label")

    page = browser.open(page_path)
    input = page.Textarea(".target")
    label = page.Label(".label")

    input.fill_text("new value")
    label.expect_to_have_text("old")

    input.enter()
    label.expect_to_have_text("new value")
