from typing_extensions import Protocol
from typing import Callable, Dict, List

from ex4nicegui.bi.types import _TFilterCallback
from .types import _TFilterCallback


class IDataSourceAble(Protocol):
    def get_data(self):
        ...

    def apply_filters(self, filters: List[_TFilterCallback]):
        ...

    def duplicates_column_values(self, data, column_name: str) -> List:
        ...

    def get_aggrid_options(self, data) -> Dict:
        ...


class DataFrameDataSourceAble(IDataSourceAble):
    def __init__(self, df) -> None:
        self.data = df

    def get_data(self):
        return self.data

    def apply_filters(self, filters: List[_TFilterCallback]):
        new_data = self.data
        for f in filters:
            new_data = f(new_data)

        return new_data

    def duplicates_column_values(self, data, column_name: str) -> List:
        return data[column_name].drop_duplicates().tolist()

    def get_aggrid_options(self, data) -> Dict:
        df = data
        return {
            "columnDefs": [{"field": col} for col in df.columns],
            "rowData": df.to_dict("records"),
        }


class CallableDataSourceAble(IDataSourceAble):
    def __init__(self, fn: Callable) -> None:
        self.data_fn = fn

    def get_data(self):
        return self.data_fn()

    def apply_filters(self, filters: List[_TFilterCallback]):
        new_data = self.get_data()
        for f in filters:
            new_data = f(new_data)

        return new_data

    def duplicates_column_values(self, data, column_name: str) -> List:
        return data[column_name].drop_duplicates().tolist()

    def get_aggrid_options(self, data) -> Dict:
        df = data
        return {
            "columnDefs": [{"field": col} for col in df.columns],
            "rowData": df.to_dict("records"),
        }
