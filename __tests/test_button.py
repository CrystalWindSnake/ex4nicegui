from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_ref_text(browser: BrowserManager, page_path: str):
    r_text = to_ref("old text")

    @ui.page(page_path)
    def _():
        rxui.button(r_text).props('data-testid="target"').props("no-caps").classes(
            "btn"
        )

    page = browser.open(page_path)

    btn = page.Button(".btn")

    btn.expect_to_have_text("old text")

    r_text.value = "new text"
    btn.expect_to_have_text(text="new text")


def test_enabled(browser: BrowserManager, page_path: str):
    r_num = to_ref(0)

    @ui.page(page_path)
    def _():
        rxui.button("").bind_enabled(lambda: r_num.value % 2 == 0).classes("btn")

    page = browser.open(page_path)
    btn = page.Button(".btn")

    btn.expect.to_be_enabled()

    r_num.value = 1

    btn.expect.not_to_be_enabled()
