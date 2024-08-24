import pandas as pd
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager
from playwright.sync_api import expect


def test_aggrid(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.aggrid(
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
        ).classes("max-h-40 target")

    page = browser.open(page_path)

    expect(page.locator(".target")).to_be_visible()


def test_aggrid_from_dataframe(browser: BrowserManager, page_path: str):
    df = pd.DataFrame(
        {
            "date": pd.date_range("today", periods=4),
            "name": list("abcd"),
            "value": range(4),
        }
    )

    @ui.page(page_path)
    def _():
        r_df = to_ref(df)
        rxui.aggrid.from_pandas(r_df).classes("max-h-40 target")
        # test lambda display
        rxui.aggrid.from_pandas(lambda: r_df.value.head(2))

    page = browser.open(page_path)

    page.Aggrid(".target").expect_table_values(df.values.tolist())


def test_aggrid_from_dataframe_columns_define_fn(
    browser: BrowserManager, page_path: str
):
    df = pd.DataFrame({"name": list("abcd"), "value": range(4)})

    @ui.page(page_path)
    def _():
        r_df = to_ref(df)
        rxui.aggrid.from_pandas(
            r_df, columns_define_fn=lambda col: {"checkboxSelection": col == "name"}
        ).classes("max-h-40 target")

    page = browser.open(page_path)

    page.Aggrid(".target").expect_table_values(df.values.tolist())
