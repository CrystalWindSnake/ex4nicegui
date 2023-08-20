import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, ref_computed
from .screen import ScreenPage
from playwright.sync_api import expect


def test_const_str(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.select(["a", "b"], label="test select").props('data-testid="target"')

    page.open(page_path)

    target = page.get_by_test_id("target")

    expect(target.page.get_by_text("test select", exact=True)).to_be_visible()

    # page.should_contain_text("target", "test select")


def test_ref_str(page: ScreenPage, page_path: str):
    r_str = to_ref("")

    @ui.page(page_path)
    def _():
        rxui.select(["a", "b"], value=r_str).props('data-testid="target"')

    page.open(page_path)
    expect(page._page.get_by_text("a", exact=True)).not_to_be_visible()
    expect(page._page.get_by_text("b", exact=True)).not_to_be_visible()

    page.wait()
    r_str.value = "a"
    expect(page._page.get_by_text("a", exact=True)).to_be_visible()

    page.wait()
    r_str.value = "b"
    expect(page._page.get_by_text("b", exact=True)).to_be_visible()

    page.wait()
    r_str.value = ""
    expect(page._page.get_by_text("a", exact=True)).not_to_be_visible()
    expect(page._page.get_by_text("b", exact=True)).not_to_be_visible()


def test_clearable(page: ScreenPage, page_path: str):
    r_str = to_ref("a")

    @ui.page(page_path)
    def _():
        rxui.select(["a", "b"], value=r_str).props('data-testid="target" clearable')

    page.open(page_path)

    expect(page._page.get_by_text("a", exact=True)).to_be_visible()

    page.wait()
    page._page.get_by_role("button", name="cancel").click()

    expect(page._page.get_by_text("a", exact=True)).not_to_be_visible()
    expect(page._page.get_by_text("b", exact=True)).not_to_be_visible()
    assert r_str.value == ""


def test_option_change(page: ScreenPage, page_path: str):
    r_str = to_ref("")
    r_has_data = to_ref(False)

    @ref_computed
    def cp_data():
        if r_has_data.value:
            return ["a", "b"]
        return []

    @ui.page(page_path)
    def _():
        rxui.switch("has data", value=r_has_data).props('data-testid="switch"')
        rxui.select(cp_data, value=r_str).props('data-testid="target"')

    page.open(page_path)

    page.wait()
    page._page.get_by_test_id("switch").locator("div").nth(2).click()

    # page.wait()
    page._page.get_by_text("arrow_drop_down").click()

    # page.wait()
    page._page.get_by_role("option", name="a").locator("div").nth(2).click()

    page.wait()
    assert r_str.value == "a"
