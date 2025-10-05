from pathlib import Path
from ex4nicegui.reactive import rxui
from nicegui import ui, app
from fastapi import Response
from ex4nicegui import ref_computed, to_ref, deep_ref
from .screen import BrowserManager
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.commons import utils


def test_chart_display(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.echarts(
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
        ).classes("target1")

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
        rxui.echarts.from_pyecharts(chart_opts).classes("target2")

        # from js
        rxui.echarts.from_javascript(
            Path(__file__).parent / "files/echarts_code.js"
        ).classes("target3")

    page = browser.open(page_path)

    target1 = page.ECharts(".target1")
    target2 = page.ECharts(".target2")
    target3 = page.ECharts(".target3")

    target1.assert_echarts_attachment()
    target2.assert_echarts_attachment()
    target3.assert_echarts_attachment()


def test_chart_deep_ref(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_opts = deep_ref(
            {
                "xAxis": {
                    "type": "category",
                    "data": ["Mon", "Tue", "Wed"],
                },
                "yAxis": {"type": "value"},
                "series": [{"data": [120, 200, 150], "type": "bar"}],
            }
        )

        rxui.number(value=rxui.vmodel(r_opts, "series", 0, "data", 0)).classes(  # type: ignore
            "number_input"
        )

        rxui.echarts(r_opts, not_merge=False).classes("chart")

    page = browser.open(page_path)

    chart = page.ECharts(".chart")
    number_input = page.Number(".number_input")

    number_input.fill_text("12")

    assert chart.get_options()["series"][0]["data"][0] == 12


def test_js_function_opt(browser: BrowserManager, page_path: str):
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
        rxui.echarts(opts).classes("target")

    page = browser.open(page_path)

    target = page.ECharts(".target")

    target.assert_canvas_exists()

    opts = target.get_options()

    assert "formatter" in opts["yAxis"][0]["axisLabel"]


def test_pyecharts(browser: BrowserManager, page_path: str):
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

        rxui.echarts.from_pyecharts(c).classes("target")

    page = browser.open(page_path)

    target = page.ECharts(".target")

    target.assert_canvas_exists()

    chart_opts = target.get_options()

    assert "formatter" in chart_opts["yAxis"][0]["axisLabel"]


def test_pyecharts_from_fn(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        data = to_ref([0.1, 0.2])

        def bar_chart():
            return Bar().add_xaxis(["A", "B"]).add_yaxis("ratio", data.value)

        rxui.echarts.from_pyecharts(bar_chart).classes("target")

    page = browser.open(page_path)

    target = page.ECharts(".target")

    target.assert_canvas_exists()


def test_click_event(browser: BrowserManager, page_path: str):
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

        chart = rxui.echarts(opts).classes("target")

        lbl_click = ui.label().classes("lbl_click")
        lbl_hover = ui.label().classes("lbl_hover")

        def onclick_series(
            e: rxui.echarts.EChartsMouseEventArguments,
        ):
            lbl_click.set_text(e.seriesName or "")

        chart.on("click", onclick_series)

        def on_mouser_over(
            e: rxui.echarts.EChartsMouseEventArguments,
        ):
            lbl_hover.set_text(e.seriesName or "")

        chart.on(
            "mouseover",
            on_mouser_over,
            query={"seriesName": "Beta"},
        )

    page = browser.open(page_path)

    target = page.ECharts(".target")
    lbl_click = page.Label(".lbl_click")
    lbl_hover = page.Label(".lbl_hover")

    target.assert_canvas_exists()

    target.click_series(0.05, "A", y_position_offset=-8)

    lbl_click.expect_to_have_text("Alpha")

    target.mouse_hover_series(
        0.05,
        "B",
        color="Alpha",
        y_position_offset=-8,
    )

    lbl_hover.expect_not_to_have_text("Alpha")

    target.mouse_hover_series(
        0.05,
        "B",
        color="Beta",
        y_position_offset=+8,
    )

    lbl_hover.expect_to_have_text("Beta")


def test_click_event_in_tab_panels(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        opts = {
            "xAxis": {"type": "value"},
            "yAxis": {
                "type": "category",
                "data": ["A", "B"],
                "inverse": True,
            },
            "series": [
                {
                    "type": "bar",
                    "data": [0.1, 0.2],
                }
            ],
        }

        names = ["Tab 1", "Tab 2"]
        current_tab = to_ref(names[0])

        click_count1 = to_ref(0)
        click_count2 = to_ref(0)

        def add_click_count1():
            click_count1.value += 1

        def add_click_count2():
            click_count2.value += 1

        rxui.label(current_tab).classes("lbl_current-tab")
        rxui.label(click_count1).classes("lbl_click-1")
        rxui.label(click_count2).classes("lbl_click-2")

        with rxui.tabs(current_tab):
            for name in names:
                rxui.tab(name)

        with rxui.tab_panels(current_tab).classes("w-full"):
            with rxui.tab_panel("Tab 1"):
                rxui.echarts(opts, init_options={"renderer": "svg"}).classes(
                    "chart-1"
                ).on("click", add_click_count1, query="series")

            with ui.tab_panel("Tab 2"):
                rxui.echarts(opts, init_options={"renderer": "svg"}).classes(
                    "chart-2"
                ).on("click", add_click_count2, query="series")

    page = browser.open(page_path)

    chart1 = page.ECharts(".chart-1")
    chart2 = page.ECharts(".chart-2")
    lbl_current_tab = page.Label(".lbl_current-tab")
    lbl_click1 = page.Label(".lbl_click-1")
    lbl_click2 = page.Label(".lbl_click-2")

    chart1.assert_svg_exists()

    chart1.click_svg_last_path(2)
    lbl_click1.expect_to_have_text("1")

    # switch to tab 2
    page.locator("css=.q-tab", has_text="Tab 2").click()
    chart2.assert_svg_exists()
    lbl_current_tab.expect_equal_text("Tab 2")

    chart2.click_svg_last_path(2)
    lbl_click2.expect_to_have_text("1")


def test_update_opts(browser: BrowserManager, page_path: str):
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

        rxui.echarts(r_opts).classes("target")
        rxui.label(lambda: str(r_opts.value["title"])).classes("label")

        def on_click():
            del r_opts.value["title"]["bottom"]
            r_opts.value = r_opts.value

        ui.button("del title bottom", on_click=on_click).classes("del-btn")

    page = browser.open(page_path)

    target = page.ECharts(".target")
    label = page.Label(".label")
    del_btn = page.Button(".del-btn")

    target.assert_canvas_exists()
    label.expect_to_have_text("{'text': 'title', 'bottom': 0}")

    del_btn.click()
    label.expect_to_have_text("{'text': 'title'}")


def test_run_chart_method(browser: BrowserManager, page_path: str):
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
        ).classes("target")

        def onclick():
            chart.run_chart_method("setOption", {"title": {"text": "new title"}})

        ui.button("change title", on_click=onclick).classes("change-btn")

    page = browser.open(page_path)

    target = page.ECharts(".target")
    button = page.Button(".change-btn")

    target.assert_canvas_exists()

    assert "title" not in target.get_options()

    button.click()
    assert target.get_options()["title"][0]["text"] == "new title"


def test_create_map(browser: BrowserManager, page_path: str):
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

        @app.get("/test/svg")
        def get_svg_map():
            headers = {"Content-Type": "text/plain; charset=utf-8"}
            return Response(
                """
        <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
        <rect x="10" y="10" width="80" height="80" fill="red"/>
        </svg>
        """,
                media_type="text/plain",
                headers=headers,
            )

        rxui.echarts.register_map("test_map", "/test/map")
        rxui.echarts.register_map("svg-rect", "/test/svg", type="svg")

        rxui.echarts(
            {
                "geo": {
                    "map": "test_map",
                    "roam": True,
                },
                "series": [],
            }
        ).classes("target")

        rxui.echarts.from_javascript(
            r"""
        chart =>{
                                    
            chart.setOption({
                "geo": {
                    "map": "test_map",
                    "roam": True,
                },
                "tooltip": {},
                "legend": {},
                "series": [],
            });

        }
        """
        ).classes("target-js")

        # svg map
        rxui.echarts(
            {
                "geo": {
                    "map": "svg-rect",
                    "roam": True,
                },
                "series": [],
            }
        ).classes("target-svg")

    page = browser.open(page_path)

    target = page.ECharts(".target")
    target_js = page.ECharts(".target-js")
    target_svg = page.ECharts(".target-svg")

    target.assert_canvas_exists()
    target_js.assert_canvas_exists()
    target_svg.assert_canvas_exists()


def test_create_from_js_code(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
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

        rxui.echarts.from_javascript(
            r"""
        chart =>{
            const option = {
                xAxis: {
                    type: 'category',
                    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                    data: [150, 230, 224, 218, 135, 147, 260],
                    type: 'line'
                    }
                ]
            }            
            chart.setOption(option);
        }
        """
        ).classes("target")

        rxui.echarts.from_javascript(
            r"""
        (chart,echarts) =>{

            fetch('/test/map')
            .then(response => response.json())
            .then(data => {
                    echarts.registerMap('test_map', data);

                    chart.setOption({
                        "geo": {
                            "map": "test_map",
                            "roam": True,
                        },
                        "tooltip": {},
                        "legend": {},
                        "series": [],
                    });
                });
        }
        """
        ).classes("target-use-echarts-register-map")

    page = browser.open(page_path)

    target = page.ECharts(".target")
    target_map = page.ECharts(".target-use-echarts-register-map")

    target.assert_canvas_exists()
    target_map.assert_canvas_exists()
