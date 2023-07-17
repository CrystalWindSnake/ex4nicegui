import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import ref_computed
from .screen import ScreenPage


def test_mouse_move(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        r_mouse = rxui.use_mouse()

        @ref_computed
        def x_label():
            return f"x:{r_mouse.x.value}"

        @ref_computed
        def y_label():
            return f"y:{r_mouse.y.value}"

        rxui.label(x_label)
        rxui.label(y_label)

    page.open(page_path)
    page.wait()
    page._page.mouse.move(10, 10)

    page.should_contain("x:10")
    page.should_contain("y:10")
