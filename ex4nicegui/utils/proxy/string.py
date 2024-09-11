from typing import (
    Any,
    Iterable,
    List,
    Optional,
    SupportsIndex,
    Tuple,
    Union,
    overload,
)
from typing_extensions import LiteralString
from collections.abc import Iterator
import sys
from ex4nicegui.utils.signals import to_ref


class StringProxy(str):
    def __new__(cls, value):
        obj = super().__new__(cls, value)
        return obj

    def __init__(self, string: str):
        self._ref = to_ref(string)

    def __str__(self):
        return self._ref.value.__str__()

    def __repr__(self):
        return self._ref.value.__repr__()

    @overload
    def capitalize(self: LiteralString) -> LiteralString: ...
    @overload
    def capitalize(self) -> str: ...  # type: ignore[misc]
    def capitalize(self) -> str:
        return self._ref.value.capitalize()

    @overload
    def casefold(self: LiteralString) -> LiteralString: ...
    @overload
    def casefold(self) -> str: ...  # type: ignore[misc]
    def casefold(self) -> str:
        return self._ref.value.casefold()

    @overload
    def center(
        self: LiteralString, width: SupportsIndex, fillchar: LiteralString = " ", /
    ) -> LiteralString: ...
    @overload
    def center(self, width: SupportsIndex, fillchar: str = " ", /) -> str: ...  # type: ignore[misc]
    def center(self, width: SupportsIndex, fillchar: str = " ", /) -> str:
        return self._ref.value.center(width, fillchar)

    def count(
        self,
        sub: str,
        start: Optional[SupportsIndex] = ...,
        end: Optional[SupportsIndex] = ...,
        /,
    ) -> int:
        return self._ref.value.count(sub, start, end)

    def encode(self, encoding: str = "utf-8", errors: str = "strict") -> bytes:
        return self._ref.value.encode(encoding, errors)

    def endswith(
        self,
        suffix: Union[str, Tuple[str, ...]],
        start: Optional[SupportsIndex] = ...,
        end: Optional[SupportsIndex] = ...,
        /,
    ) -> bool:
        return self._ref.value.endswith(suffix, start, end)

    @overload
    def expandtabs(
        self: LiteralString, tabsize: SupportsIndex = 8
    ) -> LiteralString: ...
    @overload
    def expandtabs(self, tabsize: SupportsIndex = 8) -> str: ...  # type: ignore[misc]
    def expandtabs(self, tabsize: SupportsIndex = 8) -> str:
        return self._ref.value.expandtabs(tabsize)

    def find(
        self,
        sub: str,
        start: Optional[SupportsIndex] = ...,
        end: Optional[SupportsIndex] = ...,
        /,
    ) -> int:
        return self._ref.value.find(sub, start, end)

    @overload
    def format(
        self: LiteralString, *args: LiteralString, **kwargs: LiteralString
    ) -> LiteralString: ...
    @overload
    def format(self, *args: object, **kwargs: object) -> str: ...
    def format(self, *args: object, **kwargs: object) -> str:
        return self._ref.value.format(*args, **kwargs)

    def format_map(self, mapping, /) -> str:
        return self._ref.value.format_map(mapping)

    def index(
        self,
        sub: str,
        start: Optional[SupportsIndex] = ...,
        end: Optional[SupportsIndex] = ...,
        /,
    ) -> int:
        return self._ref.value.index(sub, start, end)

    def isalnum(self) -> bool:
        return self._ref.value.isalnum()

    def isalpha(self) -> bool:
        return self._ref.value.isalpha()

    def isascii(self) -> bool:
        return self._ref.value.isascii()

    def isdecimal(self) -> bool:
        return self._ref.value.isdecimal()

    def isdigit(self) -> bool:
        return self._ref.value.isdigit()

    def isidentifier(self) -> bool:
        return self._ref.value.isidentifier()

    def islower(self) -> bool:
        return self._ref.value.islower()

    def isnumeric(self) -> bool:
        return self._ref.value.isnumeric()

    def isprintable(self) -> bool:
        return self._ref.value.isprintable()

    def isspace(self) -> bool:
        return self._ref.value.isspace()

    def istitle(self) -> bool:
        return self._ref.value.istitle()

    def isupper(self) -> bool:
        return self._ref.value.isupper()

    @overload
    def join(
        self: LiteralString, iterable: Iterable[LiteralString], /
    ) -> LiteralString: ...
    @overload
    def join(self, iterable: Iterable[str], /) -> str: ...  # type: ignore[misc]
    def join(self, iterable: Iterable[str]) -> str:
        return self._ref.value.join(iterable)

    @overload
    def ljust(
        self: LiteralString, width: SupportsIndex, fillchar: LiteralString = " ", /
    ) -> LiteralString: ...
    @overload
    def ljust(self, width: SupportsIndex, fillchar: str = " ", /) -> str: ...  # type: ignore[misc]
    def ljust(self, width: SupportsIndex, fillchar: str = " ", /) -> str:
        return self._ref.value.ljust(width, fillchar)

    @overload
    def lower(self: LiteralString) -> LiteralString: ...
    @overload
    def lower(self) -> str: ...  # type: ignore[misc]
    def lower(self) -> str:
        return self._ref.value.lower()

    @overload
    def lstrip(
        self: LiteralString, chars: Optional[LiteralString] = None, /
    ) -> LiteralString: ...
    @overload
    def lstrip(self, chars: Optional[str] = None, /) -> str: ...  # type: ignore[misc]
    def lstrip(self, chars: Optional[str] = None, /) -> str:
        return self._ref.value.lstrip(chars)

    @overload
    def partition(
        self: LiteralString, sep: LiteralString, /
    ) -> Tuple[LiteralString, LiteralString, LiteralString]: ...
    @overload
    def partition(self, sep: str, /) -> Tuple[str, str, str]: ...  # type: ignore[misc]
    def partition(self, sep: str, /) -> Tuple[str, str, str]:
        return self._ref.value.partition(sep)

    @overload
    def replace(
        self: LiteralString,
        old: LiteralString,
        new: LiteralString,
        /,
        count: SupportsIndex = -1,
    ) -> LiteralString: ...
    @overload
    def replace(self, old: str, new: str, /, count: SupportsIndex = -1) -> str: ...  # type: ignore[misc]
    def replace(self, old: str, new: str, /, count: SupportsIndex = -1) -> str:
        return self._ref.value.replace(old, new, count)

    if sys.version_info >= (3, 13):

        @overload
        def removeprefix(
            self: LiteralString, prefix: LiteralString, /
        ) -> LiteralString: ...
        @overload
        def removeprefix(self, prefix: str, /) -> str: ...  # type: ignore[misc]
        def removeprefix(self, prefix: str, /):
            return self._ref.value.removeprefix(prefix)

        @overload
        def removesuffix(
            self: LiteralString, suffix: LiteralString, /
        ) -> LiteralString: ...
        @overload
        def removesuffix(self, suffix: str, /) -> str: ...  # type: ignore[misc]
        def removesuffix(self, suffix: str, /):
            return self._ref.value.removesuffix(suffix)

    def rfind(
        self,
        sub: str,
        start: Optional[SupportsIndex] = ...,
        end: Optional[SupportsIndex] = ...,
        /,
    ) -> int:
        return self._ref.value.rfind(sub, start, end)

    def rindex(
        self,
        sub: str,
        start: Optional[SupportsIndex] = ...,
        end: Optional[SupportsIndex] = ...,
        /,
    ) -> int:
        return self._ref.value.rindex(sub, start, end)

    @overload
    def rjust(
        self: LiteralString, width: SupportsIndex, fillchar: LiteralString = " ", /
    ) -> LiteralString: ...
    @overload
    def rjust(self, width: SupportsIndex, fillchar: str = " ", /) -> str: ...  # type: ignore[misc]
    def rjust(self, width: SupportsIndex, fillchar: str = " ", /) -> str:
        return self._ref.value.rjust(width, fillchar)

    @overload
    def rpartition(
        self: LiteralString, sep: LiteralString, /
    ) -> Tuple[LiteralString, LiteralString, LiteralString]: ...
    @overload
    def rpartition(self, sep: str, /) -> Tuple[str, str, str]: ...  # type: ignore[misc]
    def rpartition(self, sep: str, /) -> Tuple[str, str, str]:
        return self._ref.value.rpartition(sep)

    @overload
    def rsplit(
        self: LiteralString,
        sep: Optional[LiteralString] = None,
        maxsplit: SupportsIndex = -1,
    ) -> List[LiteralString]: ...
    @overload
    def rsplit(
        self, sep: Optional[str] = None, maxsplit: SupportsIndex = -1
    ) -> list[str]: ...  # type: ignore[misc]
    def rsplit(
        self, sep: Optional[str] = None, maxsplit: SupportsIndex = -1
    ) -> List[str]:
        return self._ref.value.rsplit(sep, maxsplit)

    @overload
    def rstrip(
        self: LiteralString, chars: Optional[LiteralString] = None, /
    ) -> LiteralString: ...
    @overload
    def rstrip(self, chars: Optional[str] = None, /) -> str: ...  # type: ignore[misc]
    def rstrip(self, chars: Optional[str] = None, /):
        return self._ref.value.rstrip(chars)

    @overload
    def split(
        self: LiteralString,
        sep: Optional[LiteralString] = None,
        maxsplit: SupportsIndex = -1,
    ) -> list[LiteralString]: ...
    @overload
    def split(
        self, sep: Optional[str] = None, maxsplit: SupportsIndex = -1
    ) -> list[str]: ...  # type: ignore[misc]
    def split(self, sep: Optional[str] = None, maxsplit: SupportsIndex = -1):
        return self._ref.value.split(sep, maxsplit)

    @overload
    def splitlines(
        self: LiteralString, keepends: bool = False
    ) -> list[LiteralString]: ...
    @overload
    def splitlines(self, keepends: bool = False) -> list[str]: ...  # type: ignore[misc]
    def splitlines(self, keepends: bool = False):
        return self._ref.value.splitlines(keepends)

    def startswith(
        self,
        prefix: Union[str, Tuple[str, ...]],
        start: Optional[SupportsIndex] = ...,
        end: Optional[SupportsIndex] = ...,
        /,
    ) -> bool:
        return self._ref.value.startswith(prefix, start, end)

    @overload
    def strip(
        self: LiteralString, chars: Optional[LiteralString] = None, /
    ) -> LiteralString: ...
    @overload
    def strip(self, chars: Optional[str] = None, /) -> str: ...  # type: ignore[misc]
    def strip(self, chars: Optional[str] = None, /):
        return self._ref.value.strip(chars)

    @overload
    def swapcase(self: LiteralString) -> LiteralString: ...
    @overload
    def swapcase(self) -> str: ...  # type: ignore[misc]
    def swapcase(self):
        return self._ref.value.swapcase()

    @overload
    def title(self: LiteralString) -> LiteralString: ...
    @overload
    def title(self) -> str: ...  # type: ignore[misc]
    def title(self):
        return self._ref.value.title()

    def translate(self, table, /) -> str:
        return self._ref.value.translate(table)

    @overload
    def upper(self: LiteralString) -> LiteralString: ...
    @overload
    def upper(self) -> str: ...  # type: ignore[misc]
    def upper(self):
        return self._ref.value.upper()

    @overload
    def zfill(self: LiteralString, width: SupportsIndex, /) -> LiteralString: ...
    @overload
    def zfill(self, width: SupportsIndex, /) -> str: ...  # type: ignore[misc]
    def zfill(self, width: SupportsIndex, /):
        return self._ref.value.zfill(width)

    # 特殊方法
    @overload
    def __add__(self: LiteralString, value: LiteralString, /) -> LiteralString: ...
    @overload
    def __add__(self, value: str, /) -> str: ...  # type: ignore[misc]
    def __add__(self, value: str):
        return self._ref.value.__add__(value)

    def __contains__(self, key: str, /) -> bool:
        return self._ref.value.__contains__(key)

    def __eq__(self, value: object, /) -> bool:
        return self._ref.value.__eq__(value)

    def __ge__(self, value: str, /) -> bool:
        return self._ref.value.__ge__(value)

    def __getitem__(self, key: Union[SupportsIndex, slice], /) -> str:
        return self._ref.value.__getitem__(key)

    def __gt__(self, value: str, /) -> bool:
        return self._ref.value.__gt__(value)

    def __hash__(self) -> int:
        return self._ref.value.__hash__()

    @overload
    def __iter__(self: LiteralString) -> Iterator[LiteralString]: ...
    @overload
    def __iter__(self) -> Iterator[str]: ...  # type: ignore[misc]
    def __iter__(self) -> Iterator[str]:
        return self._ref.value.__iter__()

    def __le__(self, value: str, /) -> bool:
        return self._ref.value.__le__(value)

    def __len__(self) -> int:
        return self._ref.value.__len__()

    def __lt__(self, value: str, /) -> bool:
        return self._ref.value.__lt__(value)

    @overload
    def __mod__(
        self: LiteralString, value: Union[LiteralString, Tuple[LiteralString, ...]], /
    ) -> LiteralString: ...
    @overload
    def __mod__(self, value: Any, /) -> str: ...
    def __mod__(self, value: Any):
        return self._ref.value.__mod__(value)

    @overload
    def __mul__(self: LiteralString, value: SupportsIndex, /) -> LiteralString: ...
    @overload
    def __mul__(self, value: SupportsIndex, /) -> str: ...  # type: ignore[misc]
    def __mul__(self, value: SupportsIndex):
        return self._ref.value.__mul__(value)

    def __ne__(self, value: object, /) -> bool:
        return self._ref.value.__ne__(value)

    @overload
    def __rmul__(self: LiteralString, value: SupportsIndex, /) -> LiteralString: ...
    @overload
    def __rmul__(self, value: SupportsIndex, /) -> str: ...  # type: ignore[misc]
    def __rmul__(self, value: SupportsIndex):
        return self._ref.value.__rmul__(value)

    def __getnewargs__(self) -> Tuple[str]:
        return self._ref.value.__getnewargs__()


class StringDescriptor:
    def __init__(self, name: str, value: str) -> None:
        self.value = value
        self.name = name

    def __get__(self, instance: object, owner: Any):
        if instance is None:
            return self

        proxy = instance.__dict__.get(self.name)
        if proxy is None:
            proxy = StringProxy(self.value)
            instance.__dict__[self.name] = proxy

        return proxy

    def __set__(self, instance: object, value: str) -> None:
        proxy = instance.__dict__.get(self.name)
        if proxy is None:
            proxy = StringProxy(self.value)
            instance.__dict__[self.name] = proxy

        proxy._ref.value = value
