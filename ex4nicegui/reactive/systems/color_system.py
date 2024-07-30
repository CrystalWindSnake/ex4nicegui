from __future__ import annotations

from typing import Literal

from nicegui import ui
from nicegui.elements.mixins.color_elements import (
    QUASAR_COLORS,
    TAILWIND_COLORS,
)

from functools import lru_cache


_color_system_type = Literal["QUASAR", "TAILWIND", "STYLE"]


def get_text_color_info(name: str):
    system_type: _color_system_type = "STYLE"

    if name in QUASAR_COLORS:
        system_type = "QUASAR"
    elif name in TAILWIND_COLORS:
        system_type = "TAILWIND"
        name = f"text-{name}"
    else:
        pass

    return system_type, name


def get_bg_color_info(color: str):
    system_type: _color_system_type = "STYLE"

    if color in QUASAR_COLORS:
        system_type = "QUASAR"
    elif color in TAILWIND_COLORS:
        system_type = "TAILWIND"
        color = f"bg-{color}"
    else:
        pass

    return system_type, color


def _remove_text_color_from_quasar(element: ui.element, color: str):
    color_prop = getattr(element, "TEXT_COLOR_PROP", None)
    if color_prop:
        element._props.pop(color_prop, None)


def _remove_text_color_from_tailwind(element: ui.element, color: str):
    color = f"text-{color}"
    element._classes.remove(color)


def _remove_text_color(element: ui.element, color: str):
    element._style.pop("color", None)


def _add_text_color_from_quasar(element: ui.element, color: str):
    color_prop = getattr(element, "TEXT_COLOR_PROP", None)
    if color_prop:
        element._props[color_prop] = color


def _add_text_color_from_tailwind(element: ui.element, color: str):
    color = f"text-{color}"
    element.classes(color)


def _add_text_color(element: ui.element, color: str):
    element._style["color"] = f"{color} !important"


@lru_cache(maxsize=10)
def _query_text_color(color: str, add_handler=True):
    if color in QUASAR_COLORS:
        return (
            _add_text_color_from_quasar
            if add_handler
            else _remove_text_color_from_quasar
        )
    elif color in TAILWIND_COLORS:
        return (
            _add_text_color_from_tailwind
            if add_handler
            else _remove_text_color_from_tailwind
        )
    elif color is not None:
        return _add_text_color if add_handler else _remove_text_color


def remove_text_color(element: ui.element, color: str):
    handler = _query_text_color(color, add_handler=False)
    if handler:
        handler(element, color)


def add_text_color(element: ui.element, color: str):
    handler = _query_text_color(color)
    if handler:
        handler(element, color)


# background color handlers


def _remove_bg_from_quasar(element: ui.element, color: str):
    color_prop = getattr(element, "BACKGROUND_COLOR_PROP", None)
    if color_prop:
        element._props.pop(color_prop, None)


def _remove_bg_from_tailwind(element: ui.element, color: str):
    color = f"bg-{color}"
    element._classes.remove(color)


def _remove_background_color(element: ui.element, color: str):
    element._style.pop("background-color", None)


def _add_bg_from_quasar(element: ui.element, color: str):
    color_prop = getattr(element, "BACKGROUND_COLOR_PROP", None)
    if color_prop:
        element._props[color_prop] = color


def _add_bg_from_tailwind(element: ui.element, color: str):
    color = f"bg-{color}"
    element.classes(color)


def _add_background_color(element: ui.element, color: str):
    element._style["background-color"] = f"{color} !important"


@lru_cache(maxsize=10)
def _query_background_color(color: str, add_handler=True):
    if color in QUASAR_COLORS:
        return _add_bg_from_quasar if add_handler else _remove_bg_from_quasar
    elif color in TAILWIND_COLORS:
        return _add_bg_from_tailwind if add_handler else _remove_bg_from_tailwind
    elif color is not None:
        return _add_background_color if add_handler else _remove_background_color


def remove_background_color(element: ui.element, color: str):
    handler = _query_background_color(color, add_handler=False)
    if handler:
        handler(element, color)


def add_background_color(element: ui.element, color: str):
    handler = _query_background_color(color)
    if handler:
        handler(element, color)
