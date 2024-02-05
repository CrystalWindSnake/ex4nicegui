from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import InputNumberUtils, set_test_id


def test_const(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        set_test_id(rxui.number(value=1.0), "target")

    page.open(page_path)

    target = InputNumberUtils(page, "target")

    target.expect_to_have_text("1.0")


def test_ref(page: ScreenPage, page_path: str):
    r_value = to_ref(1.0)

    @ui.page(page_path)
    def _():
        set_test_id(rxui.number(value=r_value), "target")  # type: ignore

    page.open(page_path)

    target = InputNumberUtils(page, "target")

    target.expect_to_have_text("1.0")

    r_value.value = 3.11
    target.expect_to_have_text("3.11")

    # type input number
    target.input_text("66")
    page.wait()
    assert r_value.value == 3.1166

    # type replace
    target.click()
    target.dbclick()
    target.input_text("66")

    page.wait()
    assert r_value.value == 66


def test_on_change(page: ScreenPage, page_path: str):
    value_on_change = 0

    def on_change(e):
        nonlocal value_on_change
        value_on_change = e.value

    @ui.page(page_path)
    def _():
        set_test_id(rxui.number(format="%.2f", step=0.1, on_change=on_change), "target")

    page.open(page_path)

    target = InputNumberUtils(page, "target")

    target.input_text("1111")
    page.wait(1500)
    assert value_on_change == 1111.0


def test_with_format(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        set_test_id(rxui.number(format="%.2f", step=0.1), "target")

    page.open(page_path)

    target = InputNumberUtils(page, "target")

    page.wait(1000)
    target.input_text("1111")
    target.expect_to_have_text("1111")
