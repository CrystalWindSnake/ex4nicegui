from __future__ import annotations
from nicegui.element import Element
from nicegui import ui
from ex4nicegui.utils.signals import ReadonlyRef, on, to_ref, to_ref_wrapper
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    TypeVar,
    Generic,
    Union,
    cast,
)
from functools import partial
from dataclasses import dataclass
from signe.core.reactive import DictProxy as signe_DictProxy


_T = TypeVar("_T")
_T_data = ReadonlyRef[List[Any]]


class VforStore(Generic[_T]):
    def __init__(self, source: _T_data, index: int) -> None:
        self._source = source
        self._data_index = to_ref(index)

    @property
    def row_index(self):
        return self._data_index

    def get(self, attr: Optional[str] = None) -> _T:
        item = self._source.value[self._data_index.value]

        if attr:
            setter = None
            if isinstance(item, signe_DictProxy):

                def base_setter(value):
                    item[attr] = value

                setter = base_setter
            else:
                setter = lambda x: _set_attribute(item, attr, x)  # noqa: E731

            return cast(
                _T,
                to_ref_wrapper(
                    lambda: _get_attribute(item, attr),
                    setter,
                ),
            )

        return item

    def update(self, index: int):
        self._data_index.value = index


@dataclass
class StoreItem:
    __slot__ = ["elementId"]
    store: VforStore
    elementId: int


class VforContainer(Element, component="vfor.js"):
    pass


def _get_attribute(obj: Union[object, Mapping], name: str) -> Any:
    if isinstance(obj, Mapping):
        return obj[name]
    return getattr(obj, name)


def _set_attribute(obj: Union[object, Mapping], name: str, value: Any) -> None:
    if isinstance(obj, dict):
        obj[name] = value
    else:
        setattr(obj, name, value)


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

    def __init__(
        self,
        data: _T_data,
        *,
        key: Optional[str] = None,
    ) -> None:
        self._container = VforContainer()
        self._data = data
        self._get_key = (
            _get_key_with_index if key is None else partial(_get_key_with_getter, key)
        )
        self._store_map: Dict[Union[Any, int], StoreItem] = {}

    def __call__(self, fn: Callable[[Any], None]):
        def build_element(index: int, value):
            key = self._get_key(index, value)
            with VforContainer() as element:
                store = VforStore(self._data, index)
                fn(store)
            return key, element, store

        with self._container:
            for idx, value in enumerate(self._data.value):
                key, element, store = build_element(idx, value)
                self._store_map[key] = StoreItem(store, element.id)

        @on(self._data, deep=True)
        def _():
            data_map = {
                self._get_key(idx, d): d for idx, d in enumerate(self._data.value)
            }

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
                        store_item.store.update(idx)
                        element = element_map.get(store_item.elementId)
                        assert element
                        element.move(self._container)

                        new_store_map[key] = store_item
                    else:
                        # new row item
                        key, element, store = build_element(idx, value)
                        store_item = StoreItem(store, element.id)
                        element.move(self._container)
                        new_store_map[key] = store_item

            self._store_map.clear()
            self._store_map = new_store_map
            temp_box.delete()
