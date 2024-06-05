from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Protocol,
    Tuple,
    cast,
    runtime_checkable,
    Union,
)

from ex4nicegui.utils.signals import is_ref, to_value, is_setter_ref
from nicegui.events import handle_event

try:
    import pandas as pd
except ImportError:
    pass


# @runtime_checkable
# class GetItemProtocol(Protocol):
#     def __getitem__(self, key):
#         ...


# @runtime_checkable
# class SetItemProtocol(Protocol):
#     def __setitem__(self, key, value):
#         ...


# def _convert_kws_ref2value(kws: Dict) -> Dict:
#     return {key: to_value(value) for key, value in kws.items()}


# class ParameterClassifier:
#     def __init__(
#         self,
#         args: Dict,
#         *,
#         maybeRefs: Optional[Iterable[str]] = None,
#         events: Optional[List[str]] = None,
#         v_model: Optional[Tuple[str, str]] = None,
#         v_model_arg_getter: Optional[Callable[[Any], Any]] = None,
#         exclude: Optional[List[str]] = None,
#         extend_kws: Optional[str] = None,
#     ) -> None:
#         exclude = exclude or []
#         if extend_kws:
#             exclude.append(extend_kws)

#         self._args: Dict[str, Any] = {
#             k: v
#             for k, v in args.items()
#             if k != "self" and k[0] != "_" and (k not in exclude)
#         }

#         self.maybeRefs = maybeRefs or []
#         self.events = events or []
#         self.v_model = v_model
#         self.v_model_arg_getter = v_model_arg_getter or (lambda e: getattr(e, "value"))

#         if extend_kws:
#             extend_args = cast(Dict, args.get(extend_kws))
#             self.events.extend(
#                 k for k, v in extend_args.items() if isinstance(v, Callable)
#             )

#             self._args.update(
#                 {k: v for k, v in extend_args.items() if not isinstance(v, Callable)}
#             )

#     def get_values_kws(self) -> Dict:
#         value_kws = _convert_kws_ref2value(
#             {k: v for k, v in self._args.items() if k not in self.events}
#         )

#         # replace event
#         value_kws.update({k: v for k, v in self._args.items() if k in self.events})

#         if self.v_model:
#             v_name, event_name = self.v_model
#             model_value = self._args.get(v_name)
#             event = self._args.get(event_name)

#             if is_setter_ref(model_value):

#                 def inject_on_change(e):
#                     model_value.value = self.v_model_arg_getter(e)  # type: ignore
#                     handle_event(event, e)

#                 value_kws.update({event_name: inject_on_change})

#         return value_kws

#     def get_bindings(self) -> Dict:
#         return {
#             k.replace("_", "-"): v
#             for k, v in self._args.items()
#             if (k in self.maybeRefs and (is_ref(v) or isinstance(v, Callable)))
#         }


# def get_attribute(obj: Union[object, GetItemProtocol], name: Union[str, int]) -> Any:
#     if isinstance(obj, (GetItemProtocol)):
#         return obj[name]
#     return getattr(obj, name)  # type: ignore


# def set_attribute(
#     obj: Union[object, SetItemProtocol], name: Union[str, int], value: Any
# ) -> None:
#     if isinstance(obj, SetItemProtocol):
#         obj[name] = value
#     else:
#         setattr(obj, name, value)  # type: ignore


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
