from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Dict, Union, cast
from nicegui import ui
from ex4nicegui import to_ref
from ex4nicegui.utils.signals import Ref
from ex4nicegui.reactive import rxui
from ex4nicegui.reactive.EChartsComponent.ECharts import echarts
from ex4nicegui.bi.dataSource import DataSource, Filter
from .models import UiResult
from ex4nicegui.bi.dataSource import UpdateUtils

if TYPE_CHECKING:
    from ex4nicegui.bi.dataSourceFacade import DataSourceFacade


class EChartsResult(UiResult[echarts]):
    def __init__(self, element: echarts, dataSource: DataSource) -> None:
        super().__init__(element, dataSource)


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

    def on_source_update(utils: UpdateUtils):
        options = create_options(utils.apply_filters_exclude_self())
        cp.element.update_options(options)

    info = self._dataSource._register_component(cp.element.id, on_source_update)

    udpate_utils = self._dataSource.create_update_utils(info)
    cp.element.update_options(create_options(udpate_utils.apply_filters_exclude_self()))
    return EChartsResult(cp.element, self._dataSource)