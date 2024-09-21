from __future__ import annotations

from typing import (
    Any,
    Callable,
    Protocol,
    TypeVar,
)

import signe
from ex4nicegui.utils.signals import to_value, TMaybeRef
from nicegui.elements.mixins.disableable_element import DisableableElement


_T_DisableableBinder = TypeVar("_T_DisableableBinder", bound=DisableableElement)


class DisableableMixin(Protocol):
    _ui_effect: Callable[[Callable[..., Any]], signe.Effect[None]]

    @property
    def element(self) -> DisableableElement: ...

    def bind_enabled(self, value: TMaybeRef[bool]):
        @self._ui_effect
        def _():
            raw_value = to_value(value)
            self.element.set_enabled(raw_value)
            self.element._handle_enabled_change(raw_value)

        return self

    def bind_disable(self, value: TMaybeRef[bool]):
        @self._ui_effect
        def _():
            raw_value = not to_value(value)
            self.element.set_enabled(raw_value)
            self.element._handle_enabled_change(raw_value)

        return self
