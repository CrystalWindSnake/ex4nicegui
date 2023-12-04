from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional
from nicegui import ui
from ex4nicegui import to_ref, ref_computed
from ex4nicegui.utils.signals import Ref
from ex4nicegui.bi.dataSource import Filter
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


def ui_select(
    self: DataSourceFacade,
    column: str,
    *,
    custom_data_fn: Optional[Callable[[Any], Any]] = None,
    clearable=True,
    multiple=True,
    **kwargs,
) -> SelectResult:
    custom_data_fn = custom_data_fn or (lambda data: data)
    options = self._dataSource._idataSource.duplicates_column_values(
        custom_data_fn(self.data), column
    )
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

    def onchange(e):
        value = None
        if e.args:
            if isinstance(e.args, list):
                value = [arg["label"] for arg in e.args]
            else:
                value = e.args["label"]

        cp.value = value
        ref_value.value = value  # type: ignore

        def data_filter(data):
            if cp.value is None or not cp.value:
                return data

            cond = None
            if isinstance(cp.value, list):
                cond = data[column].isin(cp.value)
            else:
                cond = data[column] == cp.value
            return data[cond]

        self._dataSource.send_filter(cp.id, Filter(data_filter))

    cp.on("update:modelValue", onchange)

    def on_source_update():
        data = self._dataSource.get_filtered_data(cp)
        options = self._dataSource._idataSource.duplicates_column_values(data, column)
        value = cp.value

        # Make the value within the options
        if isinstance(value, list):
            value = list(set(value) & set(options))
        else:
            if value not in options:
                value = ""

        cp.set_options(options, value=value)

    self._dataSource._register_component(cp.id, on_source_update)

    return SelectResult(cp, self._dataSource, ref_value)
