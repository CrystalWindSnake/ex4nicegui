import os
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Union,
)

from nicegui.events import (
    handle_event,
    UiEventArguments,
)
from nicegui.element import Element
from nicegui.awaitable_response import AwaitableResponse
from nicegui import ui
from pathlib import Path
import nicegui
import uuid

from .types import _T_echats_on_callback, _T_mouse_event_name, _Chart_Click_Args
from .event import EChartsMouseEventArguments
from ex4nicegui.reactive.deferredTask import DeferredTask

NG_ROOT = Path(nicegui.__file__).parent / "elements"
libraries = [NG_ROOT / "lib/echarts/echarts.min.js"]


class echarts(Element, component="ECharts.js", libraries=libraries):  # type: ignore
    def __init__(
        self,
        options: Optional[dict] = None,
        code: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.__deferred_task = DeferredTask()

        if (options is None) and (bool(code) is False):
            raise ValueError("At least one of options and code must be valid.")

        if code:
            code = os.linesep.join([s for s in code.splitlines() if s])

            def on__update_options_from_client(e):
                self._props["options"] = e.args

            self.on("__update_options_from_client", on__update_options_from_client)

        self._props["options"] = options
        self._props["code"] = code

        self._echarts_on_callback_map: Dict[str, _T_echats_on_callback] = {}

        def echartsOn_handler(e):
            callbackId = e.args["callbackId"]
            params: Dict = e.args["params"]
            params["dataType"] = params.get("dataType")

            if callbackId in self._echarts_on_callback_map:
                event_args = EChartsMouseEventArguments(
                    sender=e.sender, client=e.client, **params
                )
                handler = self._echarts_on_callback_map[callbackId]

                handle_event(handler, event_args)

        self.on("event_on", echartsOn_handler)

    def update_chart(
        self,
        merge_opts: Optional[dict] = None,
    ):
        self.run_method("update_chart", merge_opts)
        self.update()
        return self

    def update_options(
        self,
        options: dict,
        opts: Optional[dict] = None,
    ):
        """update chart options

        Args:
            options (dict): chart setting options dict
            opts (Optional[dict], optional): update options. Defaults to None.
            ```python
                {
                    'notMerge':False,
                    'lazyUpdate':False,
                    'silent':False,
                    'replaceMerge': None,
                }
            ```
            [open echarts setOption docs](https://echarts.apache.org/zh/api.html#echartsInstance.setOption)

        """
        self._props["options"] = options
        return self.update_chart(opts)

    def on_click_blank(
        self,
        handler: Optional[Callable[[UiEventArguments], Any]],
    ):
        def inner_handler(e):
            handle_event(
                handler,
                UiEventArguments(
                    sender=self,
                    client=self.client,
                ),
            )

        self.on(
            "clickBlank",
            inner_handler,
            _Chart_Click_Args,
        )

    def echarts_on(
        self,
        event_name: _T_mouse_event_name,
        handler: _T_echats_on_callback,
        query: Optional[Union[str, Dict]] = None,
    ):
        @self.__deferred_task.register
        def _():
            callback_id = uuid.uuid4().hex
            self.run_method(
                "echarts_on",
                event_name,
                query,
                callback_id,
            )
            self._echarts_on_callback_map[callback_id] = handler

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
        return self.run_method(
            "run_chart_method",
            name,
            *args,
            timeout=timeout,
            check_interval=check_interval,
        )
