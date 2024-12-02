from typing import List, Optional
import typing
from .types import _T_event_name, _T_mouse_event_name
from .events import EChartsMouseEventArguments, _Mouse_Event_Arguments_Fields
from nicegui.events import UiEventArguments, GenericEventArguments
from functools import lru_cache


@lru_cache(maxsize=1)
def _get_mouse_event_names():
    return set(typing.get_args(_T_mouse_event_name))


def is_mouse_event(event_name: _T_event_name) -> bool:
    return event_name in _get_mouse_event_names()


def get_bound_event_args(event_name: _T_event_name) -> Optional[List[str]]:
    if is_mouse_event(event_name):
        return _Mouse_Event_Arguments_Fields

    return None


def create_event_handler_args(
    event_name: _T_event_name, e: GenericEventArguments
) -> UiEventArguments:
    if is_mouse_event(event_name):
        print(e.args)
        return EChartsMouseEventArguments(sender=e.sender, client=e.client, **e.args)

    return GenericEventArguments(sender=e.sender, client=e.client, args=e.args)
