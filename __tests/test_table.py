from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, effect, deep_ref
from .screen import ScreenPage
import pandas as pd
from .utils import TableUtils, set_test_id, InputUtils, ButtonUtils


def test_base(page: ScreenPage, page_path: str):
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
        set_test_id(rxui.table(columns, rows), "table")
        set_test_id(rxui.input(value=rxui.vmodel(rows.value[1]["a"])), "input_row2")
        set_test_id(
            rxui.input(value=rxui.vmodel(columns.value[0]["label"])), "col1_label"
        )

        def onclick():
            rows.value.append(
                {"a": "n3"},
            )

        set_test_id(ui.button("change", on_click=onclick), "btn")

    page.open(page_path)

    table = TableUtils(page, "table")
    input_row2 = InputUtils(page, "input_row2")
    col1_label = InputUtils(page, "col1_label")
    btn = ButtonUtils(page, "btn")

    table.expect_cell_to_be_visible(["a", "n1", "n2", "b", "18", "21"])

    input_row2.fill_text("new value")

    table.expect_cell_to_be_visible(["a", "n1", "new value", "b", "18", "21"])

    btn.click()
    table.expect_cell_to_be_visible(["a", "n1", "new value", "n3", "b", "18", "21"])

    col1_label.fill_text("new_col")
    table.expect_cell_to_be_visible(
        ["new_col", "n1", "new value", "n3", "b", "18", "21"]
    )


def test_should_can_use_vmodel(page: ScreenPage, page_path: str):
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
        set_test_id(rxui.table(columns, rxui.vmodel(rows)), "table")

        def onclick():
            rows.value.append(
                {"a": "n3"},
            )

        set_test_id(ui.button("change", on_click=onclick), "btn")

    page.open(page_path)

    table = TableUtils(page, "table")
    btn = ButtonUtils(page, "btn")

    table.expect_cell_to_be_visible(["a", "n1", "n2"])

    btn.click()
    table.expect_cell_to_be_visible(["a", "n1", "n2", "n3"])


def test_from_pandas(page: ScreenPage, page_path: str):
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
        set_test_id(rxui.table.from_pandas(data), "target")
        # test lambda display
        rxui.table.from_pandas(lambda: data.value.head(2))

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
