import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage


def test_const_str(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.icon("home")

    page.open(page_path)
    page.should_contain("home")


def test_ref_str(page: ScreenPage, page_path: str):
    r_str = to_ref("home")

    @ui.page(page_path)
    def _():
        rxui.icon(r_str)

    page.open(page_path)
    page.should_contain("home")


def test_ref_str_change_value(page: ScreenPage, page_path: str):
    r_str = to_ref("home")

    @ui.page(page_path)
    def _():
        rxui.icon(r_str)

    page.open(page_path)
    page.should_contain("home")

    page.wait()
    r_str.value = "add"

    page.wait()
    page.should_contain("add")
