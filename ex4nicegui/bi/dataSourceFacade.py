from __future__ import annotations
from typing import Any, Callable, Dict, TypeVar, Generic, Union, cast
from nicegui import ui
from ex4nicegui import ref_computed
from ex4nicegui.reactive import rxui
from .dataSource import DataSource, Filter
from ex4nicegui.reactive.EChartsComponent.ECharts import echarts
from .elements.ui_select import ui_select, SelectResult

_TData = TypeVar("_TData")


class DataSourceFacade(Generic[_TData]):
    def __init__(self, ds: DataSource) -> None:
        self._dataSource = ds

    @property
    def data(self) -> _TData:
        """Data without any filtering"""
        return cast(_TData, self._dataSource.data)

    @property
    def filtered_data(self) -> _TData:
        """Data after filtering"""
        return cast(_TData, self._dataSource.filtered_data)

    def ui_select(
        self, column: str, *, clearable=True, multiple=True, **kwargs
    ) -> SelectResult:
        """
        Creates a user interface select box.

        Parameters:
            column (str): The column name of the data source.
            clearable (bool, optional): Whether to allow clearing the content of the select box. Default is True.
            multiple (bool, optional): Whether to allow multiple selections.
            **kwargs: Additional optional parameters that will be passed to the ui.select constructor.

        Returns:
            ui.select: An instance of a user interface select box.
        """
        kws = {key: value for key, value in locals().items() if key not in ("kwargs")}
        return ui_select(**kws)

    def ui_aggrid(self, **kwargs):
        """
        Creates aggrid table.

        Parameters:
            **kwargs: Additional optional parameters that will be passed to the ui.aggrid constructor.

        Returns:
            ui.aggrid: aggrid table.
        """
        kwargs.update(
            {"options": self._dataSource._idataSource.get_aggrid_options(self.data)}
        )

        cp = ui.aggrid(**kwargs)

        def on_source_update(data):
            cp._props["options"] = self._dataSource._idataSource.get_aggrid_options(
                data
            )
            cp.update()

        on_source_update(self.filtered_data)

        self._dataSource._register_component(cp.id, on_source_update)

        return cp

    def ui_radio(self, column: str, **kwargs):
        """
        Creates radio Selection.

        Parameters:
            column (str): The column name of the data source.
            **kwargs: Additional optional parameters that will be passed to the ui.radio constructor.

        Returns:
            ui.radio: An radio Selection.
        """
        options = self._dataSource._idataSource.duplicates_column_values(
            self.data, column
        )
        kwargs.update({"options": options})

        cp = ui.radio(**kwargs)

        def onchange(e):
            cp.value = cp.options[e.args]

            def data_filter(data):
                if cp.value not in cp.options:
                    return data
                cond = data[column] == cp.value
                return data[cond]

            self._dataSource.send_filter(cp.id, Filter(data_filter))

        cp.on("update:modelValue", onchange)

        def on_source_update(data):
            options = self._dataSource._idataSource.duplicates_column_values(
                data, column
            )
            value = cp.value
            if value not in options:
                value = ""

            cp.set_options(options, value=value)

        self._dataSource._register_component(cp.id, on_source_update)

        return cp

    def ui_slider(self, column: str, **kwargs):
        """
        Creates Slider.

        Parameters:
            column (str): The column name of the data source.
            **kwargs: Additional optional parameters that will be passed to the ui.slider constructor.

        Returns:
            ui.radio: An Slider.
        """
        self._dataSource._idataSource.slider_check(self.data, column)

        min, max = self._dataSource._idataSource.slider_min_max(self.data, column)
        kwargs.update({"min": min, "max": max})

        cp = ui.slider(**kwargs).props("label label-always switch-label-side")

        def onchange():
            def data_filter(data):
                if cp.value is None or cp.value < min:
                    return data
                cond = data[column] == cp.value
                return data[cond]

            self._dataSource.send_filter(cp.id, Filter(data_filter))

        cp.on("change", onchange)

        def on_source_update(data):
            min, max = self._dataSource._idataSource.slider_min_max(data, column)
            if min is None or max is None:
                cp.value = None
            else:
                cp._props["min"] = min
                cp._props["max"] = max

        self._dataSource._register_component(cp.id, on_source_update)

        return cp

    def ui_echarts(
        self, fn: Callable[[Any], Union[Dict, "pyecharts.Base"]]  # pyright: ignore
    ) -> echarts:
        """Create charts

        Args:
            fn (Callable[[Any], Union[Dict, "pyecharts.Base"]]): builder function.

        ## Examples

        Support pyecharts

        ```py
        import pandas as pd
        from ex4nicegui import bi
        from pyecharts.charts import Bar

        df = pd.DataFrame({"name": list("abcdc"), "value": range(5)})
        ds = bi.data_source(df)

        @ds.ui_echarts
        def bar(data: pd.DataFrame):
            c = (
                Bar()
                .add_xaxis(data["name"].tolist())
                .add_yaxis("value", data["value"].tolist())
            )

            return c

        bar.classes("h-[20rem]")
        ```

        """

        @ref_computed
        def chart_options():
            options = fn(self.filtered_data)
            if isinstance(options, Dict):
                return options

            import simplejson as json
            from pyecharts.charts.chart import Base

            if isinstance(options, Base):
                return cast(Dict, json.loads(options.dump_options()))

        cp = rxui.echarts(chart_options)  # type: ignore

        return cp.element  # type: ignore
