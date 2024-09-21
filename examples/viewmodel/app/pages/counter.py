from ex4nicegui import rxui
from nicegui import ui


class Counter(rxui.ViewModel):
    number = 0

    def increment(self):
        self.number += 1

    def decrement(self):
        self.number -= 1

    def text_color(self):
        return "red" if self.number < 0 else "green"


def index():
    number_props = "outlined dense"
    button_props = "round dense outline"

    counter = Counter()

    rxui.label(lambda: f"Counter: {counter.number}").bind_style(
        {"color": counter.text_color}
    )

    with ui.row(align_items="center"):
        ui.button(icon="remove", on_click=counter.decrement).props(button_props)
        rxui.number(value=counter.number).classes("w-[8ch]").props(number_props)
        ui.button(icon="add", on_click=counter.increment).props(button_props)
