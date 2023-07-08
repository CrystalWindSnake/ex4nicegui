from typing import Callable
import inspect


def get_func_args_len(fn: Callable):
    return len(inspect.getfullargspec(fn).args)


def convert_dataframe(df):
    import pandas as pd

    assert isinstance(df, pd.DataFrame)
    with pd.option_context("mode.chained_assignment", None):
        for col in df.select_dtypes(["datetime"]).columns:
            df[col] = df[col].dt.strftime("%Y-%m-%d")

    return df
