from typing import Any, Callable, Dict, List, Union, cast, Optional
from typing_extensions import Literal

from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    ref_computed,
    _TMaybeRef as TMaybeRef,
    to_ref,
    effect,
)
from .base import BindableUi
from .utils import _convert_kws_ref2value
from ex4nicegui.reactive.EChartsComponent.ECharts import (
    echarts,
    EChartsMouseEventArguments,
)


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
        options: TMaybeRef[Dict],
    ) -> None:
        kws = {
            "options": options,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = echarts(**value_kws).classes("grow self-stretch h-[16rem]")

        super().__init__(element)

        self.__click_info_ref = to_ref(cast(Optional[EChartsMouseEventArguments], None))

        def on_chart_click(e: EChartsMouseEventArguments):
            self.__click_info_ref.value = e

        self.on("click", on_chart_click)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    @staticmethod
    def _pyecharts2opts(chart):
        return PyechartsUtils._chart2opts(chart)

    @staticmethod
    def from_pyecharts(chart: TMaybeRef):
        if is_ref(chart):

            @ref_computed
            def chart_opt():
                return EChartsBindableUi._pyecharts2opts(chart.value)

            return EChartsBindableUi(chart_opt)

        return EChartsBindableUi(EChartsBindableUi._pyecharts2opts(chart))

    @property
    def click_info_ref(self):
        return self.__click_info_ref

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "options":
            return self.bind_options(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_options(self, ref_ui: ReadonlyRef[Dict]):
        @effect
        def _():
            ele = self.element
            ele.update_options(ref_ui.value)
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
