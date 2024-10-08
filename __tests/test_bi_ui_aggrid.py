from nicegui import ui
from .screen import BrowserManager
import pandas as pd

from ex4nicegui import bi


def test_base(browser: BrowserManager, page_path: str):
    data = [
        ["f", 1],
        ["a", 2],
        ["c", 3],
        ["b", 1],
    ]

    @ui.page(page_path)
    def _():
        df = pd.DataFrame(data, columns=["name", "age"])

        source = bi.data_source(df)
        source.ui_aggrid().classes("target")

    page = browser.open(page_path)

    target = page.Aggrid(".target")
    target.expect_table_values(data)


def test_options_define(browser: BrowserManager, page_path: str):
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

        source = bi.data_source(df)
        source.ui_aggrid(
            options={
                "columnDefs": [
                    {"headerName": "xx", "field": "no exists"},
                    {"headerName": "new colA", "field": "colA"},
                    {
                        "field": "colC",
                        "cellClassRules": {
                            "bg-red-300": "x < 3",
                            "bg-green-300": "x >= 3",
                        },
                    },
                ],
                "rowData": [{"colX": [1, 2, 3, 4, 5]}],
            }
        ).classes("target")

    page = browser.open(page_path)

    target = page.Aggrid(".target")
    cells = target.get_cells()

    assert cells[2][2].evaluate("node => node.classList.contains('bg-red-300')")
    assert cells[4][2].evaluate("node => node.classList.contains('bg-green-300')")
