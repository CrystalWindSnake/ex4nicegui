from typing import (
    Any,
    Callable,
    List,
    Optional,
    Dict,
)
from typing_extensions import Literal
import ex4nicegui.utils.common as utils_common
from signe import effect
from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    ref_computed,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import BindableUi
from .utils import _convert_kws_ref2value


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
    ) -> None:
        kws = {
            "columns": columns,
            "rows": rows,
            "row_key": row_key,
            "title": title,
            "selection": selection,
            "pagination": pagination,
            "on_select": on_select,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.table(**value_kws)

        super().__init__(element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    @staticmethod
    def from_pandas(df: TMaybeRef):
        if is_ref(df):

            @ref_computed
            def cp_convert_df():
                return utils_common.convert_dataframe(df.value)

            @ref_computed
            def cp_rows():
                return cp_convert_df.value.to_dict("records")

            @ref_computed
            def cp_cols():
                return [
                    {
                        "name": col,
                        "label": col,
                        "field": col,
                    }
                    for col in cp_convert_df.value.columns
                ]

            return TableBindableUi(cp_cols, cp_rows)

        df = utils_common.convert_dataframe(df)
        rows = df.to_dict("records")

        cols = [
            {
                "name": col,
                "label": col,
                "field": col,
            }
            for col in df.columns
        ]
        return TableBindableUi(cols, rows)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "dataframe":
            return self.bind_dataframe(ref_ui)

        if prop == "rows":
            return self.bind_rows(ref_ui)

        if prop == "columns":
            return self.bind_columns(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_dataframe(self, ref_df: ReadonlyRef):
        @ref_computed
        def cp_converted_df():
            df = ref_df.value
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

        self.bind_rows(cp_rows).bind_columns(cp_cols)

        return self

    def bind_rows(self, ref_ui: ReadonlyRef[List[Dict]]):
        @effect
        def _():
            ele = self.element
            ele._props["rows"] = ref_ui.value
            ele.update()

        return self

    def bind_columns(self, ref_ui: ReadonlyRef[List[Dict]]):
        @effect
        def _():
            ele = self.element
            ele._props["columns"] = ref_ui.value
            ele.update()

        return self
