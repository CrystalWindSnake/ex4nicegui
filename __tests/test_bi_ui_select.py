from nicegui import ui
from .screen import ScreenPage
import pandas as pd

from ex4nicegui import bi
from .utils import SelectUtils, set_test_id


def test_(page: ScreenPage, page_path: str):
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
    menu_items = target1.get_selection_values()
    assert menu_items == ["L1_A", "L1_B"]
    target1.click()

    target2.click()
    page.wait()
    menu_items = target2.get_selection_values()
    assert menu_items == ["L2_M_1", "L2_M_2", "L2_M_3", "L2_M_4"]
    target2.click()

    target3.click()
    page.wait()
    menu_items = target3.get_selection_values()
    assert menu_items == [f"L3_Z_{n}" for n in range(1, 8)]
    target3.click()
