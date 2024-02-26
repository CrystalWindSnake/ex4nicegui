from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import CheckboxUtils, LabelUtils, set_test_id


target_test_id = "checkbox"


def test_const_value(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        set_test_id(rxui.checkbox("test checkbox"), "target")

    page.open(page_path)

    target = CheckboxUtils(page, "target")

    target.expect_to_be_visible()
    target.expect.not_to_be_checked()

    target.click()

    target.expect.to_be_checked()


def test_ref_value(page: ScreenPage, page_path: str):
    r_value = to_ref(False)

    @ui.page(page_path)
    def _():
        cb = rxui.checkbox("test checkbox", value=r_value)
        set_test_id(cb, "target")

        set_test_id(rxui.label(r_value), "value")

    page.open(page_path)

    target = CheckboxUtils(page, "target")
    value_label = LabelUtils(page, "value")

    target.expect_to_be_visible()

    target.expect.not_to_be_checked()
    value_label.expect.to_have_text("False")

    target.click()
    value_label.expect.to_have_text("True")


def test_ref_str_change_value(page: ScreenPage, page_path: str):
    r_value = to_ref(False)

    @ui.page(page_path)
    def _():
        cb = rxui.checkbox("test checkbox", value=r_value)
        set_test_id(cb, "target")

    page.open(page_path)

    target = CheckboxUtils(page, "target")

    target.expect_to_be_visible()

    r_value.value = True

    target.expect.to_be_checked()
