import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import ref_computed
from .screen import ScreenPage


def test_draggable(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        box = ui.element("div").classes("my-box w-[10rem] h-[10rem] bg-blue")
        r_drag = rxui.use_draggable(box)

        @ref_computed
        def x_label():
            return f"x:{r_drag.x.value}"

        @ref_computed
        def y_label():
            return f"y:{r_drag.y.value}"

        rxui.label(x_label)
        rxui.label(y_label)

    page.open(page_path)
    page.wait()

    box_target = page._page.query_selector(".my-box")
    assert box_target is not None

    box_rect = box_target.bounding_box()
    assert box_rect is not None

    org_x = box_rect["x"]

    x = box_rect["x"] + box_rect["width"] / 2
    y = box_rect["y"] + box_rect["height"] / 2

    page._page.mouse.move(x, y)
    page._page.mouse.down()

    page._page.mouse.move(x + 500, y)
    page._page.mouse.up()

    box_rect = box_target.bounding_box()
    assert box_rect is not None

    assert box_rect["x"] == org_x + 500
