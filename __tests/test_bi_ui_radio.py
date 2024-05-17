from nicegui import ui
from .screen import BrowserManager
import pandas as pd
from ex4nicegui import bi


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

        source.ui_radio("level1", custom_options_map={"L1_A": "A值"}).classes("level1")

        def custom_options_map(v: str):
            if v == "L2_M_2":
                return {"label": "level2@m_2", "color": "red"}
            return v

        source.ui_radio("level2", custom_options_map=custom_options_map).classes(
            "level2"
        )
        source.ui_radio("level3").classes("level3")

    page = browser.open(page_path)

    level1 = page.Radio(".level1")
    level2 = page.Radio(".level2")

    assert not level1.is_checked_by_label("A值")
    assert not level1.is_checked_by_label("L1_B")

    level1.check_by_label("A值")

    assert level1.is_checked_by_label("A值")
    assert not level1.is_checked_by_label("L1_B")

    assert not level2.is_checked_by_label("L2_M_1")
    assert not level2.is_checked_by_label("level2@m_2")

    assert level2.get_all_labels() == ["L2_M_1", "level2@m_2"]


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
        source.ui_radio("name", sort_options={"cls": "asc", "value": "desc"}).classes(
            "name"
        )

    page = browser.open(page_path)

    target = page.Radio(".name")

    assert target.get_all_labels() == ["c", "b", "a", "d", "f"]


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
        source.ui_radio("cls").classes("target1")
        source.ui_radio("cls", exclude_null_value=True).classes("target2")

    page = browser.open(page_path)

    # target1
    target1 = page.Radio(".target1")

    assert target1.get_all_labels() == ["c1", "c2", "c3", ""]

    # target2
    target2 = page.Radio(".target2")

    assert target2.get_all_labels() == ["c1", "c2", "c3"]
