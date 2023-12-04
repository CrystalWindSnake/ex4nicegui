from nicegui import ui
from .screen import ScreenPage
import pandas as pd

from ex4nicegui import bi
from .utils import RadioUtils, set_test_id


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

        set_test_id(
            source.ui_radio("level1", custom_options_map={"L1_A": "A值"}), "target1"
        )

        def custom_options_map(v: str):
            if v == "L2_M_2":
                return {"label": "level2@m_2", "color": "red"}
            return v

        set_test_id(
            source.ui_radio("level2", custom_options_map=custom_options_map), "target2"
        )
        set_test_id(source.ui_radio("level3"), "target3")

    page.open(page_path)

    target1 = RadioUtils(page, "target1")
    target2 = RadioUtils(page, "target2")
    target3 = RadioUtils(page, "target3")

    assert not target1.is_checked_by_label("A值")
    assert not target1.is_checked_by_label("L1_B")

    page.wait()

    target1.check_by_label("A值")
    page.wait()
    assert target1.is_checked_by_label("A值")
    assert not target1.is_checked_by_label("L1_B")

    assert not target2.is_checked_by_label("L2_M_1")
    assert not target2.is_checked_by_label("level2@m_2")

    assert target2.get_all_labels() == ["L2_M_1", "level2@m_2"]
