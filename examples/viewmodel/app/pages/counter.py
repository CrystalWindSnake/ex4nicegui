from ex4nicegui import rxui
from nicegui import ui


class State(rxui.ViewModel):
    number = 0

    def increment(self):
        self.number += 1

    def decrement(self):
        self.number -= 1


ui.number.default_props("outlined dense")
ui.button.default_props("round dense outline")


def index():
    state = State()

    rxui.label(lambda: f"Counter: {state.number}")

    with ui.row(align_items="center"):
        ui.button(icon="remove", on_click=state.decrement)
        rxui.number(value=state.number).classes("w-[8ch]")
        ui.button(icon="add", on_click=state.increment)
