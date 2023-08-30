from typing import Any, Callable, Dict, List, Optional
from nicegui import ui, app
from nicegui.element import Element
from ex4nicegui.utils.signals import to_ref, Ref
from dataclasses import dataclass
from nicegui.dataclasses import KWONLY_SLOTS
from nicegui.events import handle_event, UiEventArguments


_Update_Args = [
    "keys",
]


@dataclass(**KWONLY_SLOTS)
class DropZoneUpdatedEventArguments(UiEventArguments):
    keys: List[str]


class DropZone(Element, component="dropZone.js"):
    def __init__(self, drop_zone: ui.element) -> None:
        super().__init__()
        self._props["dropZoneId"] = f"c{drop_zone.id}"

    def on_keys_update(self, handler: Optional[Callable[..., Any]]):
        def inner_handler(e):
            args = e.args
            handle_event(
                handler,
                DropZoneUpdatedEventArguments(
                    sender=self, client=self.client, keys=args["keys"]
                ),
            )

        self.on("onDraggableKeysUpdated", inner_handler, args=_Update_Args)

    def apply(self, draggable_item_id: str, key_str: str):
        self.run_method("apply", draggable_item_id, key_str)
        return self

    def remove_key(self, key_str: str):
        self.run_method("removeKey", key_str)
        return self


class DropZoneResult:
    def __init__(self, zone_box: ui.element) -> None:
        self.__drop_zone = DropZone(zone_box)
        self.__drag_keys: Ref[List[str]] = to_ref([])
        self.__apply_infos: Optional[Dict[str, str]] = {}

        def on_keys_updated(e: DropZoneUpdatedEventArguments):
            self.__drag_keys.value = e.keys

        self.__drop_zone.on_keys_update(on_keys_updated)

        def on_connect():
            if self.__apply_infos is None:
                return

            for id, key_str in self.__apply_infos.items():
                self.__drop_zone.apply(id, key_str)

            self.__apply_infos = None

        app.on_connect(on_connect)

    @property
    def drag_keys(self):
        return self.__drag_keys

    def apply(self, draggable_item: ui.element, key_str: str):
        id = f"c{draggable_item.id}"
        if self.__apply_infos is not None:
            self.__apply_infos[id] = key_str
        else:
            self.__drop_zone.apply(id, key_str)
        return self

    def remove_item(self, key_str: str):
        self.__drop_zone.remove_key(key_str)
        return self


def use_drag_zone(
    zone_box: ui.element,
):
    return DropZoneResult(zone_box)
