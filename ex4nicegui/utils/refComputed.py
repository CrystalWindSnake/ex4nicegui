from functools import partial
import types
import signe
from .clientScope import _CLIENT_SCOPE_MANAGER
from typing import (
    Any,
    Dict,
    Protocol,
    Type,
    TypeVar,
    Generic,
    overload,
    Optional,
    Callable,
    cast,
    Union,
)
from .scheduler import get_uiScheduler
from .types import (
    ReadonlyRef,
    DescReadonlyRef,
)

import inspect


T = TypeVar("T", covariant=True)


class TInstanceCall(Protocol[T]):
    def __call__(_, self) -> T:  # type: ignore
        ...


@overload
def ref_computed(
    fn: Union[Callable[[], T], TInstanceCall[T]],
    *,
    desc="",
    debug_trigger: Optional[Callable[..., None]] = None,
    priority_level: int = 1,
    debug_name: Optional[str] = None,
) -> ReadonlyRef[T]:
    """Takes a getter function and returns a readonly reactive ref object for the returned value from the getter. It can also take an object with get and set functions to create a writable ref object.

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#ref_computed
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#ref_computed


    Args:
        fn (Callable[[], T]): _description_
        desc (str, optional): _description_. Defaults to "".
        debug_trigger (Optional[Callable[..., None]], optional): _description_. Defaults to None.
        priority_level (int, optional): _description_. Defaults to 1.
        debug_name (Optional[str], optional): _description_. Defaults to None.

    """
    ...


@overload
def ref_computed(
    fn=None,
    *,
    desc="",
    debug_trigger: Optional[Callable[..., None]] = None,
    priority_level: int = 1,
    debug_name: Optional[str] = None,
) -> Callable[[Callable[..., T]], ReadonlyRef[T]]:
    ...


def ref_computed(
    fn: Optional[Union[Callable[[], T], TInstanceCall[T]]] = None,
    *,
    desc="",
    debug_trigger: Optional[Callable[..., None]] = None,
    priority_level: int = 1,
    debug_name: Optional[str] = None,
) -> Union[ReadonlyRef[T], Callable[[Callable[..., T]], ReadonlyRef[T]]]:
    kws = {
        "debug_trigger": debug_trigger,
        "priority_level": priority_level,
        "debug_name": debug_name,
    }

    if fn:
        if _systems.is_class_define_method(fn):
            return cast(
                ref_computed_method[T],
                ref_computed_method(fn, computed_args=kws),  # type: ignore
            )  # type: ignore

        getter = signe.Computed(
            cast(Callable[[], T], fn),
            **kws,
            scope=_CLIENT_SCOPE_MANAGER.get_current_scope(),
            scheduler=get_uiScheduler(),
        )
        return cast(DescReadonlyRef[T], getter)

    else:

        def wrap(fn: Callable[[], T]):
            return ref_computed(fn, **kws)

        return wrap


class ref_computed_method(Generic[T]):
    __isabstractmethod__: bool

    def __init__(self, fget: Callable[[Any], T], computed_args: Dict) -> None:
        self._fget = fget
        self._computed_args = computed_args

    def __set_name__(self, owner, name):
        _systems.add_computed_to_instance(owner, name, self._fget, self._computed_args)


class _systems:
    @staticmethod
    def is_class_define_method(fn: Callable):
        has_name = hasattr(fn, "__name__")
        qualname_prefix = f".<locals>.{fn.__name__}" if has_name else ""

        return (
            hasattr(fn, "__qualname__")
            and has_name
            and "." in fn.__qualname__
            and qualname_prefix != fn.__qualname__[-len(qualname_prefix) :]
            and (isinstance(fn, types.FunctionType))
        )

    @staticmethod
    def get_method_class(method):
        """
        Get the class of a class-defined method.
        """
        if not inspect.isfunction(method):
            raise ValueError("The provided argument is not a class-defined method")

        method_name = method.__qualname__
        if "." not in method_name:
            raise ValueError(
                "The provided method does not appear to be a class-defined method"
            )

        class_name = method_name.split(".")[0]
        for cls in inspect.getmembers(inspect.getmodule(method), inspect.isclass):
            if cls[0] == class_name:
                return cls[1]

        raise ValueError(f"Class {class_name} not found")

    @staticmethod
    def add_computed_to_instance(
        cls_type: Type, attr_name: str, fn: Callable, computed_args: Dict
    ):
        """
        Add an attribute to an instance of a class.
        """
        original_init = cls_type.__init__

        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            setattr(self, attr_name, ref_computed(partial(fn, self), **computed_args))

        cls_type.__init__ = new_init
        return cls_type
