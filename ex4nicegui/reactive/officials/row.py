from typing import (
    Any,
    Literal,
    Optional,
)
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.reactive.mixins.flexLayout import FlexAlignItemsMixin, FlexWrapMixin
from ex4nicegui.utils.signals import TMaybeRef
from nicegui import ui
from .base import BindableUi


class RowBindableUi(BindableUi[ui.row], FlexAlignItemsMixin, FlexWrapMixin):
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
        if FlexAlignItemsMixin._bind_specified_props(self, prop, value):
            return self
        if FlexWrapMixin._bind_specified_props(self, prop, value):
            return self

        return super().bind_prop(prop, value)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)
