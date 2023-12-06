from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional, Union
from nicegui import ui
from ex4nicegui.bi.dataSource import DataSource
from .models import UiResult

if TYPE_CHECKING:
    from ex4nicegui.bi.dataSourceFacade import DataSourceFacade


class TableResult(UiResult[ui.table]):
    def __init__(
        self, element: ui.table, dataSource: DataSource, table_update: Callable
    ) -> None:
        super().__init__(element, dataSource)
        self.table_update = table_update

    def cancel_linkage(self, *source: Union[ui.element, "UiResult"]):
        super().cancel_linkage(*source)
        self.table_update()


def ui_table(
    self: DataSourceFacade,
    **kwargs,
):
    kwargs.update({"columns": [], "rows": []})
    cp = ui.table(**kwargs)

    def on_source_update():
        data = self._dataSource.get_filtered_data(cp)
        opts = self._dataSource._idataSource.get_table_options(data)
        cp.rows = opts["rows"]
        cp.columns = opts["columns"]
        cp.update()

    info = self._dataSource._register_component(cp.id, on_source_update)

    on_source_update()

    return TableResult(cp, self._dataSource, on_source_update)
