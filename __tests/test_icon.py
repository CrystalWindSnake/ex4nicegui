from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_const_str(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.icon("home")

    page = browser.open(page_path)
    page.should_contain("home")


def test_ref_str(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_str = to_ref("home")
        rxui.icon(r_str)
        ui.button(
            "change",
            on_click=lambda: r_str.set_value("add"),
        ).classes("btn-change")

    page = browser.open(page_path)
    btn = page.Button(".btn-change")
    page.should_contain("home")

    btn.click()
    page.should_contain("add")


def test_color(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_color = to_ref("primary")
        rxui.icon("home", color=r_color).classes("target")
        ui.button(
            "change",
            on_click=lambda: r_color.set_value("rgba(224,52,52,1)"),
        ).classes("btn-change")

    page = browser.open(page_path)

    icon = page.Base(".target")
    btn = page.Button(".btn-change")

    icon.expect_to_have_style("color", "rgb(88, 152, 212)")

    btn.click()

    icon.expect_to_have_style("color", "rgb(224, 52, 52)")
