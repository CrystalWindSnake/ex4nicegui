from __future__ import annotations
from nicegui.element import Element
from nicegui import ui
from ex4nicegui.utils.clientScope import _CLIENT_SCOPE_MANAGER
from ex4nicegui.utils.signals import (
    Ref,
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
    Literal,
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
    def __init__(self, transition_props: Optional[Dict[str, Any]] = None) -> None:
        super().__init__()
        self._props["itemIds"] = []

        if transition_props:
            self._props["transitionProps"] = transition_props

    def update_items(self, item_ids: List[Dict]):
        self._props["itemIds"] = item_ids
        self.update()


def wrapper_getter_setter(ref: Ref, index: Ref[int], *keys: Union[str, int]):
    proxy = ref.value

    def getter():
        item = proxy[index.value]
        result = item

        for k in keys:
            result = result[k]
        return result

    def setter(value):
        item = proxy[index.value]

        if len(keys) == 0:
            proxy[index.value] = value

        if len(keys) == 1:
            item[keys[0]] = value
            return

        obj = item[keys[0]]
        for k in keys[1:-1]:
            obj = obj[k]
        obj[keys[-1]] = value

    return getter, setter


class VforStoreItem(Generic[_T], RefWrapper[_T]):
    def __init__(
        self,
        source: _T_data,
        index: Ref[int],
        keys: Optional[List[Union[str, int]]] = None,
    ) -> None:
        self._source = source
        self._data_index = index
        self._keys = keys or []

        getter, setter = wrapper_getter_setter(source, index, *self._keys)
        super().__init__(getter, setter)

    def __getitem__(self, key: Union[str, int]):
        return VforStoreItem(self._source, self._data_index, self._keys + [key])


class VforStore(Generic[_T]):
    def __init__(self, source: _T_data, index: int) -> None:
        self._source = source
        self._raw_index = index
        self._data_index = to_ref(index)

    @property
    def row_index(self):
        """Returns the responsive index of the current row."""
        return self._data_index

    @property
    def raw_index(self):
        """Returns the index of the current row."""
        return self._raw_index

    def get_item(self) -> _T:
        """Returns the current item."""
        return to_value(self._source)[self.raw_index]  # type: ignore

    def get(self) -> Ref[_T]:
        """Returns a ref object of the current item.
        Suitable for immutable types such as `int`, `str`, `float`, etc.
        """
        return VforStoreItem(self._source, self._data_index)  # type: ignore

    def update(self, index: int):
        self._data_index.value = index


@dataclass
class StoreItem:
    __slot__ = ["elementId"]
    store: VforStore
    elementId: int
    scope: Scope


def _get_key_with_getter(attr: str, idx: int, data: Any):
    return get_attribute(data, attr)


class vfor(Generic[_T]):
    """render a list of items based on an array.


    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#vfor
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#vfor


    ## Examples

    .. code-block:: python
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

    """

    def __init__(
        self,
        data: _T_data,
        *,
        key: Optional[Union[str, Callable[[int, Any], Any]]] = None,
    ) -> None:
        self._data = to_ref_wrapper(lambda: data) if is_reactive(data) else data
        self._get_key = vfor.index_key
        self._transition_props = {}

        if isinstance(key, str):
            self._get_key = partial(_get_key_with_getter, key)
        elif isinstance(key, Callable):
            self._get_key = key

        self._store_map: Dict[Union[Any, int], StoreItem] = {}

    def transition_group(
        self,
        css=True,
        name: Optional[str] = "list",
        duration: Optional[float] = None,
        type: Optional[Literal["transition", "animation"]] = None,
        mode: Optional[Literal["in-out", "out-in", "default"]] = None,
        appear=False,
    ):
        kws = {k: v for k, v in locals().items() if k != "self" and v is not None}
        self._transition_props.update(**kws)

        return self

    def __call__(self, fn: Callable[[Any], None]):
        _vfor_container = VforContainer(self._transition_props)

        def build_element(index: int, value):
            key = self._get_key(index, value)

            with _vfor_container, VforItem() as element:
                store = VforStore(self._data, index)  # type: ignore
                scope = _CLIENT_SCOPE_MANAGER.new_scope()

                @scope.run
                def _():
                    fn(store)

            return key, element, store, scope

        ng_client = ui.context.client

        @on(self._data, deep=True, priority_level=-1)
        def _():
            data_map = {
                self._get_key(idx, d): d for idx, d in enumerate(to_value(self._data))
            }

            # remove item if it's not in the new data
            remove_items = [
                (key, value)
                for key, value in self._store_map.items()
                if key not in data_map
            ]

            for key, item in remove_items:
                target = ng_client.elements.get(item.elementId)
                _vfor_container.remove(target)  # type: ignore
                item.scope.dispose()
                del self._store_map[key]

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

            item_ids = [
                {"key": key, "elementId": self._store_map.get(key).elementId}  # type: ignore
                for key in data_map.keys()
            ]

            _vfor_container.update_items(item_ids)

    @staticmethod
    def value_key(_, data):
        return data

    @staticmethod
    def index_key(idx, _):
        return idx
