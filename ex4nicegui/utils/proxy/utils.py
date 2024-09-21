from typing import Any
from .base import Proxy


def to_value(value: Any):
    return value._ref.value if isinstance(value, Proxy) else value
