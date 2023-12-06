from typing import Callable
import inspect


def get_func_args_len(fn: Callable):
    return len(inspect.getfullargspec(fn).args)


def convert_dataframe(df):
    import pandas as pd

    assert isinstance(df, pd.DataFrame)
    with pd.option_context("mode.chained_assignment", None):
        date_cols = df.columns[df.dtypes == "datetime64[ns]"]
        time_cols = df.columns[df.dtypes == "timedelta64[ns]"]
        complex_cols = df.columns[df.dtypes == "complex128"]
        period_cols = df.columns[df.dtypes == "period[M]"]
        if (
            len(date_cols) != 0
            or len(time_cols) != 0
            or len(complex_cols) != 0
            or len(period_cols) != 0
        ):
            df = df.copy()
            df[date_cols] = df[date_cols].astype(str)
            df[time_cols] = df[time_cols].astype(str)
            df[complex_cols] = df[complex_cols].astype(str)
            df[period_cols] = df[period_cols].astype(str)

    return df
