from typing import Any, Callable, Optional
from ex4nicegui.reactive.utils import ParameterClassifier
from ex4nicegui.utils.signals import (
    to_value,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import BindableUi


class TabBindableUi(BindableUi[ui.tab]):
    def __init__(
        self,
        name: TMaybeRef[str],
        label: Optional[TMaybeRef[str]] = None,
        icon: Optional[TMaybeRef[str]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=["name", "label", "icon"],
        )

        element = ui.tab(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore
