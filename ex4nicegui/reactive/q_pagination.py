from typing import Any, Optional, Callable
from ex4nicegui.reactive.utils import ParameterClassifier
from ex4nicegui import (
    TGetterOrReadonlyRef,
    to_value,
    TMaybeRef,
)
from nicegui import ui
from ex4nicegui.reactive.officials.base import BindableUi


class PaginationBindableUi(BindableUi[ui.pagination]):
    def __init__(
        self,
        min: TMaybeRef[int],
        max: TMaybeRef[int],
        *,  # pylint: disable=redefined-builtin
        direction_links: TMaybeRef[bool] = False,
        value: TMaybeRef[int] = ...,  # type: ignore
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=["min", "max", "direction_links", "value"],
            v_model=("value", "on_change"),
            events=["on_change"],
        )

        element = ui.pagination(**pc.get_values_kws())
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

    def bind_value(self, ref_ui: TGetterOrReadonlyRef[int]):
        @self._ui_effect
        def _():
            self.element.set_value(to_value(ref_ui))

        return self
