import asyncio
from ex4nicegui.reactive.utils import ParameterClassifier

from ex4nicegui.utils.signals import (
    _TMaybeRef as TMaybeRef,
    effect,
    to_value,
)
from nicegui import ui
from .base import BindableUi


class HtmlBindableUi(BindableUi[ui.html]):
    @staticmethod
    def _setup_(element: ui.element, content: TMaybeRef[str]):
        first = True

        # f"getElement({element.id}).innerHTML= '{to_value(content)}' ",
        @effect
        def _():
            nonlocal first

            async def task():
                pass
                await ui.run_javascript(
                    f"document.getElementById('c{element.id}').innerText = '{to_value(content)}'",
                    respond=False,
                )

            if not first:
                asyncio.run(task())
            else:
                first = False

    def __init__(
        self,
        content: TMaybeRef[str] = "",
    ) -> None:
        pc = ParameterClassifier(locals(), maybeRefs=["content"], events=[])

        element = ui.html(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

        HtmlBindableUi._setup_(element, content)

    def bind_prop(self, prop: str, ref_ui: TMaybeRef):
        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: TMaybeRef):
        @effect
        def _():
            ele = self.element
            color = to_value(ref_ui)
            ele._style["color"] = color
            ele.update()
