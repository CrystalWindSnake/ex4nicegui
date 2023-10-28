from pathlib import Path
from typing import (
    Union,
)
from signe import effect
from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import SingleValueBindableUi
from .utils import _convert_kws_ref2value


class ImageBindableUi(SingleValueBindableUi[Union[str, Path], ui.image]):
    @staticmethod
    def _setup_(binder: "ImageBindableUi"):
        @effect
        def _():
            value = binder.value
            binder.element.set_source(value)
            binder.element._handle_source_change(value)

    def __init__(
        self,
        source: Union[TMaybeRef[str], TMaybeRef[Path]] = "",
    ) -> None:
        kws = {
            "source": source,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.image(**value_kws)

        super().__init__(source, element)  # type: ignore

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

        # ImageBindableUi._setup_(self)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "source":
            return self.bind_source(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_source(self, ref_ui: ReadonlyRef[Union[str, Path]]):
        @effect
        def _():
            ele = self.element
            source = ref_ui.value
            ele.on_source_change(source)
