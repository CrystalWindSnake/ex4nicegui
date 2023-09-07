from typing import Callable, List, Optional, Union, TypeVar, Generic
from typing_extensions import Literal

from ex4nicegui.layout import grid_box, mark_area
from nicegui import ui, app
from .types import *

_T_itemWraper_add_var = TypeVar("_T_itemWraper_add_var")


class ItemWraper:
    def __init__(self, fn: Callable[[ui.element], ui.element]):
        self.fn = fn

    def __radd__(self, other: _T_itemWraper_add_var) -> _T_itemWraper_add_var:
        return self.fn(other)  # type: ignore


class rx_flex_box(ui.element):
    def space(self):
        return ui.element("q-space")

    def gap(self, value: Union[int, float, str]):
        if isinstance(value, (int, float)):
            value = f"{value}rem"
        self._style["gap"] = str(value)
        self.update()
        return self

    def all_items_grow(self):
        self._props["ex4ng-rx-flex-auto-grow"] = ""
        return self


def _q_space():
    return ui.element("q-space")


class rx_column(ui.column, rx_flex_box):
    def __init__(
        self,
        horizontal: TColumn_Horizontal = "left",
        vertical: TColumn_Vertical = "top",
    ) -> None:
        super().__init__()
        self.tailwind.align_items
        self.horizontal(horizontal)
        self.vertical(vertical)

        self._props["ex4ng-rx-column"] = ""

    def item_horizontal(self, value: TColumn_Item_Horizontal):
        def fn(ele: ui.element):
            ele._style["align-self"] = Column_Item_Horizontal_map.get(value, value)
            # ele.update()
            return ele

        return ItemWraper(fn)

    def horizontal(self, value: TColumn_Horizontal):
        self._style["align-items"] = Column_Horizontal_map.get(value, value)
        self.update()
        return self

    def vertical(self, value: TColumn_Vertical):
        self._style["justify-content"] = Column_Vertical_map.get(value, value)
        self.update()
        return self

    def space(self):
        return _q_space()


class rx_row(ui.row, rx_flex_box):
    def __init__(
        self,
        horizontal: TRow_Horizontal = "left",
        vertical: TRow_Vertical = "top",
    ) -> None:
        super().__init__()
        self.horizontal(horizontal)
        self.vertical(vertical)
        self._props["ex4ng-rx-row"] = ""

    def item_vertical(self, value: TRow_Item_Vertical):
        def fn(ele: ui.element):
            ele._style["align-self"] = Row_Vertical_map.get(value, value)
            return ele

        return ItemWraper(fn)

    def horizontal(self, value: TRow_Horizontal):
        self._style["justify-content"] = Row_Horizontal_map.get(value, value)
        self.update()
        return self

    def vertical(self, value: TRow_Vertical):
        self._style["align-items"] = Row_Vertical_map.get(value, value)
        self.update()
        return

    def space(self):
        return _q_space()


class page_view(rx_column):
    def __init__(
        self,
        horizontal: TColumn_Horizontal = "left",
        vertical: TColumn_Vertical = "top",
    ) -> None:
        super().__init__(horizontal, vertical)
        self.classes("w-full h-full no-wrap")
        ui.query("main.q-page").classes("flex")
        ui.query(".nicegui-content").classes("grow p-0")

    def all_center(self):
        return self.horizontal("center").vertical("center")

    def full_screen(self):
        return self.classes("fullscreen")
