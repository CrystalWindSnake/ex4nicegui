from .dataSourceFacade import DataSourceFacade
from .dataSource import DataSource
from .protocols import CallableDataSourceAble, DataFrameDataSourceAble
from typing import Callable, cast, TypeVar, Union


_TData = TypeVar("_TData")


def data_source(data: Union[Callable[..., _TData], _TData]) -> DataSourceFacade[_TData]:
    """Create a data source

    Args:
        data (_TData): Any supported data

    Raises:
        TypeError: Throw an error when the data type is not supported

    Returns:
        DataSourceFacade[_TData]: _description_

    ## Examples

    ---

    pandas dataframe source:
    ```python
    df = pd.DataFrame({"name": list("abcdc"), "value": range(5)})
    ds = bi.data_source(df)
    ```

    ---

    Link multiple data sources

    ---
    ```python
    df = pd.DataFrame({"name": list("abcdc"), "value": range(5)})
    ds = bi.data_source(df)

    @bi.data_source
    def ds_other():
        #  ds.filtered_data is DataFrame after filtering
        where = ds.filtered_data[''].isin(['b','c','d'])
        return ds.filtered_data[where]

    ```

    ---

    Now, when `ds` changes, it will trigger changes to `ds_other` and thus drive the related interface components to change.

    ```python
    # select box of data source 'ds'
    # it change will trigger changes to table
    ds.ui_select('name')

    # table of data 'ds_other'
    ds_other.ui_aggrid()
    ```


    """
    ds_protocol = None

    if type(data).__name__ == "DataFrame":
        ds_protocol = DataFrameDataSourceAble(data)

    if isinstance(data, Callable):
        ds_protocol = CallableDataSourceAble(data)

    if ds_protocol is None:
        raise TypeError(f"not support type[{type(data)}]")

    ds = DataSource(ds_protocol)
    return cast(DataSourceFacade[_TData], DataSourceFacade(ds))
