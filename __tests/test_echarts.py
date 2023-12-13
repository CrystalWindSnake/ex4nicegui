import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import ref_computed, to_ref
from .screen import ScreenPage
from .utils import EChartsUtils, set_test_id


def test_chart_display(
    page: ScreenPage, page_path: str
):
    @ui.page(page_path)
    def _():
        ins = rxui.echarts(
            {
                "title": {"text": "echart title"},
                "xAxis": {
                    "type": "category",
                    "data": [
                        "Mon",
                        "Tue",
                        "Wed",
                        "Thu",
                        "Fri",
                        "Sat",
                        "Sun",
                    ],
                },
                "yAxis": {"type": "value"},
                "series": [
                    {
                        "data": [
                            120,
                            200,
                            150,
                            80,
                            70,
                            110,
                            130,
                        ],
                        "type": "bar",
                    }
                ],
            }
        )

        set_test_id(ins, "target")

    page.open(page_path)

    target = EChartsUtils(page, "target")

    page.wait()

    target.assert_chart_exists()


def test_js_function_opt(
    page: ScreenPage, page_path: str
):
    r_unit = to_ref("kg")

    yAxis_formatter = ref_computed(
        lambda: f"""function (value, index) {{
        return value + '{r_unit.value}';
    }}
    """
    )

    opts = ref_computed(
        lambda: {
            "xAxis": {
                "type": "category",
                "data": [
                    "Mon",
                    "Tue",
                    "Wed",
                    "Thu",
                    "Fri",
                    "Sat",
                    "Sun",
                ],
            },
            "yAxis": {
                "type": "value",
                "axisLabel": {
                    ":formatter": yAxis_formatter.value
                },
            },
            "series": [
                {
                    "data": [
                        120,
                        200,
                        150,
                        80,
                        70,
                        110,
                        130,
                    ],
                    "type": "bar",
                }
            ],
        }
    )

    @ui.page(page_path)
    def _():
        ins = rxui.echarts(opts)

        set_test_id(ins, "target")

    page.open(page_path)

    target = EChartsUtils(page, "target")

    page.wait()

    opts = target.get_options()

    assert (
        "formatter"
        in opts["yAxis"][0]["axisLabel"]
    )


def test_pyecharts(
    page: ScreenPage, page_path: str
):
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.commons import utils

    @ui.page(page_path)
    def _():
        c = (
            Bar()
            .add_xaxis(
                [
                    "Mon",
                    "Tue",
                    "Wed",
                    "Thu",
                    "Fri",
                    "Sat",
                    "Sun",
                ]
            )
            .add_yaxis(
                "商家A",
                [120, 200, 150, 80, 70, 110, 130],
            )
            .set_global_opts(
                yaxis_opts=opts.AxisOpts(
                    axislabel_opts={
                        "formatter": utils.JsCode(
                            """function (value, index) {
                    return value + 'kg';
                }"""
                        )
                    }
                )
            )
        )

        ins = rxui.echarts.from_pyecharts(c)

        set_test_id(ins, "target")

    page.open(page_path)

    target = EChartsUtils(page, "target")

    page.wait()

    opts = target.get_options()

    assert (
        "formatter"
        in opts["yAxis"][0]["axisLabel"]
    )


def test_click_event(
    page: ScreenPage, page_path: str
):
    click_data = {}
    hover_data = {}

    @ui.page(page_path)
    def _():
        opts = {
            "xAxis": {"type": "value"},
            "yAxis": {
                "type": "category",
                "data": ["A", "B"],
                "inverse": True,
            },
            "legend": {
                "textStyle": {"color": "gray"}
            },
            "series": [
                {
                    "type": "bar",
                    "name": "Alpha",
                    "data": [0.1, 0.2],
                },
                {
                    "type": "bar",
                    "name": "Beta",
                    "data": [0.3, 0.4],
                },
            ],
        }

        ins = rxui.echarts(opts)

        def onclick_series(
            e: rxui.echarts.EChartsMouseEventArguments,
        ):
            click_data[
                "seriesName"
            ] = e.seriesName

        ins.on("click", onclick_series)

        def on_mouser_over(
            e: rxui.echarts.EChartsMouseEventArguments,
        ):
            hover_data[
                "seriesName"
            ] = e.seriesName

        ins.on(
            "mouseover",
            on_mouser_over,
            query={"seriesName": "Beta"},
        )

        set_test_id(ins, "target")

    page.open(page_path)

    target = EChartsUtils(page, "target")

    page.wait(1000)

    target.click_series(
        0.05, "A", y_position_offset=-8
    )

    page.wait(1000)

    assert click_data["seriesName"] == "Alpha"

    target.mouse_hover_series(
        0.05,
        "B",
        color="Alpha",
        y_position_offset=-8,
    )

    page.wait(1000)

    assert "seriesName" not in hover_data

    target.mouse_hover_series(
        0.05,
        "B",
        color="Beta",
        y_position_offset=+8,
    )

    page.wait(1000)

    assert hover_data["seriesName"] == "Beta"
