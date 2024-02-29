from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import set_test_id, BaseUiUtils, InputNumberUtils


def test_base(page: ScreenPage, page_path: str):
    value = to_ref(0.3)

    @ui.page(page_path)
    def _():
        set_test_id(rxui.knob(value, show_value=True), "knob")
        set_test_id(rxui.label(value), "label")
        set_test_id(rxui.number(value=value), "number")

    page.open(page_path)

    knob = BaseUiUtils(page, "knob")
    label = BaseUiUtils(page, "label")
    number = InputNumberUtils(page, "number")

    knob.expect.to_contain_text("0.3")

    knob.target_locator.click()
    knob.expect.not_to_contain_text("0.3")
    label.expect.not_to_contain_text("0.3")

    # value.value = 0.9
    number.fill_text("0.9")

    knob.expect.to_contain_text("0.9")
    label.expect.to_contain_text("0.9")