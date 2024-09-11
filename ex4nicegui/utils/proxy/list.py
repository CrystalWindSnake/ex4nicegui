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
from . import utils


_T = TypeVar("_T")
_S = TypeVar("_S")


class ListProxy(list, Generic[_T]):
    def __init__(self, value: List[_T]):
        from ex4nicegui.utils.signals import deep_ref

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
    # Use List[SupportsRichComparisonT] for the first overload rather than [SupportsRichComparison]
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
    def __getitem__(self, s: slice, /) -> List[_T]: ...

    def __getitem__(self, i: Union[SupportsIndex, slice], /) -> Union[_T, List[_T]]:
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
    def __add__(self, value: List[_T], /) -> List[_T]: ...
    @overload
    def __add__(self, value: List[_S], /) -> List[Union[_S, _T]]: ...

    def __add__(
        self, value: Union[List[_T], List[_S]], /
    ) -> Union[List[_T], List[Union[_S, _T]]]:
        return self._ref.value.__add__(utils.to_value(value))

    def __iadd__(self, value: Iterable[_T], /) -> Self:  # type: ignore[misc]
        self._ref.value.__iadd__(utils.to_value(value))
        return self

    def __mul__(self, value: SupportsIndex, /) -> List[_T]:
        return self._ref.value.__mul__(utils.to_value(value))

    def __rmul__(self, value: SupportsIndex, /) -> List[_T]:
        return self._ref.value.__rmul__(utils.to_value(value))

    def __imul__(self, value: SupportsIndex, /) -> Self:
        self._ref.value.__imul__(utils.to_value(value))
        return self

    def __contains__(self, key: object, /) -> bool:
        return self._ref.value.__contains__(key)

    def __reversed__(self) -> Iterator[_T]:
        return self._ref.value.__reversed__()

    def __gt__(self, value: List[_T], /) -> bool:
        return self._ref.value.__gt__(utils.to_value(value))

    def __ge__(self, value: List[_T], /) -> bool:
        return self._ref.value.__ge__(utils.to_value(value))

    def __lt__(self, value: List[_T], /) -> bool:
        return self._ref.value.__lt__(utils.to_value(value))

    def __le__(self, value: List[_T], /) -> bool:
        return self._ref.value.__le__(utils.to_value(value))

    def __eq__(self, value: object, /) -> bool:
        return self._ref.value.__eq__(utils.to_value(value))
