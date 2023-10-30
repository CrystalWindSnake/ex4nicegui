from typing import Callable, Any, Union
from nicegui import ui
from ex4nicegui.utils.signals import effect


_T_Maybe_Callable = Any


def _ui_label(text_or_build: _T_Maybe_Callable):
    label = ui.label()

    if isinstance(text_or_build, Callable):

        @effect
        def _():
            label.text = text_or_build()

    else:
        label.text = str(text_or_build)

    return label


def ui_title(text_or_build: _T_Maybe_Callable):
    return _ui_label(text_or_build).style("font-size: calc(1.4rem + 1.8vw)")


def ui_header(text_or_build: _T_Maybe_Callable):
    return _ui_label(text_or_build).style("font-size: calc(1.35rem + 1.2vw)")


def ui_subheader(text_or_build: _T_Maybe_Callable):
    return _ui_label(text_or_build).style("font-size: calc(1.3rem + .6vw)")
