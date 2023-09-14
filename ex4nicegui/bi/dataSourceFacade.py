from typing import TypeVar, Generic, cast
from nicegui import ui


from .dataSource import DataSource, Filter


_TData = TypeVar("_TData")


class DataSourceFacade(Generic[_TData]):
    def __init__(self, ds: DataSource) -> None:
        self._dataSource = ds

    @property
    def data(self) -> _TData:
        return cast(_TData, self._dataSource.data)

    @property
    def filtered_data(self) -> _TData:
        return cast(_TData, self._dataSource.filtered_data)

    def ui_select(self, column: str, *, clearable=True, **kwargs) -> ui.select:
        """
        Creates a user interface select box.

        Parameters:
            column (str): The column name of the data source.
            clearable (bool, optional): Whether to allow clearing the content of the select box. Default is True.
            **kwargs: Additional optional parameters that will be passed to the ui.select constructor.

        Returns:
            ui.select: An instance of a user interface select box.
        """
        options = self._dataSource._idataSource.duplicates_column_values(
            self.data, column
        )
        kwargs.update({"options": options, "clearable": clearable, "label": column})

        cp = ui.select(**kwargs)

        def onchange(e):
            value = None
            if e.args:
                value = e.args["label"]

            cp.value = value

            def data_filter(data):
                if cp.value is None:
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
