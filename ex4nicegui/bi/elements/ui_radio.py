from __future__ import annotations
from typing import TYPE_CHECKING
from nicegui import ui
from ex4nicegui import to_ref, ref_computed
from ex4nicegui.utils.signals import Ref
from ex4nicegui.bi.dataSource import Filter
from .models import UiResult

if TYPE_CHECKING:
    from ex4nicegui.bi.dataSourceFacade import DataSourceFacade


class RadioResult(UiResult[ui.radio]):
    def __init__(
        self,
        element: ui.radio,
        ref_value: Ref,
    ) -> None:
        super().__init__(element)
        self._ref_value = ref_value

    @property
    def value(self):
        return self._ref_value.value


def ui_radio(self: DataSourceFacade, column: str, **kwargs) -> RadioResult:
    options = self._dataSource._idataSource.duplicates_column_values(self.data, column)
    kwargs.update({"options": options})

    cp = ui.radio(**kwargs)
    ref_value = to_ref(cp.value)

    def onchange(e):
        cp.value = cp.options[e.args]

        def data_filter(data):
            if cp.value not in cp.options:
                return data
            cond = data[column] == cp.value
            return data[cond]

        self._dataSource.send_filter(cp.id, Filter(data_filter))

    cp.on("update:modelValue", onchange)

    def on_source_update(data):
        options = self._dataSource._idataSource.duplicates_column_values(data, column)
        value = cp.value
        if value not in options:
            value = ""

        cp.set_options(options, value=value)

    self._dataSource._register_component(cp.id, on_source_update)

    return RadioResult(cp, ref_value)
