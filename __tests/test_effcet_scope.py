import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, effect, on
from .screen import ScreenPage
from .utils import fn


def test_effect_cleanup_when_page_close(page: ScreenPage, page_path: str):
    other_page_path = f"{page_path}/other"
    value = to_ref("org")

    @fn
    def call():
        value.value

    @ui.page(page_path)
    def _():
        ui.link("to other page", other_page_path)
        effect(call)

    @ui.page(other_page_path)
    def _():
        ui.link("back to main", page_path)

    page.open(page_path)
    page.wait(1000)

    assert call.calledTimes == 1

    page._page.get_by_role("link", name="to other page").click()

    # must wait for background execution to clean up
    page.wait(4000)
    value.value = "new"

    assert call.calledTimes == 1


def test_on_cleanup_when_page_close(page: ScreenPage, page_path: str):
    other_page_path = f"{page_path}/other"
    value = to_ref("org")

    @fn
    def call():
        value.value

    @ui.page(page_path)
    def _():
        ui.link("to other page", other_page_path)
        on(value)(call)

    @ui.page(other_page_path)
    def _():
        ui.link("back to main", page_path)

    page.open(page_path)
    page.wait(1000)

    assert call.calledTimes == 1
    page._page.get_by_role("link", name="to other page").click()

    # must wait for background execution to clean up
    page.wait(4000)
    value.value = "new"
    assert call.calledTimes == 1
