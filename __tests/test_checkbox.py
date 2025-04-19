from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


target_test_id = "checkbox"


def test_const_value(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.checkbox("test checkbox").classes("target")

    page = browser.open(page_path)

    target = page.Checkbox(".target")

    target.expect_to_be_visible()
    target.expect.not_to_be_checked()

    target.click()

    target.expect.to_be_checked()


def test_ref_value(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_value = to_ref(False)
        rxui.checkbox("test checkbox", value=r_value).classes("target")

        rxui.label(r_value).classes("value")

    page = browser.open(page_path)

    target = page.Checkbox(".target")
    value_label = page.Label(".value")

    target.expect_to_be_visible()

    target.expect.not_to_be_checked()
    value_label.expect.to_have_text("False")

    target.click()
    value_label.expect.to_have_text("True")


def test_ref_str_change_value(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_value = to_ref(False)
        rxui.checkbox("test checkbox", value=r_value).classes("target")
        ui.button("change value").on_click(lambda: r_value.set_value(True)).classes(
            "change-value"
        )

    page = browser.open(page_path)

    target = page.Checkbox(".target")
    change_value_btn = page.Button(".change-value")

    target.expect_to_be_visible()

    change_value_btn.click()

    target.expect.to_be_checked()
