from typing import Dict, List, Optional, cast

from ex4nicegui import to_ref, ref_computed, on


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


@dataclass
class ComponentInfo:
    element_id: types._TElementID
    update_callback: types._TComponentUpdateCallback
    filter: Optional[Filter] = None


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
        self._component_map: Dict[types._TElementID, ComponentInfo] = {}

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

    def _register_component(
        self,
        element_id: types._TElementID,
        update_callback: types._TComponentUpdateCallback,
    ):
        self._component_map[element_id] = ComponentInfo(element_id, update_callback)
        return self

    def send_filter(self, element_id: types._TElementID, filter: Filter):
        assert element_id in self._component_map
        self._component_map[element_id].filter = filter
        self.__notify_update([element_id])
        return self

    def __notify_update(
        self, ignore_element_ids: Optional[List[types._TElementID]] = None
    ):
        ignore_element_ids = ignore_element_ids or []

        ignore_ids_set = set(ignore_element_ids)

        # nodify every component
        for info in self._component_map.values():
            target_id = info.element_id
            if target_id in ignore_ids_set:
                continue

            # apply filters ,except current target
            filters = [
                info.filter.callback
                for info in self._component_map.values()
                if info.element_id != target_id and info.filter
            ]

            new_data = self._idataSource.apply_filters(filters)
            info.update_callback(new_data)

        self.__filters.value = [
            info.filter for info in self._component_map.values() if info.filter
        ]
