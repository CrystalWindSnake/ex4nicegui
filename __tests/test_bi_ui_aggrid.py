from nicegui import ui
from .screen import ScreenPage
import pandas as pd

from ex4nicegui import bi
from .utils import set_test_id, AggridUtils


def test_base(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        data = pd.DataFrame({"name": ["f", "a", "c", "b"], "age": [1, 2, 3, 1]})
        df = pd.DataFrame(data)

        source = bi.data_source(df)

        set_test_id(source.ui_aggrid(), "target")

    page.open(page_path)

    target = AggridUtils(page, "target")
    target.expect_cell_to_be_visible(list("facb"))


def test_options_define(page: ScreenPage, page_path: str):
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

        set_test_id(
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
            ),
            "target",
        )

    page.open(page_path)

    target = AggridUtils(page, "target")
    cells = target.get_cells()

    assert cells[2][2].evaluate("node => node.classList.contains('bg-red-300')")
    assert cells[4][2].evaluate("node => node.classList.contains('bg-green-300')")
