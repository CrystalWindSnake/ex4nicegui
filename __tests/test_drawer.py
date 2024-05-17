from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage


def test_display(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        with rxui.drawer():
            ui.label("drawer showed")

    page = browser.open(page_path)
    page.should_contain("drawer showed")


def test_toggle_side(browser: BrowserManager, page_path: str):
    r_side = to_ref("left")

    def toggle_side():
        if r_side.value == "left":
            r_side.value = "right"
        else:
            r_side.value = "left"

    @ui.page(page_path)
    def _():
        with rxui.drawer(r_side):
            ui.label("drawer showed")
            rxui.label(r_side)

            def onclick():
                toggle_side()

            rxui.button("switch side", on_click=onclick).classes("my-btn")

    body_width = page._page.evaluate("()=>document.body.clientWidth")

    page = browser.open(page_path)
    page.should_contain("drawer showed")
    rect = page._page.get_by_text("drawer showed").bounding_box()
    assert rect is not None
    assert rect["x"] < body_width / 2

    page.wait()
    page._page.query_selector(".my-btn").click()
    page.wait()

    rect = page._page.get_by_text("drawer showed").bounding_box()
    assert rect is not None
    assert rect["x"] > body_width / 2


def test_toggle_show(browser: BrowserManager, page_path: str):
    r_show = to_ref(True)

    def toggle_show():
        r_show.value = not r_show.value

    @ui.page(page_path)
    def _():
        with rxui.drawer(value=r_show):
            ui.label("drawer showed")

            def onclick():
                toggle_show()

        rxui.button("switch show", on_click=onclick).classes("my-btn")

    page = browser.open(page_path)
    page.should_contain("drawer showed")

    page.wait()
    page._page.query_selector(".my-btn").click()
    page.wait()

    page.should_not_contain("drawer showed")

    page.wait()
    page._page.query_selector(".my-btn").click()
    page.wait()

    page.should_contain("drawer showed")
