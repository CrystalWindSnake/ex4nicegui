from __future__ import annotations
from typing import TYPE_CHECKING
from nicegui import ui
from nicegui.elements.radio import Radio
from ex4nicegui import to_ref
from ex4nicegui.utils.signals import Ref
from ex4nicegui.bi.dataSource import DataSource, Filter
from .models import UiResult

if TYPE_CHECKING:
    from ex4nicegui.bi.dataSourceFacade import DataSourceFacade
    from ex4nicegui.bi.dataSource import UpdateUtils


class RadioResult(UiResult[ui.radio]):
    def __init__(
        self,
        element: Radio,
        dataSource: DataSource,
        ref_value: Ref,
    ) -> None:
        super().__init__(element, dataSource)
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

    def on_source_update(utils: UpdateUtils):
        data = utils.apply_filters_exclude_self()
        options = self._dataSource._idataSource.duplicates_column_values(data, column)
        value = cp.value
        if value not in options:
            value = ""

        cp.set_options(options, value=value)

    self._dataSource._register_component(cp.id, on_source_update)

    return RadioResult(cp, self._dataSource, ref_value)
