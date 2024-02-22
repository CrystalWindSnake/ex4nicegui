from pathlib import Path
from typing import (
    Union,
)
from ex4nicegui.reactive.utils import ParameterClassifier

from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    _TMaybeRef as TMaybeRef,
    effect,
    to_ref,
    to_value,
)
from nicegui import ui
from .base import BindableUi
from .utils import _convert_kws_ref2value


class ImageBindableUi(BindableUi[ui.image]):
    def __init__(
        self,
        source: Union[TMaybeRef[str], TMaybeRef[Path]] = "",
    ) -> None:
        pc = ParameterClassifier(locals(), maybeRefs=["source"], events=[])

        element = ui.image(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "source":
            return self.bind_source(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_source(self, ref_ui: ReadonlyRef[Union[str, Path]]):
        @effect
        def _():
            self.element.set_source(to_value(ref_ui))
