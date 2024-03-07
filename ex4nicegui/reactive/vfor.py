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
from .utils import get_attribute

_T = TypeVar("_T")
_T_data = TGetterOrReadonlyRef[List[Any]]


class VforStore(Generic[_T]):
    def __init__(self, source: _T_data, index: int) -> None:
        self._source = source
        self._data_index = to_ref(index)

    @property
    def row_index(self):
        return self._data_index

    def get(self) -> TReadonlyRef[_T]:
        def base_setter(value):
            self._source.value[self._data_index.value] = value

        wrapper = to_ref_wrapper(
            lambda: self._source.value[self._data_index.value],
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


class VforContainer(Element, component="vfor.js"):
    _applyTransitionGroupName = "applyTransitionGroup"

    def __init__(self, transition_group=False) -> None:
        super().__init__()
        self._transition_group = transition_group
        self._props[self._applyTransitionGroupName] = transition_group

    def apply_transition_group(self, args: Dict[str, Any]):
        self._transition_group = True
        self._props[self._applyTransitionGroupName] = True
        self._props["transitionGroupArgs"] = args
        self.update()

    def update_child_order_keys(self, keys: List[Any]):
        print(f"keys:{keys=}")
        self._props["childOrderKey"] = keys
        self.update()


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
        self._container = VforContainer()
        self._data = data
        self._get_key = _get_key_with_index

        if isinstance(key, str):
            self._get_key = partial(_get_key_with_getter, key)
        elif isinstance(key, Callable):
            self._get_key = key

        # self._get_key = (
        #     _get_key_with_index if key is None else partial(_get_key_with_getter, key)
        # )
        self._store_map: Dict[Union[Any, int], StoreItem] = {}

    def transition_group(self, *, name="list", css=True):
        self._container.apply_transition_group({"name": name, "css": css})
        return self

    def __call__(self, fn: Callable[[Any], None]):
        def build_element(index: int, value):
            key = self._get_key(index, value)
            with VforContainer() as element:
                store = VforStore(self._data, index)
                scope = _CLIENT_SCOPE_MANAGER.new_scope()

                @scope.run
                def _():
                    fn(store)

            return key, element, store, scope

        with self._container:
            for idx, value in enumerate(self._data.value):
                key, element, store, scope = build_element(idx, value)
                self._store_map[key] = StoreItem(store, element.id, scope)

        # records init children position
        if self._container._transition_group:
            self._container.update_child_order_keys(list(self._store_map.keys()))

        @on(self._data, deep=True, onchanges=True)
        def _():
            print()
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
                        key, element, store, score = build_element(idx, value)
                        store_item = StoreItem(store, element.id, score)
                        element.move(self._container)
                        new_store_map[key] = store_item

            del_store_items = tuple(
                value
                for key, value in self._store_map.items()
                if key not in new_store_map
            )

            for store_item in del_store_items:
                store_item.scope.dispose()

            self._store_map.clear()
            self._store_map = new_store_map
            temp_box.delete()
            print(f"data:{self._data.value=}")
            if self._container._transition_group:
                self._container.update_child_order_keys(list(self._store_map.keys()))
