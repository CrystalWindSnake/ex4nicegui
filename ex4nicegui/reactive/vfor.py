from nicegui.element import Element
from nicegui import ui
from signe import batch
from ex4nicegui.utils.signals import Ref, on, to_ref
from typing import Any, Callable, List, Optional, TypeVar, Generic
from itertools import zip_longest
from weakref import WeakValueDictionary

_T = TypeVar("_T")


class VforStore(Generic[_T]):
    def __init__(self, r: Ref[_T], source: Ref[List[Any]], index: int) -> None:
        self._ref = r
        self._source = source
        self._index = index
        self._attr_cache: WeakValueDictionary[str, Ref] = WeakValueDictionary()

    @property
    def row_index(self):
        return self._index

    def get(self, attr: Optional[str] = None):
        if attr:
            ref = self._attr_cache.get(attr)
            if ref is None:
                ref = to_ref(self._ref.value[attr])  # type: ignore
                self._attr_cache[attr] = ref

                @on(ref, onchanges=True)
                def _():
                    self._source.value[self._index][attr] = ref.value
                    self._source.value = self._source.value

            return ref
        return self._ref

    def update_item(self, item):
        if isinstance(item, dict):
            for attr, ref in self._attr_cache.items():
                ref.value = item[attr]

        self._ref.value = item  # type: ignore

    @classmethod
    def create_from_ref(cls, ref: Ref[_T], source: Ref[List], index: int):
        return cls(ref, source, index)


class VforContainer(Element, component="vfor.js"):
    pass


class vfor(Generic[_T]):
    def __init__(self, data: Ref[List[_T]], key: Optional[str] = None) -> None:
        self._box = VforContainer()
        self._data = data

    def __call__(self, fn: Callable[[VforStore], ui.element]):
        clone_stores = [
            VforStore.create_from_ref(to_ref(d), self._data, idx)
            for idx, d in enumerate(self._data.value)
        ]

        def build_element(idx, store: VforStore):
            ele = fn(store)
            ele._props["data-vfor-key"] = f"{idx}"
            ele.update()

        with self._box:
            for idx, store in enumerate(clone_stores):
                build_element(idx, store)

        @on(self._data)
        def _():
            elements = list(self._box)

            will_dels: List[ui.element] = []
            will_del_clones = []

            will_add_clone_refs = []

            with self._box:

                @batch
                def _():
                    for idx, (value, element, store) in enumerate(
                        zip_longest(self._data.value, elements, clone_stores)
                    ):
                        if value is None:
                            will_dels.append(element)
                            will_del_clones.append(store)
                            continue

                        if element is None:
                            store = VforStore.create_from_ref(
                                to_ref(value), self._data, idx
                            )
                            will_add_clone_refs.append((idx, store))
                            build_element(idx, store)
                            continue

                        if value != store.get().value:
                            store.update_item(value)

                    for element in will_dels:
                        element.delete()

                    for idx, store in will_add_clone_refs:
                        clone_stores.append(store)

                    for store in will_del_clones:
                        clone_stores.remove(store)
