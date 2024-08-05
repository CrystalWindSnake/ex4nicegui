from __future__ import annotations
from typing import Union, Type
from ex4nicegui.utils.signals import (
    deep_ref,
    is_ref,
    to_value,
    to_ref,
    on,
    to_raw,
)


class ViewModel:
    def __init__(self):
        for name, value in self.__class__.__dict__.items():
            if is_ref(value):
                setattr(self, name, deep_ref(to_value(value)))

    @staticmethod
    def display(model: Union[ViewModel, Type]):
        result = to_ref("")

        all_refs = {
            key: value for key, value in model.__dict__.items() if is_ref(value)
        }

        @on(list(all_refs.values()))
        def _():
            result.value = str(
                {key: recursive_to_value(value) for key, value in all_refs.items()}
            )

        return result


def recursive_to_value(value_or_model):
    value = to_raw(to_value(value_or_model))

    if isinstance(value, ViewModel):
        all_refs = {
            key: value for key, value in value.__dict__.items() if is_ref(value)
        }
        return {key: recursive_to_value(value) for key, value in all_refs.items()}
    elif isinstance(value, dict):
        return {key: recursive_to_value(val) for key, val in value.items()}
    elif isinstance(value, list):
        return [recursive_to_value(val) for val in value]
    else:
        return value