import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import TestPage


def test_const_str(page: TestPage, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.lazy_input(value="const value").props('data-testid="input"')

    page.open(page_path)
    page.should_contain_text("input", "const value")


def test_ref_str(page: TestPage, page_path: str):
    r_str = to_ref("ref value")

    @ui.page(page_path)
    def _():
        rxui.lazy_input(value=r_str).props('data-testid="input"')

    page.open(page_path)
    page.should_contain_text("input", "ref value")


def test_ref_str_change_value(page: TestPage, page_path: str):
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


def test_input_change_value_when_enter(page: TestPage, page_path: str):
    r_str = to_ref("old")

    @ui.page(page_path)
    def _():
        rxui.lazy_input(value=r_str).props('data-testid="input"')
        rxui.label(r_str).props('data-testid="label"')

    page.open(page_path)

    page.wait()
    # page.pause()
    page.fill("input", "new value")
    page.wait()
    assert page.get_by_testid("label").inner_text() == "old"

    page.enter("input")
    page.wait()
    assert page.get_by_testid("label").inner_text() == "new value"
