from typing import (
    Any,
)
from ex4nicegui.reactive.systems.reactive_system import ParameterClassifier
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

    def bind_prop(self, prop: str, ref_ui: TGetterOrReadonlyRef):
        if prop == "wrap":
            return self.bind_wrap(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_wrap(self, ref_ui: TGetterOrReadonlyRef):
        self.bind_classes({"wrap": ref_ui})

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)
