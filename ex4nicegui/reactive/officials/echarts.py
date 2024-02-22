from pathlib import Path
from typing import Any, Callable, Dict, List, Union, cast, Optional
from typing_extensions import Literal
from ex4nicegui.reactive.utils import ParameterClassifier

from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    ref_computed,
    _TMaybeRef as TMaybeRef,
    effect,
    to_value,
)
from .base import BindableUi
from ex4nicegui.reactive.EChartsComponent.ECharts import (
    echarts,
    EChartsMouseEventArguments,
)

from nicegui.awaitable_response import AwaitableResponse
from nicegui import ui, app

_TEventName = Literal[
    "click",
    "dblclick",
    "mousedown",
    "mousemove",
    "mouseup",
    "mouseover",
    "mouseout",
    "globalout",
    "contextmenu",
]


class EChartsBindableUi(BindableUi[echarts]):
    EChartsMouseEventArguments = EChartsMouseEventArguments

    def __init__(
        self,
        options: Optional[TMaybeRef[Dict]] = None,
        not_merge: TMaybeRef[Union[bool, None]] = None,
        code: Optional[str] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(), maybeRefs=["options", "code"], exclude=["not_merge"]
        )

        value_kws = pc.get_values_kws()

        element = echarts(**value_kws).classes("grow self-stretch h-[16rem]")
        super().__init__(element)  # type: ignore

        self.__update_setting = None
        if not_merge is not None:
            self.__update_setting = {"notMerge": not_merge}

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @classmethod
    def register_map(cls, map_name: str, src: Union[str, Path]):
        """Registers available maps. This can only be used after including geo component or chart series of map.

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#rxuiechartsregister_map
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#rxuiechartsregister_map

        Args:
            map_name (str): Map name, referring to map value set in geo component or map.
            src (Union[str, Path]): Map data. If str, it should be a network address. If path, it should be a valid file.
        """
        if isinstance(src, Path):
            src = app.add_static_file(local_file=src)

        assert isinstance(src, str)

        ui.add_body_html(
            rf"""
            <script>
                window.addEventListener('DOMContentLoaded', () => {{
                    fetch("{src}")
                        .then((response) => response.json())
                        .then((data) => {{
                            echarts.registerMap('{map_name}', data);
                        }});
                }});
            </script>
        """
        )

    @classmethod
    def from_pyecharts(cls, chart: TMaybeRef):
        if is_ref(chart):

            @ref_computed
            def chart_opt():
                if not bool(chart.value):
                    return {}
                return PyechartsUtils._chart2opts(chart.value)

            return cls(chart_opt)

        return cls(PyechartsUtils._chart2opts(chart))

    @classmethod
    def from_javascript(cls, code: Union[str, Path]):
        """Create echart from javascript code.

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#rxuiechartsfrom_javascript
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#rxuiechartsfrom_javascript


        Args:
            code (Union[str, Path]): Text of the js code. If it is of type `Path` reads the text of the file.

        ## Examples

        ```python
        rxui.echarts.from_javascript(
            r'''(myChart) => {
                option = {...};
                myChart.setOption(option);
            }
        ''')
        ```

        """
        if isinstance(code, Path):
            code = code.read_text("utf8")
        return cls(code=code)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "options":
            return self.bind_options(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_options(self, ref_ui: ReadonlyRef[Dict]):
        @effect
        def _():
            ele = self.element
            ele.update_options(to_value(ref_ui), self.__update_setting)
            ele.update()

        return self

    def on(
        self,
        event_name: _TEventName,
        handler: Callable[..., Any],
        query: Optional[Union[str, Dict]] = None,
    ):
        """echart instance event on.

        [English Documentation](https://echarts.apache.org/handbook/en/concepts/event/)

        [中文文档](https://echarts.apache.org/handbook/zh/concepts/event/)


        Args:
            event_name (_TEventName): general mouse events name.`'click', 'dblclick', 'mousedown', 'mousemove', 'mouseup', 'mouseover', 'mouseout', 'globalout', 'contextmenu'`
            handler (Callable[..., Any]): event callback
            query (Optional[Union[str,Dict]], optional): trigger callback of the specified component. Defaults to None.

        ## Examples

        ---

        ### click event:
        ```python
        bar = rxui.echarts(opts)

        def on_click(e):
            ui.notify(f"on_click:{e}")

        bar.on("click", on_click)
        ```

        ---

        ### Use query to trigger callback of the specified component:

        ```python
        ...
        def on_line_click(e):
            ui.notify(e)

        bar.on("click", on_line_click,query='series.line')
        ```

        ---
        ### only trigger for specified series
        ```python

        opts = {
            "xAxis": {"type": "value", "boundaryGap": [0, 0.01]},
            "yAxis": {
                "type": "category",
                "data": ["Brazil", "Indonesia", "USA", "India", "China", "World"],
            },
            "series": [
                {
                    "name": "first",
                    "type": "bar",
                    "data": [18203, 23489, 29034, 104970, 131744, 630230],
                },
                {
                    "name": "second",
                    "type": "bar",
                    "data": [19325, 23438, 31000, 121594, 134141, 681807],
                },
            ],
        }

        bar = rxui.echarts(opts)

        def on_first_series_mouseover(e):
            ui.notify(f"on_first_series_mouseover:{e}")

        bar.on("mouseover", on_first_series_mouseover, query={"seriesName": "first"})
        ```

        ---
        """
        self.element.echarts_on(event_name, handler, query)

    def run_chart_method(
        self, name: str, *args, timeout: float = 1, check_interval: float = 0.01
    ) -> AwaitableResponse:
        """Run a method of the JSONEditor instance.

        See the `ECharts documentation <https://echarts.apache.org/en/api.html#echartsInstance>`_ for a list of methods.

        If the function is awaited, the result of the method call is returned.
        Otherwise, the method is executed without waiting for a response.

        :param name: name of the method (a prefix ":" indicates that the arguments are JavaScript expressions)
        :param args: arguments to pass to the method (Python objects or JavaScript expressions)
        :param timeout: timeout in seconds (default: 1 second)
        :param check_interval: interval in seconds to check for a response (default: 0.01 seconds)

        :return: AwaitableResponse that can be awaited to get the result of the method call
        """
        return self.element.run_chart_method(
            name,
            *args,
            timeout=timeout,
            check_interval=check_interval,
        )


class PyechartsUtils:
    JS_CODE_FIX = "--x_x--0_0--"

    @staticmethod
    def _chart2opts(chart):
        import simplejson as json
        from pyecharts.charts.chart import Base
        from pyecharts.charts.base import default

        assert isinstance(chart, Base), "must be pyecharts chart object"

        dumps_str = json.dumps(chart.get_options(), default=default, ignore_nan=True)
        opts = json.loads(dumps_str)
        PyechartsUtils._replace_key_name_of_js_code(opts)
        return opts

    @staticmethod
    def _replace_key_name_of_js_code(opts: Dict):
        stack = cast(List[Any], [opts])

        while len(stack) > 0:
            cur = stack.pop()
            if isinstance(cur, list):
                stack.extend(cur)
            elif isinstance(cur, dict):
                for key, value in tuple(cur.items()):
                    if isinstance(value, str) and PyechartsUtils._is_js_code_str(value):
                        cur[f":{key}"] = PyechartsUtils._replace_js_code_fix(value)
                        del cur[key]
                    else:
                        stack.append(value)

    @staticmethod
    def _is_js_code_str(text: str):
        return (
            len(text) > 2 * len(PyechartsUtils.JS_CODE_FIX)
            and text[: len(PyechartsUtils.JS_CODE_FIX)] == PyechartsUtils.JS_CODE_FIX
            and text[-len(PyechartsUtils.JS_CODE_FIX) :] == PyechartsUtils.JS_CODE_FIX
        )

    @staticmethod
    def _replace_js_code_fix(text: str):
        start = len(PyechartsUtils.JS_CODE_FIX)
        end = len(text) - len(PyechartsUtils.JS_CODE_FIX)
        return text[start:end]
