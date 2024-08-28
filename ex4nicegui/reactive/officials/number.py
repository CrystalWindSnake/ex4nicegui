from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
    Dict,
    Union,
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


def _default_vmodel_args_getter(e):
    return e.sender.value


class NumberBindableUi(BindableUi[ui.number]):
    def __init__(
        self,
        label: Optional[TMaybeRef[str]] = None,
        *,
        placeholder: Optional[TMaybeRef[str]] = None,
        value: Optional[Union[TMaybeRef[float], TMaybeRef[int]]] = None,
        min: Optional[TMaybeRef[float]] = None,
        max: Optional[TMaybeRef[float]] = None,
        precision: Optional[TMaybeRef[int]] = None,
        step: Optional[TMaybeRef[float]] = None,
        prefix: Optional[TMaybeRef[str]] = None,
        suffix: Optional[TMaybeRef[str]] = None,
        format: Optional[TMaybeRef[str]] = None,
        on_change: Optional[Callable[..., Any]] = None,
        validation: Dict[str, Callable[..., bool]] = {},
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "label",
                "placeholder",
                "value",
                "min",
                "max",
                "precision",
                "step",
                "prefix",
                "suffix",
                "format",
                "validation",
            ],
            v_model=("value", "on_change"),
            events=["on_change"],
            v_model_arg_getter=_default_vmodel_args_getter,
        )

        value_kws = pc.get_values_kws()
        element = ui.number(**value_kws)
        super().__init__(element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if prop == "value":
            return self.bind_value(value)

        if prop == "precision":
            return self._bind_precision(value)

        return super().bind_prop(prop, value)

    def bind_value(self, value: TGetterOrReadonlyRef[float]):
        @self._ui_signal_on(value)
        def _():
            self.element.set_value(to_value(value))

        return self

    def _bind_precision(self, precision: TGetterOrReadonlyRef[int]):
        @self._ui_signal_on(precision)
        def _():
            self.element.precision = to_value(precision)
            self.element.sanitize()

        return self
