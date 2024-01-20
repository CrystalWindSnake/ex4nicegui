from functools import partial
import types
from weakref import WeakKeyDictionary
from signe import batch as signe_batch, effect as signe_effect, computed, on as signe_on
from signe.core.signal import Signal, SignalOption
from signe.core.effect import Effect
from signe import utils as signe_utils
from .clientScope import NgClientScopeManager
from signe.types import TSetter, TGetter
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
from nicegui import ui

T = TypeVar("T")

_CLIENT_SCOPE_MANAGER = NgClientScopeManager()


class ReadonlyRef(Generic[T]):
    def __init__(self, getter: TGetter[T]) -> None:
        self.___getter = getter

    @property
    def value(self):
        return self.___getter()

    # def __repr__(self) -> str:
    #     return str(self.value)


class Ref(ReadonlyRef[T]):
    def __init__(
        self, getter: TGetter[T], setter: TSetter[T], signal: Optional[Signal] = None
    ) -> None:
        super().__init__(getter)
        self.___setter = setter
        self.___signal = signal

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, value: T):
        self.___setter(value)


class DescReadonlyRef(ReadonlyRef[T]):
    def __init__(self, getter: Callable[[], T], desc="") -> None:
        super().__init__(getter)
        self.__desc = desc

    @property
    def desc(self):
        return self.__desc


@overload
def ref_from_signal(getter: TGetter[T]) -> ReadonlyRef[T]:
    ...


@overload
def ref_from_signal(getter: TGetter[T], setter: TSetter[T]) -> Ref[T]:
    ...


def ref_from_signal(getter: TGetter[T], setter: Optional[TSetter[T]] = None):
    if setter is None:
        return cast(ReadonlyRef[T], ReadonlyRef(getter))

    return cast(Ref[T], Ref(getter, setter))


_TMaybeRef = Union[T, Union[Ref[T], ReadonlyRef[T]]]


def is_ref(maybe_ref: _TMaybeRef):
    return isinstance(maybe_ref, ReadonlyRef)


def to_value(maybe_ref: _TMaybeRef[T]) -> T:
    if is_ref(maybe_ref):
        return cast(ReadonlyRef, maybe_ref).value

    return cast(T, maybe_ref)


def to_ref(maybe_ref: _TMaybeRef[T]):
    """Takes an inner value and returns a reactive and mutable ref object, which has a single property .value that points to the inner value.

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#to_ref
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#to_ref


    Args:
        maybe_ref (_TMaybeRef[T]): _description_


    """
    if is_ref(maybe_ref):
        return cast(Ref[T], maybe_ref)

    return cast(Ref[T], ref(maybe_ref))


def ref(value: T):
    comp = (
        False
        if not isinstance(
            value,
            (
                str,
                int,
                float,
            ),
        )
        else None
    )
    # getter, setter = createSignal(value, comp)

    s = Signal(signe_utils.exec, value, SignalOption(comp))

    return cast(Ref[T], Ref(s.getValue, s.setValue, s))


@overload
def effect(
    fn: None = ...,
    *,
    priority_level=1,
    debug_trigger: Optional[Callable] = None,
    debug_name: Optional[str] = None,
) -> signe_utils._TEffect_Fn[None]:
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
) -> Effect[None]:
    ...


def effect(
    fn: Optional[Callable[..., None]] = None,
    *,
    priority_level=1,
    debug_trigger: Optional[Callable] = None,
    debug_name: Optional[str] = None,
) -> Union[signe_utils._TEffect_Fn[None], Effect[None]]:
    kws = {
        "debug_trigger": debug_trigger,
        "priority_level": priority_level,
        "debug_name": debug_name,
    }
    return signe_effect(fn, **kws, scope=_CLIENT_SCOPE_MANAGER.get_scope())


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
        is_class_define_method = (
            hasattr(fn, "__qualname__")
            and "." in fn.__qualname__
            and (isinstance(fn, types.FunctionType))
        )

        if is_class_define_method:
            return cast(ref_computed_method[T], ref_computed_method(fn))  # type: ignore

        getter = computed(fn, **kws, scope=_CLIENT_SCOPE_MANAGER.get_scope())
        return cast(DescReadonlyRef[T], DescReadonlyRef(getter, desc))

    else:

        def wrap(fn: Callable[[], T]):
            return ref_computed(fn, **kws)

        return wrap


class ref_computed_method(Generic[T]):
    __isabstractmethod__: bool

    def __init__(
        self,
        fget: Callable[[Any], T],
    ) -> None:
        self._fget = fget
        self.__instance_map: WeakKeyDictionary[
            object, ReadonlyRef
        ] = WeakKeyDictionary()

    def __get_computed(self, instance):
        if instance not in self.__instance_map:
            cp = ref_computed(partial(self._fget, instance))
            self.__instance_map[instance] = cp

        return self.__instance_map[instance]

    def __get__(self, __instance: Any, __owner: type | None = None):
        return cast(ReadonlyRef[T], self.__get_computed(__instance))


class effect_refreshable:
    def __init__(
        self, fn: Callable, refs: Union[ReadonlyRef, Sequence[ReadonlyRef]] = []
    ) -> None:
        self._fn = fn
        self._refs = refs if isinstance(refs, Sequence) else [refs]
        self()

    @staticmethod
    def on(refs: Union[ReadonlyRef, Sequence[ReadonlyRef]]):
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
            runner = signe_effect(runner)
        else:
            runner = on(self._refs)(runner)

        return runner


def on(
    refs: Union[ReadonlyRef, Sequence[ReadonlyRef]],
    onchanges=False,
    priority_level=1,
    effect_kws: Optional[Dict[str, Any]] = None,
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
        refs = [refs]

    getters = [getattr(r, "_ReadonlyRef___getter") for r in refs]

    effect_kws.update(
        {"scope": _CLIENT_SCOPE_MANAGER.get_scope(), "priority_level": priority_level}
    )

    def wrap(fn: Callable):
        return signe_on(getters, fn, onchanges=onchanges, effect_kws=effect_kws)

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
        @signe_batch
        def _():
            event_fn(*args, **kwargs)

    return wrap
