from __future__ import annotations
from functools import partial
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Literal, Optional, Union
from nicegui import ui
from ex4nicegui import to_ref
from ex4nicegui.utils.signals import Ref
from ex4nicegui.bi.dataSource import DataSource, Filter
from ex4nicegui.bi import types as bi_types
from .models import UiResult
import copy

if TYPE_CHECKING:
    from ex4nicegui.bi.dataSourceFacade import DataSourceFacade


class RadioResult(UiResult["OptionGroup"]):
    def __init__(
        self,
        element: "OptionGroup",
        dataSource: DataSource,
        ref_value: Ref,
    ) -> None:
        super().__init__(element, dataSource)
        self._ref_value = ref_value

    @property
    def value(self):
        return self._ref_value.value

    def _reset_state(self):
        self._ref_value.value = None
        self.element.value = None


class OptionGroup(ui.element):
    def __init__(
        self,
        options: List,
        *,
        value: Any = None,
    ) -> None:
        super().__init__("q-option-group")

        self._value = value
        self._options = options
        self._props["options"] = options
        self._props["modelValue"] = value

        self._on_change_callbacks: List[Callable[[Any], None]] = []

        def on_modelValue(e):
            value = e.args

            self._value = value
            self._props["modelValue"] = value
            self.update()

            for fn in self._on_change_callbacks:
                fn(value)

        self.on("update:modelValue", on_modelValue)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self._props["modelValue"] = new_value
        self.update()

    @property
    def options(self):
        return self._options

    def set_options(self, options, value):
        self._options = options
        self._props["options"] = options

        self.value = value
        self.update()

    def on_change(self, callback: Callable[[Any], None]):
        self._on_change_callbacks.append(callback)


def ui_radio(
    self: DataSourceFacade,
    column: str,
    *,
    sort_options: Optional[bi_types._TDuplicates_column_values_sort_options] = None,
    exclude_null_value=False,
    hide_filtered=True,
    custom_options_map: Optional[Union[Dict, Callable[[List], Dict]]] = None,
    **kwargs,
) -> RadioResult:
    duplicates_column_values = partial(
        self._dataSource._idataSource.duplicates_column_values,
        sort_options=sort_options,
        exclude_null_value=exclude_null_value,
    )
    custom_options_map = custom_options_map or {}

    options = duplicates_column_values(self.data, column)
    option_items = _options_to_items(options, custom_options_map)
    kwargs.update({"options": option_items})

    cp = OptionGroup(**kwargs)
    ref_value = to_ref(cp.value)

    @cp.on_change
    def onchange(value):
        cp.value = value
        self._dataSource.notify_update([result])

    def on_source_update():
        pass
        data = self._dataSource.get_filtered_data(cp)
        filtered_options = duplicates_column_values(data, column)

        filtered_options_set = set(filtered_options)

        value = None if cp.value == "" else cp.value
        if value not in filtered_options_set:
            value = None

        if hide_filtered:
            cp.set_options(
                _options_to_items(filtered_options, custom_options_map), value=value
            )
        else:
            new_opt_items = copy.deepcopy(
                _options_to_items(filtered_options, custom_options_map)
            )

            for opt in new_opt_items:
                temp_value = None if opt["value"] == "" else opt["value"]
                opt["disable"] = temp_value not in filtered_options_set

            cp.set_options(new_opt_items, value=value)

    result = RadioResult(cp, self._dataSource, ref_value)
    self._dataSource._register_component(cp.id, on_source_update, result)

    def data_filter(data):
        value_in_options = any(cp.value == opt["value"] for opt in cp.options)
        if not value_in_options:
            return data

        cond = data[column].isnull() if cp.value == "" else data[column] == cp.value
        return data[cond]

    self._dataSource.send_filter(cp.id, Filter(data_filter))

    return result


def _options_to_items(
    options: List, custom_options_map: Union[Dict, Callable[[Any], Dict]]
):
    items = []

    custom_options_fn: Callable[[Any], Dict] = None  # type: ignore

    if isinstance(custom_options_map, Dict):
        custom_options_fn = custom_options_map.get  # type: ignore
    else:
        custom_options_fn = custom_options_map

    for opt in options:
        opt = "" if opt is None else opt
        cus_config = custom_options_fn(opt)
        item = {"value": opt, "label": opt}
        if cus_config:
            if not isinstance(cus_config, dict):
                cus_config = {"label": str(cus_config)}

            cus_config.pop("value", None)
            item.update(cus_config)

        items.append(item)

    return items
