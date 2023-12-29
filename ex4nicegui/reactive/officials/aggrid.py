from typing import (
    Callable,
    List,
    Dict,
    Optional,
)
from ex4nicegui.utils.signals import (
    effect,
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
        auto_size_columns: bool = True,
        **org_kws,
    ) -> None:
        kws = {
            "options": options,
            "html_columns": html_columns,
            "theme": theme,
            "auto_size_columns": auto_size_columns,
        }

        value_kws = _convert_kws_ref2value(kws)
        element = ui.aggrid(**value_kws, **org_kws)

        super().__init__(element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    @staticmethod
    def _get_columnDefs_from_dataframe(df, columns_define_fn: Callable[[str], Dict]):
        return [
            {**{"headerName": col, "field": col}, **columns_define_fn(col)}
            for col in df.columns  # type: ignore
        ]

    @staticmethod
    def from_pandas(
        df: TMaybeRef,
        columns_define_fn: Optional[Callable[[str], Dict]] = None,
        **org_kws,
    ):
        columns_define_fn = columns_define_fn or (lambda x: {})
        if is_ref(df):

            @ref_computed
            def cp_options():
                columnDefs = AggridBindableUi._get_columnDefs_from_dataframe(
                    df.value, columns_define_fn
                )
                rowData = df.value.to_dict("records")
                data = {"columnDefs": columnDefs, "rowData": rowData}
                return data

            return AggridBindableUi(cp_options, **org_kws)

        columnDefs = AggridBindableUi._get_columnDefs_from_dataframe(
            df, columns_define_fn
        )
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
