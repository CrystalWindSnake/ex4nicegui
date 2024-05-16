from nicegui import ui
from .screen import BrowserManager
import pandas as pd

from ex4nicegui import bi
from .utils import SelectUtils, set_test_id, AggridUtils


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        data = [
            ("L1_A", "L2_M_1", "L3_Z_1", 1),
            ("L1_A", "L2_M_1", "L3_Z_2", 2),
            ("L1_A", "L2_M_2", "L3_Z_3", 3),
            ("L1_B", "L2_M_3", "L3_Z_4", 4),
            ("L1_B", "L2_M_3", "L3_Z_5", 5),
            ("L1_B", "L2_M_3", "L3_Z_6", 6),
            ("L1_B", "L2_M_4", "L3_Z_7", 7),
        ]

        columns = ["level1", "level2", "level3", "value"]

        df = pd.DataFrame(data, columns=columns)

        source = bi.data_source(df)

        source.ui_select("level1").classes("target1")
        source.ui_select("level2").classes("target2")
        source.ui_select("level3").classes("target3")

    page = browser.open(page_path)

    target1 = SelectUtils(page.locator(".target1"), page)
    target2 = SelectUtils(page.locator(".target2"), page)
    target3 = SelectUtils(page.locator(".target3"), page)

    target1.show_popup_click()
    menu_items = target1.get_options_values()
    assert menu_items == ["L1_A", "L1_B"]
    target1.click()

    target2.show_popup_click()
    menu_items = target2.get_options_values()
    assert menu_items == ["L2_M_1", "L2_M_2", "L2_M_3", "L2_M_4"]
    target2.click()

    target3.show_popup_click()
    menu_items = target3.get_options_values()
    assert menu_items == [f"L3_Z_{n}" for n in range(1, 8)]
    target3.click()


def test_sort_options(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        data = pd.DataFrame(
            {
                "name": list("aabcdf"),
                "cls": ["c1", "c2", "c1", "c1", "c3", None],
                "value": range(6),
            }
        )
        source = bi.data_source(data)
        source.ui_select("name", sort_options={"cls": "asc", "value": "desc"}).classes(
            "target"
        )

    page = browser.open(page_path)

    target = SelectUtils(page.locator(".target"), page)

    target.show_popup_click()
    menu_items = target.get_options_values()
    assert menu_items == ["c", "b", "a", "d", "f"]


def test_null_options(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        data = pd.DataFrame(
            {
                "name": list("aabcdf"),
                "cls": ["c1", "c2", "c1", "c1", "c3", None],
                "value": range(6),
            }
        )
        source = bi.data_source(data)
        source.ui_select("cls").classes("target1")
        source.ui_select("cls", exclude_null_value=True).classes("target2")

    page = browser.open(page_path)

    # target1
    target1 = SelectUtils(page.locator(".target1"), page)

    target1.show_popup_click()
    menu_items = target1.get_options_values()
    assert menu_items == ["c1", "c2", "c3", ""]

    # target2
    target2 = SelectUtils(page.locator(".target2"), page)

    page.press("body", "Enter")

    target2.show_popup_click()
    menu_items = target2.get_options_values()
    assert menu_items == ["c1", "c2", "c3"]


def test_default_value(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        data = pd.DataFrame(
            {
                "name": list("aabcdf"),
                "cls": ["c1", "c2", "c1", "c1", "c3", None],
                "value": range(6),
            }
        )
        ds = bi.data_source(data)

        @bi.data_source
        def ds1():
            df = ds.filtered_data.copy()
            df["value"] = df["value"] * 100
            return df

        ds.ui_select("name", value=["a", "b"]).classes("name-select")
        ds.ui_select("cls", multiple=False, value="c1").classes("cls-select")
        ds.ui_aggrid().classes("table")
        ds1.ui_aggrid().classes("table1")

    page = browser.open(page_path)

    name_select = SelectUtils(page.locator(".name-select"), page)
    cls_select = SelectUtils(page.locator(".cls-select"), page)
    table = AggridUtils(page.locator(".table"))
    table1 = AggridUtils(page.locator(".table1"))

    assert name_select.get_selected_values() == ["a", "b"]
    assert cls_select.get_selected_values() == ["c1"]

    assert table.get_data() == [
        ["a", "c1", "0"],
        ["b", "c1", "2"],
    ]

    assert table1.get_data() == [
        ["a", "c1", "0"],
        ["b", "c1", "200"],
    ]


def test_update_options(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        df = pd.DataFrame(
            {
                "cls1": [
                    "x1",
                    "x1",
                    "x1",
                    "x2",
                    "x2",
                    "x2",
                ],
                "cls2": ["a", "b", "c", "c", "b", "a"],
            }
        )
        ds = bi.data_source(df)
        ds.ui_select("cls1", value="x1", multiple=False).classes("min-w-[20ch] cls1")

        ds.ui_select("cls2", clearable=False).classes("min-w-[20ch] cls2")

    page = browser.open(page_path)

    cls1_select = SelectUtils(page.locator(".cls1"), page)
    cls2_select = SelectUtils(page.locator(".cls2"), page)

    cls2_select.click_and_select("a")
    cls1_select.click_and_select("x2")
    cls2_select.click_and_select("a")
    assert cls2_select.get_selected_values() == []
