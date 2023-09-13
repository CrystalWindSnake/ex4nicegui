from .dataSourceFacade import DataSourceFacade
from .dataSource import DataSource
from .protocols import CallableDataSourceAble, DataFrameDataSourceAble
from typing import Callable, cast, TypeVar


_TData = TypeVar("_TData")


def data_source(data: _TData) -> DataSourceFacade[_TData]:
    ds_protocol = None

    if type(data).__name__ == "DataFrame":
        ds_protocol = DataFrameDataSourceAble(data)

    if isinstance(data, Callable):
        ds_protocol = CallableDataSourceAble(data)

    if ds_protocol is None:
        raise ValueError(f"not support type[{type(data)}]")

    ds = DataSource(ds_protocol)
    return cast(DataSourceFacade[_TData], DataSourceFacade(ds))
