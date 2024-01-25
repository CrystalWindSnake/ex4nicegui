from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import ColorPickerUtils, LabelUtils, set_test_id


def test_display(page: ScreenPage, page_path: str):
    r_color = to_ref("red")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.color_picker(r_color), "target")
        set_test_id(rxui.label(r_color), "label")

    page.open(page_path)

    target = ColorPickerUtils(page, "target")
    label = LabelUtils(page, "label")

    target.expect_has_button()
    label.expect_contain_text("red")

    target.click_button()
    target.click_color_panel()

    label.expect_contain_text("rgba")
