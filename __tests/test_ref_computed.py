from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, ref_computed
from .screen import ScreenPage
from .utils import InputUtils, LabelUtils, set_test_id


def test_method_decorator(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        class MyState:
            def __init__(self) -> None:
                self.r_text = to_ref("")

            @ref_computed
            def post_text(self):
                return self.r_text.value + " post"

        state = MyState()

        set_test_id(rxui.input(value=state.r_text), "input")

        set_test_id(rxui.label(state.post_text), "label")

    page.open(page_path)

    input = InputUtils(page, "input")
    label = LabelUtils(page, "label")

    label.expect_to_have_text("post")
    input.fill_text("new text")
    label.expect_to_have_text("new text post")
