from nicegui.element import Element
from nicegui import ui
from signe import batch
from ex4nicegui.utils.signals import Ref, on, to_ref
from typing import Any, Callable, Dict, List, Mapping, Optional, TypeVar, Generic, Union
from weakref import WeakValueDictionary
from functools import partial
from dataclasses import dataclass


_T = TypeVar("_T")


class VforStore(Generic[_T]):
    def __init__(self, r: Ref[_T], source: Ref[List[Any]], index: int) -> None:
        self._ref = r
        self._source = source
        self._data_index = index
        self._attr_cache: WeakValueDictionary[str, Ref] = WeakValueDictionary()

    @property
    def row_index(self):
        return self._data_index

    def get(self, attr: Optional[str] = None) -> Ref[_T]:
        if attr:
            ref = self._attr_cache.get(attr)
            if ref is None:
                value = _get_attribute(self._ref.value, attr)
                ref = to_ref(value)  # type: ignore
                self._attr_cache[attr] = ref

                @on(ref, onchanges=True)
                def _():
                    _set_attribute(
                        self._source.value[self._data_index], attr, ref.value
                    )
                    self._source.value = self._source.value

            return ref
        return self._ref

    def update_item(self, item, index: int):
        self._data_index = index

        for attr, ref in self._attr_cache.items():
            ref.value = _get_attribute(item, attr)

        self._ref.value = item  # type: ignore

    @classmethod
    def create_from_ref(cls, ref: Ref[_T], source: Ref[List], index: int):
        return cls(ref, source, index)


@dataclass
class StoreItem:
    __slot__ = ["store", "elementId"]
    store: VforStore
    elementId: int


class VforContainer(Element, component="vfor.js"):
    pass


def _set_attribute(obj: Union[object, Mapping], name: str, value: Any) -> None:
    if isinstance(obj, dict):
        obj[name] = value
    else:
        setattr(obj, name, value)


def _get_attribute(obj: Union[object, Mapping], name: str) -> Any:
    if isinstance(obj, Mapping):
        return obj[name]
    return getattr(obj, name)


def _get_key_with_index(idx: int, data: Any):
    return idx


def _get_key_with_getter(attr: str, idx: int, data: Any):
    return _get_attribute(data, attr)


class vfor(Generic[_T]):
    """render a list of items based on an array.


    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#vfor
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#vfor


    ## Examples
    ```python
    from ex4nicegui.reactive import rxui
    from ex4nicegui import to_ref
    items = to_ref(
        [
            {"message": "foo", "done": False},
            {"message": "bar", "done": True},
        ]
    )


    @rxui.vfor(items,key='message')
    def _(store: rxui.VforStore):
        msg_ref = store.get("message")  # this is ref object

        # type text into the input box and
        # the title of the checkbox changes sync
        with ui.card():
            rxui.input(value=msg_ref)
            rxui.checkbox(text=msg_ref, value=store.get("done"))

    ```

    """

    def __init__(self, data: Ref[List[_T]], *, key: Optional[str] = None) -> None:
        self._container = VforContainer()
        self._data = data
        self._get_key = (
            _get_key_with_index if key is None else partial(_get_key_with_getter, key)
        )
        self._store_map: Dict[Union[Any, int], StoreItem] = {}

    def __call__(self, fn: Callable[[VforStore], None]):
        def build_element(index: int, value):
            key = self._get_key(index, value)
            store = VforStore.create_from_ref(to_ref(value), self._data, index)

            with VforContainer() as element:
                fn(store)
            # element._props["data-vfor-key"] = f"{key}"
            # element.update()
            return (key, store, element)

        with self._container:
            for idx, value in enumerate(self._data.value):
                key, store, element = build_element(idx, value)
                self._store_map[key] = StoreItem(store, element.id)

        @on(self._data)
        def _():
            data_map = {
                self._get_key(idx, d): d for idx, d in enumerate(self._data.value)
            }

            @batch
            def _():
                temp_box = ui.element("div")

                element_map: Dict[int, ui.element] = {}
                for element in list(self._container):
                    element.move(temp_box)
                    element_map[element.id] = element

                new_store_map: Dict[Union[Any, int], StoreItem] = {}

                with self._container:
                    for idx, (key, value) in enumerate(data_map.items()):
                        store_item = self._store_map.get(key)
                        if store_item:
                            # `data` may have changed the value of a dictionary item,
                            # so should update the values in the store one by one.
                            store_item.store.update_item(value, idx)
                            element = element_map.get(store_item.elementId)
                            assert element
                            element.move(self._container)

                            new_store_map[key] = store_item
                        else:
                            # new row item
                            key, store, element = build_element(idx, value)
                            store_item = StoreItem(store, element.id)
                            element.move(self._container)
                            new_store_map[key] = store_item

                self._store_map.clear()
                self._store_map = new_store_map
                temp_box.delete()
