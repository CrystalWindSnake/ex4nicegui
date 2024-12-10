from typing import (
    Any,
    Optional,
    Union,
)

from ex4nicegui.reactive.services.reactive_service import ParameterClassifier

from nicegui import ui
from .base import BindableUi
from ex4nicegui.utils.signals import (
    _TMaybeRef as TMaybeRef,
    TGetterOrReadonlyRef,
    to_value,
)


_T_Template = Union[TMaybeRef[str], TMaybeRef[int]]


class GridBindableUi(BindableUi[ui.grid]):
    def __init__(
        self,
        rows: Optional[_T_Template] = None,
        columns: Optional[_T_Template] = None,
    ) -> None:
        pc = ParameterClassifier(locals(), maybeRefs=["rows", "columns"], events=[])

        element = ui.grid(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if prop == "rows":
            return self.bind_rows(value)

        if prop == "columns":
            return self.bind_columns(value)

        return super().bind_prop(prop, value)

    def bind_rows(self, rows: TGetterOrReadonlyRef[Union[int, str]]):
        def template():
            _rows = to_value(rows)
            return (
                f"repeat({_rows}, minmax(0, 1fr))" if isinstance(_rows, int) else _rows
            )

        self.bind_style({"grid-template-rows": template})

        return self

    def bind_columns(self, columns: TGetterOrReadonlyRef[Union[int, str]]):
        def template():
            _columns = to_value(columns)
            return (
                f"repeat({_columns}, minmax(0, 1fr))"
                if isinstance(_columns, int)
                else _columns
            )

        self.bind_style({"grid-template-columns": template})

        return self

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)
