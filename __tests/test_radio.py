from typing import Optional
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, Ref
from .screen import BrowserManager


def test_display(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.radio(["a", "b"]).classes("target")

    page = browser.open(page_path)

    target = page.Radio(".target")

    target.expect_to_be_visible()
    target.expect_not_to_be_checked("a")
    target.expect_not_to_be_checked("b")

    target.check_by_label("a")

    target.expect_to_be_checked("a")
    target.expect_not_to_be_checked("b")

    target.check_by_label("b")

    target.expect_not_to_be_checked("a")
    target.expect_to_be_checked("b")


def test_ref_value(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_value = to_ref(None)
        rxui.radio(["a", "b"], value=r_value).classes("target")
        rxui.label(r_value).classes("label")

    page = browser.open(page_path)

    target = page.Radio(".target")
    label = page.Label(".label")

    target.expect_to_be_visible()

    target.expect_not_to_be_checked("a")
    target.expect_not_to_be_checked("b")

    target.check_by_label("a")

    target.expect_to_be_checked("a")
    target.expect_not_to_be_checked("b")
    label.expect_contain_text("a")

    target.check_by_label("b")

    target.expect_not_to_be_checked("a")
    target.expect_to_be_checked("b")
    label.expect_contain_text("b")


def test_ref_str_change_value(browser: BrowserManager, page_path: str):
    data = iter(["a", "b"])

    @ui.page(page_path)
    def _():
        r_value: Ref[Optional[str]] = to_ref(None)
        rxui.radio(["a", "b"], value=r_value).classes("target")
        ui.button(
            "change",
            on_click=lambda: r_value.set_value(next(data)),
        ).classes("btn-change")

    page = browser.open(page_path)

    target = page.Radio(".target")
    btn = page.Button(".btn-change")

    target.expect_to_be_visible()

    btn.click()

    target.expect_to_be_checked("a")
    target.expect_not_to_be_checked("b")

    btn.click()
    target.expect_not_to_be_checked("a")
    target.expect_to_be_checked("b")


def test_ref_value_dict_options(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_value: Ref[Optional[str]] = to_ref(None)
        opts = {
            "a": "a value",
            "b": "b value",
        }
        rxui.radio(opts, value=r_value).classes("target")
        rxui.label(r_value).classes("label")

    page = browser.open(page_path)

    target = page.Radio(".target")
    label = page.Label(".label")

    target.expect_to_be_visible()

    target.check_by_label("a value")

    target.expect_to_be_checked("a value")
    target.expect_not_to_be_checked("b value")
    label.expect_contain_text("a")

    target.check_by_label("b value")

    target.expect_not_to_be_checked("a value")
    target.expect_to_be_checked("b value")
    label.expect_contain_text("b")
