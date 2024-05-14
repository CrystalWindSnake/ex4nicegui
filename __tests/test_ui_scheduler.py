from ex4nicegui import rxui, ref_computed, effect, to_ref
from nicegui import ui
from .screen import ScreenPage
from .utils import InputUtils, LabelUtils, set_test_id


def test_when_error_in_effect(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        text = to_ref("Hello")
        dummy = to_ref("")

        @ref_computed
        def cp():
            if text.value == "foo":
                raise Exception("")

            return text.value + " world"

        @effect
        def _():
            dummy.value = str(cp.value)

        set_test_id(rxui.input(value=text), "input")
        set_test_id(rxui.label(dummy), "label")

    page.open(page_path)
    page.wait(600)

    input = InputUtils(page, "input")
    label = LabelUtils(page, "label")

    label.expect_contain_text("Hello world")

    input.fill_text("foo")
    label.expect_contain_text("Hello world")

    input.fill_text("bar")
    label.expect_contain_text("bar world")
