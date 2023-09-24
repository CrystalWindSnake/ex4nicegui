from typing_extensions import Protocol
from typing import Callable, Dict, List, Optional, Tuple

from ex4nicegui.bi.types import _TFilterCallback
from .types import _TFilterCallback
from ex4nicegui.utils import common as utils_common


class IDataSourceAble(Protocol):
    def get_data(self):
        ...

    def apply_filters(self, data, filters: List[_TFilterCallback]):
        ...

    def duplicates_column_values(self, data, column_name: str) -> List:
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


class DataFrameDataSourceAble(IDataSourceAble):
    def __init__(self, df) -> None:
        self.data = df

    def get_data(self):
        return self.data

    def apply_filters(self, data, filters: List[_TFilterCallback]):
        new_data = data
        for f in filters:
            new_data = f(new_data)

        return new_data

    def duplicates_column_values(self, data, column_name: str) -> List:
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


class CallableDataSourceAble(IDataSourceAble):
    def __init__(self, fn: Callable) -> None:
        self.data_fn = fn

    def get_data(self):
        return self.data_fn()

    def apply_filters(self, data, filters: List[_TFilterCallback]):
        new_data = data
        for f in filters:
            new_data = f(new_data)

        return new_data

    def duplicates_column_values(self, data, column_name: str) -> List:
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
