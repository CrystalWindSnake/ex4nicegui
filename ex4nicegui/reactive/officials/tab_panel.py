from typing import Any, Callable, Optional, Union
from ex4nicegui.reactive.utils import ParameterClassifier
from ex4nicegui.utils.signals import (
    to_value,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import BindableUi


class TabPanelBindableUi(BindableUi[ui.tab_panel]):
    def __init__(
        self,
        name: TMaybeRef[str],
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=["name"],
        )

        element = ui.tab_panel(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore
