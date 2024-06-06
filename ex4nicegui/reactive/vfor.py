from __future__ import annotations
from nicegui.element import Element
from nicegui import ui
from ex4nicegui.utils.clientScope import _CLIENT_SCOPE_MANAGER
from ex4nicegui.utils.signals import (
    TReadonlyRef,
    on,
    to_ref,
    to_ref_wrapper,
    TGetterOrReadonlyRef,
    to_value,
    is_reactive,
    RefWrapper,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    TypeVar,
    Generic,
    Union,
    cast,
)
from functools import partial
from dataclasses import dataclass
from signe.core.scope import Scope
from ex4nicegui.reactive.systems.object_system import get_attribute
from ex4nicegui.reactive.empty import Empty

_T = TypeVar("_T")
_T_data = Union[List[Any], TGetterOrReadonlyRef[List[Any]], RefWrapper]


class VforItem(Empty):
    pass


class VforContainer(Element, component="vfor.js"):
    def __init__(self) -> None:
        super().__init__()
        self._props["itemIds"] = []

    def update_items(self, item_ids: List[Dict]):
        self._props["itemIds"] = item_ids
        self.update()


class VforStore(Generic[_T]):
    def __init__(self, source: _T_data, index: int) -> None:
        self._source = source
        self._data_index = to_ref(index)

    @property
    def row_index(self):
        return self._data_index

    def get(self) -> TReadonlyRef[_T]:
        def base_setter(value):
            to_value(self._source)[self._data_index.value] = value

        wrapper = to_ref_wrapper(
            lambda: to_value(self._source)[self._data_index.value],
            base_setter,
        )
        wrapper._is_readonly = True

        return cast(TReadonlyRef, wrapper)

    def update(self, index: int):
        self._data_index.value = index


@dataclass
class StoreItem:
    __slot__ = ["elementId"]
    store: VforStore
    elementId: int
    scope: Scope


def _get_key_with_index(idx: int, data: Any):
    return idx


def _get_key_with_getter(attr: str, idx: int, data: Any):
    return get_attribute(data, attr)


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
        key: Optional[Union[str, Callable[[int, Any], Any]]] = None,
    ) -> None:
        self._vfor_container = VforContainer()
        self._data = to_ref_wrapper(lambda: data) if is_reactive(data) else data
        self._get_key = _get_key_with_index

        if isinstance(key, str):
            self._get_key = partial(_get_key_with_getter, key)
        elif isinstance(key, Callable):
            self._get_key = key

        self._store_map: Dict[Union[Any, int], StoreItem] = {}

    def __call__(self, fn: Callable[[Any], None]):
        def build_element(index: int, value):
            key = self._get_key(index, value)

            with self._vfor_container, VforItem() as element:
                store = VforStore(self._data, index)  # type: ignore
                scope = _CLIENT_SCOPE_MANAGER.new_scope()

                @scope.run
                def _():
                    fn(store)

            return key, element, store, scope

        for idx, value in enumerate(to_value(self._data)):  # type: ignore
            key, element, store, scope = build_element(idx, value)
            self._store_map[key] = StoreItem(store, element.id, scope)

        ng_client = ui.context.client

        @on(self._data, deep=True)
        def _():
            data_map = {
                self._get_key(idx, d): d for idx, d in enumerate(to_value(self._data))
            }

            for idx, (key, value) in enumerate(data_map.items()):
                store_item = self._store_map.get(key)
                if store_item:
                    # `data` may have changed the value of a dictionary item,
                    # so should update the values in the store one by one.
                    store_item.store.update(idx)

                else:
                    # new row item
                    key, element, store, score = build_element(idx, value)
                    self._store_map[key] = StoreItem(store, element.id, score)

            # remove item
            remove_items = [
                (key, value)
                for key, value in self._store_map.items()
                if key not in data_map
            ]

            for key, item in remove_items:
                target = ng_client.elements.get(item.elementId)
                self._vfor_container.remove(target)  # type: ignore
                item.scope.dispose()
                del self._store_map[key]

            self._vfor_container.update_items(
                [
                    {"key": key, "elementId": self._store_map.get(key).elementId}  # type: ignore
                    for key in data_map.keys()
                ]
            )
