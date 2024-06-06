from __future__ import annotations

from typing import Literal

from nicegui.elements.mixins.color_elements import (
    QUASAR_COLORS,
    TAILWIND_COLORS,
)


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
