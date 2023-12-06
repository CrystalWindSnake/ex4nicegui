from nicegui import ui
from .screen import ScreenPage
import pandas as pd

from ex4nicegui import bi
from .utils import set_test_id
from . import utils as cp_utils
from pyecharts.charts import Bar


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

        @source.ui_echarts
        def bar(data: pd.DataFrame):
            c = (
                Bar()
                .add_xaxis(data["name"].tolist())
                .add_yaxis("value", data["value"].tolist())
            )

            return c

        bar.classes("w-[50vw]")
        set_test_id(bar, "echart bar")

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
    cls_radio = cp_utils.RadioUtils(page, "cls radio")

    bar_chart = cp_utils.EChartsUtils(page, "echart bar")

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

    assert cls_radio.get_all_labels() == ["c2"]

    assert bar_chart.get_options()["series"][0]["data"] == [4]

    assert len(table1.get_rows()) == 1
    assert len(table2.get_rows()) == 1

    reset_btn.click()

    assert cls_radio.get_all_labels() == ["c1", "c2"]

    assert bar_chart.get_options()["series"][0]["data"] == [0, 1, 2, 3, 4]

    assert len(table1.get_rows()) == 5
    assert len(table2.get_rows()) == 3


def test_reload_source(page: ScreenPage, page_path: str):
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

        ds1 = bi.data_source(df)

        df1 = pd.DataFrame(
            {
                "name": list("xxmny"),
                "cls": [
                    "cls1",
                    "cls2",
                    "cls1",
                    "cls1",
                    "cls2",
                ],
                "value": range(5),
                "value1": range(100, 105),
            }
        )

        @bi.data_source
        def ds2():
            return ds1.filtered_data.head(3)

        def onclick():
            ds1.reload(df1)

        set_test_id(ui.button("reload", on_click=onclick), "button")

        set_test_id(ds1.ui_select("name", multiple=False), "name select")
        set_test_id(ds1.ui_select("cls", multiple=False), "cls select")

        set_test_id(
            ds1.ui_radio(
                "name", hide_filtered=True, custom_options_map={"": "null", "c1": "类别1"}
            ),
            "name radio",
        )

        set_test_id(
            ds1.ui_radio(
                "cls",
                hide_filtered=False,
                custom_options_map={"": "null", "c1": "类别1", "cls1": "new 类别1"},
            ),
            "cls radio",
        )

        set_test_id(ds1.ui_aggrid(), "table1")

        set_test_id(ds2.ui_aggrid(), "table2")

    page.open(page_path)

    reset_btn = cp_utils.ButtonUtils(page, "button")

    name_select = cp_utils.SelectUtils(page, "name select")
    cls_select = cp_utils.SelectUtils(page, "cls select")

    name_radio = cp_utils.RadioUtils(page, "name radio")
    cls_radio = cp_utils.RadioUtils(page, "cls radio")

    table1 = cp_utils.AggridUtils(page, "table1")
    table2 = cp_utils.AggridUtils(page, "table2")

    name_select.click_and_select("a")
    page.wait()

    except_data = [
        ["a", "c1", "0"],
        ["a", "c2", "1"],
    ]

    assert table1.get_data() == except_data
    assert table2.get_data() == except_data

    assert name_radio.get_all_labels() == ["a"]
    assert cls_radio.get_all_labels() == ["类别1", "c2"]

    # reload
    reset_btn.click()

    except_all_data = [
        ["x", "cls1", "0", "100"],
        ["x", "cls2", "1", "101"],
        ["m", "cls1", "2", "102"],
        ["n", "cls1", "3", "103"],
        ["y", "cls2", "4", "104"],
    ]

    assert table1.get_data() == except_all_data
    assert table2.get_data() == except_all_data[:3]

    assert name_radio.get_all_labels() == ["x", "m", "n", "y"]
    assert cls_radio.get_all_labels() == ["new 类别1", "cls2"]

    #
    name_select.click_and_select("x")
    page.wait()

    except_data = [
        ["x", "cls1", "0", "100"],
        ["x", "cls2", "1", "101"],
    ]

    assert table1.get_data() == except_data
    assert table2.get_data() == except_data

    assert name_radio.get_all_labels() == ["x"]
    assert cls_radio.get_all_labels() == ["new 类别1", "cls2"]
