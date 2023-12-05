from typing_extensions import Protocol
from typing import Any, Callable, Dict, List, Optional, Tuple

from ex4nicegui.bi.types import (
    _TFilterCallback,
    _TDuplicates_column_values_sort_options,
)
from .types import _TFilterCallback
from ex4nicegui.utils import common as utils_common


class IDataSourceAble(Protocol):
    def get_data(self) -> Any:
        ...

    def reload(self, data) -> None:
        ...

    def apply_filters(self, data, filters: List[_TFilterCallback]) -> Any:
        ...

    def duplicates_column_values(
        self,
        data,
        column_name: str,
        *,
        exclude_null_value=True,
        sort_options: Optional[_TDuplicates_column_values_sort_options],
    ) -> List:
        ...

    def get_aggrid_options(self, data) -> Dict:
        ...

    def slider_check(self, data, column_name: str) -> None:
        ...

    def slider_min_max(
        self, data, column_name: str
    ) -> Tuple[Optional[float], Optional[float]]:
        ...

    def range_check(self, data, column_name: str) -> None:
        ...

    def range_min_max(
        self, data, column_name: str
    ) -> Tuple[Optional[float], Optional[float]]:
        ...


class CallableDataSourceAble(IDataSourceAble):
    def __init__(self, fn: Callable) -> None:
        self.data_fn = fn

    def reload(self, data) -> None:
        raise NotImplementedError("CallableDataSource not support reload")

    def get_data(self):
        return self.data_fn()

    def apply_filters(self, data, filters: List[_TFilterCallback]):
        new_data = data
        for f in filters:
            new_data = f(new_data)

        return new_data

    def duplicates_column_values(
        self,
        data,
        column_name: str,
        *,
        exclude_null_value=True,
        sort_options: Optional[_TDuplicates_column_values_sort_options],
    ) -> List:
        sort_options = sort_options or {}
        sort_cols = list(sort_options.keys())
        ascendings = list(opt == "asc" for opt in sort_options.values())

        data = data.sort_values(sort_cols, ascending=ascendings)
        if exclude_null_value:
            data = data[data[column_name].notnull()]

        return data[column_name].drop_duplicates().tolist()

    def get_aggrid_options(self, data) -> Dict:
        df = utils_common.convert_dataframe(data)
        return {
            "columnDefs": [{"field": col} for col in df.columns],
            "rowData": df.to_dict("records"),
        }

    def slider_check(self, data, column_name: str) -> None:
        from pandas.api.types import is_numeric_dtype

        if not is_numeric_dtype(data[column_name]):
            raise ValueError(f"column[{column_name}] must be numeric type")

    def slider_min_max(
        self, data, column_name: str
    ) -> Tuple[Optional[float], Optional[float]]:
        import numpy as np

        min, max = data[column_name].min(), data[column_name].max()

        if np.isnan(min) or np.isnan(max):
            return None, None

        return min, max

    def range_check(self, data, column_name: str) -> None:
        from pandas.api.types import is_numeric_dtype

        if not is_numeric_dtype(data[column_name]):
            raise ValueError(f"column[{column_name}] must be numeric type")

    def range_min_max(
        self, data, column_name: str
    ) -> Tuple[Optional[float], Optional[float]]:
        import numpy as np

        min, max = data[column_name].min(), data[column_name].max()

        if np.isnan(min) or np.isnan(max):
            return None, None

        return min, max


class DataFrameDataSourceAble(CallableDataSourceAble):
    def __init__(self, df) -> None:
        self.data = df
        super().__init__(lambda: self.data)

    def reload(self, data) -> None:
        self.data = data

    def get_data(self):
        return self.data

    def apply_filters(self, data, filters: List[_TFilterCallback]):
        new_data = data
        for f in filters:
            new_data = f(new_data)

        return new_data
