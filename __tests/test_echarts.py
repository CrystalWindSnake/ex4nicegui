import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import ref_computed
from .screen import ScreenPage


def test_chart_display(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.echarts(
            {
                "title": {"text": "echart title"},
                "xAxis": {
                    "type": "category",
                    "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                },
                "yAxis": {"type": "value"},
                "series": [{"data": [120, 200, 150, 80, 70, 110, 130], "type": "bar"}],
            }
        )

    page.open(page_path)
    page.wait()

    chart = page._page.query_selector("*[_echarts_instance_]")

    assert chart is not None
