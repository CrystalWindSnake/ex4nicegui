from typing import (
    Any,
    Optional,
)
from .utils import _convert_kws_ref2value

from nicegui import ui
from .base import BindableUi
from ex4nicegui.utils.signals import _TMaybeRef as TMaybeRef, is_ref


class GridBindableUi(BindableUi[ui.grid]):
    def __init__(
        self,
        rows: Optional[TMaybeRef[int]] = None,
        columns: Optional[TMaybeRef[int]] = None,
    ) -> None:
        kws = {
            "rows": rows,
            "columns": columns,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.grid(**value_kws)

        super().__init__(element)
        for key, value in kws.items():
            if value is not None and is_ref(value):
                self.bind_prop(key, value)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)
