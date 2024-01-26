from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import InputUtils, LabelUtils, set_test_id


def test_const_str(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        set_test_id(rxui.input(value="const value"), "target")

    page.open(page_path)
    target = InputUtils(page, "target")
    target.expect_to_have_text("const value")


def test_ref_str(page: ScreenPage, page_path: str):
    r_str = to_ref("ref value")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.input(value=r_str), "target")

    page.open(page_path)
    target = InputUtils(page, "target")
    target.expect_to_have_text("ref value")


def test_ref_str_change_value(page: ScreenPage, page_path: str):
    r_str = to_ref("old")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.input(value=r_str), "target")

    page.open(page_path)
    target = InputUtils(page, "target")
    target.expect_to_have_text("old")

    r_str.value = "new"

    target.expect_to_have_text("new")


def test_input_change_value(page: ScreenPage, page_path: str):
    r_str = to_ref("old")
    dummy = ""

    @ui.page(page_path)
    def _():
        def onchange():
            nonlocal dummy
            dummy = r_str.value

        set_test_id(rxui.input(value=r_str, on_change=onchange), "input")
        set_test_id(rxui.label(r_str), "label")

    page.open(page_path)
    input = InputUtils(page, "input")
    label = LabelUtils(page, "label")

    input.fill_text("new value")

    label.expect_to_have_text("new value")

    assert dummy == "new value"
