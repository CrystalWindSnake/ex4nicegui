from .string import StringProxy
from .int import IntProxy
from .list import ListProxy


def is_base_type_proxy(obj):
    return isinstance(obj, (StringProxy, IntProxy, ListProxy))


def to_ref_if_base_type_proxy(obj):
    if is_base_type_proxy(obj):
        return obj._ref
    else:
        return obj
