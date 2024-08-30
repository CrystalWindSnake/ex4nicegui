from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_display(browser: BrowserManager, page_path: str):
    icon = to_ref("home")

    @ui.page(page_path)
    def _():
        rxui.avatar(icon).classes("target")

    page = browser.open(page_path)

    target = page.Base(".target")
    target.expect_to_have_text("home")


def test_change_icon(browser: BrowserManager, page_path: str):
    icon = to_ref("home")

    @ui.page(page_path)
    def _():
        rxui.avatar(icon).classes("target")

    page = browser.open(page_path)

    target = page.Base(".target")
    target.expect_to_have_text("home")

    icon.value = "add"

    target.expect_to_have_text("add")


def test_bind_background_color(browser: BrowserManager, page_path: str):
    bg_color = to_ref("red")

    @ui.page(page_path)
    def _():
        rxui.avatar("home").classes("target").bind_color(bg_color)

    page = browser.open(page_path)
    target = page.Base(".target")

    # page.pause()
    target.expect_to_contain_class("bg-red")

    bg_color.value = "green"
    target.expect_not_to_contain_class("bg-red")
    target.expect_to_contain_class("bg-green")


def test_bind_text_color(browser: BrowserManager, page_path: str):
    text_color = to_ref("red")

    @ui.page(page_path)
    def _():
        rxui.avatar("home").classes("target").bind_text_color(text_color)

    page = browser.open(page_path)
    target = page.Base(".target")

    # page.pause()
    target.expect_to_contain_class("text-red")

    text_color.value = "green"
    target.expect_not_to_contain_class("text-red")
    target.expect_to_contain_class("text-green")
