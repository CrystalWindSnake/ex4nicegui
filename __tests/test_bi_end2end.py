from nicegui import ui
from .screen import BrowserManager
import pandas as pd

from ex4nicegui import bi
from pyecharts.charts import Bar


def test_remove_filters(browser: BrowserManager, page_path: str):
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

        ui.button("remove filters", on_click=source.remove_filters).classes(
            "remove-filters"
        )

        source.ui_select("name", multiple=False).classes("name-select")

        source.ui_select("cls", multiple=False).classes("cls-select")

        source.ui_radio("cls").classes("cls-radio")

        source.ui_range("value").classes("value-range")
        source.ui_slider("value").classes("value-slider")

        @source.ui_echarts
        def bar(data: pd.DataFrame):
            c = (
                Bar()
                .add_xaxis(data["name"].tolist())
                .add_yaxis("value", data["value"].tolist())
            )

            return c

        bar.classes("w-[50vw] echart-bar")

        source.ui_aggrid().classes("table1")

        #
        @bi.data_source
        def ds1():
            return source.filtered_data.head(3)

        ds1.ui_aggrid().classes("table2")

    page = browser.open(page_path)

    remove_filters_btn = page.Button(".remove-filters")
    name_select = page.Select(".name-select")
    cls_select = page.Select(".cls-select")
    cls_radio = page.Radio(".cls-radio")
    bar_chart = page.ECharts(".echart-bar")
    table1 = page.Aggrid(".table1")
    table2 = page.Aggrid(".table2")

    # page.pause()
    name_select.click_and_select("a")

    cls_select.show_popup_click()
    assert cls_select.get_options_values() == ["c1", "c2"]

    page.press("body", "Enter")

    name_select.click_cancel()
    name_select.click_and_select("d")

    cls_select.show_popup_click()
    assert cls_select.get_options_values() == ["c2"]

    assert cls_radio.get_all_labels() == ["c2"]

    assert bar_chart.get_options()["series"][0]["data"] == [4]

    assert len(table1.get_rows()) == 1
    assert len(table2.get_rows()) == 1

    remove_filters_btn.click()

    assert cls_radio.get_all_labels() == ["c1", "c2"]

    assert bar_chart.get_options()["series"][0]["data"] == [0, 1, 2, 3, 4]

    assert len(table1.get_rows()) == 5
    assert len(table2.get_rows()) == 3


def test_reload_source(browser: BrowserManager, page_path: str):
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

        ui.button("reload", on_click=lambda: ds1.reload(df1)).classes("reload-btn")

        ds1.ui_select("name", multiple=False).classes("name-select")
        ds1.ui_select("cls", multiple=False).classes("cls-select")
        ds1.ui_radio(
            "name",
            hide_filtered=True,
            custom_options_map={"": "null", "c1": "类别1"},
        ).classes("name-radio")

        ds1.ui_radio(
            "cls",
            hide_filtered=False,
            custom_options_map={"": "null", "c1": "类别1", "cls1": "new 类别1"},
        ).classes("cls-radio")

        ds1.ui_aggrid().classes("table1")
        ds2.ui_aggrid().classes("table2")

    page = browser.open(page_path)

    reload_btn = page.Button(".reload-btn")
    name_select = page.Select(".name-select")
    # cls_select = page.Select(".cls-select")
    name_radio = page.Radio(".name-radio")
    cls_radio = page.Radio(".cls-radio")
    table1 = page.Aggrid(".table1")
    table2 = page.Aggrid(".table2")

    name_select.click_and_select("a")

    except_data = [
        ["a", "c1", "0"],
        ["a", "c2", "1"],
    ]

    assert table1.get_data() == except_data
    assert table2.get_data() == except_data

    assert name_radio.get_all_labels() == ["a"]
    assert cls_radio.get_all_labels() == ["类别1", "c2"]

    # reload
    reload_btn.click()

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

    except_data = [
        ["x", "cls1", "0", "100"],
        ["x", "cls2", "1", "101"],
    ]

    assert table1.get_data() == except_data
    assert table2.get_data() == except_data

    assert name_radio.get_all_labels() == ["x"]
    assert cls_radio.get_all_labels() == ["new 类别1", "cls2"]
