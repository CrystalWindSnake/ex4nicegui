import pytest
from nicegui import ui
from ex4nicegui import to_ref, on, effect, batch
from .screen import ScreenPage
from playwright.sync_api import expect
from .utils import SelectUtils, set_test_id


def test_on_priority_level():
    foo = to_ref("org")
    records = []

    @on(foo, onchanges=True, priority_level=2)
    def _():
        records.append("first")

    @on(foo, onchanges=True)
    def _():
        records.append("second")

    foo.value = "new"
    assert records == ["second", "first"]


def test_batch_event(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        set_test_id(rxui.select(["a", "b"], label="test select"), "target")

    page.open(page_path)
