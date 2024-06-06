from typing import Any, Callable, Optional
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    to_value,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import BindableUi


class TabPanelsBindableUi(BindableUi[ui.tab_panels]):
    def __init__(
        self,
        value: Optional[TMaybeRef[str]] = None,
        *,
        on_change: Optional[Callable[..., Any]] = None,
        animated: TMaybeRef[bool] = True,
        keep_alive: TMaybeRef[bool] = True,
    ) -> None:
        """Tab Panels

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#tab_panels
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#tab_panels

        Args:
            value (TMaybeRef[str], optional): The value of the tab panel. Defaults to None.
            on_change (Callable[..., Any], optional): The callback function when the value of the tab panel changes. Defaults to None.
            animated (TMaybeRef[bool], optional): Whether to animate the tab panel. Defaults to True.
            keep_alive (TMaybeRef[bool], optional): Whether to keep the tab panel alive. Defaults to True.
        """
        pc = ParameterClassifier(
            locals(),
            maybeRefs=["value", "animated", "keep_alive"],
            v_model=("value", "on_change"),
            events=["on_change"],
        )

        element = ui.tab_panels(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, ref_ui: TGetterOrReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: TGetterOrReadonlyRef):
        @self._ui_effect
        def _():
            self.element.set_value(to_value(ref_ui))
