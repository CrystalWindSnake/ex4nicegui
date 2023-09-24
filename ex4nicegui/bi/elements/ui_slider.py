from __future__ import annotations
from typing import TYPE_CHECKING
from nicegui import ui
from ex4nicegui import to_ref
from ex4nicegui.utils.signals import Ref
from ex4nicegui.bi.dataSource import Filter
from .models import UiResult

if TYPE_CHECKING:
    from ex4nicegui.bi.dataSourceFacade import DataSourceFacade, DataSource
    from ex4nicegui.bi.dataSource import UpdateUtils


class SliderResult(UiResult[ui.slider]):
    def __init__(
        self,
        element: ui.slider,
        dataSource: DataSource,
        ref_value: Ref,
    ) -> None:
        super().__init__(element, dataSource)
        self._ref_value = ref_value

    @property
    def value(self):
        return self._ref_value.value


def ui_slider(self: DataSourceFacade, column: str, **kwargs):
    self._dataSource._idataSource.slider_check(self.data, column)

    min, max = self._dataSource._idataSource.slider_min_max(self.data, column)
    kwargs.update({"min": min, "max": max})

    cp = ui.slider(**kwargs).props("label label-always switch-label-side")
    ref_value = to_ref(cp.value)

    def onchange():
        def data_filter(data):
            if cp.value is None or cp.value < min:
                return data
            cond = data[column] == cp.value
            return data[cond]

        self._dataSource.send_filter(cp.id, Filter(data_filter))

    cp.on("change", onchange)

    def on_source_update(utils: UpdateUtils):
        data = utils.apply_filters_exclude_self()
        min, max = self._dataSource._idataSource.slider_min_max(data, column)
        if min is None or max is None:
            cp.value = None
        else:
            cp._props["min"] = min
            cp._props["max"] = max

    self._dataSource._register_component(cp.id, on_source_update)

    return SliderResult(cp, self._dataSource, ref_value)
