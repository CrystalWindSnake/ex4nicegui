from __future__ import annotations
from typing import (
    Sequence,
    TypeVar,
    Callable,
    Optional,
    Union,
)
import signe
from ex4nicegui.utils.clientScope import _CLIENT_SCOPE_MANAGER
from ex4nicegui.utils.scheduler import get_uiScheduler

from ex4nicegui.utils.signals import TGetterOrReadonlyRef, TRef


_T = TypeVar("_T")


def async_computed(
    refs: Union[TGetterOrReadonlyRef, Sequence[TGetterOrReadonlyRef]],
    *,
    init: Optional[_T] = None,
    evaluating: Optional[TRef[bool]] = None,
    onchanges=True,
    debug_trigger: Optional[Callable] = None,
    debug_name: Optional[str] = None,
):
    """Create an asynchronous computed dependency.

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#async_computed
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#async_computed


    Args:
        refs (Union[TGetterOrReadonlyRef, Sequence[TGetterOrReadonlyRef]]): _description_
        init (Optional[_T], optional): The initial state, used until the first evaluation finishes. Defaults to None.
        evaluating (Optional[TRef[bool]], optional): Ref passed to receive the updated of async evaluation. Defaults to None.
        onchanges (bool, optional): If set to `False`, it will trigger an immediate computation. Defaults to True.

    """
    return signe.async_computed(
        refs,
        init=init,
        evaluating=evaluating,
        onchanges=onchanges,
        debug_name=debug_name,
        debug_trigger=debug_trigger,
        scope=_CLIENT_SCOPE_MANAGER.get_current_scope(),
        scheduler=get_uiScheduler(),
    )
