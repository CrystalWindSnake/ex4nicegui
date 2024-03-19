from typing import (
    Any,
)
from nicegui import ui
from .base import BindableUi


class ElementBindableUi(BindableUi[ui.element]):
    def __init__(self, tag: str) -> None:
        element = ui.element(tag)

        super().__init__(element)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)
