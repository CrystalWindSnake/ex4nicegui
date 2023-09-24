from __future__ import annotations
from typing import Optional, TypeVar, Generic, TYPE_CHECKING
from nicegui import globals as ng_globals, ui
from ex4nicegui.bi.dataSource import ComponentInfoKey

if TYPE_CHECKING:
    from ex4nicegui.bi.dataSource import DataSource, ComponentInfo


_T_ELEMENT = TypeVar("_T_ELEMENT", bound=ui.element)


class UiResult(Generic[_T_ELEMENT]):
    def __init__(self, element: _T_ELEMENT, dataSource: "DataSource") -> None:
        self.__element = element
        self.__dataSource = dataSource

    @property
    def element(self):
        return self.__element

    def classes(
        self,
        add: Optional[str] = None,
        *,
        remove: Optional[str] = None,
        replace: Optional[str] = None,
    ):
        return self.element.classes(add, remove=remove, replace=replace)

    def props(
        self,
        add: Optional[str] = None,
        *,
        remove: Optional[str] = None,
    ):
        return self.element.props(add, remove=remove)

    def cancel_linkage(self, *ui_results: "UiResult"):
        client_id = ng_globals.get_client().id

        cancel_keys = set(
            ComponentInfoKey(client_id, res.element.id) for res in ui_results
        )

        def can_update_fn(trigger: ComponentInfo):
            return trigger.key not in cancel_keys

        self.__dataSource.reset_can_update_fn(
            ComponentInfoKey(client_id, self.element.id), can_update_fn
        )
