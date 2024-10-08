from typing import (
    Any,
    Callable,
    List,
    Optional,
    Dict,
)
from typing_extensions import Literal
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.reactive.services.pandas_service import dataframe2col_str

import ex4nicegui.utils.common as utils_common
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    TReadonlyRef,
    is_ref,
    ref_computed,
    to_ref,
    _TMaybeRef as TMaybeRef,
    to_value,
    to_raw,
    RefWrapper,
)
from nicegui import ui
from .base import BindableUi


class TableBindableUi(BindableUi[ui.table]):
    def __init__(
        self,
        columns: TMaybeRef[List[Dict]],
        rows: TMaybeRef[List[Dict]],
        row_key: TMaybeRef[str] = "id",
        title: Optional[TMaybeRef[str]] = None,
        selection: Optional[TMaybeRef[Literal["single", "multiple"]]] = None,
        pagination: Optional[TMaybeRef[int]] = 15,
        on_select: Optional[Callable[..., Any]] = None,
        on_pagination_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        local_args = locals()
        rows_data = local_args.get("rows")
        if isinstance(rows_data, RefWrapper):
            local_args.update(rows=lambda: rows_data.value)
        columns_data = local_args.get("columns")  # type: ignore
        if isinstance(columns_data, RefWrapper):
            local_args.update(columns=lambda: columns_data.value)

        pc = ParameterClassifier(
            local_args,
            maybeRefs=[
                "columns",
                "rows",
                "row_key",
                "title",
                "selection",
                "pagination",
            ],
            events=["on_select", "on_pagination_change"],
        )

        value_kws = pc.get_values_kws()

        element = ui.table(**value_kws)
        super().__init__(element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

        self._arg_selection = selection
        self._arg_row_key = row_key
        self._selection_ref: TReadonlyRef[List[Any]] = to_ref([])  # type: ignore

        def on_selection(_):
            self._selection_ref.value = self.element.selected  # type: ignore

        self.element.on("selection", on_selection)

    @property
    def selection_ref(self):
        return self._selection_ref

    @classmethod
    def from_pandas(
        cls,
        df: TMaybeRef,
        *,
        columns_define_fn: Optional[Callable[[str], Dict]] = None,
        row_key="id",
        title: Optional[TMaybeRef[str]] = None,
        selection: Optional[TMaybeRef[Literal["single", "multiple"]]] = None,
        pagination: Optional[TMaybeRef[int]] = 15,
        on_select: Optional[Callable[..., Any]] = None,
        on_pagination_change: Optional[Callable[..., Any]] = None,
    ):
        columns_define_fn = columns_define_fn or (lambda x: {})
        other_kws = {
            "row_key": row_key,
            "title": title,
            "selection": selection,
            "pagination": pagination,
            "on_select": on_select,
            "on_pagination_change": on_pagination_change,
        }

        if is_ref(df) or isinstance(df, Callable):

            @ref_computed
            def cp_rows_columns():
                copy_df = dataframe2col_str(to_value(df))
                rows = copy_df.to_dict("records")

                columns = [
                    {
                        **{
                            "name": col,
                            "label": col,
                            "field": col,
                        },
                        **columns_define_fn(col),  # type: ignore
                    }
                    for col in copy_df.columns
                ]

                return rows, columns

            return cls(
                lambda: cp_rows_columns.value[1],
                lambda: cp_rows_columns.value[0],
                **other_kws,
            )

        df = dataframe2col_str(df)
        rows = df.to_dict("records")  # type: ignore

        cols = [
            {
                **{
                    "name": col,
                    "label": col,
                    "field": col,
                },
                **columns_define_fn(col),
            }
            for col in df.columns  # type: ignore
        ]
        return cls(cols, rows, **other_kws)

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if prop == "dataframe":
            return self.bind_dataframe(value)

        if prop == "rows":
            return self.bind_rows(value)

        if prop == "columns":
            return self.bind_columns(value)

        return super().bind_prop(prop, value)

    def bind_dataframe(self, dataframe: TGetterOrReadonlyRef):
        @ref_computed
        def cp_converted_df():
            df = dataframe.value
            return utils_common.convert_dataframe(df)

        @ref_computed
        def cp_rows():
            return cp_converted_df.value.to_dict("records")

        @ref_computed
        def cp_cols():
            return [
                {
                    "name": col,
                    "label": col,
                    "field": col,
                }
                for col in cp_converted_df.value.columns
            ]

        self.bind_rows(cp_rows).bind_columns(cp_cols)  # type: ignore

        return self

    def bind_rows(self, rows: TGetterOrReadonlyRef[List[Dict]]):
        @self._ui_signal_on(rows, deep=True)
        def _():
            ele = self.element
            ele._props["rows"] = list(to_raw(to_value(rows)))
            ele.update()

        return self

    def bind_columns(self, columns: TGetterOrReadonlyRef[List[Dict]]):
        @self._ui_signal_on(columns, deep=True)
        def _():
            ele = self.element
            ele._props["columns"] = list(to_raw(to_value(columns)))
            ele.update()

        return self
