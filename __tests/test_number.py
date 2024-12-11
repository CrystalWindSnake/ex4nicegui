from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_const(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.number(value=1.0).classes("target")

    page = browser.open(page_path)

    target = page.Number(".target")

    target.expect_to_have_text("1")


def test_ref(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_value = to_ref(1.0)
        rxui.number(value=r_value).classes("target")
        rxui.label(text=r_value).classes("label")
        ui.button(
            "change",
            on_click=lambda: r_value.set_value(3.11),
        ).classes("btn-change")

    page = browser.open(page_path)
    btn = page.Button(".btn-change")
    target = page.Number(".target")
    label = page.Label(".label")

    target.expect_to_have_text("1")

    btn.click()
    target.expect_to_have_text("3.11")

    # type input number
    target.input_text("66")
    label.expect_to_have_text("3.1166")

    # type replace
    target.click()
    target.dbclick()
    target.input_text("66")
    label.expect_to_have_text("66.0")

    # should_return_none_when_empty
    target.clear_text()
    label.expect_to_have_text("None")


def test_on_change(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        def on_change(e):
            label.set_text(e.value)

        label = ui.label("").classes("label")
        rxui.number(format="%.2f", step=0.1, on_change=on_change).classes("target")

    page = browser.open(page_path)

    target = page.Number(".target")
    label = page.Label(".label")

    target.fill_text("1111")
    label.expect_to_have_text("1111")


def test_with_format(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.number(format="%.2f", step=0.1).classes("target")

    page = browser.open(page_path)

    target = page.Number(".target")

    target.input_text("1111")
    target.expect_to_have_text("1111")


def test_precision(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        value = to_ref(3.14159265359)
        precision = to_ref(5)
        rxui.number(value=value, precision=precision).classes("target")
        rxui.button("change", on_click=lambda: precision.set_value(2)).classes(
            "btn-change"
        )

    page = browser.open(page_path)

    target = page.Number(".target")
    btn = page.Button(".btn-change")

    target.expect_to_have_text("3.14159265359")

    btn.click()
    target.expect_to_have_text("3.14")
