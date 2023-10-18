from typing import cast
import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage


def fname(arg):
    pass


def test_const_str(page: ScreenPage, page_path: str):
    sd = cast(rxui.slider, None)

    @ui.page(page_path)
    def _():
        nonlocal sd
        sd = rxui.slider(min=0, max=10).props('data-testid="target"')

    page.open(page_path)

    btn = page._page.query_selector(".q-slider__inner")
    assert btn is not None

    rect = btn.bounding_box()
    assert rect is not None

    page._page.mouse.move(rect["x"], rect["y"])
    page._page.mouse.down()

    def get_container_width():
        ct = page._page.query_selector(".q-slider__track-container")
        return ct.bounding_box()["width"]

    page._page.mouse.move(rect["x"] + get_container_width(), rect["y"])
    page._page.mouse.up()

    # page.pause()
    page.wait()
    assert sd.element.value == 10


def test_ref_str(page: ScreenPage, page_path: str):
    r_str = to_ref("ref value")

    @ui.page(page_path)
    def _():
        rxui.input(value=r_str).props('data-testid="input"')

    page.open(page_path)
    page.should_contain_text("input", "ref value")


def test_ref_str_change_value(page: ScreenPage, page_path: str):
    r_str = to_ref("old")

    @ui.page(page_path)
    def _():
        rxui.input(value=r_str).props('data-testid="input"')

    page.open(page_path)
    page.should_contain_text("input", "old")

    page.wait()
    r_str.value = "new"

    page.wait()
    page.should_contain_text("input", "new")


def test_input_change_value(page: ScreenPage, page_path: str):
    r_str = to_ref("old")

    @ui.page(page_path)
    def _():
        rxui.input(value=r_str).props('data-testid="input"')
        rxui.label(r_str).props('data-testid="label"')

    page.open(page_path)

    page.wait()
    # page.pause()
    page.fill("input", "new value")

    page.wait()
    assert page.get_by_test_id("label").inner_text() == "new value"
