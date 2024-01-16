from typing import (
    Any,
    Callable,
    Optional,
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


class ColorPickerBindableUi(SingleValueBindableUi[str, ui.color_picker]):
    def __init__(
        self,
        color: TMaybeRef[str] = "",
        *,
        on_pick: Optional[Callable[..., Any]] = None,
        value: TMaybeRef[bool] = False,
    ) -> None:
        """Color Picker

        Args:
            color (TMaybeRef[str], optional): color value str. Defaults to "".
            on_pick (Optional[Callable[..., Any]], optional): callback to execute when a color is picked. Defaults to None.
            value (TMaybeRef[bool], optional): whether the menu is already opened. Defaults to False.
        """
        color_ref = to_ref(color)
        kws = {
            "color": color_ref,
            "value": value,
            "on_pick": on_pick,
        }

        value_kws = _convert_kws_ref2value(kws)

        def inject_on_change(e):
            color_ref.value = e.value
            if on_pick:
                on_pick(e)

        value_kws.update({"on_pick": inject_on_change})

        with ui.card().tight():
            element_menu = ui.color_picker(**value_kws)
            self._element_picker = element_menu.default_slot.children[0]
            self._element_picker.props('format-model="rgba"')

            ui.button(on_click=element_menu.open, icon="colorize")

        super().__init__(color_ref, element_menu)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: ReadonlyRef[str]):
        @effect
        def _():
            self._element_picker._props["modelValue"] = ref_ui.value

        return self

    def bind_value(self, ref_ui: ReadonlyRef[bool]):
        @effect
        def _():
            self._element_picker._props["value"] = ref_ui.value

        return self


class ColorPickerLazyBindableUi(ColorPickerBindableUi):
    def __init__(
        self,
        color: TMaybeRef[str] = "",
        *,
        on_pick: Optional[Callable[..., Any]] = None,
        value: TMaybeRef[bool] = False,
    ) -> None:
        super().__init__(color, on_pick=None, value=value)

        ele = self._element_picker

        def onModelValueChanged(e):
            self._ref.value = e.args  # type: ignore

            if on_pick:
                on_pick()

        ele.on("change", handler=onModelValueChanged)
