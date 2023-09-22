import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage


class Uilts:
    def __init__(self, page: ScreenPage, testid="target"):
        self.page = page
        self.testid = testid

    def assert_button_text(self, text: str):
        assert self.page.get_by_test_id(self.testid).inner_text() == text


def test_ref_text(page: ScreenPage, page_path: str):
    r_text = to_ref("old text")

    @ui.page(page_path)
    def _():
        rxui.button(r_text).props('data-testid="target"').props("no-caps")

    page.open(page_path)

    utils = Uilts(page)

    page.wait()
    utils.assert_button_text(text="old text")

    r_text.value = "new text"
    page.wait()
    utils.assert_button_text(text="new text")
