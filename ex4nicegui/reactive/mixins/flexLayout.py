from typing import (
    Any,
    Callable,
    Protocol,
)
from typing_extensions import Self
import signe
from ex4nicegui.utils.signals import to_value, TMaybeRef
from nicegui import ui


class FlexWrapMixin(Protocol):
    _ui_signal_on: Callable[[Callable[..., Any]], signe.Effect[None]]

    @property
    def element(self) -> ui.element:
        ...

    def bind_style(self, classes) -> Self:
        ...

    def bind_wrap(self, value: TMaybeRef[bool]) -> Self:
        return self.bind_style(
            {"flex-wrap": lambda: "wrap" if to_value(value) else "nowrap"}
        )

    def _bind_specified_props(self, prop: str, value: TMaybeRef[Any]):
        if prop == "wrap":
            return self.bind_wrap(value)

        return None


class FlexAlignItemsMixin(Protocol):
    _ui_signal_on: Callable[[Callable[..., Any]], signe.Effect[None]]

    @property
    def element(self) -> ui.element:
        ...

    def bind_classes(self, classes) -> Self:
        ...

    def bind_align_items(self, value: TMaybeRef[str]):
        return self.bind_classes(lambda: f"items-{to_value(value)}")

    def _bind_specified_props(self, prop: str, value: TMaybeRef[Any]):
        if prop == "align-items":
            return self.bind_align_items(value)

        return None
