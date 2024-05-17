from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import InputUtils, set_test_id, LabelUtils


def test_display(browser: BrowserManager, page_path: str):
    r_str = to_ref("ref value")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.lazy_input(value="const value"), "const input")
        set_test_id(rxui.lazy_input(value=r_str), "ref input")

    page = browser.open(page_path)
    target_const = InputUtils(page, "const input")
    target_const.expect_to_have_text("const value")

    target_ref = InputUtils(page, "ref input")
    target_ref.expect_to_have_text("ref value")

    r_str.value = "new"
    page.wait()
    target_ref.expect_to_have_text("new")


def test_input_change_value_when_enter(browser: BrowserManager, page_path: str):
    r_str = to_ref("old")

    @ui.page(page_path)
    def _():
        input = rxui.lazy_input(value=r_str).props("clearable")
        set_test_id(input, "input")

        label = rxui.label(r_str)
        set_test_id(label, "label")

    page = browser.open(page_path)
    page.wait()

    input = InputUtils(page, "input")
    label = LabelUtils(page, "label")

    input.fill_text("new value")

    label.expect_to_have_text("old")

    input.enter()
    label.expect_to_have_text("new value")

    input.click_cancel_icon()

    label.expect_to_have_text("")
