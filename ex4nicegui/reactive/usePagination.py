import sys
from ex4nicegui.utils.signals import (
    ref_computed,
    to_ref,
    to_value,
    effect,
    _TMaybeRef as TMaybeRef,
)
from typing import Any, TypeVar
from typing_extensions import Protocol
import math
from ex4nicegui.reactive.q_pagination import PaginationBindableUi


def _clamp(value, min_v, max_v) -> int:
    return min(max(value, min_v), max_v)


class _SourceProtocol(Protocol):
    def __len__(self) -> int:
        ...

    def __getitem__(self, __idx: slice) -> Any:
        ...


class PaginationRef:
    def __init__(
        self,
        source: TMaybeRef[_SourceProtocol],
        page_size: TMaybeRef[int] = 10,
        page: TMaybeRef[int] = 1,
    ) -> None:
        total = ref_computed(lambda: len(to_value(source)))

        # -1 => 1 or 5 =>5
        self.__cur_page_size = ref_computed(
            lambda: _clamp(to_value(page_size), 1, sys.maxsize)
        )

        #
        self.__page_count = ref_computed(
            lambda: max(1, math.ceil(to_value(total) / to_value(self.__cur_page_size)))
        )
        self.__current_page = to_ref(0)

        @effect
        def _():
            self.__current_page.value = _clamp(
                to_value(page), 1, to_value(self.__page_count)
            )

        @ref_computed
        def cur_source():
            start = (self.__current_page.value - 1) * self.__cur_page_size.value
            end = start + self.__cur_page_size.value
            return to_value(source)[start:end]

        self.__cur_source = cur_source

    def prev(self):
        self.__current_page.value -= 1

    def next(self):
        self.__current_page.value += 1

    @property
    def page_count(self):
        return self.__page_count

    @property
    def current_page(self):
        return self.__current_page

    @property
    def current_page_size(self):
        return self.__cur_page_size

    @property
    def current_source(self):
        return self.__cur_source

    @property
    def is_first_page(self):
        @ref_computed
        def cp():
            return self.current_page.value == 1

        return cp

    @property
    def is_last_page(self):
        @ref_computed
        def cp():
            return self.current_page.value == self.page_count.value

        return cp

    def create_q_pagination(self):
        page = PaginationBindableUi(
            self.current_page, max=self.page_count, direction_links=True
        )
        page.props("boundary-links")
        return page
