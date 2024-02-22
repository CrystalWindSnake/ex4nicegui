from typing import (
    Any,
)
from typing_extensions import Literal
from ex4nicegui.reactive.utils import ParameterClassifier

from ex4nicegui.utils.signals import (
    is_setter_ref,
    to_ref,
    to_value,
    is_ref,
    _TMaybeRef as TMaybeRef,
    effect,
)
from nicegui import ui
from nicegui.page_layout import Drawer
from .base import BindableUi
from .utils import _convert_kws_ref2value

_TDrawerSide = Literal["left", "right"]


class DrawerBindableUi(BindableUi[Drawer]):
    def __init__(
        self,
        side: TMaybeRef[_TDrawerSide] = "left",
        overlay: TMaybeRef[bool] = False,
        *,
        value: TMaybeRef[bool] = True,
        fixed: TMaybeRef[bool] = False,
        bordered: TMaybeRef[bool] = True,
        elevated: TMaybeRef[bool] = False,
        top_corner: TMaybeRef[bool] = False,
        bottom_corner: TMaybeRef[bool] = False,
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "side",
                "overlay",
                "value",
                "fixed",
                "bordered",
                "elevated",
                "top_corner",
                "bottom_corner",
            ],
        )

        value_kws = pc.get_values_kws()

        del value_kws["side"]
        del value_kws["overlay"]

        element = None

        if to_value(side) == "left":
            element = ui.left_drawer(**value_kws)
        else:
            element = ui.right_drawer(**value_kws)

        element.classes("flex flex-col gap-4 backdrop-blur-md bg-[#5898d4]/30")

        super().__init__(element)  # type: ignore

        @effect
        def _():
            mvalue = "true" if to_value(value) else "false"
            element.props(f":model-value={mvalue}")

        if is_setter_ref(value):
            ref = to_ref(value)

            def on_update(e):
                ref.value = e.args

            element.on("update:modelValue", on_update)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def toggle(self):
        self.element.toggle()
        return self

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)
