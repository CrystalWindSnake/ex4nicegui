from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import set_test_id, BaseUiUtils


def test_base(page: ScreenPage, page_path: str):
    value = to_ref(0.3)

    @ui.page(page_path)
    def _():
        set_test_id(rxui.circular_progress(value, show_value=True, size="100px"), "cp")
        set_test_id(rxui.number(value=value), "number")

    page.open(page_path)

    cp = BaseUiUtils(page, "cp")

    cp.expect.to_contain_text("0.3")

    value.value = 0.9

    cp.expect.to_contain_text("0.9")
