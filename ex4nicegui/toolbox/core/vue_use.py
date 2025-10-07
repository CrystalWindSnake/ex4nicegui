from typing import Any, Callable, List, Optional
from nicegui.element import Element
from collections import defaultdict


class VueUse(Element, component="VueUse.js"):
    def __init__(
        self,
        method: str,
        args: Optional[List[Any]] = None,
    ) -> None:
        super().__init__()

        self._props["method"] = method
        self._props["args"] = args

        self.__on_events: defaultdict[str, List[Callable]] = defaultdict(list)

        def on_change(e):
            event_name = e.args["eventName"]
            value = e.args["value"]

            self.trigger_event(event_name, value)

        self.on("change", on_change)

    def on_event(self, event_name: str, callback: Callable) -> None:
        self.__on_events[event_name].append(callback)

    def trigger_event(self, event_name: str, value: Any) -> None:
        for callback in self.__on_events[event_name]:
            callback(value)
