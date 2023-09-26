from nicegui import ui
from ex4nicegui.reactive import rxui
from ex4nicegui import to_ref


def ui_left_drawer():
    drawer_show = to_ref(True)

    with rxui.drawer("left", value=drawer_show) as drawer:
        with ui.page_sticky("top-right", x_offset=10, y_offset=10):
            icon_close = (
                rxui.icon(name="close")
                .classes("cursor-pointer")
                .props("round ")
                .bind_visible(drawer_show)
            )
            icon_close.on("click", drawer.toggle)

    with ui.page_sticky("top-left", x_offset=10, y_offset=10):
        icon_close = (
            rxui.icon(name="keyboard_arrow_right", size="1.2rem")
            .classes("cursor-pointer")
            .props("round ")
            .bind_not_visible(drawer_show)
        )
        icon_close.on("click", drawer.toggle)

    return drawer.element
