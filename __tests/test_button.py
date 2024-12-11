from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_ref_text(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_text = to_ref("old text")
        rxui.button(r_text).props('data-testid="target"').props("no-caps").classes(
            "btn"
        )
        ui.button("change text").on_click(lambda: r_text.set_value("new text")).classes(
            "btn-change-text"
        )

    page = browser.open(page_path)

    btn = page.Button(".btn")
    btn_change_text = page.Button(".btn-change-text")

    btn.expect_to_have_text("old text")

    btn_change_text.click()
    btn.expect_to_have_text(text="new text")


def test_enabled(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_num = to_ref(0)
        rxui.button("").bind_enabled(lambda: r_num.value % 2 == 0).classes("btn")
        ui.button("change num").on_click(lambda: r_num.set_value(1)).classes(
            "btn-change-num"
        )

    page = browser.open(page_path)
    btn = page.Button(".btn")
    btn_change_num = page.Button(".btn-change-num")

    btn.expect.to_be_enabled()

    btn_change_num.click()

    btn.expect.not_to_be_enabled()
