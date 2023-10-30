from typing import (
    List,
    Dict,
)
import ex4nicegui.utils.common as utils_common
from ex4nicegui import effect
from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    ref_computed,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import BindableUi
from .utils import _convert_kws_ref2value


class AggridBindableUi(BindableUi[ui.aggrid]):
    def __init__(
        self,
        options: TMaybeRef[Dict],
        *,
        html_columns: TMaybeRef[List[int]] = [],
        theme: TMaybeRef[str] = "balham",
        **org_kws
    ) -> None:
        kws = {
            "options": options,
            "html_columns": html_columns,
            "theme": theme,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.aggrid(**value_kws, **org_kws)

        super().__init__(element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    @staticmethod
    def from_pandas(df: TMaybeRef, **org_kws):
        if is_ref(df):

            @ref_computed
            def cp_convert_df():
                return utils_common.convert_dataframe(df.value)

            @ref_computed
            def cp_options():
                columnDefs = [
                    {"headerName": col, "field": col}
                    for col in cp_convert_df.value.columns
                ]
                rowData = cp_convert_df.value.to_dict("records")
                data = {"columnDefs": columnDefs, "rowData": rowData}
                return data

            return AggridBindableUi(cp_options, **org_kws)

        columnDefs = [{"headerName": col, "field": col} for col in df.columns]  # type: ignore
        rowData = df.to_dict("records")  # type: ignore
        options = {"columnDefs": columnDefs, "rowData": rowData}
        return AggridBindableUi(options, **org_kws)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "options":
            return self.bind_options(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_options(self, ref_ui: ReadonlyRef[List[Dict]]):
        @effect
        def _():
            ele = self.element
            data = ref_ui.value
            ele._props["options"].update(data)
            ele.update()

        return self
