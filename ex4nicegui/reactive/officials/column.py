from typing import (
    Any,
)
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import BindableUi


class ColumnBindableUi(BindableUi[ui.column]):
    def __init__(self, *, wrap: TMaybeRef[bool] = True) -> None:
        pc = ParameterClassifier(locals(), maybeRefs=["wrap"], events=[])
        element = ui.column(**pc.get_values_kws())

        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if prop == "wrap":
            return self.bind_wrap(value)

        return super().bind_prop(prop, value)

    def bind_wrap(self, value: TGetterOrReadonlyRef):
        self.bind_classes({"wrap": value})

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)
