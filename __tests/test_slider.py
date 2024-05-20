from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    r_value = to_ref(0)

    @ui.page(page_path)
    def _():
        rxui.slider(min=0, max=100, value=r_value).classes("target")
        rxui.label(r_value).classes("label")

    page = browser.open(page_path)

    label = page.Label(".label")

    page_g = page._page

    rect = page_g.locator(".q-slider__focus-ring").bounding_box()
    assert rect
    x = rect["x"] + rect["width"] / 2
    y = rect["y"] + rect["height"] / 2
    page_g.mouse.move(x, y)
    page_g.mouse.down()

    win_width = page_g.evaluate("()=> window.innerWidth")
    page_g.mouse.move(x + win_width, 0)

    label.expect_contain_text("100")
