import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage


def test_const_str(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.label("test label")

    page.open(page_path)
    page.should_contain("test label")


def test_ref_str(page: ScreenPage, page_path: str):
    r_str = to_ref("test label")

    @ui.page(page_path)
    def _():
        rxui.label(r_str)

    page.open(page_path)
    page.should_contain("test label")


def test_ref_str_change_value(page: ScreenPage, page_path: str):
    r_str = to_ref("old")

    @ui.page(page_path)
    def _():
        rxui.label(r_str)

    page.open(page_path)
    page.should_contain("old")

    page.wait()
    r_str.value = "new"

    page.wait()
    page.should_contain("new")


def test_bind_color(page: ScreenPage, page_path: str):
    r_color = to_ref("red")

    @ui.page(page_path)
    def _():
        rxui.label("label").bind_color(r_color)

    page.open(page_path)

    assert page.get_ele("label").evaluate("node=> node.style.color=='red'")


def test_bind_color_changed(page: ScreenPage, page_path: str):
    r_color = to_ref("red")

    @ui.page(page_path)
    def _():
        rxui.label("label").bind_color(r_color)

    page.open(page_path)

    assert page.get_ele("label").evaluate("node=> node.style.color=='red'")

    page.wait()
    r_color.value = "green"
    page.wait()
    assert page.get_ele("label").evaluate("node=> node.style.color=='green'")
