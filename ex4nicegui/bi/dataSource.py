from typing import Callable, Dict, List, Optional, Set, cast
from ex4nicegui import to_ref, ref_computed, on
from nicegui import globals as ng_globals, Client

from dataclasses import dataclass, field
from . import types
from .protocols import IDataSourceAble

_TComponentUpdateCallback = Callable[[], None]


@dataclass
class Filter:
    callback: types._TFilterCallback


@dataclass(frozen=True)
class ComponentInfoKey:
    client_id: types._TNgClientID
    element_id: types._TElementID


@dataclass
class ComponentInfo:
    key: ComponentInfoKey
    update_callback: Optional[_TComponentUpdateCallback] = None
    filter: Optional[Filter] = None
    exclude_keys: Set[ComponentInfoKey] = field(default_factory=set)

    def __eq__(self, other):
        return isinstance(other, ComponentInfo) and self.key == other.key


class ComponentMap:
    def __init__(self) -> None:
        self._client_map: Dict[
            types._TNgClientID, Dict[types._TElementID, ComponentInfo]
        ] = {}

    def has_client_record(self, client_id: types._TNgClientID):
        return client_id in self._client_map

    def add_info(self, info: ComponentInfo):
        client_id = info.key.client_id
        element_id = info.key.element_id

        if client_id not in self._client_map:
            self._client_map[client_id] = {element_id: info}

        element_map = self._client_map[client_id]

        if element_id not in element_map:
            element_map[element_id] = info

    def remove_client(self, client_id: types._TNgClientID):
        if client_id in self._client_map:
            del self._client_map[client_id]

    def has_record(self, key: ComponentInfoKey):
        return (
            key.client_id in self._client_map
            and key.element_id in self._client_map[key.client_id]
        )

    def set_filter(
        self,
        client_id: types._TNgClientID,
        element_id: types._TElementID,
        filter: Filter,
    ):
        self._client_map[client_id][element_id].filter = filter

    def get_all_info(self):
        return (
            info for ele_map in self._client_map.values() for info in ele_map.values()
        )

    def get_info(self, key: ComponentInfoKey) -> ComponentInfo:
        return self._client_map[key.client_id][key.element_id]


class DataSource:
    _global_id_count: types._TDataSourceId = 0

    def __init__(self, data: IDataSourceAble) -> None:
        DataSource._global_id_count += 1
        self.__id = DataSource._global_id_count

        self._idataSource = data

        data_fn = lambda: data.get_data()
        data_fn = ref_computed(data_fn)

        self.__filters = to_ref(cast(List[Filter], []))

        @ref_computed
        def apply_filters():
            df = data_fn.value
            for f in self.__filters.value:
                df = f.callback(df)

            return df

        self.__filtered_data = apply_filters

        self.__data = data_fn
        self._component_map = ComponentMap()

        @on(data_fn)
        def _():
            self.__notify_update()

    @property
    def data(self):
        return self.__data.value

    @property
    def filtered_data(self):
        return self.__filtered_data.value

    @property
    def id(self):
        return self.__id

    def get_component_info_key(self, element_id: types._TElementID):
        client_id = ng_globals.get_client().id
        return ComponentInfoKey(client_id, element_id)

    def get_filtered_data(self, element_id: types._TElementID):
        data = self._idataSource.get_data()
        current_info = self._component_map.get_info(
            self.get_component_info_key(element_id)
        )

        filters = [
            info.filter.callback
            for info in self._component_map.get_all_info()
            if current_info.key != info.key
            and (info.key not in current_info.exclude_keys)
            and info.filter
        ]

        return self._idataSource.apply_filters(data, filters)

    def _register_component(
        self,
        element_id: types._TElementID,
        update_callback: Optional[_TComponentUpdateCallback] = None,
    ):
        ng_client = ng_globals.get_client()
        client_id = ng_client.id

        if not self._component_map.has_client_record(client_id):

            @ng_client.on_disconnect
            def _(e: Client):
                if not e.shared:
                    self._component_map.remove_client(e.id)

        info = ComponentInfo(ComponentInfoKey(client_id, element_id), update_callback)
        self._component_map.add_info(info)

        return info

    def send_filter(self, element_id: types._TElementID, filter: Filter):
        client_id = ng_globals.get_client().id
        key = ComponentInfoKey(client_id, element_id)

        if not self._component_map.has_record(key):
            raise ValueError("element not register")

        self._component_map.set_filter(client_id, element_id, filter)

        trigger_info = self._component_map.get_info(
            ComponentInfoKey(client_id, element_id)
        )

        self.__notify_update(trigger_info)
        self.__filters.value = [
            info.filter for info in self._component_map.get_all_info() if info.filter
        ]

        return self

    def __notify_update(self, trigger_info: Optional[ComponentInfo] = None):
        # nodify every component
        for current_info in self._component_map.get_all_info():
            # not nodify the self triggering
            if trigger_info and current_info.key == trigger_info.key:
                continue

            update_callback = current_info.update_callback
            if update_callback:
                update_callback()

    def on_source_update(
        self,
        element_id: types._TElementID,
        callback: _TComponentUpdateCallback,
    ):
        key = self.get_component_info_key(element_id)
        self._component_map.get_info(key).update_callback = callback
