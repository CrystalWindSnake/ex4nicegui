from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Union
from nicegui import ui
from ex4nicegui.bi.dataSource import DataSource
from .models import UiResult

if TYPE_CHECKING:
    from ex4nicegui.bi.dataSourceFacade import DataSourceFacade


class AggridResult(UiResult[ui.aggrid]):
    def __init__(
        self, element: ui.aggrid, dataSource: DataSource, table_update: Callable
    ) -> None:
        super().__init__(element, dataSource)
        self.table_update = table_update

    def cancel_linkage(self, *source: Union[ui.element, "UiResult"]):
        super().cancel_linkage(*source)
        self.table_update()


def _merge_options(fixed_options: Dict, new_options: Dict):
    columnDefs = new_options["columnDefs"]  # type:list[dict]
    new_options.update(fixed_options)

    if "columnDefs" in fixed_options:
        fixed_columnDefs_map = {
            col_info["field"]: col_info
            for col_info in fixed_options["columnDefs"]
            if "field" in col_info
        }

        for colDef in columnDefs:
            info = fixed_columnDefs_map.get(colDef["field"])
            if info:
                colDef.update(info)

        new_options.update({"columnDefs": columnDefs})

    return new_options


def ui_aggrid(
    self: DataSourceFacade,
    options: Optional[Dict] = None,
    **kwargs,
):
    fixed_options = options or {}
    fixed_options.pop("rowData", None)

    kwargs.update({"options": {}})

    cp = ui.aggrid(**kwargs)

    def on_source_update():
        data = self._dataSource.get_filtered_data(cp)
        new_opts = self._dataSource._idataSource.get_aggrid_options(data)
        options = _merge_options(fixed_options, new_opts)
        cp._props["options"] = options
        cp.update()

    info = self._dataSource._register_component(cp.id, on_source_update)

    on_source_update()

    return AggridResult(cp, self._dataSource, on_source_update)
