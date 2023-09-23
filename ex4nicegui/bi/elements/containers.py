from nicegui import ui
from ex4nicegui.layout import grid_box


def ui_cols(num: int, min_width="0"):
    with grid_box(template_columns=f"repeat({num},1fr)").classes(
        "justify-between"
    ) as gb:
        divs = [ui.column() for _ in range(num)]

    gb.grid_box(template_columns="1fr", break_point="<sm[0-599.99px]")

    return divs
