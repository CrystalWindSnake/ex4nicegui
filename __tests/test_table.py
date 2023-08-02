import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, effect
from .screen import ScreenPage
from playwright.sync_api import expect
import pandas as pd


def test_const_value(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        data = pd.DataFrame({"name": ["a", "b", "c"], "age": [1, 2, 3]})

        rxui.table.from_pandas(data)

    page.open(page_path)

    for cell_value in ["name", "a", "b", "c"]:
        expect(
            page._page.get_by_role("cell", name=cell_value, exact=True)
        ).to_be_visible()


def test_ref_value(page: ScreenPage, page_path: str):
    data = to_ref(pd.DataFrame({"name": ["a", "b", "c"], "age": [1, 2, 3]}))

    @ui.page(page_path)
    def _():
        rxui.table.from_pandas(data)

    page.open(page_path)

    for cell_value in ["name", "a", "b", "c"]:
        expect(
            page._page.get_by_role("cell", name=cell_value, exact=True)
        ).to_be_visible()

    page.wait()
    data.value = pd.DataFrame({"new name": ["x", "y", "z"], "age": [1, 2, 3]})
    page.wait()

    for cell_value in ["name", "a", "b", "c"]:
        expect(
            page._page.get_by_role("cell", name=cell_value, exact=True)
        ).not_to_be_visible()

    for cell_value in ["new name", "x", "y", "z"]:
        expect(
            page._page.get_by_role("cell", name=cell_value, exact=True)
        ).to_be_visible()


def test_single_selection(page: ScreenPage, page_path: str):
    data = pd.DataFrame({"name": ["a", "b", "c"], "age": [1, 2, 3]})
    r_select = to_ref([])

    @ui.page(page_path)
    def _():
        r_table = rxui.table.from_pandas(data, selection="single", row_key="name")

        @effect
        def _():
            r_select.value = r_table.selection_ref.value

    page.open(page_path)

    page.wait()
    page._page.get_by_role("row", name="a 1").get_by_role("checkbox").click()
    page.wait()

    assert r_select.value == [{"name": "a", "age": 1}]

    page.wait()
    page._page.get_by_role("row", name="b 2").get_by_role("checkbox").click()
    page.wait()

    assert r_select.value == [{"name": "b", "age": 2}]


def test_multiple_selection(page: ScreenPage, page_path: str):
    data = pd.DataFrame({"name": ["a", "b", "c"], "age": [1, 2, 3]})
    r_select = to_ref([])

    @ui.page(page_path)
    def _():
        r_table = rxui.table.from_pandas(data, selection="multiple", row_key="name")

        @effect
        def _():
            r_select.value = r_table.selection_ref.value

    page.open(page_path)

    page.wait()
    page._page.get_by_role("row", name="a 1").get_by_role("checkbox").click()
    page._page.get_by_role("row", name="b 2").get_by_role("checkbox").click()
    page.wait()

    assert r_select.value == [{"name": "a", "age": 1}, {"name": "b", "age": 2}]


def test_columns_define(page: ScreenPage, page_path: str):
    data = pd.DataFrame({"name": ["a", "b", "c"], "age": [1, 2, 3]})

    @ui.page(page_path)
    def _():
        rxui.table.from_pandas(
            data,
            columns_define_fn=lambda col: {"style": "color:red"}
            if col == "name"
            else {},
        )

    page.open(page_path)

    # page.pause()
    style = page._page.get_by_role("cell", name="a", exact=True).get_attribute("style")
    assert style == "color: red;"

    style = page._page.get_by_role("cell", name="1", exact=True).get_attribute("style")
    assert style is None
