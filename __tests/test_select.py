import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, ref_computed
from .screen import ScreenPage
from playwright.sync_api import expect
from .utils import SelectUtils, set_test_id


def test_const_str(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        set_test_id(rxui.select(["a", "b"], label="test select"), "target")

    page.open(page_path)

    target = SelectUtils(page, "target")

    expect(target.page.get_by_text("test select", exact=True)).to_be_visible()


def test_ref_str(page: ScreenPage, page_path: str):
    r_str = to_ref("")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.select(["a", "b"], value=r_str), "target")

    page.open(page_path)
    target = SelectUtils(page, "target")

    expect(target.page.get_by_text("a", exact=True)).not_to_be_visible()
    expect(target.page.get_by_text("b", exact=True)).not_to_be_visible()

    page.wait()
    r_str.value = "a"
    expect(target.page.get_by_text("a", exact=True)).to_be_visible()

    page.wait()
    r_str.value = "b"
    expect(target.page.get_by_text("b", exact=True)).to_be_visible()

    page.wait()
    r_str.value = ""
    expect(target.page.get_by_text("a", exact=True)).not_to_be_visible()
    expect(target.page.get_by_text("b", exact=True)).not_to_be_visible()


def test_clearable(page: ScreenPage, page_path: str):
    r_str = to_ref("a")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.select(["a", "b"], value=r_str), "target").props("clearable")

    page.open(page_path)
    target = SelectUtils(page, "target")

    expect(target.page.get_by_text("a", exact=True)).to_be_visible()

    page.wait()
    target.click_cancel()

    expect(target.page.get_by_text("a", exact=True)).not_to_be_visible()
    expect(target.page.get_by_text("b", exact=True)).not_to_be_visible()
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
        set_test_id(rxui.select(cp_data, value=r_str), "target")

    page.open(page_path)
    target = SelectUtils(page, "target")

    page.wait()
    page._page.get_by_test_id("switch").locator("div").nth(2).click()

    target.click_and_select("a")

    page.wait()
    assert r_str.value == "a"


def test_multiple_list_opts(page: ScreenPage, page_path: str):
    r_value = to_ref(["a", "b"])

    @ui.page(page_path)
    def _():
        set_test_id(
            rxui.select(["a", "b", "c", "d"], value=r_value, multiple=True), "target"
        )

    page.open(page_path)
    target = SelectUtils(page, "target")

    assert target.get_input_value() == "a, b"

    page.wait()
    target.click_and_select("d")

    assert target.get_input_value() == "a, b, d"

    # page.wait()
    assert r_value.value == ["a", "b", "d"]


def test_multiple_dict_opts(page: ScreenPage, page_path: str):
    r_value = to_ref([1, 2])

    @ui.page(page_path)
    def _():
        set_test_id(
            rxui.select({1: "a", 2: "b", 3: "c", 4: "d"}, value=r_value, multiple=True),
            "target",
        )

    page.open(page_path)
    target = SelectUtils(page, "target")

    assert target.get_input_value() == "a, b"

    page.wait()
    target.click_and_select("d")

    assert target.get_input_value() == "a, b, d"

    # page.wait()
    assert r_value.value == [1, 2, 4]
