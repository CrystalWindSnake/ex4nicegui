from typing import Dict, Optional
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
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

        value_kws = pc.get_values_kws()
        element = ui.tab(**value_kws)
        super().__init__(element)

        bindings_kws = pc.get_bindings()
        self.__bind_label(bindings_kws, value_kws)

        if "label" in bindings_kws:
            bindings_kws.pop("label")

        for key, value in bindings_kws.items():
            self.bind_prop(key, value)  # type: ignore

    def __bind_label(self, binding_kws: Dict, value_kws: Dict):
        name_ref = binding_kws.get("name") or value_kws.get("name")
        label_ref = binding_kws.get("label") or value_kws.get("label")

        @self._ui_effect
        def _():
            self.element._props["label"] = (
                to_value(label_ref) if label_ref is not None else to_value(name_ref)
            )
            self.element.update()
