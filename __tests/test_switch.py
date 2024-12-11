from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager

target_test_id = "switch"


def test_const_value(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.switch(value=False).classes("target")

    page = browser.open(page_path)

    target = page.Switch(".target")

    target.expect_to_be_visible()
    target.expect_not_checked()

    target.click()
    target.expect_checked()


def test_ref_value(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_on = to_ref(False)
        rxui.switch(value=r_on).classes("target")
        rxui.label(text=r_on).classes("label")

    page = browser.open(page_path)
    target = page.Switch(".target")
    label = page.Label(".label")

    target.expect_to_be_visible()
    target.expect_not_checked()
    label.expect_contain_text("False")

    target.click()
    target.expect_checked()
    label.expect_contain_text("True")


def test_ref_str_change_value(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_on = to_ref(False)
        rxui.switch(value=r_on).classes("target")
        ui.button(
            "change",
            on_click=lambda: r_on.set_value(True),
        ).classes("btn-change")

    page = browser.open(page_path)
    target = page.Switch(".target")
    btn = page.Button(".btn-change")

    target.expect_to_be_visible()
    target.expect_not_checked()

    btn.click()

    target.expect_checked()
