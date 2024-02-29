from __future__ import annotations
from nicegui.element import Element
from nicegui import ui
from ex4nicegui.utils.clientScope import _CLIENT_SCOPE_MANAGER
from ex4nicegui.utils.signals import (
    TReadonlyRef,
    TRef,
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
    Protocol,
    TypeVar,
    Generic,
    Union,
    cast,
    runtime_checkable,
)
from functools import partial
from dataclasses import dataclass
from signe.core.reactive import DictProxy as signe_DictProxy
from signe.core.scope import Scope

_T = TypeVar("_T")
_T_data = TGetterOrReadonlyRef[List[Any]]


@runtime_checkable
class GetItemProtocol(Protocol):
    def __getitem__(self, key):
        ...


@runtime_checkable
class SetItemProtocol(Protocol):
    def __setitem__(self, key, value):
        ...


class VforStore(Generic[_T]):
    def __init__(self, source: _T_data, index: int) -> None:
        self._source = source
        self._data_index = to_ref(index)

    @property
    def row_index(self):
        return self._data_index

    def get(self, attr: Optional[Union[str, int]] = None) -> TReadonlyRef[_T]:
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
                TReadonlyRef,
                to_ref_wrapper(
                    lambda: _get_attribute(item, attr),
                    setter,
                ),
            )

        def base_setter(value):
            self._source.value[self._data_index.value] = value

        return cast(
            TReadonlyRef,
            to_ref_wrapper(
                lambda: self._source.value[self._data_index.value],
                base_setter,
            ),
        )

    def update(self, index: int):
        self._data_index.value = index


@dataclass
class StoreItem:
    __slot__ = ["elementId"]
    store: VforStore
    elementId: int
    scope: Scope


def vmodel(ref: TGetterOrReadonlyRef[_T], *attrs: str) -> TRef[Any]:
    if not attrs:
        return cast(TRef, ref)

    def get_obj():
        if len(attrs) == 1:
            return ref.value, attrs[0]

        # gt 1
        obj = _get_attribute(ref.value, attrs[0])
        for attr in attrs[1:-1]:
            obj = _get_attribute(obj, attr)

        return obj, attrs[-1]

    def setter(value):
        obj, attr = get_obj()
        _set_attribute(obj, attr, value)

    def getter():
        obj, attr = get_obj()
        return _get_attribute(obj, attr)

    return cast(
        TRef,
        to_ref_wrapper(
            getter,
            setter,
        ),
    )


class VforContainer(Element, component="vfor.js"):
    pass


def _get_attribute(obj: Union[object, GetItemProtocol], name: Union[str, int]) -> Any:
    if isinstance(obj, (GetItemProtocol)):
        return obj[name]
    return getattr(obj, name)  # type: ignore


def _set_attribute(
    obj: Union[object, SetItemProtocol], name: Union[str, int], value: Any
) -> None:
    if isinstance(obj, SetItemProtocol):
        obj[name] = value
    else:
        setattr(obj, name, value)  # type: ignore


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
                scope = _CLIENT_SCOPE_MANAGER.new_scope()

                @scope.run
                def _():
                    fn(store)

            return key, element, store, scope

        with self._container:
            for idx, value in enumerate(self._data.value):
                key, element, store, scope = build_element(idx, value)
                self._store_map[key] = StoreItem(store, element.id, scope)

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
