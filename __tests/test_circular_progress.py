from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        value = to_ref(0.3)
        rxui.circular_progress(value, show_value=True, size="100px").classes("cp")
        rxui.number(value=value).classes("number")
        ui.button("change value").on_click(lambda: value.set_value(0.9)).classes(
            "change-value"
        )

    page = browser.open(page_path)

    cp = page.Base(".cp")
    btn = page.Button(".change-value")

    cp.expect.to_contain_text("0.3")

    btn.click()

    cp.expect.to_contain_text("0.9")
