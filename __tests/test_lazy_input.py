from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import InputUtils, set_test_id, LabelUtils


def test_const_str(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.lazy_input(value="const value").props('data-testid="input"')

    page.open(page_path)
    page.should_contain_text("input", "const value")


def test_ref_str(page: ScreenPage, page_path: str):
    r_str = to_ref("ref value")

    @ui.page(page_path)
    def _():
        rxui.lazy_input(value=r_str).props('data-testid="input"')

    page.open(page_path)
    page.should_contain_text("input", "ref value")


def test_ref_str_change_value(page: ScreenPage, page_path: str):
    r_str = to_ref("old")

    @ui.page(page_path)
    def _():
        rxui.lazy_input(value=r_str).props('data-testid="input"')

    page.open(page_path)
    page.should_contain_text("input", "old")

    page.wait()
    r_str.value = "new"

    page.wait()
    page.should_contain_text("input", "new")


def test_input_change_value_when_enter(page: ScreenPage, page_path: str):
    r_str = to_ref("old")

    @ui.page(page_path)
    def _():
        input = rxui.lazy_input(value=r_str).props("clearable")
        set_test_id(input, "input")
        label = rxui.label(r_str)
        set_test_id(label, "label")

    page.open(page_path)
    page.wait()

    input = InputUtils(page, "input")
    label = LabelUtils(page, "label")

    # page.pause()
    input.fill_text("new value")
    page.wait()
    assert label.get_text() == "old"

    input.enter()
    page.wait()
    assert label.get_text() == "new value"

    input.click_cancel_icon()
    page.wait()
    assert label.get_text() == ""
