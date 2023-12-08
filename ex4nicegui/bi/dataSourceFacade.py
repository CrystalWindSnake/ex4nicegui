from __future__ import annotations
from typing import (
    Any,
    Callable,
    Dict,
    TYPE_CHECKING,
    List,
    Optional,
    TypeVar,
    Generic,
    Union,
    cast,
)
from nicegui import ui
from .dataSource import DataSource, Filter
from . import types as bi_types
from .elements.ui_select import ui_select
from .elements.ui_radio import ui_radio
from .elements.ui_slider import ui_slider
from .elements.ui_range import ui_range
from .elements.ui_echarts import ui_echarts
from .elements.ui_aggrid import ui_aggrid
from .elements.ui_table import ui_table
from ex4nicegui.bi import types as bi_types

if TYPE_CHECKING:
    from ex4nicegui.bi.elements.models import UiResult

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

    def reload(self, data, reset_filters=True):
        """Reload the data source with the provided new data.

        Args:
            data (_type_): The new data source to be loaded.
            reset_filters (bool, optional): Whether to remove all filters. Defaults to True.
        """
        self._dataSource.reload(data)

        if reset_filters:
            self.remove_filters()

    def remove_filters(self, *components: UiResult):
        """Remove the filter from the data source"""
        if len(components) == 0:
            # remove all
            self._dataSource.remove_all_filters()
        else:
            pass

    def ui_select(
        self,
        column: str,
        *,
        sort_options: Optional[bi_types._TDuplicates_column_values_sort_options] = None,
        exclude_null_value=False,
        clearable=True,
        multiple=True,
        **kwargs,
    ):
        """
        Creates a user interface select box.

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#dropdown-select-box-dsui_select
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/docs/apis#dsui_select

        Args:
            column (str): The column name of the data source.
            clearable (bool, optional): Whether to allow clearing the content of the select box. Default is True.
            multiple (bool, optional): Whether to allow multiple selections.
            **kwargs: Additional optional parameters that will be passed to the ui.select constructor.

        Returns:
            SelectResult: An instance of a user interface select box.
        """
        kws = {key: value for key, value in locals().items() if key not in ("kwargs")}
        kws.update(kwargs)
        return ui_select(**kws)

    def ui_aggrid(self, *, options: Optional[Dict] = None, **kwargs):
        """
        Creates aggrid table.

        Parameters:
            **kwargs: Additional optional parameters that will be passed to the ui.aggrid constructor.

        Returns:
            ui.aggrid: aggrid table.
        """
        kws = {key: value for key, value in locals().items() if key not in ("kwargs")}
        kws.update(kwargs)
        return ui_aggrid(**kws)

    def ui_table(
        self,
        *,
        columns: Optional[List[Dict]] = None,
        pagination=20,
        **kwargs,
    ):
        """
        Creates table.

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#dropdown-select-box-dsui_select
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#%E4%B8%8B%E6%8B%89%E6%A1%86%E9%80%89%E6%8B%A9%E6%A1%86-dsui_select


        Parameters:
            **kwargs: Additional optional parameters that will be passed to the ui.table constructor.

        Returns:
            ui.table: ui.table.
        """
        kws = {key: value for key, value in locals().items() if key not in ("kwargs")}
        kws.update(kwargs)
        return ui_table(**kws)

    def ui_radio(
        self,
        column: str,
        *,
        sort_options: Optional[bi_types._TDuplicates_column_values_sort_options] = None,
        exclude_null_value=False,
        hide_filtered=True,
        custom_options_map: Optional[Union[Dict, Callable[[Any], Any]]] = None,
        **kwargs,
    ):
        """
        Creates radio Selection.

        Parameters:
            column (str): The column name of the data source.

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
