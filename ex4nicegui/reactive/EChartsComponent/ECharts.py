from typing import Any, Callable, Dict, List, Optional, Union
from typing_extensions import Literal
from dataclasses import dataclass
from nicegui.dataclasses import KWONLY_SLOTS
from nicegui.events import handle_event, UiEventArguments
from nicegui.element import Element
from nicegui import context as ng_context
from pathlib import Path
import nicegui
import uuid

NG_ROOT = Path(nicegui.__file__).parent / "elements"
libraries = [NG_ROOT / "lib/echarts/echarts.min.js"]


_Chart_Click_Args = [
    "componentType",
    "seriesType",
    "seriesIndex",
    "seriesName",
    "name",
    "dataIndex",
    "data",
    "dataType",
    "value",
    "color",
]


@dataclass(**KWONLY_SLOTS)
class EChartsMouseEventArguments(UiEventArguments):
    componentType: str
    seriesType: str
    seriesIndex: int
    seriesName: str
    name: str
    dataIndex: int
    data: dict
    dataType: Optional[str]
    value: Any
    color: str


_T_echats_on_callback = Callable[[EChartsMouseEventArguments], Any]
_T_mouse_event_name = Literal[
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


class echarts(Element, component="ECharts.js", libraries=libraries):  # type: ignore
    def __init__(self, options: dict) -> None:
        super().__init__()
        self._props["options"] = options

        self._echarts_on_tasks: List[Callable] = []
        self._echarts_on_callback_map: Dict[str, _T_echats_on_callback] = {}

        async def on_client_connect(client: nicegui.Client) -> Any:
            await client.connected()

            for func in self._echarts_on_tasks:
                func()

            client.connect_handlers.remove(on_client_connect)  # type: ignore

        ng_context.get_client().on_connect(on_client_connect)

        def echartsOn_handler(e):
            callbackId = e.args["callbackId"]
            params: Dict = e.args["params"]
            params["dataType"] = params.get("dataType")

            if callbackId in self._echarts_on_callback_map:
                event_args = EChartsMouseEventArguments(e.sender, e.client, **params)
                handler = self._echarts_on_callback_map[callbackId]

                handle_event(handler, event_args)

        self.on("event_on", echartsOn_handler)

    def update_options(self, options: dict, opts: Optional[dict] = None):
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
        self.run_method("updateOptions", options, opts)
        self.update()
        return self

    def on_click_blank(self, handler: Optional[Callable[[UiEventArguments], Any]]):
        def inner_handler(e):
            handle_event(
                handler,
                UiEventArguments(
                    sender=self,
                    client=self.client,
                ),
            )

        self.on("clickBlank", inner_handler, _Chart_Click_Args)

    def echarts_on(
        self,
        event_name: _T_mouse_event_name,
        handler: _T_echats_on_callback,
        query: Optional[Union[str, Dict]] = None,
    ):
        if not ng_context.get_client().has_socket_connection:

            def task_func():
                self.echarts_on(event_name, handler, query)

            self._echarts_on_tasks.append(task_func)
            return

        callback_id = uuid.uuid4().hex
        print("echarts_on:", event_name, query, callback_id)
        self.run_method("echarts_on", event_name, query, callback_id)
        self._echarts_on_callback_map[callback_id] = handler
