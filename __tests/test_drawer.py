from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_display(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        with rxui.drawer():
            ui.label("drawer showed").classes("label")

    page = browser.open(page_path)

    label = page.Label(".label")
    label.expect_to_be_visible()


def test_toggle_side(browser: BrowserManager, page_path: str):
    r_side = to_ref("left")

    def toggle_side():
        if r_side.value == "left":
            r_side.value = "right"
        else:
            r_side.value = "left"

    @ui.page(page_path)
    def _():
        with rxui.drawer(r_side):  # type: ignore
            ui.label("drawer showed")
            rxui.label(r_side)

            def onclick():
                toggle_side()

            rxui.button("switch side", on_click=onclick).classes("my-btn")

    page = browser.open(page_path)

    btn = page.Button(".my-btn")

    body_width = page.evaluate("()=>document.body.clientWidth")
    rect = page.get_by_text("drawer showed").bounding_box()
    assert rect is not None
    assert rect["x"] < body_width / 2

    btn.click()
    rect = page.get_by_text("drawer showed").bounding_box()
    assert rect is not None
    assert rect["x"] > body_width / 2


def test_toggle_show(browser: BrowserManager, page_path: str):
    r_show = to_ref(True)

    def toggle_show():
        r_show.value = not r_show.value

    @ui.page(page_path)
    def _():
        with rxui.drawer(value=r_show):
            ui.label("drawer showed").classes("label")

            def onclick():
                toggle_show()

        rxui.button("switch show", on_click=onclick).classes("my-btn")

    page = browser.open(page_path)

    btn = page.Button(".my-btn")
    label = page.Label(".label")

    btn.click()
    label.expect_to_be_hidden()

    btn.click()
    label.expect_to_be_visible()
