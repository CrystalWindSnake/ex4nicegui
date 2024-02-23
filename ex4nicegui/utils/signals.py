from datetime import date, datetime
from functools import partial
import types
from weakref import WeakValueDictionary
import signe
from .clientScope import NgClientScopeManager
from typing import (
    Any,
    Dict,
    Protocol,
    TypeVar,
    Generic,
    overload,
    Optional,
    Callable,
    cast,
    Union,
    Sequence,
)
from .scheduler import reset_execution_scheduler
from nicegui import ui

T = TypeVar("T")


_CLIENT_SCOPE_MANAGER = NgClientScopeManager()


TReadonlyRef = signe.TGetterSignal[T]
ReadonlyRef = TReadonlyRef[T]
DescReadonlyRef = TReadonlyRef[T]

TGetterOrReadonlyRef = signe.TGetter[T]


reactive = signe.reactive


class RefWrapper(Generic[T]):
    __slot__ = ("_getter_fn", "_setter_fn")

    def __init__(
        self,
        getter_or_ref: TGetterOrReadonlyRef[T],
        setter_or_ref: Optional[Callable[[T], None]] = None,
    ):
        if signe.is_signal(getter_or_ref):
            self._getter_fn = lambda: getter_or_ref.value

            def ref_setter(v):
                getter_or_ref.value = v  # type: ignore

            self._setter_fn = ref_setter
        elif isinstance(getter_or_ref, Callable):
            self._getter_fn = getter_or_ref
            self._setter_fn = setter_or_ref or (lambda x: None)
        else:
            self._getter_fn = lambda: getter_or_ref
            self._setter_fn = lambda x: None

    @property
    def value(self) -> T:
        return cast(T, self._getter_fn())

    @value.setter
    def value(self, new_value: T):
        return self._setter_fn(new_value)


def to_ref_wrapper(
    getter_or_ref: TGetterOrReadonlyRef[T],
    setter_or_ref: Optional[Callable[[T], None]] = None,
):
    return RefWrapper(getter_or_ref, setter_or_ref)


_TMaybeRef = signe.TMaybeSignal[T]
TRef = signe.TSignal[T]
Ref = TRef[T]


to_raw = signe.to_raw


def is_ref(obj):
    return signe.is_signal(obj) or isinstance(obj, RefWrapper)


def to_value(obj: TGetterOrReadonlyRef[T]) -> T:
    if is_ref(obj):
        return obj.value
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


def ref(value: T, is_deep=False):
    comp = False  # Default never equal

    if _is_comp_values(value):
        comp = None  # comparison of `==`

    if value is None:
        comp = _ref_comp_with_None

    s = signe.signal(value, comp, is_shallow=not is_deep)

    return cast(Ref[T], s)


def deep_ref(value: T) -> Ref[T]:
    """Deep response version of `to_ref`.

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#deep_ref
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#deep_ref

    >>> deep_ref(1)
    >>> deep_ref([1,2,3])

    """
    return to_ref(value, is_deep=True)


_TEffect_Fn = Callable[[Callable[..., T]], signe.Effect]


@overload
def effect(
    fn: None = ...,
    *,
    priority_level=1,
    debug_trigger: Optional[Callable] = None,
    debug_name: Optional[str] = None,
) -> _TEffect_Fn:
    """Runs a function immediately while reactively tracking its dependencies and re-runs it whenever the dependencies are changed.

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#effect
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#effect


    Args:
        fn (None, optional): _description_. Defaults to ....
        priority_level (int, optional): _description_. Defaults to 1.
        debug_trigger (Optional[Callable], optional): _description_. Defaults to None.
        debug_name (Optional[str], optional): _description_. Defaults to None.

    """
    ...


@overload
def effect(
    fn: Callable[..., None],
    *,
    priority_level=1,
    debug_trigger: Optional[Callable] = None,
    debug_name: Optional[str] = None,
) -> signe.Effect[None]:
    ...


def effect(
    fn: Optional[Callable[..., None]] = None,
    *,
    priority_level=1,
    debug_trigger: Optional[Callable] = None,
    debug_name: Optional[str] = None,
) -> Union[signe.Effect[None], _TEffect_Fn]:
    kws = {
        "debug_trigger": debug_trigger,
        "priority_level": priority_level,
        "debug_name": debug_name,
    }
    if fn:
        return signe.effect(fn, **kws, scope=_CLIENT_SCOPE_MANAGER.get_scope())
    else:

        def wrap(fn: Callable[..., None]):
            return effect(fn, **kws)

        return wrap


class TInstanceCall(Protocol[T]):
    def __call__(_, self) -> T:
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
        if _is_class_define_method(fn):
            return cast(
                ref_computed_method[T],
                ref_computed_method(fn, computed_args=kws),  # type: ignore
            )  # type: ignore

        getter = signe.computed(fn, **kws, scope=_CLIENT_SCOPE_MANAGER.get_scope())  # type: ignore
        return cast(DescReadonlyRef[T], getter)

    else:

        def wrap(fn: Callable[[], T]):
            return ref_computed(fn, **kws)

        return wrap


def _is_class_define_method(fn: Callable):
    has_name = hasattr(fn, "__name__")
    qualname_prefix = f".<locals>.{fn.__name__}" if has_name else ""

    return (
        hasattr(fn, "__qualname__")
        and has_name
        and "." in fn.__qualname__
        and qualname_prefix != fn.__qualname__[-len(qualname_prefix) :]
        and (isinstance(fn, types.FunctionType))
    )


class ref_computed_method(Generic[T]):
    __isabstractmethod__: bool

    def __init__(self, fget: Callable[[Any], T], computed_args: Dict) -> None:
        self._fget = fget
        self._computed_args = computed_args
        self._instance_map: WeakValueDictionary[int, TRef[T]] = WeakValueDictionary()

    def __get_computed(self, instance):
        ins_id = id(instance)
        if ins_id not in self._instance_map:
            cp = ref_computed(partial(self._fget, instance), **self._computed_args)
            self._instance_map[ins_id] = cp  # type: ignore

        return self._instance_map[ins_id]

    def __get__(self, __instance: Any, __owner: Optional[type] = None):
        return cast(TRef[T], self.__get_computed(__instance))


class effect_refreshable:
    def __init__(self, fn: Callable, refs: Union[TRef, Sequence[TRef]] = []) -> None:
        self._fn = fn
        self._refs = refs if isinstance(refs, Sequence) else [refs]
        self()

    @staticmethod
    def on(refs: Union[TRef, Sequence[TRef]]):
        def warp(
            fn: Callable,
        ):
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
            runner = on(self._refs)(runner)

        return runner


def on(
    refs: Union[TGetterOrReadonlyRef, Sequence[TGetterOrReadonlyRef]],
    onchanges=False,
    priority_level=1,
    effect_kws: Optional[Dict[str, Any]] = None,
    deep: bool = True,
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
    # if not isinstance(refs, Sequence):
    #     refs = [refs]

    effect_kws.update({"priority_level": priority_level})

    def wrap(fn: Callable):
        return signe.on(
            refs,
            fn,
            onchanges=onchanges,
            effect_kws=effect_kws,
            scope=_CLIENT_SCOPE_MANAGER.get_scope(),
            deep=deep,
        )

    return wrap


def event_batch(event_fn: Callable[..., None]):
    """This decorator makes multiple data signals can be changed in a single tick.

    Args:
        event_fn (Callable[..., None]): event callback

    @Example
    ```python
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
    ```
    """

    def wrap(*args, **kwargs):
        @signe.batch
        def _():
            event_fn(*args, **kwargs)

    return wrap
