from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager, PageUtils
from typing import Literal


def drap_move_and_hold(type: Literal["min", "max"], page: PageUtils, offset_x: int):
    targets = page.locator(".q-slider__focus-ring")
    if type == "min":
        target = targets.first
    else:
        target = targets.last

    rect = target.bounding_box()
    assert rect
    x = rect["x"] + rect["width"] / 2
    y = rect["y"] + rect["height"] / 2

    page._page.mouse.move(x, y)
    page._page.mouse.down()
    page._page.mouse.move(x + offset_x, y)


def mouse_up(
    page: PageUtils,
):
    page._page.mouse.up()


def test_ref_value_change(browser: BrowserManager, page_path: str):
    r_value = to_ref(
        {
            "min": 0,
            "max": 100,
        }
    )

    @ui.page(page_path)
    def _():
        rxui.lazy_range(min=0, max=100, value=r_value).classes("target")
        rxui.label(r_value).classes("label")

    page = browser.open(page_path)
    label = page.Label(".label")

    label.expect_equal_text("{'min': 0, 'max': 100}")
    drap_move_and_hold("min", page, offset_x=100)
    label.expect_equal_text("{'min': 0, 'max': 100}")

    mouse_up(page)
    label.expect_equal_text("{'min': 8, 'max': 100}")


def test_on_change_event(browser: BrowserManager, page_path: str):
    r_value = to_ref(
        {
            "min": 0,
            "max": 100,
        }
    )

    @ui.page(page_path)
    def _():
        def on_change(e):
            label.text = str(e.args)

        rxui.lazy_range(min=0, max=100, value=r_value, on_change=on_change).classes(
            "target"
        )

        label = ui.label("old").classes("label")

    page = browser.open(page_path)
    label = page.Label(".label")

    label.expect_equal_text("old")
    drap_move_and_hold("min", page, offset_x=100)
    label.expect_equal_text("old")

    mouse_up(page)
    label.expect_equal_text("{'min': 8, 'max': 100}")


def test_on_update_event(browser: BrowserManager, page_path: str):
    r_value = to_ref(
        {
            "min": 0,
            "max": 100,
        }
    )

    @ui.page(page_path)
    def _():
        def on_update(e):
            label.text = str(e.value)

        rxui.lazy_range(min=0, max=100, value=r_value, on_update=on_update).classes(
            "target"
        )

        label = ui.label("old").classes("label")

    page = browser.open(page_path)
    label = page.Label(".label")

    label.expect_equal_text("old")
    drap_move_and_hold("min", page, offset_x=100)
    label.expect_equal_text("{'min': 8, 'max': 100}")

    mouse_up(page)
    label.expect_equal_text("{'min': 8, 'max': 100}")
