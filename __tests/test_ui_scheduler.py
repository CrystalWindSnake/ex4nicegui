from ex4nicegui import rxui, ref_computed, effect, to_ref
from nicegui import ui
from .screen import BrowserManager


def test_when_error_in_effect(browser: BrowserManager, page_path: str):
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

        rxui.input(value=text).classes("input")
        rxui.label(dummy).classes("label")

    page = browser.open(page_path)

    input = page.Input(".input")
    label = page.Label(".label")

    label.expect_contain_text("Hello world")

    input.fill_text("foo")
    label.expect_contain_text("Hello world")

    input.fill_text("bar")
    label.expect_contain_text("bar world")
