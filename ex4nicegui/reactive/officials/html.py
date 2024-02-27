from ex4nicegui.utils.apiEffect import ui_effect

from ex4nicegui.utils.signals import (
    _TMaybeRef as TMaybeRef,
    to_value,
)
from nicegui import ui
from .base import BindableUi


class HtmlComponent(ui.element, component="html.js"):
    def __init__(self, content: str) -> None:
        super().__init__()
        self._props["content"] = content


class html(BindableUi[HtmlComponent]):
    def __init__(self, content: TMaybeRef[str]) -> None:
        element = HtmlComponent("")

        super().__init__(element)

        @ui_effect
        def _():
            element._props["content"] = to_value(content)
            element.update()
