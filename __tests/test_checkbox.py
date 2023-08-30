import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from playwright.sync_api import expect

target_test_id = "checkbox"


def test_const_value(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.checkbox("test checkbox").props(f'data-testid="{target_test_id}"')

    page.open(page_path)

    target = page.get_by_test_id(target_test_id)

    expect(target).to_be_visible()

    assert not target.is_checked()

    page.wait()
    target.click()

    assert target.is_checked()


def test_ref_value(page: ScreenPage, page_path: str):
    r_value = to_ref(False)

    @ui.page(page_path)
    def _():
        rxui.checkbox("test checkbox", value=r_value).props(
            f'data-testid="{target_test_id}"'
        )

    page.open(page_path)

    target = page.get_by_test_id(target_test_id)

    expect(target).to_be_visible()

    assert not target.is_checked()
    assert r_value.value == False

    page.wait()
    target.click()

    assert r_value.value == True


def test_ref_str_change_value(page: ScreenPage, page_path: str):
    r_value = to_ref(False)

    @ui.page(page_path)
    def _():
        rxui.checkbox("test checkbox", value=r_value).props(
            f'data-testid="{target_test_id}"'
        )

    page.open(page_path)

    target = page.get_by_test_id(target_test_id)

    expect(target).to_be_visible()

    page.wait()
    r_value.value = True

    assert target.is_checked()
