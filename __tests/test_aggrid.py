import pandas as pd
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from playwright.sync_api import expect
from .utils import AggridUtils, set_test_id


def test_aggrid(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        table = rxui.aggird(
            {
                "columnDefs": [
                    {"headerName": "Name", "field": "name", "checkboxSelection": True},
                    {"headerName": "Age", "field": "age"},
                ],
                "rowData": [
                    {"name": "Alice", "age": 18},
                    {"name": "Bob", "age": 21},
                    {"name": "Carol", "age": 42},
                ],
                "rowSelection": "multiple",
            }
        ).classes("max-h-40")
        set_test_id(table, "target")

    page.open(page_path)

    expect(page._page.locator("css=[data-testid=target]")).to_be_visible()


def test_aggrid_from_dataframe(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        r_df = to_ref(pd.DataFrame({"name": list("abcd"), "value": range(4)}))
        table = rxui.aggird.from_pandas(r_df).classes("max-h-40")
        set_test_id(table, "target")

    page.open(page_path)

    table = AggridUtils(page, "target")
    table.expect_cell_to_be_visible(list("abcd"))


def test_aggrid_from_dataframe_columns_define_fn(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        r_df = to_ref(pd.DataFrame({"name": list("abcd"), "value": range(4)}))
        table = rxui.aggird.from_pandas(
            r_df, columns_define_fn=lambda col: {"checkboxSelection": col == "name"}
        ).classes("max-h-40")
        set_test_id(table, "target")

    page.open(page_path)

    table = AggridUtils(page, "target")
    table.expect_selection_cell_to_be_visible(list("abcd"))
