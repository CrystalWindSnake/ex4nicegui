from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager
from .utils import LabelUtils, set_test_id


def test_display(browser: BrowserManager, page_path: str):
    r_str = to_ref("ref label")
    r_bool = to_ref("init")

    @ui.page(page_path)
    def _():
        rxui.label("test label").classes("target")
        rxui.label(r_str).classes("ref-target")

        r_bool.value = True  # type: ignore
        rxui.label(r_bool).classes("bool-ref-target")

    page = browser.open(page_path)

    target_const = page.Label(".target")
    target_const.expect_to_have_text("test label")

    target_ref = page.Label(".ref-target")
    target_ref.expect_to_have_text("ref label")

    target_bool_ref = page.Label(".bool-ref-target")
    target_bool_ref.expect_to_have_text("True")


def test_ref_str_change_value(browser: BrowserManager, page_path: str):
    r_str = to_ref("old")

    @ui.page(page_path)
    def _():
        rxui.label(r_str).classes("target")

    page = browser.open(page_path)

    target = page.Label(".target")
    target.expect_to_have_text("old")

    r_str.value = "new"

    target.expect_to_have_text("new")


def test_bind_color(browser: BrowserManager, page_path: str):
    r_color = to_ref("red")

    @ui.page(page_path)
    def _():
        rxui.label("label").classes("target").bind_color(r_color)

    page = browser.open(page_path)
    target = page.Label(".target")

    target.expect_to_have_style("color", "rgb(255, 0, 0)")

    r_color.value = "green"
    target.expect_to_have_style("color", "rgb(0, 128, 0)")
