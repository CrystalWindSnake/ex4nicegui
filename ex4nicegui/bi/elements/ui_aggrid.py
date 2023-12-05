from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional, Union
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


def ui_aggrid(
    self: DataSourceFacade,
    **kwargs,
):
    kwargs.update({"options": {}})

    cp = ui.aggrid(**kwargs)

    def on_source_update():
        data = self._dataSource.get_filtered_data(cp)
        cp._props["options"] = self._dataSource._idataSource.get_aggrid_options(data)
        cp.update()

    info = self._dataSource._register_component(cp.id, on_source_update)

    on_source_update()

    return AggridResult(cp, self._dataSource, on_source_update)
