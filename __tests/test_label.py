import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import TestPage


class PathCounnter:
    def __init__(self) -> None:
        self.__num = 0

    def get_path(self):
        self.__num += 1
        return f"/{self.__num}"


path_counter = PathCounnter()


def test_const_str(page: TestPage):
    path = path_counter.get_path()

    @ui.page(path)
    def _():
        rxui.label("test label")

    page.open(path)
    page.should_contain("test label")


def test_ref_str(page: TestPage):
    path = path_counter.get_path()

    r_str = to_ref("test label")

    @ui.page(path)
    def _():
        rxui.label(r_str)

    page.open(path)
    page.should_contain("test label")


def test_ref_str_change_value(page: TestPage):
    path = path_counter.get_path()

    r_str = to_ref("old")

    @ui.page(path)
    def _():
        rxui.label(r_str)

    page.open(path)
    page.should_contain("old")

    page.wait()
    r_str.value = "new"

    page.wait()
    page.should_contain("new")


def test_bind_color(page: TestPage):
    path = path_counter.get_path()

    r_color = to_ref("red")

    @ui.page(path)
    def _():
        rxui.label("label").bind_color(r_color)

    page.open(path)

    assert page.get_ele("label").evaluate("node=> node.style.color=='red'")


def test_bind_color_changed(page: TestPage):
    path = path_counter.get_path()

    r_color = to_ref("red")

    @ui.page(path)
    def _():
        rxui.label("label").bind_color(r_color)

    page.open(path)

    assert page.get_ele("label").evaluate("node=> node.style.color=='red'")

    page.wait()
    r_color.value = "green"
    page.wait()
    assert page.get_ele("label").evaluate("node=> node.style.color=='green'")
