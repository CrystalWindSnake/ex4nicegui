from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import InputNumberUtils, set_test_id, fn


def test_const(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        set_test_id(rxui.number(value=1.0), "target")

    page.open(page_path)

    target = InputNumberUtils(page, "target")

    assert target.get_input_value() == "1.0"


def test_ref(page: ScreenPage, page_path: str):
    r_value = to_ref(1.0)

    @ui.page(page_path)
    def _():
        set_test_id(rxui.number(value=r_value), "target")

    page.open(page_path)

    target = InputNumberUtils(page, "target")

    assert target.get_input_value() == "1.0"

    page.wait()
    r_value.value = 3.11

    page.wait()
    assert target.get_input_value() == "3.11"

    # type input number
    target.input_text("66")

    page.wait()
    assert r_value.value == 3.1166


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

    page.wait(1000)
    target.input_text("1111")
    assert value_on_change == 1111.0


def test_with_format(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        set_test_id(rxui.number(format="%.2f", step=0.1), "target")

    page.open(page_path)

    target = InputNumberUtils(page, "target")

    page.wait(1000)
    target.input_text("1111")
    assert target.get_input_value() == "1111"
