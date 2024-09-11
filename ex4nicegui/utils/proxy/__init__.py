from .string import StringProxy
from .int import IntProxy

def is_base_type_proxy(obj):
    return isinstance(obj, (StringProxy, IntProxy))
