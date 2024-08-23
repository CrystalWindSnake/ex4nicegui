from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
)
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    _TMaybeRef as TMaybeRef,
    to_value,
)
from nicegui import ui
from .base import BindableUi

T = TypeVar("T")


class SwitchBindableUi(BindableUi[ui.switch]):
    def __init__(
        self,
        text: TMaybeRef[str] = "",
        *,
        value: TMaybeRef[bool] = False,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "text",
                "value",
            ],
            v_model=("value", "on_change"),
            events=["on_change"],
        )

        value_kws = pc.get_values_kws()
        value_kws.update({"value": 0 if value is None else value})

        element = ui.switch(**value_kws)
        super().__init__(element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if prop == "value":
            return self.bind_value(value)

        return super().bind_prop(prop, value)

    def bind_value(self, value: TGetterOrReadonlyRef[bool]):
        @self._ui_effect
        def _():
            self.element.set_value(to_value(value))

        return self
