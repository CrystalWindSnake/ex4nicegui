from __future__ import annotations
from nicegui.element import Element
from typing import (
    Any,
    Dict,
    List,
)


class TransitionGroup(Element, component="transitionGroup.js"):
    def __init__(self) -> None:
        super().__init__()

    def apply_transition_group(self, args: Dict[str, Any]):
        self._props["transitionGroupArgs"] = args
        self.update()

    def update_child_order_keys(self, keys: List[Any]):
        print(f"keys:{keys=}")
        self._props["childOrderKey"] = keys
        self.update()


def transition_group(fn):
    pass
