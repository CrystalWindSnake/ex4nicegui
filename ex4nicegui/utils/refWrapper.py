import signe
from typing import (
    TypeVar,
    Generic,
    Optional,
    Callable,
    cast,
)
import warnings
from .types import (
    TGetterOrReadonlyRef,
)

T = TypeVar("T")


class RefWrapper(Generic[T]):
    __slot__ = ("_getter_fn", "_setter_fn", "")

    def __init__(
        self,
        getter_or_ref: TGetterOrReadonlyRef[T],
        setter_or_ref: Optional[Callable[[T], None]] = None,
    ):
        if signe.is_signal(getter_or_ref):
            self._getter_fn = lambda: getter_or_ref.value

            def ref_setter(v):
                getter_or_ref.value = v  # type: ignore

            self._setter_fn = ref_setter
        elif isinstance(getter_or_ref, Callable):
            self._getter_fn = getter_or_ref
            self._setter_fn = setter_or_ref or (lambda x: None)
        else:
            self._getter_fn = lambda: getter_or_ref
            self._setter_fn = lambda x: None

        self._is_readonly = False

    @property
    def value(self) -> T:
        return cast(T, self._getter_fn())

    @value.setter
    def value(self, new_value: T):
        if self._is_readonly:
            warnings.warn("readonly ref cannot be assigned.")
            return
        return self._setter_fn(new_value)


def to_ref_wrapper(
    getter_or_ref: TGetterOrReadonlyRef[T],
    setter_or_ref: Optional[Callable[[T], None]] = None,
):
    return RefWrapper(getter_or_ref, setter_or_ref)
