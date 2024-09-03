from typing import (
    Any,
    Literal,
    Optional,
)
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import _TMaybeRef as TMaybeRef, to_value
from nicegui import ui
from .base import BindableUi


class RowBindableUi(BindableUi[ui.row]):
    def __init__(
        self,
        *,
        wrap: TMaybeRef[bool] = True,
        align_items: Optional[
            TMaybeRef[Literal["start", "end", "center", "baseline", "stretch"]]
        ] = None,
    ) -> None:
        pc = ParameterClassifier(locals(), maybeRefs=["wrap", "align_items"], events=[])
        element = ui.row(**pc.get_values_kws())

        super().__init__(element)
        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, value: TMaybeRef):
        print(f"bind_prop: {prop} {value}")
        if prop == "wrap":
            return self.bind_wrap(value)
        if prop == "align-items":
            return self.bind_align_items(value)

        return super().bind_prop(prop, value)

    def bind_wrap(self, value: TMaybeRef):
        self.bind_classes({"wrap": value})

    def bind_align_items(self, value: TMaybeRef):
        self.bind_classes(lambda: f"items-{to_value(value)}")

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)
