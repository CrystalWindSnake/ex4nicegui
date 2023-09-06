# region type

from typing_extensions import Literal


Space_map = {
    "between": "space-between",
    "around": "space-around",
    "evenly": "space-evenly",
}

TColumn_Item_Horizontal = Literal[
    "auto",
    "left",
    "right",
    "center",
    "stretch",
    "baseline",
]
Column_Item_Horizontal_map = {"left": "flex-start", "right": "flex-end"}


TColumn_Horizontal = Literal[
    "left",
    "right",
    "center",
    "baseline",
    "stretch",
]

Column_Horizontal_map = {"left": "flex-start", "right": "flex-end"}

TColumn_Vertical = Literal[
    "normal",
    "top",
    "bottom",
    "center",
    "between",
    "around",
    "evenly",
    "stretch",
]

Column_Vertical_map = {"top": "flex-start", "bottom": "flex-end", **Space_map}


TRow_Horizontal = Literal[
    "normal",
    "left",
    "right",
    "center",
    "between",
    "around",
    "evenly",
    "stretch",
]

Row_Horizontal_map = {"left": "flex-start", "right": "flex-end", **Space_map}

TRow_Vertical = Literal[
    "top",
    "bottom",
    "center",
    "baseline",
    "stretch",
]

Row_Vertical_map = {"top": "flex-start", "bottom": "flex-end"}


TRow_Item_Vertical = Literal[
    "auto",
    "top",
    "bottom",
    "center",
    "stretch",
    "baseline",
]
TRow_Item_Vertical_map = {"top": "flex-start", "bottom": "flex-end"}
# endregion
