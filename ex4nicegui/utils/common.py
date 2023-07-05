from typing import Callable
import inspect


def get_func_args_len(fn: Callable):
    return len(inspect.getfullargspec(fn).args)
