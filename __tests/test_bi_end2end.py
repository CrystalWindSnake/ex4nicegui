from nicegui import ui
from .screen import ScreenPage
import pandas as pd

from ex4nicegui import bi
from .utils import set_test_id
from . import utils as cp_utils


def test_remove_filters(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        df = pd.DataFrame(
            {
                "name": list("aabcd"),
                "cls": [
                    "c1",
                    "c2",
                    "c1",
                    "c1",
                    "c2",
                ],
                "value": range(5),
            }
        )

        source = bi.data_source(df)

        def onclick():
            source.remove_filters()

        set_test_id(ui.button("reload", on_click=onclick), "button")

        set_test_id(source.ui_select("name", multiple=False), "name select")
        set_test_id(source.ui_select("cls", multiple=False), "cls select")
        set_test_id(source.ui_radio("cls"), "cls radio")
        set_test_id(source.ui_range("value"), "value range")
        set_test_id(source.ui_slider("value"), "value slider")

        set_test_id(source.ui_aggrid(), "table1")

        #
        @bi.data_source
        def ds1():
            return source.filtered_data.head(3)

        set_test_id(ds1.ui_aggrid(), "table2")

    page.open(page_path)

    reset_btn = cp_utils.ButtonUtils(page, "button")

    name_select = cp_utils.SelectUtils(page, "name select")
    cls_select = cp_utils.SelectUtils(page, "cls select")

    table1 = cp_utils.AggridUtils(page, "table1")
    table2 = cp_utils.AggridUtils(page, "table2")

    name_select.click_and_select("a")
    page.wait()
    page._page.press("body", "Enter")
    cls_select.click()
    page.wait()

    assert cls_select.get_selection_values() == ["c1", "c2"]

    page.wait()
    page._page.press("body", "Enter")

    page.wait()
    name_select.click_cancel()
    page.wait()
    name_select.click_and_select("d")

    page.wait()
    cls_select.click()
    assert cls_select.get_selection_values() == ["c2"]

    assert len(table1.get_rows()) == 1
    assert len(table2.get_rows()) == 1

    reset_btn.click()

    assert len(table1.get_rows()) == 5
    assert len(table2.get_rows()) == 3
