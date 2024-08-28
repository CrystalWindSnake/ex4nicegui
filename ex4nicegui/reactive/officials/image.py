from pathlib import Path
from typing import (
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

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if prop == "source":
            return self.bind_source(value)

        return super().bind_prop(prop, value)

    def bind_source(self, source: TGetterOrReadonlyRef[Union[str, Path]]):
        @self._ui_signal_on(source, deep=False)
        def _():
            self.element.set_source(to_value(source))
