from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_value_change(browser: BrowserManager, page_path: str):
    show = to_ref(False)

    @ui.page(page_path)
    def _():
        def open_dialog():
            show.value = True

        def close_dialog():
            show.value = False

        with rxui.dialog(value=show), ui.card():
            ui.label("Content")
            ui.button("Close", on_click=close_dialog).classes("btn-close")

        ui.button("Open", on_click=open_dialog).classes("btn-open")

    page = browser.open(page_path)
    btn_open = page.Button(".btn-open")
    btn_close = page.Button(".btn-close")

    btn_open.click()
    page.should_contain("Content")

    btn_close.click()
    page.should_not_contain("Content")


def test_ref_change(browser: BrowserManager, page_path: str):
    show = to_ref(False)

    @ui.page(page_path)
    def _():
        rxui.checkbox(value=show).classes("checkbox")

        with rxui.dialog(value=show), ui.card():
            ui.label("Content")

    page = browser.open(page_path)
    checkbox = page.Checkbox(".checkbox")

    checkbox.click()
    page.should_contain("Content")
