from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic, Union, cast
from nicegui import ui
from .dataSource import DataSource, Filter
from . import types as bi_types
from .elements.ui_select import ui_select
from .elements.ui_radio import ui_radio
from .elements.ui_slider import ui_slider
from .elements.ui_range import ui_range
from .elements.ui_echarts import ui_echarts
from .elements.ui_aggrid import ui_aggrid


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
        self,
        column: str,
        *,
        custom_data_fn: Optional[Callable[[Any], Any]] = None,
        clearable=True,
        multiple=True,
        **kwargs,
    ):
        """
        Creates a user interface select box.

        Parameters:
            column (str): The column name of the data source.
            custom_data_fn (callback[[pd.DataFrame],pd.DataFrame]): allows for custom data sources. After the data source is filtered, it will be passed into this function, and the result returned by the function will be used for duplicate removal processing.
            clearable (bool, optional): Whether to allow clearing the content of the select box. Default is True.
            multiple (bool, optional): Whether to allow multiple selections.
            **kwargs: Additional optional parameters that will be passed to the ui.select constructor.

        Returns:
            SelectResult: An instance of a user interface select box.
        """
        kws = {key: value for key, value in locals().items() if key not in ("kwargs")}
        kws.update(kwargs)
        return ui_select(**kws)

    def ui_aggrid(
        self, *, custom_data_fn: Optional[Callable[[Any], Any]] = None, **kwargs
    ):
        """
        Creates aggrid table.

        Parameters:
            **kwargs: Additional optional parameters that will be passed to the ui.aggrid constructor.

        Returns:
            ui.aggrid: aggrid table.
        """
        return ui_aggrid(self, custom_data_fn=custom_data_fn, **kwargs)

    def ui_radio(
        self,
        column: str,
        *,
        hide_filtered=True,
        custom_data_fn: Optional[Callable[[Any], Any]] = None,
        custom_options_map: Optional[Union[Dict, Callable[[List], Dict]]] = None,
        **kwargs,
    ):
        """
        Creates radio Selection.

        Parameters:
            column (str): The column name of the data source.
            custom_data_fn (callback[[pd.DataFrame],pd.DataFrame]): allows for custom data sources. After the data source is filtered, it will be passed into this function, and the result returned by the function will be used for duplicate removal processing.

            **kwargs: Additional optional parameters that will be passed to the ui.radio constructor.

        Returns:
            RadioResult: An radio Selection.
        """
        kws = {key: value for key, value in locals().items() if key not in ("kwargs")}
        kws.update(kwargs)
        return ui_radio(**kws)

    def ui_slider(self, column: str, **kwargs):
        """
        Creates Slider.

        Parameters:
            column (str): The column name of the data source.
            **kwargs: Additional optional parameters that will be passed to the ui.slider constructor.

        Returns:
            ui.radio: An Slider.
        """
        kws = {key: value for key, value in locals().items() if key not in ("kwargs")}
        kws.update(kwargs)
        return ui_slider(**kws)

    def ui_range(self, column: str, **kwargs):
        """
        Creates Range.

        Parameters:
            column (str): The column name of the data source.
            **kwargs: Additional optional parameters that will be passed to the ui.slider constructor.

        Returns:
            QRange: An Range.
        """
        kws = {key: value for key, value in locals().items() if key not in ("kwargs")}
        kws.update(kwargs)
        return ui_range(**kws)

    def ui_echarts(
        self, fn: Callable[[Any], Union[Dict, "pyecharts.Base"]]  # pyright: ignore
    ):
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
        return ui_echarts(self, fn)

    def send_filter(
        self, element: ui.element, filter: bi_types._TFilterCallback[_TData]
    ):
        ele_id = element.id
        key = self._dataSource.get_component_info_key(ele_id)
        if not self._dataSource._component_map.has_record(key):
            self._dataSource._register_component(ele_id)
        self._dataSource.send_filter(ele_id, Filter(filter))
