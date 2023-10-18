import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, effect
from .screen import ScreenPage
from playwright.sync_api import expect
import pandas as pd
from .utils import TableUtils, set_test_id


def test_const_value(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        data = pd.DataFrame({"name": ["a", "b", "c"], "age": [1, 2, 3]})
        set_test_id(rxui.table.from_pandas(data), "target")

    page.open(page_path)

    target = TableUtils(page, "target")

    target.expect_cell_to_be_visible(["name", "a", "b", "c"])


def test_ref_value(page: ScreenPage, page_path: str):
    data = to_ref(pd.DataFrame({"name": ["a", "b", "c"], "age": [1, 2, 3]}))

    @ui.page(page_path)
    def _():
        set_test_id(rxui.table.from_pandas(data), "target")

    page.open(page_path)

    target = TableUtils(page, "target")

    target.expect_cell_to_be_visible(["name", "a", "b", "c"])

    page.wait()
    data.value = pd.DataFrame({"new name": ["x", "y", "z"], "age": [1, 2, 3]})
    page.wait()

    target.expect_cell_not_to_be_visible(["name", "a", "b", "c"])

    target.expect_cell_to_be_visible(["new name", "x", "y", "z"])


def test_selection_ref(page: ScreenPage, page_path: str):
    data = pd.DataFrame({"name": ["a", "b", "c"], "age": [1, 2, 3]})

    r_table: rxui.table = None  # type: ignore

    @ui.page(page_path)
    def _():
        nonlocal r_table
        r_table = rxui.table.from_pandas(data, selection="single", row_key="name")
        set_test_id(r_table, "target")

    page.open(page_path)

    assert r_table

    target = TableUtils(page, "target")

    page.wait()
    target.click_checkbox(["a", 1])
    page.wait()

    assert r_table.selection_ref.value == [{"name": "a", "age": 1}]


def test_single_selection(page: ScreenPage, page_path: str):
    data = pd.DataFrame({"name": ["a", "b", "c"], "age": [1, 2, 3]})
    r_select = to_ref([])

    @ui.page(page_path)
    def _():
        r_table = rxui.table.from_pandas(data, selection="single", row_key="name")
        set_test_id(r_table, "target")

        @effect
        def _():
            r_select.value = r_table.selection_ref.value

    page.open(page_path)

    target = TableUtils(page, "target")

    page.wait()
    target.click_checkbox(["a", 1])
    page.wait()

    assert r_select.value == [{"name": "a", "age": 1}]

    page.wait()
    target.click_checkbox(["b", 2])
    page.wait()

    assert r_select.value == [{"name": "b", "age": 2}]


def test_multiple_selection(page: ScreenPage, page_path: str):
    data = pd.DataFrame({"name": ["a", "b", "c"], "age": [1, 2, 3]})
    r_select = to_ref([])

    @ui.page(page_path)
    def _():
        r_table = rxui.table.from_pandas(data, selection="multiple", row_key="name")
        set_test_id(r_table, "target")

        @effect
        def _():
            r_select.value = r_table.selection_ref.value

    page.open(page_path)
    target = TableUtils(page, "target")

    page.wait()
    target.click_checkbox(["a", 1])
    target.click_checkbox(["b", 2])
    page.wait()

    assert r_select.value == [{"name": "a", "age": 1}, {"name": "b", "age": 2}]


def test_columns_define(page: ScreenPage, page_path: str):
    data = pd.DataFrame({"name": ["a", "b", "c"], "age": [1, 2, 3]})

    @ui.page(page_path)
    def _():
        r_table = rxui.table.from_pandas(
            data,
            columns_define_fn=lambda col: {"style": "color:red"}
            if col == "name"
            else {},
        )
        set_test_id(r_table, "target")

    page.open(page_path)

    target = TableUtils(page, "target")

    assert target.get_cell_style("a") == "color: red;"

    assert target.get_cell_style("1") is None
