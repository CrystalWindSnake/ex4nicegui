from typing import Callable, Dict
from ex4nicegui.utils.signals import to_value


def convert_kws_ref2value(kws: Dict) -> Dict:
    return {key: to_value(value) for key, value in kws.items()}


def inject_method(obj, method_name: str, new_handle: Callable):
    if hasattr(obj, method_name):
        original_method = getattr(obj, method_name)

        def injected_method(*args, **kwargs):
            new_handle(*args, **kwargs)
            return original_method(*args, **kwargs)

        setattr(obj, method_name, injected_method)
    else:
        raise AttributeError(
            f"'{type(obj).__name__}' object has no attribute '{method_name}'."
        )
