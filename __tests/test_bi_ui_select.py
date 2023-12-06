from nicegui import ui
from .screen import ScreenPage
import pandas as pd

from ex4nicegui import bi
from .utils import SelectUtils, set_test_id, AggridUtils


def test_base(page: ScreenPage, page_path: str):
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

        set_test_id(source.ui_select("level1"), "target1")
        set_test_id(source.ui_select("level2"), "target2")
        set_test_id(source.ui_select("level3"), "target3")

    page.open(page_path)

    target1 = SelectUtils(page, "target1")
    target2 = SelectUtils(page, "target2")
    target3 = SelectUtils(page, "target3")

    target1.click()
    page.wait()
    menu_items = target1.get_options_values()
    assert menu_items == ["L1_A", "L1_B"]
    target1.click()

    target2.click()
    page.wait()
    menu_items = target2.get_options_values()
    assert menu_items == ["L2_M_1", "L2_M_2", "L2_M_3", "L2_M_4"]
    target2.click()

    target3.click()
    page.wait()
    menu_items = target3.get_options_values()
    assert menu_items == [f"L3_Z_{n}" for n in range(1, 8)]
    target3.click()


def test_sort_options(page: ScreenPage, page_path: str):
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

        set_test_id(
            source.ui_select("name", sort_options={"cls": "asc", "value": "desc"}),
            "target",
        )

    page.open(page_path)

    target = SelectUtils(page, "target")

    target.click()
    page.wait()
    menu_items = target.get_options_values()
    assert menu_items == ["c", "b", "a", "d", "f"]


def test_null_options(page: ScreenPage, page_path: str):
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

        set_test_id(
            source.ui_select("cls"),
            "target1",
        )

        set_test_id(
            source.ui_select("cls", exclude_null_value=True),
            "target2",
        )

    page.open(page_path)

    # target1
    target1 = SelectUtils(page, "target1")

    target1.click()
    page.wait()
    menu_items = target1.get_options_values()
    assert menu_items == ["c1", "c2", "c3", ""]

    # target2
    target2 = SelectUtils(page, "target2")

    page.wait()
    page._page.press("body", "Enter")
    page.wait()
    target2.click()
    page.wait()
    menu_items = target2.get_options_values()
    assert menu_items == ["c1", "c2", "c3"]


def test_default_value(page: ScreenPage, page_path: str):
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

        set_test_id(ds.ui_select("name", value=["a", "b"]), "name select")
        set_test_id(ds.ui_select("cls", multiple=False, value="c1"), "cls select")

        set_test_id(ds.ui_aggrid(), "table")
        set_test_id(ds1.ui_aggrid(), "table1")

    page.open(page_path)

    name_select = SelectUtils(page, "name select")
    cls_select = SelectUtils(page, "cls select")
    table = AggridUtils(page, "table")
    table1 = AggridUtils(page, "table1")

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
