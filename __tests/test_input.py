from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager
from .utils import InputUtils, LabelUtils, set_test_id


def test_display(browser: BrowserManager, page_path: str):
    r_str = to_ref("ref value")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.input(value="const value"), "const target")
        set_test_id(rxui.input(value=r_str), "ref target")

    page = browser.open(page_path)
    target_const = InputUtils(page, "const target")
    target_const.expect_to_have_text("const value")

    target_ref = InputUtils(page, "ref target")
    target_ref.expect_to_have_text("ref value")

    r_str.value = "new"
    target_ref.expect_to_have_text("new")


def test_input_change_value(browser: BrowserManager, page_path: str):
    r_str = to_ref("old")
    dummy = ""

    @ui.page(page_path)
    def _():
        def onchange():
            nonlocal dummy
            dummy = r_str.value

        set_test_id(rxui.input(value=r_str, on_change=onchange), "input")
        set_test_id(rxui.label(r_str), "label")

    page = browser.open(page_path)
    input = InputUtils(page, "input")
    label = LabelUtils(page, "label")

    input.fill_text("new value")

    label.expect_to_have_text("new value")

    assert dummy == "new value"
