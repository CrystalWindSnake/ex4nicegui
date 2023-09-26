from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Union, cast
from nicegui.events import UiEventArguments
from ex4nicegui.reactive import rxui
from ex4nicegui.reactive.EChartsComponent.ECharts import (
    EChartsClickEventArguments,
    echarts,
)
from nicegui import ui
from ex4nicegui.bi.dataSource import DataSource
from .models import UiResult

if TYPE_CHECKING:
    from ex4nicegui.bi.dataSourceFacade import DataSourceFacade


class EChartsResult(UiResult[echarts]):
    def __init__(
        self, element: echarts, dataSource: DataSource, chart_update: Callable
    ) -> None:
        super().__init__(element, dataSource)
        self.chart_update = chart_update

    def on_chart_click(
        self, handler: Optional[Callable[[EChartsClickEventArguments], Any]]
    ):
        return self.element.on_chart_click(handler)

    def on_chart_click_blank(
        self, handler: Optional[Callable[[UiEventArguments], Any]]
    ):
        return self.element.on_chart_click_blank(handler)

    def cancel_linkage(self, *source: Union[ui.element, "UiResult"]):
        super().cancel_linkage(*source)
        self.element.update_options(
            self.chart_update(self._dataSource.get_filtered_data(self.element))
        )


def ui_echarts(
    self: DataSourceFacade,
    fn: Callable[[Any], Union[Dict, "pyecharts.Base"]],  # pyright: ignore
    **kwargs,
):
    def create_options(data):
        options = fn(data)
        if isinstance(options, Dict):
            return options

        import simplejson as json
        from pyecharts.charts.chart import Base

        if isinstance(options, Base):
            return cast(Dict, json.loads(options.dump_options()))

        raise TypeError(f"not support options type[{type(options)}]")

    cp = rxui.echarts({})
    ele_id = cp.element.id

    def on_source_update():
        data = self._dataSource.get_filtered_data(cp.element)
        options = create_options(data)
        cp.element.update_options(options)

    info = self._dataSource._register_component(ele_id, on_source_update)

    cp.element.update_options(
        create_options(self._dataSource.get_filtered_data(cp.element))
    )
    return EChartsResult(cp.element, self._dataSource, create_options)
