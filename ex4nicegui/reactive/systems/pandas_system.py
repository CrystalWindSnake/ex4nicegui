try:
    import pandas as pd
except ImportError:
    pass


def dataframe2col_str(df, copy=True):
    if isinstance(df.columns, pd.MultiIndex):
        raise ValueError(
            "MultiIndex columns are not supported. "
            "You can convert them to strings using something like "
            '`df.columns = ["_".join(col) for col in df.columns.values]`.'
        )

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
        df = df.copy() if copy else df
        df[date_cols] = df[date_cols].astype(str)
        df[time_cols] = df[time_cols].astype(str)
        df[complex_cols] = df[complex_cols].astype(str)
        df[period_cols] = df[period_cols].astype(str)

    return df
