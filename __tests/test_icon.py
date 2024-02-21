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

    page.wait()
    r_str.value = "add"

    page.wait()
    page.should_contain("add")


def test_color(page: ScreenPage, page_path: str):
    r_color = to_ref("primary")

    @ui.page(page_path)
    def _():
        rxui.icon("home", color=r_color).classes("target")

    page.open(page_path)

    def get_color_value():
        return page._page.locator(".target").evaluate(
            "(node)=>window.getComputedStyle(node).color"
        )

    assert get_color_value() == "rgb(88, 152, 212)"

    r_color.value = "rgba(224,52,52,1)"
    page.wait()
    assert get_color_value() == "rgb(224, 52, 52)"
