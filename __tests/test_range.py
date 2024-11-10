from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager, PageUtils
from typing import Literal


def drap_move(type: Literal["min", "max"], page: PageUtils, offset_x: int):
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
    page._page.mouse.up()


def test_min_change(browser: BrowserManager, page_path: str):
    r_value = to_ref(
        {
            "min": 0,
            "max": 100,
        }
    )

    @ui.page(page_path)
    def _():
        rxui.range(min=0, max=100, value=r_value).classes("target")
        rxui.label(r_value).classes("label")

    page = browser.open(page_path)
    label = page.Label(".label")

    label.expect_equal_text("{'min': 0, 'max': 100}")
    drap_move("min", page, offset_x=100)
    label.expect_equal_text("{'min': 8, 'max': 100}")

    drap_move("max", page, offset_x=-100)
    label.expect_equal_text("{'min': 8, 'max': 92}")


def test_max_change(browser: BrowserManager, page_path: str):
    r_value = to_ref(
        {
            "min": 0,
            "max": 100,
        }
    )

    @ui.page(page_path)
    def _():
        rxui.range(min=0, max=100, value=r_value).classes("target")
        rxui.label(r_value).classes("label")

    page = browser.open(page_path)
    label = page.Label(".label")

    drap_move("max", page, offset_x=-100)
    label.expect_equal_text("{'min': 0, 'max': 92}")
