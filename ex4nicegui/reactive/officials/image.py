from pathlib import Path
from typing import (
    Union,
)

from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    _TMaybeRef as TMaybeRef,
    effect,
    to_ref,
)
from nicegui import ui
from .base import SingleValueBindableUi
from .utils import _convert_kws_ref2value


class ImageBindableUi(SingleValueBindableUi[Union[str, Path], ui.image]):
    def __init__(
        self,
        source: Union[TMaybeRef[str], TMaybeRef[Path]] = "",
    ) -> None:
        source_ref = to_ref(source)  # type: ignore
        kws = {
            "source": source_ref,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.image(**value_kws)

        super().__init__(source_ref, element)  # type: ignore

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "source":
            return self.bind_source(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_source(self, ref_ui: ReadonlyRef[Union[str, Path]]):
        @effect
        def _():
            self.element.set_source(ref_ui.value)
