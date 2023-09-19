from typing import Dict, List, Optional, cast
from ex4nicegui import to_ref, ref_computed, on
from nicegui import globals, Client

from dataclasses import dataclass
from . import types
from .protocols import IDataSourceAble


@dataclass
class DataSourceInfo:
    source: "DataSource"
    update_callback: types._TSourceBuildFn


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
    update_callback: types._TComponentUpdateCallback
    filter: Optional[Filter] = None


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

    def has_record(self, client_id: types._TNgClientID, element_id: types._TElementID):
        return (
            client_id in self._client_map and element_id in self._client_map[client_id]
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

    @property
    def data(self):
        return self.__data.value

    @property
    def filtered_data(self):
        return self.__filtered_data.value

    @property
    def id(self):
        return self.__id

    def _register_component(
        self,
        element_id: types._TElementID,
        update_callback: types._TComponentUpdateCallback,
    ):
        ng_client = globals.get_client()
        client_id = ng_client.id

        if not self._component_map.has_client_record(client_id):

            @ng_client.on_disconnect
            def _(e: Client):
                if not e.shared:
                    self._component_map.remove_client(e.id)

        self._component_map.add_info(
            ComponentInfo(ComponentInfoKey(client_id, element_id), update_callback)
        )

        return self

    def send_filter(self, element_id: types._TElementID, filter: Filter):
        client_id = globals.get_client().id

        if not self._component_map.has_record(client_id, element_id):
            raise ValueError("element not register")

        self._component_map.set_filter(client_id, element_id, filter)

        self.__notify_update([ComponentInfoKey(client_id, element_id)])
        return self

    def __notify_update(self, ignore_keys: Optional[List[ComponentInfoKey]] = None):
        ignore_keys = ignore_keys or []
        ignore_ids_set = set(ignore_keys)

        # nodify every component
        for current_info in self._component_map.get_all_info():
            if current_info.key in ignore_ids_set:
                continue

            # apply filters ,except current target
            filters = [
                info.filter.callback
                for info in self._component_map.get_all_info()
                if (info.key != current_info.key) and info.filter
            ]

            new_data = self._idataSource.apply_filters(filters)
            current_info.update_callback(new_data)

        self.__filters.value = [
            info.filter for info in self._component_map.get_all_info() if info.filter
        ]
