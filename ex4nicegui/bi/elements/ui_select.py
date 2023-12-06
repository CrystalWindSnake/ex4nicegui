from __future__ import annotations
from functools import partial
from typing import TYPE_CHECKING, Optional
from nicegui import ui
from ex4nicegui import to_ref, ref_computed, on
from ex4nicegui.utils.signals import Ref
from ex4nicegui.bi.dataSource import Filter
from ex4nicegui.bi import types as bi_types
from .models import UiResult


if TYPE_CHECKING:
    from ex4nicegui.bi.dataSourceFacade import DataSourceFacade, DataSource


class SelectResult(UiResult[ui.select]):
    def __init__(
        self,
        element: ui.select,
        dataSource: DataSource,
        ref_value: Ref,
    ) -> None:
        super().__init__(element, dataSource)
        self._ref_value = ref_value

        @ref_computed
        def value_or_options():
            if not self._ref_value.value:
                return self.element.options
            return self._ref_value.value

        self._value_or_options = value_or_options

    @property
    def value(self):
        return self.get_value()

    def get_value(self, no_select_eq_all=True):
        """Get the selected items of the dropdown box

        Args:
            no_select_eq_all (bool, optional): When there is no selection, it is eq to selecting all. Defaults to True.
        """
        if no_select_eq_all:
            return self._value_or_options.value

        return self._ref_value.value

    def _reset_state(self):
        self._ref_value.value = []
        self.element.value = []


def ui_select(
    self: DataSourceFacade,
    column: str,
    *,
    sort_options: Optional[bi_types._TDuplicates_column_values_sort_options] = None,
    exclude_null_value=True,
    clearable=True,
    multiple=True,
    **kwargs,
) -> SelectResult:
    duplicates_column_values = partial(
        self._dataSource._idataSource.duplicates_column_values,
        sort_options=sort_options,
        exclude_null_value=exclude_null_value,
    )

    options = duplicates_column_values(self.data, column)
    kwargs.update(
        {
            "options": options,
            "multiple": multiple,
            "clearable": clearable,
            "label": column,
        }
    )

    cp = ui.select(**kwargs).props("use-chips outlined").classes("min-w-[8rem]")
    ref_value = to_ref(cp.value)

    @on(ref_value)
    def _():
        cp.value = ref_value.value

    def onchange(e):
        value = None
        if e.args:
            if isinstance(e.args, list):
                value = [arg["label"] for arg in e.args]
            else:
                value = e.args["label"]

        ref_value.value = value  # type: ignore

        self._dataSource.notify_update([result])

    cp.on("update:modelValue", onchange)

    def on_source_update():
        data = self._dataSource.get_filtered_data(cp)
        options = duplicates_column_values(data, column)
        value = cp.value

        # Make the value within the options
        if isinstance(value, list):
            value = [v for v in value if v in options]
        else:
            if value not in options:
                value = ""

        cp.set_options(options, value=value)

    result = SelectResult(cp, self._dataSource, ref_value)
    self._dataSource._register_component(
        cp.id,
        on_source_update,
        result,
    )

    def data_filter(data):
        if cp.value is None or not cp.value:
            return data

        cond = None
        if isinstance(cp.value, list):
            cond = data[column].isin(cp.value)
        else:
            cond = data[column] == cp.value
        return data[cond]

    self._dataSource.send_filter(cp.id, Filter(data_filter), notify_update=False)
    self._dataSource.notify_update()

    return result
