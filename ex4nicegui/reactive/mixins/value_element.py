from typing import Any, Callable, Protocol, Generic, TypeVar
from typing_extensions import Self
import signe
from ex4nicegui.utils.signals import to_value, TMaybeRef
from nicegui.elements.mixins.value_element import ValueElement
from ex4nicegui.utils.types import TGetterOrReadonlyRef

T = TypeVar("T", contravariant=True)


class ValueElementMixin(Protocol, Generic[T]):
    _ui_signal_on: Callable[[Callable[..., Any]], signe.Effect[None]]

    @property
    def element(self) -> ValueElement:
        ...

    def bind_value(self, value: TMaybeRef[T]):
        @self._ui_signal_on(value)  # type: ignore
        def _():
            self.element.set_value(to_value(value))

        return self

    def _bind_specified_props(self, prop: str, value: TMaybeRef[T]):
        if prop == "value":
            return self.bind_value(value)

        return None
