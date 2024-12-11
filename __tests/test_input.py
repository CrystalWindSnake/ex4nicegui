from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_display(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_str = to_ref("ref value")
        rxui.input(value="const value").classes("const-input")
        rxui.input(value=r_str).classes("ref-input")
        ui.button(
            "change",
            on_click=lambda: r_str.set_value("new"),
        ).classes("btn-change")

    page = browser.open(page_path)
    target_const = page.Input(".const-input")
    btn_change = page.Button(".btn-change")
    target_const.expect_to_have_text("const value")

    target_ref = page.Input(".ref-input")
    target_ref.expect_to_have_text("ref value")

    btn_change.click()
    target_ref.expect_to_have_text("new")


def test_input_change_value(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_str = to_ref("old")
        dummy = ""

        def onchange():
            nonlocal dummy
            dummy = r_str.value

        rxui.input(value=r_str, on_change=onchange).classes("input")
        rxui.label(r_str).classes("label")

    page = browser.open(page_path)
    input = page.Input(".input")
    label = page.Label(".label")

    input.fill_text("new value")

    label.expect_to_have_text("new value")


def test_autocomplete(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        autocomplete_options = {
            0: ["apple", "ant", "apricot"],
            1: ["banana", "boat", "bar"],
        }

        text = to_ref("")
        ac_selected = to_ref(0)

        def autocomplete():
            return autocomplete_options[ac_selected.value]

        rxui.radio(list(autocomplete_options.keys()), value=ac_selected).classes(
            "radio"
        )
        rxui.input(value=text, autocomplete=autocomplete).classes("input")

    page = browser.open(page_path)
    radio = page.Radio(".radio")
    input = page.Input(".input")

    input.fill_text("a")
    input.expect_autocomplete_text(inputed_text="a", tips_text="pple")

    radio.check_by_label("1")
    input.fill_text("b")
    input.expect_autocomplete_text(inputed_text="b", tips_text="anana")

    input.fill_text("bo")
    input.expect_autocomplete_text(inputed_text="bo", tips_text="at")
