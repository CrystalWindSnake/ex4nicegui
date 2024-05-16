from nicegui import ui
from .screen import BrowserManager
import pandas as pd
from ex4nicegui import bi
from .utils import TableUtils


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        data = pd.DataFrame({"name": ["f", "a", "c", "b"], "age": [1, 2, 3, 1]})
        df = pd.DataFrame(data)

        source = bi.data_source(df)

        source.ui_table().classes("target")

    page = browser.open(page_path)

    target = TableUtils(page.locator(".target"))

    target.expect_cell_to_be_visible(list("facb"))


def test_columns_define(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        data = pd.DataFrame(
            {
                "colA": list("abcde"),
                "colB": [f"n{idx}" for idx in range(5)],
                "colC": list(range(5)),
            }
        )
        df = pd.DataFrame(data)

        ds = bi.data_source(df)
        ds.ui_table(
            columns=[
                {
                    "name": "xx",
                    "label": "xx",
                    "field": "no exists",
                    "required": True,
                },
                {"label": "new colA", "field": "colA", "sortable": True},
            ],
            rows=[
                {"name": "Alice", "age": 18},
                {"name": "Bob", "age": 21},
                {"name": "Carol"},
            ],
        ).classes("target")

    page = browser.open(page_path)

    target = TableUtils(page.locator(".target"))
    target.is_sortable("new colA")
