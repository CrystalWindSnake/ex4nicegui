import signe
from signe.core.scope import Scope
from typing import (
    TypeVar,
    overload,
    Optional,
    Callable,
    Union,
)

from .scheduler import get_uiScheduler
from .clientScope import _CLIENT_SCOPE_MANAGER


T = TypeVar("T")


_TEffect_Fn = Callable[[Callable[..., T]], signe.Effect]


@overload
def ui_effect(
    fn: None = ...,
    *,
    priority_level=1,
    debug_trigger: Optional[Callable] = None,
    debug_name: Optional[str] = None,
    scope: Optional[Scope] = None,
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
def ui_effect(
    fn: Callable[..., None],
    *,
    priority_level=1,
    debug_trigger: Optional[Callable] = None,
    debug_name: Optional[str] = None,
    scope: Optional[Scope] = None,
) -> signe.Effect[None]:
    ...


def ui_effect(
    fn: Optional[Callable[..., None]] = None,
    *,
    priority_level=1,
    debug_trigger: Optional[Callable] = None,
    debug_name: Optional[str] = None,
    scope: Optional[Scope] = None,
) -> Union[signe.Effect[None], _TEffect_Fn]:
    kws = {
        "debug_trigger": debug_trigger,
        "priority_level": priority_level,
        "debug_name": debug_name,
        "scope": scope,
    }
    if fn:
        scheduler = get_uiScheduler()

        def scheduler_fn(effect: signe.Effect):
            def job():
                if effect.is_need_update():
                    effect.update()

            scheduler.pre_job(job)

        kws.pop("scope")

        res = signe.Effect(
            fn,
            scheduler_fn=scheduler_fn,
            scheduler=scheduler,
            **kws,
            scope=scope or _CLIENT_SCOPE_MANAGER.get_current_scope(),
        )
        res.update()

        return res

    else:

        def wrap(fn: Callable[..., None]):
            return ui_effect(fn, **kws)

        return wrap
