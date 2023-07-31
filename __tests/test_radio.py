import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from playwright.sync_api import expect

target_test_id = "radio"


def test_const_value(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.radio(["a", "b"]).props(f'data-testid="{target_test_id}"')

    page.open(page_path)

    radio = page.get_by_test_id(target_test_id)

    expect(radio).to_be_visible()

    assert not radio.get_by_label("a").is_checked()
    assert not radio.get_by_label("b").is_checked()

    page.wait()
    radio.get_by_label("a").check()
    assert radio.get_by_label("a").is_checked()
    assert not radio.get_by_label("b").is_checked()

    page.wait(2000)
    # page.click("text=b")
    radio.get_by_label("b").check(force=True)
    assert not radio.get_by_label("a").is_checked()
    assert radio.get_by_label("b").is_checked()


def test_ref_value(page: ScreenPage, page_path: str):
    r_value = to_ref("")

    @ui.page(page_path)
    def _():
        rxui.radio(["a", "b"], value=r_value).props(f'data-testid="{target_test_id}"')

    page.open(page_path)

    radio = page.get_by_test_id(target_test_id)

    expect(radio).to_be_visible()

    assert not radio.get_by_label("a").is_checked()
    assert not radio.get_by_label("b").is_checked()
    assert r_value.value == ""

    page.wait()
    radio.get_by_label("a").check()
    assert radio.get_by_label("a").is_checked()
    assert not radio.get_by_label("b").is_checked()
    assert r_value.value == "a"

    page.wait()
    radio.get_by_label("b").check(force=True)
    assert not radio.get_by_label("a").is_checked()
    assert radio.get_by_label("b").is_checked()
    assert r_value.value == "b"


def test_ref_str_change_value(page: ScreenPage, page_path: str):
    r_value = to_ref("")

    @ui.page(page_path)
    def _():
        rxui.radio(["a", "b"], value=r_value).props(f'data-testid="{target_test_id}"')

    page.open(page_path)

    radio = page.get_by_test_id(target_test_id)

    expect(radio).to_be_visible()

    page.wait()
    r_value.value = "a"

    radio.get_by_label("a").check()
    assert radio.get_by_label("a").is_checked()
    assert not radio.get_by_label("b").is_checked()

    page.wait()
    r_value.value = "b"
    radio.get_by_label("b").check()
    assert not radio.get_by_label("a").is_checked()
    assert radio.get_by_label("b").is_checked()
