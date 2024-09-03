from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.reactive.mixins.value_element import ValueElementMixin
from ex4nicegui.utils.signals import (
    _TMaybeRef as TMaybeRef,
    is_setter_ref,
    TGetterOrReadonlyRef,
)
from nicegui import ui
from .base import BindableUi


class DialogBindableUi(BindableUi[ui.dialog], ValueElementMixin[bool]):
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
        if ValueElementMixin._bind_specified_props(self, prop, value):
            return self

        return super().bind_prop(prop, value)
