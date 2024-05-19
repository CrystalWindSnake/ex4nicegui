from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, deep_ref
from .screen import BrowserManager
import pandas as pd


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        columns = deep_ref(
            [
                {
                    "name": "a",
                    "label": "a",
                    "field": "a",
                },
                {"name": "b", "label": "b", "field": "b"},
            ]
        )
        rows = deep_ref(
            [
                {"a": "n1", "b": 18},
                {"a": "n2", "b": 21},
            ]
        )
        rxui.table(columns, rows).classes("table")
        rxui.input(value=rxui.vmodel(rows.value[1]["a"])).classes("input_row2")
        rxui.input(value=rxui.vmodel(columns.value[0]["label"])).classes("col1_label")

        def onclick():
            rows.value.append(
                {"a": "n3"},
            )

        ui.button("change", on_click=onclick).classes("btn")

    page = browser.open(page_path)

    table = page.Table(".table")
    input_row2 = page.Input(".input_row2")
    col1_label = page.Input(".col1_label")
    btn = page.Button(".btn")

    table.expect_cell_to_be_visible(["a", "n1", "n2", "b", "18", "21"])

    input_row2.fill_text("new value")

    table.expect_cell_to_be_visible(["a", "n1", "new value", "b", "18", "21"])

    btn.click()
    table.expect_cell_to_be_visible(["a", "n1", "new value", "n3", "b", "18", "21"])

    col1_label.fill_text("new_col")
    table.expect_cell_to_be_visible(
        ["new_col", "n1", "new value", "n3", "b", "18", "21"]
    )


def test_should_can_use_vmodel(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        columns = deep_ref(
            [
                {
                    "name": "a",
                    "label": "a",
                    "field": "a",
                }
            ]
        )
        rows = deep_ref(
            [
                {"a": "n1"},
                {"a": "n2"},
            ]
        )
        rxui.table(columns, rxui.vmodel(rows)).classes("table")

        def onclick():
            rows.value.append(
                {"a": "n3"},
            )

        ui.button("change", on_click=onclick).classes("btn")

    page = browser.open(page_path)

    table = page.Table(".table")
    btn = page.Button(".btn")

    table.expect_cell_to_be_visible(["a", "n1", "n2"])

    btn.click()
    table.expect_cell_to_be_visible(["a", "n1", "n2", "n3"])


def test_from_pandas(browser: BrowserManager, page_path: str):
    data = to_ref(
        pd.DataFrame(
            {
                "date": pd.date_range("today", periods=3),
                "name": ["a", "b", "c"],
                "age": [1, 2, 3],
            }
        )
    )

    @ui.page(page_path)
    def _():
        rxui.table.from_pandas(data).classes("target")
        # test lambda display
        rxui.table.from_pandas(lambda: data.value.head(2))

    page = browser.open(page_path)

    target = page.Table(".target")

    target.expect_cell_to_be_visible(["name", "a", "b", "c"])

    data.value = pd.DataFrame({"new name": ["x", "y", "z"], "age": [1, 2, 3]})

    target.expect_cell_not_to_be_visible(["name", "a", "b", "c"])

    target.expect_cell_to_be_visible(["new name", "x", "y", "z"])


def test_single_selection(browser: BrowserManager, page_path: str):
    data = pd.DataFrame({"name": ["a", "b", "c"], "age": [1, 2, 3]})

    @ui.page(page_path)
    def _():
        table = rxui.table.from_pandas(
            data, selection="single", row_key="name"
        ).classes("target")
        rxui.label(table.selection_ref).classes("selection")

    page = browser.open(page_path)

    target = page.Table(".target")
    label = page.Label(".selection")

    target.click_checkbox(["a", 1])

    label.expect_contain_text("""[{'name': 'a', 'age': 1}]""")

    target.click_checkbox(["b", 2])

    label.expect_contain_text("""[{'name': 'b', 'age': 2}]""")


def test_multiple_selection(browser: BrowserManager, page_path: str):
    data = pd.DataFrame({"name": ["a", "b", "c"], "age": [1, 2, 3]})

    @ui.page(page_path)
    def _():
        table = rxui.table.from_pandas(
            data, selection="multiple", row_key="name"
        ).classes("target")
        rxui.label(table.selection_ref).classes("selection")

    page = browser.open(page_path)
    target = page.Table(".target")
    label = page.Label(".selection")

    target.click_checkbox(["a", 1])
    target.click_checkbox(["b", 2])

    label.expect_contain_text("""[{'name': 'a', 'age': 1}, {'name': 'b', 'age': 2}]""")


def test_columns_define(browser: BrowserManager, page_path: str):
    data = pd.DataFrame({"name": ["a", "b", "c"], "age": [1, 2, 3]})

    @ui.page(page_path)
    def _():
        rxui.table.from_pandas(
            data,
            columns_define_fn=lambda col: {"style": "color:red"}
            if col == "name"
            else {},
        ).classes("target")

    page = browser.open(page_path)

    target = page.Table(".target")
    target.expect_cell_style("a", "color", "rgb(255, 0, 0)")
