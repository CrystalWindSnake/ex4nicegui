from __future__ import annotations

from typing import (
    Any,
    Callable,
    Protocol,
    TypeVar,
)

import signe
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    to_value,
)
from nicegui.elements.mixins.disableable_element import DisableableElement


_T_DisableableBinder = TypeVar("_T_DisableableBinder", bound=DisableableElement)


class DisableableMixin(Protocol):
    _ui_effect: Callable[[Callable[..., Any]], signe.Effect[None]]

    @property
    def element(self) -> DisableableElement:
        ...

    def bind_enabled(self, ref_ui: TGetterOrReadonlyRef[bool]):
        @self._ui_effect
        def _():
            value = to_value(ref_ui)
            self.element.set_enabled(value)
            self.element._handle_enabled_change(value)

        return self

    def bind_disable(self, ref_ui: TGetterOrReadonlyRef[bool]):
        @self._ui_effect
        def _():
            value = not to_value(ref_ui)
            self.element.set_enabled(value)
            self.element._handle_enabled_change(value)

        return self
