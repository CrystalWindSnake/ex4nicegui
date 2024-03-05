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
    debug_trigger: Optional[Callable] = None,
    debug_name: Optional[str] = None,
):
    return signe.async_computed(
        refs,
        init=init,
        evaluating=evaluating,
        debug_name=debug_name,
        debug_trigger=debug_trigger,
        scope=_CLIENT_SCOPE_MANAGER.get_current_scope(),
        scheduler=get_uiScheduler(),
    )
