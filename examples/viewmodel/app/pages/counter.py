from ex4nicegui import rxui
from nicegui import ui


class State(rxui.ViewModel):
    number = 0

    def increment(self):
        self.number += 1

    def decrement(self):
        self.number -= 1


def index():
    number_props = "outlined dense"
    button_props = "round dense outline"

    state = State()

    rxui.label(lambda: f"Counter: {state.number}")

    with ui.row(align_items="center"):
        ui.button(icon="remove", on_click=state.decrement).props(button_props)
        rxui.number(value=state.number).classes("w-[8ch]").props(number_props)
        ui.button(icon="add", on_click=state.increment).props(button_props)
