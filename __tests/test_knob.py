from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        value = to_ref(0.3)
        knob = rxui.knob(value, show_value=True, size="200px").classes("knob")
        rxui.label(value).classes("label")
        ui.button("change value", on_click=lambda: knob.element.set_value(0.9)).classes(
            "btn"
        )

    page = browser.open(page_path)

    knob = page.Base(".knob")
    label = page.Label(".label")
    btn = page.Button(".btn")

    knob.expect.to_contain_text("0.3")

    btn.click()

    knob.expect.to_contain_text("0.9")
    label.expect.to_contain_text("0.9")
