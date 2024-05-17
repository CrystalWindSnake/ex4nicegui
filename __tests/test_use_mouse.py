from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, effect
from .screen import BrowserManager


def test_mouse_move(browser: BrowserManager, page_path: str):
    r_x = to_ref(0.0)
    r_y = to_ref(0.0)

    @ui.page(page_path)
    def _():
        r_mouse = rxui.use_mouse()

        @effect
        def _():
            r_x.value = r_mouse.x.value
            r_y.value = r_mouse.y.value

    page = browser.open(page_path)
    page.wait()
    page._page.mouse.move(10, 10)

    page.wait()
    assert r_x.value == 10
    assert r_y.value == 10
