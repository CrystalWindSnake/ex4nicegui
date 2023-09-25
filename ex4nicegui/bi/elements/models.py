from __future__ import annotations
from typing import Optional, TypeVar, Generic, TYPE_CHECKING, Union
from nicegui import globals as ng_globals, ui
from ex4nicegui.bi.dataSource import ComponentInfoKey

if TYPE_CHECKING:
    from ex4nicegui.bi.dataSource import DataSource, ComponentInfo


_T_ELEMENT = TypeVar("_T_ELEMENT", bound=ui.element)


class UiResult(Generic[_T_ELEMENT]):
    def __init__(self, element: _T_ELEMENT, dataSource: "DataSource") -> None:
        self.__element = element
        self._dataSource = dataSource

    @property
    def element(self):
        return self.__element

    @property
    def id(self):
        return self.element.id

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

    def cancel_linkage(self, *source: Union[ui.element, "UiResult"]):
        get_info_key = self._dataSource.get_component_info_key

        key = get_info_key(self.element.id)

        info = self._dataSource._component_map.get_info(key)

        for s in source:
            res_key = get_info_key(s.id)
            info.exclude_keys.add(res_key)
