from .base import Proxy


def is_base_type_proxy(obj):
    return isinstance(obj, Proxy)


def to_ref_if_base_type_proxy(obj):
    if is_base_type_proxy(obj):
        return obj._ref
    else:
        return obj


def to_value_if_base_type_proxy(obj):
    if is_base_type_proxy(obj):
        return obj._ref.value
    else:
        return obj
