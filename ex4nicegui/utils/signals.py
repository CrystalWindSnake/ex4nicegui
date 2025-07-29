from datetime import date, datetime
import inspect
import signe
from signe.core.scope import Scope
from .clientScope import _CLIENT_SCOPE_MANAGER
from typing import (
    Any,
    Dict,
    TypeVar,
    Optional,
    Callable,
    cast,
    Union,
    Sequence,
)
from nicegui import ui
from nicegui.functions.refreshable import RefreshableContainer
from .effect import effect
from .scheduler import get_uiScheduler
from .types import (
    _TMaybeRef,
    TGetterOrReadonlyRef,
    Ref,
    TReadonlyRef,  # noqa: F401
    TRef,  # noqa: F401
    DescReadonlyRef,  # noqa: F401
    _TMaybeRef as TMaybeRef,  # noqa: F401
)
from .refWrapper import RefWrapper, to_ref_wrapper  # noqa: F401
from .refComputed import ref_computed  # noqa: F401
from ex4nicegui.utils.proxy import (
    to_ref_if_base_type_proxy,
    to_value_if_base_type_proxy,
)

T = TypeVar("T")


is_reactive = signe.is_reactive
to_raw = signe.to_raw


def reactive(obj: T) -> T:
    return signe.reactive(obj, get_uiScheduler())


def is_setter_ref(obj):
    return isinstance(obj, (signe.Signal, RefWrapper))


def is_ref(obj: Any):
    """Checks if a value is a ref object."""
    return signe.is_signal(obj) or isinstance(obj, (RefWrapper))


def to_value(obj: Union[_TMaybeRef[T], RefWrapper]) -> T:
    """unwraps a ref object and returns its inner value.

    Args:
        obj (Union[_TMaybeRef[T], RefWrapper]): A getter function, an existing ref, or a non-function value.

    ## Example

    .. code-block:: python
        to_value(1)  # 1
        to_value(lambda: 1)  # 1
        to_value(to_ref(1))  # 1

    """
    obj = to_value_if_base_type_proxy(obj)
    if is_ref(obj):
        return obj.value  # type: ignore
    if isinstance(obj, Callable):
        return obj()

    return cast(T, obj)


WatchedState = signe.WatchedState


def to_ref(maybe_ref: _TMaybeRef[T], is_deep=False):
    """Takes an inner value and returns a reactive and mutable ref object, which has a single property .value that points to the inner value.

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#to_ref
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#to_ref


    Args:
        maybe_ref (_TMaybeRef[T]): _description_


    """
    if is_ref(maybe_ref):
        return cast(Ref[T], maybe_ref)

    return cast(Ref[T], ref(maybe_ref, is_deep))


def _is_comp_values(value):
    return isinstance(
        value,
        (str, int, float, date, datetime),
    )


def _ref_comp_with_None(old, new):
    # Prevent Constant Repeated Assignment of None
    if old is None and new is None:
        return True

    return False


def ref(value: T, is_deep=False) -> Ref[T]:
    comp = False  # Default never equal

    if _is_comp_values(value):
        comp = None  # comparison of `==`

    if value is None:
        comp = _ref_comp_with_None

    s = signe.signal(value, comp, is_shallow=not is_deep, scheduler=get_uiScheduler())
    return cast(Ref[T], s)


def deep_ref(value: T) -> Ref[T]:
    """Deep response version of `to_ref`.

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#deep_ref
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#deep_ref

    >>> deep_ref(1)
    >>> deep_ref([1,2,3])

    """
    return to_ref(value, is_deep=True)


_T_effect_refreshable_refs = Union[
    TGetterOrReadonlyRef,
    RefWrapper,
    Sequence[TGetterOrReadonlyRef],
    _TMaybeRef,
    Sequence[_TMaybeRef],
]


class effect_refreshable:
    def __init__(self, fn: Callable, refs: _T_effect_refreshable_refs = []) -> None:
        self._fn = fn

        refs = to_ref_if_base_type_proxy(refs)

        if isinstance(refs, Sequence):
            ref_arg = [ref for ref in refs if self._is_valid_ref(ref)]
        else:
            ref_arg = [refs] if self._is_valid_ref(refs) else []

        self._refs = ref_arg
        self()

    @classmethod
    def _is_valid_ref(cls, ref):
        return is_ref(ref) or isinstance(ref, Callable)

    @staticmethod
    def on(refs: _T_effect_refreshable_refs):
        def warp(
            fn: Callable,
        ):
            if inspect.iscoroutinefunction(fn):
                return async_effect_refreshable(refs)(fn)

            return effect_refreshable(fn, refs)

        return warp

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        re_func = ui.refreshable(self._fn)

        first = True

        def runner():
            nonlocal first
            if first:
                re_func()
                first = False
                return

            re_func.refresh()

        if len(self._refs) == 0:
            runner = effect(runner)
        else:
            runner = on(self._refs)(runner)  # type: ignore

        return runner


def async_effect_refreshable(source: _T_effect_refreshable_refs):
    def wrapper(fn: Callable[[], Any]):
        @on(source, onchanges=False)
        async def on_source_changed():
            with temp_box:
                await fn()

            container.clear()

            for child in list(temp_box):
                child.move(container)

            temp_box.clear()

        # 临时容器做中转，避免异步等待时，页面内容空白的问题
        temp_box = RefreshableContainer()
        container = RefreshableContainer()

    return wrapper


def on(
    refs: Union[TGetterOrReadonlyRef, RefWrapper, Sequence[TGetterOrReadonlyRef], Any],
    onchanges=False,
    priority_level=1,
    effect_kws: Optional[Dict[str, Any]] = None,
    deep: bool = True,
    scope: Optional[Scope] = None,
):
    """Watches one or more reactive data sources and invokes a callback function when the sources change.

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#on
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#on


    Args:
        refs (Union[ReadonlyRef, Sequence[ReadonlyRef]]): _description_
        onchanges (bool, optional): _description_. Defaults to False.
        priority_level (int, optional): _description_. Defaults to 1.
        effect_kws (Optional[Dict[str, Any]], optional): _description_. Defaults to None.

    """
    effect_kws = effect_kws or {}
    if not isinstance(refs, Sequence):
        refs = [refs]  # type: ignore

    refs = (to_ref_if_base_type_proxy(ref) for ref in refs)
    refs = [(lambda: ref.value) if isinstance(ref, RefWrapper) else ref for ref in refs]  # type: ignore

    effect_kws.update({"priority_level": priority_level})

    def wrap(fn: Callable):
        return signe.on(
            refs,
            fn,
            onchanges=onchanges,
            effect_kws=effect_kws,
            scope=scope or _CLIENT_SCOPE_MANAGER.get_current_scope(),
            deep=deep,
            scheduler=get_uiScheduler(),
        )

    return wrap


def batch(fn: Callable[..., None]):
    return signe.batch(fn, get_uiScheduler())


def event_batch(event_fn: Callable[..., None]):
    """This decorator makes multiple data signals can be changed in a single tick.

    Args:
        event_fn (Callable[..., None]): event callback

    ## Example

    .. code-block:: python
        from nicegui import ui
        from ex4nicegui import on, to_ref, effect, ref_computed, batch

        a = to_ref(0)
        b = to_ref(0)
        text = ref_computed(lambda: f"a={a.value};b={b.value}")

        @on([a, b, text])
        def when_vars_changed():
            ui.notify(f"a:{a.value};b:{b.value};text={text.value}")

        @event_batch
        def when_click():
            a.value += 1
            b.value += 1

        ui.button("change all values", on_click=when_click)

    """

    def wrap(*args, **kwargs):
        def real_event_fn():
            event_fn(*args, **kwargs)

        signe.batch(real_event_fn, scheduler=get_uiScheduler())

    return wrap
