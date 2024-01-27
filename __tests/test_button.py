from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import ButtonUtils, set_test_id


def test_ref_text(page: ScreenPage, page_path: str):
    r_text = to_ref("old text")

    @ui.page(page_path)
    def _():
        set_test_id(
            rxui.button(r_text).props('data-testid="target"').props("no-caps"), "btn"
        )

    page.open(page_path)

    btn = ButtonUtils(page, "btn")

    btn.expect_to_have_text("old text")

    r_text.value = "new text"
    btn.expect_to_have_text(text="new text")
