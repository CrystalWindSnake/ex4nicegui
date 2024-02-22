from typing import (
    Any,
    Callable,
    List,
    Optional,
    Dict,
)
from typing_extensions import Literal
from ex4nicegui.reactive.utils import ParameterClassifier
import ex4nicegui.utils.common as utils_common
from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    ref_computed,
    to_ref,
    effect,
    _TMaybeRef as TMaybeRef,
    to_value,
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
        pc = ParameterClassifier(
            locals(),
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
        self._selection_ref: ReadonlyRef[List[Any]] = to_ref([])

        def on_selection(_):
            self._selection_ref.value = self.element.selected  # type: ignore

        self.element.on("selection", on_selection)

    @property
    def selection_ref(self):
        return self._selection_ref

    @staticmethod
    def from_pandas(
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

        if is_ref(df):

            @ref_computed
            def cp_rows():
                return df.value.to_dict("records")

            @ref_computed
            def cp_cols():
                return [
                    {
                        **{
                            "name": col,
                            "label": col,
                            "field": col,
                        },
                        **columns_define_fn(col),  # type: ignore
                    }
                    for col in df.value.columns
                ]

            return TableBindableUi(cp_cols, cp_rows, **other_kws)

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
        return TableBindableUi(cols, rows, **other_kws)

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

        self.bind_rows(cp_rows).bind_columns(cp_cols)  # type: ignore

        return self

    def bind_rows(self, ref_ui: ReadonlyRef[List[Dict]]):
        @effect
        def _():
            ele = self.element
            ele._props["rows"] = to_value(ref_ui)
            ele.update()

        return self

    def bind_columns(self, ref_ui: ReadonlyRef[List[Dict]]):
        @effect
        def _():
            ele = self.element
            ele._props["columns"] = to_value(ref_ui)
            ele.update()

        return self
