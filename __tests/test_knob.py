from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import set_test_id, BaseUiUtils, ButtonUtils


def test_base(browser: BrowserManager, page_path: str):
    value = to_ref(0.3)

    @ui.page(page_path)
    def _():
        knob = rxui.knob(value, show_value=True, size="200px")
        set_test_id(knob, "knob")
        set_test_id(rxui.label(value), "label")
        set_test_id(
            ui.button("change value", on_click=lambda: knob.element.set_value(0.9)),
            "btn",
        )

    page = browser.open(page_path)

    knob = BaseUiUtils(page, "knob")
    label = BaseUiUtils(page, "label")
    btn = ButtonUtils(page, "btn")

    knob.expect.to_contain_text("0.3")

    btn.click()

    knob.expect.to_contain_text("0.9")
    label.expect.to_contain_text("0.9")
