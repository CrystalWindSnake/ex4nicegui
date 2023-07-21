import asyncio
from signe import effect
from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import SingleValueBindableUi
from .utils import _convert_kws_ref2value


class HtmlBindableUi(SingleValueBindableUi[str, ui.html]):
    @staticmethod
    def _setup_(binder: "HtmlBindableUi"):
        first = True

        @effect
        def _():
            nonlocal first

            async def task():
                pass
                await ui.run_javascript(
                    f"getElement({binder.element.id}).innerText= '{binder.value}' ",
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
        kws = {
            "content": content,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.html(**value_kws)

        super().__init__(content, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

        HtmlBindableUi._setup_(self)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            ele = self.element
            color = ref_ui.value
            ele._style["color"] = color
            ele.update()
