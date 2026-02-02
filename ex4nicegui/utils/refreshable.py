import inspect
from typing import (
    Any,
    Awaitable,
    Callable,
    Union,
    Sequence,
)
from nicegui.functions.refreshable import RefreshableContainer
from ex4nicegui.utils.effect import effect
from ex4nicegui.utils.types import (
    _TMaybeRef,
    TGetterOrReadonlyRef,  # noqa: F401
)
from ex4nicegui.utils.refWrapper import RefWrapper  # noqa: F401
from ex4nicegui.utils.proxy import (
    to_ref_if_base_type_proxy,
)
from ex4nicegui.utils.signals import is_ref, on

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
        buffered_view = AsyncBufferedView()

        first = True

        def runner():
            nonlocal first
            if first:
                buffered_view.render(self._fn)
                first = False
                return

            buffered_view.render(self._fn)

        if len(self._refs) == 0:
            runner = effect(runner)
        else:
            runner = on(self._refs)(runner)  # type: ignore

        return runner


def async_effect_refreshable(source: _T_effect_refreshable_refs):
    def wrapper(fn: Callable[[], Any]):
        buffered_view = AsyncBufferedView()

        @on(source, onchanges=False)
        async def on_source_changed():
            await buffered_view.async_render(fn)

    return wrapper


class AsyncBufferedView:
    """
    临时容器做中转，避免异步等待时，页面内容空白的问题
    """

    def __init__(self):
        self.viewport = RefreshableContainer()
        self.staging = RefreshableContainer()

    async def async_render(self, content_creator: Callable[[], Awaitable[Any]]):
        with self.staging:
            await content_creator()

        self.viewport.clear()

        for child in list(self.staging):
            child.move(self.viewport)

        self.staging.clear()

    def render(self, content_creator: Callable[[], Any]):
        with self.staging:
            content_creator()

        self.viewport.clear()

        for child in list(self.staging):
            child.move(self.viewport)

        self.staging.clear()
