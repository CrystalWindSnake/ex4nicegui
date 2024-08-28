from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    _TMaybeRef as TMaybeRef,
    is_setter_ref,
    to_value,
    TGetterOrReadonlyRef,
)
from nicegui import ui
from .base import BindableUi


class DialogBindableUi(BindableUi[ui.dialog]):
    def __init__(
        self,
        *,
        value: TMaybeRef[bool] = False,
    ) -> None:
        pc = ParameterClassifier(locals(), maybeRefs=["value"])

        value_kws = pc.get_values_kws()
        element = ui.dialog(**value_kws)
        super().__init__(element)  # type: ignore

        if is_setter_ref(value):

            def on_value_change():
                value.value = element.value  # type: ignore

            element.on_value_change(on_value_change)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if prop == "value":
            return self.bind_value(value)

        return super().bind_prop(prop, value)

    def bind_value(self, value: TGetterOrReadonlyRef[float]):
        @self._ui_signal_on(value)
        def _():
            self.element.set_value(to_value(value))

        return self
