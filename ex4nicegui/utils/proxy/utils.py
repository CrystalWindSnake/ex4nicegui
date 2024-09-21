from typing import Any, TypeVar


def to_value(value: Any):
    return value._ref.value if hasattr(value, "_ref") else value
