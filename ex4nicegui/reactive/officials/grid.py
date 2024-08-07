from typing import (
    Any,
    Optional,
    Union,
)

from ex4nicegui.reactive.services.reactive_service import ParameterClassifier

from nicegui import ui
from .base import BindableUi
from ex4nicegui.utils.signals import _TMaybeRef as TMaybeRef


class GridBindableUi(BindableUi[ui.grid]):
    def __init__(
        self,
        rows: Optional[TMaybeRef[Union[int, str]]] = None,
        columns: Optional[TMaybeRef[Union[int, str]]] = None,
    ) -> None:
        pc = ParameterClassifier(locals(), maybeRefs=["rows", "columns"], events=[])

        element = ui.grid(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)
