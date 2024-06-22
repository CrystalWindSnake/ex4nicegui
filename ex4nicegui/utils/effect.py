import signe
from signe.core.consts import EffectState
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
        scheduler = get_uiScheduler()

        def scheduler_fn(effect: signe.Effect):
            def job():
                if effect.is_need_update():
                    effect.update()

            scheduler.post_job(job)

        res = signe.Effect(
            fn,
            scheduler_fn=scheduler_fn,
            scheduler=scheduler,
            **kws,
            scope=_CLIENT_SCOPE_MANAGER.get_current_scope(),
        )

        res.trigger(EffectState.NEED_UPDATE)
        scheduler.run()

        return res

    else:

        def wrap(fn: Callable[..., None]):
            return effect(fn, **kws)

        return wrap
