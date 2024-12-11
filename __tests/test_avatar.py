from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_display(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        icon = to_ref("home")
        rxui.avatar(icon).classes("target")

    page = browser.open(page_path)

    target = page.Base(".target")
    target.expect_to_have_text("home")


def test_change_icon(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        icon = to_ref("home")
        rxui.avatar(icon).classes("target")
        ui.button("change icon", on_click=lambda: icon.set_value("add")).classes("btn")

    page = browser.open(page_path)

    target = page.Base(".target")
    btn = page.Button(".btn")
    target.expect_to_have_text("home")

    btn.click()

    target.expect_to_have_text("add")


def test_bind_background_color(browser: BrowserManager, page_path: str):

    @ui.page(page_path)
    def _():
        bg_color = to_ref("red")
        rxui.avatar("home").classes("target").bind_color(bg_color)
        ui.button("change color", on_click=lambda: bg_color.set_value("green")).classes("btn")

    page = browser.open(page_path)
    target = page.Base(".target")
    btn = page.Button(".btn")

    # page.pause()
    target.expect_to_contain_class("bg-red")

    btn.click()
    target.expect_not_to_contain_class("bg-red")
    target.expect_to_contain_class("bg-green")


def test_bind_text_color(browser: BrowserManager, page_path: str):

    @ui.page(page_path)
    def _():
        text_color = to_ref("red")
        rxui.avatar("home").classes("target").bind_text_color(text_color)
        ui.button("change color", on_click=lambda: text_color.set_value("green")).classes("btn")

    page = browser.open(page_path)
    target = page.Base(".target")
    btn = page.Button(".btn")

    # page.pause()
    target.expect_to_contain_class("text-red")

    btn.click()
    target.expect_not_to_contain_class("text-red")
    target.expect_to_contain_class("text-green")
