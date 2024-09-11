from .string import StringProxy
from .int import IntProxy
from .list import ListProxy


def is_base_type_proxy(obj):
    return isinstance(obj, (StringProxy, IntProxy, ListProxy))
