from typing import (
    Any,
)
from nicegui import ui
from .base import BindableUi


class CardBindableUi(BindableUi[ui.card]):
    def __init__(
        self,
    ) -> None:
        element = ui.card()

        super().__init__(element)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)

    def tight(self):
        """Removes padding and gaps between nested elements."""
        self.element._classes.clear()
        self.element._style.clear()
        return self


class CardSectionBindableUi(BindableUi[ui.card_section]):
    def __init__(
        self,
    ) -> None:
        element = ui.card_section()

        super().__init__(element)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)


class CardActionsBindableUi(BindableUi[ui.card_actions]):
    def __init__(
        self,
    ) -> None:
        element = ui.card_actions()

        super().__init__(element)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)
