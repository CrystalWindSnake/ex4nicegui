from typing import cast
import pytest
from ex4nicegui.reactive import rxui
from ex4nicegui.reactive.UseDraggable.UseDraggable import UseDraggable
from nicegui import ui
from ex4nicegui import ref_computed, to_ref
from .screen import ScreenPage
from .utils import set_test_id, LabelUtils


def test_draggable(page: ScreenPage, page_path: str):
    x_ref = to_ref(100.0)
    y_ref = to_ref(100.0)
    r_drag = cast(UseDraggable, None)

    @ui.page(page_path)
    def _():
        nonlocal r_drag

        @ref_computed
        def position_text():
            return f"x:{x_ref.value},y:{y_ref.value}"

        with ui.card().classes("my-box w-[10rem] h-[10rem] bg-blue") as card:
            ui.label("卡片")
            rxui.label(position_text)

        r_drag = rxui.use_draggable(card, init_x=x_ref, init_y=y_ref)

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

    assert x_ref.value == 100.0
    assert y_ref.value == 100.0
    assert r_drag.x.value == 100.0
    assert r_drag.y.value == 100.0

    # start drag
    org_x = box_rect["x"]

    x = box_rect["x"] + box_rect["width"] / 2
    y = box_rect["y"] + box_rect["height"] / 2

    page._page.mouse.move(x, y)
    page._page.mouse.down()

    page._page.mouse.move(x + 500, y)
    page._page.mouse.up()

    page.wait()

    box_rect = box_target.bounding_box()
    assert box_rect is not None

    assert box_rect["x"] == org_x + 500

    assert x_ref.value == 600.0
    assert y_ref.value == 100.0
    assert r_drag.x.value == 600.0
    assert r_drag.y.value == 100.0
