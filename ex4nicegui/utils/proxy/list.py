import sys
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    List,
    SupportsIndex,
    TypeVar,
    Generic,
    Union,
    overload,
)
from typing_extensions import Self
from ex4nicegui.utils.signals import deep_ref

_T = TypeVar("_T")
_S = TypeVar("_S")


class ListProxy(list, Generic[_T]):
    def __init__(self, value: List[_T]):
        super().__init__(value)
        self._ref = deep_ref(value)

    def copy(self) -> List:
        return self._ref.value.copy()

    def append(self, object: _T, /) -> None:
        self._ref.value.append(object)

    def extend(self, iterable: Iterable[_T], /) -> None:
        self._ref.value.extend(iterable)

    def pop(self, index: SupportsIndex = -1, /) -> _T:
        return self._ref.value.pop(index)

    # Signature of `list.index` should be kept in line with `collections.UserList.index()`
    # and multiprocessing.managers.ListProxy.index()
    def index(
        self, value: _T, start: SupportsIndex = 0, stop: SupportsIndex = sys.maxsize, /
    ) -> int:
        return self._ref.value.index(value, start, stop)

    def count(self, value: _T, /) -> int:
        return self._ref.value.count(value)

    def insert(self, index: SupportsIndex, object: _T, /) -> None:
        self._ref.value.insert(index, object)

    def remove(self, value: _T, /) -> None:
        self._ref.value.remove(value)

    # Signature of `list.sort` should be kept inline with `collections.UserList.sort()`
    # and multiprocessing.managers.ListProxy.sort()
    #
    # Use list[SupportsRichComparisonT] for the first overload rather than [SupportsRichComparison]
    # to work around invariance
    @overload
    def sort(self: list, *, key: None = None, reverse: bool = False) -> None: ...
    @overload
    def sort(self, *, key: Callable[[_T], Any], reverse: bool = False) -> None: ...

    def sort(
        self, *, key: Union[Callable[[_T], Any], None] = None, reverse: bool = False
    ) -> None:
        self._ref.value.sort(key=key, reverse=reverse)  # type: ignore

    def __len__(self) -> int:
        return len(self._ref.value)

    def __iter__(self) -> Iterator[_T]:
        return iter(self._ref.value)

    @overload
    def __getitem__(self, i: SupportsIndex, /) -> _T: ...
    @overload
    def __getitem__(self, s: slice, /) -> list[_T]: ...

    def __getitem__(self, i: Union[SupportsIndex, slice], /) -> Union[_T, list[_T]]:
        return self._ref.value.__getitem__(i)

    @overload
    def __setitem__(self, key: SupportsIndex, value: _T, /) -> None: ...
    @overload
    def __setitem__(self, key: slice, value: Iterable[_T], /) -> None: ...

    def __setitem__(
        self, key: Union[SupportsIndex, slice], value: Union[_T, Iterable[_T]], /
    ) -> None:
        self._ref.value.__setitem__(key, value)

    def __delitem__(self, key: Union[SupportsIndex, slice], /) -> None:
        self._ref.value.__delitem__(key)

    # Overloading looks unnecessary, but is needed to work around complex mypy problems
    @overload
    def __add__(self, value: list[_T], /) -> list[_T]: ...
    @overload
    def __add__(self, value: list[_S], /) -> list[Union[_S, _T]]: ...

    def __add__(
        self, value: Union[list[_T], list[_S]], /
    ) -> Union[list[_T], list[Union[_S, _T]]]:
        return self._ref.value.__add__(value)

    def __iadd__(self, value: Iterable[_T], /) -> Self:  # type: ignore[misc]
        self._ref.value.__iadd__(value)
        return self

    def __mul__(self, value: SupportsIndex, /) -> list[_T]:
        return self._ref.value.__mul__(value)

    def __rmul__(self, value: SupportsIndex, /) -> list[_T]:
        return self._ref.value.__rmul__(value)

    def __imul__(self, value: SupportsIndex, /) -> Self:
        self._ref.value.__imul__(value)
        return self

    def __contains__(self, key: object, /) -> bool:
        return self._ref.value.__contains__(key)

    def __reversed__(self) -> Iterator[_T]:
        return self._ref.value.__reversed__()

    def __gt__(self, value: list[_T], /) -> bool:
        return self._ref.value.__gt__(value)

    def __ge__(self, value: list[_T], /) -> bool:
        return self._ref.value.__ge__(value)

    def __lt__(self, value: list[_T], /) -> bool:
        return self._ref.value.__lt__(value)

    def __le__(self, value: list[_T], /) -> bool:
        return self._ref.value.__le__(value)

    def __eq__(self, value: object, /) -> bool:
        return self._ref.value.__eq__(value)


class ListDescriptor:
    def __init__(self, name: str, value: List) -> None:
        self.value = value
        self.name = name

    def __get__(self, instance: object, owner: Any):
        if instance is None:
            return self

        proxy = instance.__dict__.get(self.name)
        if proxy is None:
            proxy = ListProxy(self.value)
            instance.__dict__[self.name] = proxy

        return proxy

    def __set__(self, instance: object, value: List) -> None:
        proxy = instance.__dict__.get(self.name)
        if proxy is None:
            proxy = ListProxy(self.value)
            instance.__dict__[self.name] = proxy

        proxy._ref.value = value
