from typing import (
    Any,
    Callable,
    Dict,
    Protocol,
)

import signe
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    WatchedState,
)
from nicegui import ui
from ex4nicegui.reactive.systems import color_system


class TextColorableMixin(Protocol):
    _ui_signal_on: Callable[[Callable[[TGetterOrReadonlyRef[str]], Any]], signe.Effect]

    @property
    def element(self) -> ui.element:
        ...

    def _bind_text_color(self, color: TGetterOrReadonlyRef[str]):
        @self._ui_signal_on(color)  # type: ignore
        def _(state: WatchedState):
            if state.previous is not None:
                color_system.remove_text_color(self.element, state.previous)

            color_system.add_text_color(self.element, state.current)

            self.element.update()

    def bind_color(self, color: TGetterOrReadonlyRef[str]):
        """bind text color to the element

        Args:
            color (TGetterOrReadonlyRef[str]): a reference to the color value

        """
        self._bind_text_color(color)
        return self


class HtmlTextColorableMixin(Protocol):
    _ui_signal_on: Callable[[Callable[[TGetterOrReadonlyRef[str]], Any]], signe.Effect]

    @property
    def element(self) -> ui.element:
        ...

    def bind_style(self, style: Dict[str, TGetterOrReadonlyRef[Any]]):
        ...

    def _bind_text_color(self, value: TGetterOrReadonlyRef[str]):
        return self.bind_style({"color": value})

    def bind_color(self, color: TGetterOrReadonlyRef[str]):
        """bind text color to the element

        Args:
            color (TGetterOrReadonlyRef[str]): a reference to the color value

        """
        self._bind_text_color(color)
        return self
