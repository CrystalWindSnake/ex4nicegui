from typing import (
    Any,
    Callable,
    List,
    Dict,
    Optional,
)
from ex4nicegui.utils.signals import (
    is_ref,
    ref_computed,
    to_value,
    _TMaybeRef as TMaybeRef,
    TGetterOrReadonlyRef,
)
from ex4nicegui.utils.apiEffect import ui_effect
from nicegui import ui
from .base import BindableUi
from ex4nicegui.reactive.utils import ParameterClassifier, dataframe2col_str


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
        pc = ParameterClassifier(
            locals(),
            maybeRefs=["options", "html_columns", "theme", "auto_size_columns"],
            extend_kws="org_kws",
        )

        element = ui.aggrid(**pc.get_values_kws(), **org_kws)

        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @staticmethod
    def _get_columnDefs_from_dataframe(df, columns_define_fn: Callable[[str], Dict]):
        return [
            {**{"headerName": col, "field": col}, **columns_define_fn(col)}
            for col in df.columns  # type: ignore
        ]

    @classmethod
    def from_pandas(
        cls,
        df: TMaybeRef,
        columns_define_fn: Optional[Callable[[str], Dict]] = None,
        **org_kws,
    ):
        columns_define_fn = columns_define_fn or (lambda x: {})
        if is_ref(df) or isinstance(df, Callable):

            @ref_computed
            def cp_options():
                copy_df = dataframe2col_str(to_value(df))
                columnDefs = AggridBindableUi._get_columnDefs_from_dataframe(
                    copy_df, columns_define_fn
                )
                rowData = copy_df.to_dict("records")
                data = {"columnDefs": columnDefs, "rowData": rowData}
                return data

            return cls(cp_options, **org_kws)

        copy_df = dataframe2col_str(df)
        columnDefs = AggridBindableUi._get_columnDefs_from_dataframe(
            copy_df, columns_define_fn
        )
        rowData = copy_df.to_dict("records")  # type: ignore
        options = {"columnDefs": columnDefs, "rowData": rowData}
        return cls(options, **org_kws)

    def bind_prop(self, prop: str, ref_ui: TGetterOrReadonlyRef[Any]):
        if prop == "options":
            return self.bind_options(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_options(self, ref_ui: TGetterOrReadonlyRef[List[Dict]]):
        @ui_effect
        def _():
            ele = self.element
            data = to_value(ref_ui)
            ele._props["options"].update(data)
            ele.update()

        return self
