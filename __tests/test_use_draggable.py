from typing import cast
from ex4nicegui.reactive import rxui
from ex4nicegui.reactive.UseDraggable.UseDraggable import UseDraggable
from nicegui import ui
from ex4nicegui import ref_computed
from .screen import ScreenPage


def test_draggable(page: ScreenPage, page_path: str):
    # r_drag = cast(UseDraggable, None)

    @ui.page(page_path)
    def _():
        # nonlocal r_drag
        r_drag = rxui.use_draggable(init_x=100, init_y=100)

        @ref_computed
        def position_text():
            return f"x:{r_drag.x},y:{r_drag.y}"

        with ui.card().classes("my-box w-[10rem] h-[10rem] bg-blue") as card:
            ui.label("卡片")
            rxui.label(position_text)

        r_drag.apply(card)

        @ref_computed
        def x_label():
            return f"x:{r_drag.x}"

        @ref_computed
        def y_label():
            return f"y:{r_drag.y}"

        rxui.label(x_label)
        rxui.label(y_label)

    page.open(page_path)
    page.wait()

    box_target = page._page.query_selector(".my-box")
    assert box_target is not None

    box_rect = box_target.bounding_box()
    assert box_rect is not None

    # assert r_drag.x == 100.0
    # assert r_drag.y == 100.0

    page.pause()

    # start drag
    org_x = box_rect["x"]

    x = box_rect["x"] + box_rect["width"] / 2
    y = box_rect["y"] + box_rect["height"] / 2

    page._page.mouse.move(x, y)
    page._page.mouse.down()

    page._page.mouse.move(x + 500, y)
    page._page.mouse.up()

    page.pause()
    page.wait()

    box_rect = box_target.bounding_box()
    assert box_rect is not None

    assert box_rect["x"] == org_x + 500

    # assert r_drag.x == 600.0
    # assert r_drag.y == 100.0
