from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from nicegui import ui
from ex4nicegui import to_ref, on
from ex4nicegui.utils.signals import Ref
from ex4nicegui.bi.dataSource import Filter
from .models import UiResult

if TYPE_CHECKING:
    from ex4nicegui.bi.dataSourceFacade import DataSourceFacade, DataSource


class UiDatePicker(ui.element, component="ui_date_picker.js"):
    def __init__(self, date: str) -> None:
        super().__init__()
        self._props["id"] = self.id
        self.value = date.replace("-", "/")
        self._props["date"] = self.value


class DatePickerResult(UiResult[UiDatePicker]):
    def __init__(
        self,
        element: UiDatePicker,
        dataSource: DataSource,
        ref_value: Ref,
    ) -> None:
        super().__init__(element, dataSource)
        self._ref_value = ref_value

    @property
    def value(self) -> str:
        return self._ref_value.value


def ui_date_picker(
    self: DataSourceFacade, column: str, *, value: Optional[str] = None, **kwargs
):
    options = self._dataSource._idataSource.duplicates_column_values(self.data, column)
    kwargs.update(
        {
            "options": options,
            "label": column,
        }
    )

    cp = UiDatePicker(value or "")
    ref_value = to_ref(cp.value)

    @on(ref_value)
    def _():
        cp.value = ref_value.value

    def onchange(e):
        value = e.args
        ref_value.value = value  # type: ignore
        self._dataSource.notify_update([result])

    cp.on("update:value", onchange)

    def on_source_update():
        pass
        # data = self._dataSource.get_filtered_data(cp)
        # options = self._dataSource._idataSource.duplicates_column_values(data, column)
        # value = cp.value

    result = DatePickerResult(cp, self._dataSource, ref_value)
    self._dataSource._register_component(cp.id, on_source_update, result)

    def data_filter(data):
        if cp.value is None or not cp.value:
            return data

        cond = None
        cond = data[column] == cp.value
        return data[cond]

    self._dataSource.send_filter(cp.id, Filter(data_filter))

    return result
