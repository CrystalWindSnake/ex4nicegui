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
    r_str = to_ref("home")

    @ui.page(page_path)
    def _():
        rxui.icon(r_str)

    page = browser.open(page_path)
    page.should_contain("home")

    r_str.value = "add"
    page.should_contain("add")


def test_color(browser: BrowserManager, page_path: str):
    r_color = to_ref("primary")

    @ui.page(page_path)
    def _():
        rxui.icon("home", color=r_color).classes("target")

    page = browser.open(page_path)

    icon = page.Base(".target")

    icon.expect_to_have_style("color", "rgb(88, 152, 212)")

    r_color.value = "rgba(224,52,52,1)"

    icon.expect_to_have_style("color", "rgb(224, 52, 52)")
