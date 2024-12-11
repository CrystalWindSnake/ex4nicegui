from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_display(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_str = to_ref("ref label")
        r_bool = to_ref("init")
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
    @ui.page(page_path)
    def _():
        r_str = to_ref("old")
        rxui.label(r_str).classes("target")
        ui.button(
            "change",
            on_click=lambda: r_str.set_value("new"),
        ).classes("btn-change")

    page = browser.open(page_path)
    btn = page.Button(".btn-change")
    target = page.Label(".target")
    target.expect_to_have_text("old")

    btn.click()

    target.expect_to_have_text("new")


def test_bind_color(browser: BrowserManager, page_path: str):

    @ui.page(page_path)
    def _():
        r_color = to_ref("red")
        rxui.label("label").classes("target").bind_color(r_color)
        ui.button(
            "change",
            on_click=lambda: r_color.set_value("green"),
        ).classes("btn-change")

    page = browser.open(page_path)
    target = page.Label(".target")
    btn = page.Button(".btn-change")

    target.expect_to_have_style("color", "rgb(255, 0, 0)")

    btn.click()
    target.expect_to_have_style("color", "rgb(0, 128, 0)")
