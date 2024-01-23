from ex4nicegui.reactive import rxui
from nicegui import ui, app
from ex4nicegui import ref_computed, to_ref
from .screen import ScreenPage
from .utils import EChartsUtils, ButtonUtils, set_test_id
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.commons import utils


def test_chart_display(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        target1 = rxui.echarts(
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

        show = to_ref(False)

        @ref_computed
        def chart_opts():
            if not show.value:
                return None

            c = (
                Bar()
                .add_xaxis(
                    [
                        "Mon",
                    ]
                )
                .add_yaxis(
                    "商家A",
                    [120],
                )
            )

            return c

        # Charts don't show up in ui, but the instance tag are still there
        # i.g. https://github.com/CrystalWindSnake/ex4nicegui/issues/77
        target2 = rxui.echarts.from_pyecharts(chart_opts)

        set_test_id(target1, "target1")
        set_test_id(target2, "target2")

    page.open(page_path)

    target1 = EChartsUtils(page, "target1")
    target2 = EChartsUtils(page, "target2")

    target1.assert_chart_exists()
    target2.assert_chart_exists()


def test_js_function_opt(page: ScreenPage, page_path: str):
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
                "axisLabel": {":formatter": yAxis_formatter.value},
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
    target.assert_chart_exists()

    opts = target.get_options()

    assert "formatter" in opts["yAxis"][0]["axisLabel"]


def test_pyecharts(page: ScreenPage, page_path: str):
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

    target.assert_chart_exists()

    chart_opts = target.get_options()

    assert "formatter" in chart_opts["yAxis"][0]["axisLabel"]


def test_click_event(page: ScreenPage, page_path: str):
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
            "legend": {"textStyle": {"color": "gray"}},
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
            click_data["seriesName"] = e.seriesName

        ins.on("click", onclick_series)

        def on_mouser_over(
            e: rxui.echarts.EChartsMouseEventArguments,
        ):
            hover_data["seriesName"] = e.seriesName

        ins.on(
            "mouseover",
            on_mouser_over,
            query={"seriesName": "Beta"},
        )

        set_test_id(ins, "target")

    page.open(page_path)

    target = EChartsUtils(page, "target")

    target.assert_chart_exists()

    target.click_series(0.05, "A", y_position_offset=-8)

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


def test_update_opts(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        opts = {
            "title": {"text": "title", "bottom": 0},
            "xAxis": {"type": "value"},
            "yAxis": {
                "type": "category",
                "data": ["a", "b"],
            },
            "series": [
                {
                    "name": "first",
                    "type": "bar",
                    "data": [18203, 23489],
                },
                {
                    "name": "second",
                    "type": "bar",
                    "data": [19325, 23438],
                },
            ],
        }

        r_opts = to_ref(opts)

        set_test_id(rxui.echarts(r_opts), "target")

        def on_click():
            del r_opts.value["title"]["bottom"]
            r_opts.value = r_opts.value

        set_test_id(ui.button("del title bottom", on_click=on_click), "botton")

    page.open(page_path)

    target = EChartsUtils(page, "target")
    button = ButtonUtils(page, "botton")

    target.assert_chart_exists()
    assert target.get_options()["title"][0]["bottom"] == 0

    button.click()

    assert target.get_options()["title"][0]["bottom"] is None


def test_run_chart_method(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        chart = rxui.echarts(
            {
                "xAxis": {"type": "value"},
                "yAxis": {"type": "category", "data": ["A", "B"], "inverse": True},
                "series": [
                    {"type": "bar", "name": "Alpha", "data": [0.1, 0.2]},
                ],
            }
        )

        def onclick():
            chart.run_chart_method("setOption", {"title": {"text": "new title"}})

        btn = ui.button("clear", on_click=onclick)

        set_test_id(chart, "target")

        set_test_id(btn, "botton")

    page.open(page_path)

    target = EChartsUtils(page, "target")
    button = ButtonUtils(page, "botton")

    assert "title" not in target.get_options()

    button.click()
    page.wait()

    target.assert_chart_exists()

    assert target.get_options()["title"][0]["text"] == "new title"


def test_create_map(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        #
        @app.get("/test/map")
        def get_map_data():
            return {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {"adcode": 110000, "name": "北京市"},
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [[35, 10], [45, 45], [15, 40], [10, 20], [35, 10]],
                                [[20, 30], [35, 35], [30, 20], [20, 30]],
                            ],
                        },
                    }
                ],
            }

        rxui.echarts.register_map("test_map", "/test/map")

        chart = rxui.echarts(
            {
                "geo": {
                    "map": "test_map",
                    "roam": True,
                },
                "series": [],
            }
        )

        set_test_id(chart, "target")

    page.open(page_path)
    page.wait()

    target = EChartsUtils(page, "target")
    target.assert_chart_exists()
