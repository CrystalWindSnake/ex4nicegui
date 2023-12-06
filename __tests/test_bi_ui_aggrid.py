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
