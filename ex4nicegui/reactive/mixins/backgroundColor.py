from typing import (
    Any,
    Callable,
    Protocol,
)

import signe
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    WatchedState,
)
from nicegui import ui
from ex4nicegui.reactive.systems import color_system


class BackgroundColorableMixin(Protocol):
    _ui_signal_on: Callable[[Callable[..., Any]], signe.Effect[None]]

    @property
    def element(self) -> ui.element:
        ...

    def _bind_background_color(self, ref_ui: TGetterOrReadonlyRef[str]):
        @self._ui_signal_on(ref_ui)  # type: ignore
        def _(state: WatchedState):
            if state.previous is not None:
                color_system.remove_background_color(self.element, state.previous)

            color_system.add_background_color(self.element, state.current)

            self.element.update()

    def bind_color(self, ref_ui: TGetterOrReadonlyRef[str]):
        """bind color to the element

        Args:
            ref_ui (TGetterOrReadonlyRef[str]): a reference to the color value

        """
        self._bind_background_color(ref_ui)
        return self
