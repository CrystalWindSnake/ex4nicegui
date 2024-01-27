from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import TextareaUtils, LabelUtils, set_test_id


def test_display(page: ScreenPage, page_path: str):
    r_str = to_ref("ref value")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.lazy_textarea(value="const value"), "const input")
        set_test_id(rxui.lazy_textarea(value=r_str), "ref input")

    page.open(page_path)
    target_const = TextareaUtils(page, "const input")
    target_const.expect_to_have_text("const value")

    target_ref = TextareaUtils(page, "ref input")
    target_ref.expect_to_have_text("ref value")

    r_str.value = "new"
    page.wait()
    target_ref.expect_to_have_text("new")


def test_input_change_value_when_enter(page: ScreenPage, page_path: str):
    r_str = to_ref("old")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.lazy_textarea(value=r_str), "target")
        set_test_id(rxui.label(r_str), "label")

    page.open(page_path)
    input = TextareaUtils(page, "target")
    label = LabelUtils(page, "label")

    input.fill_text("new value")
    label.expect_to_have_text("old")

    input.enter()
    label.expect_to_have_text("new value")
