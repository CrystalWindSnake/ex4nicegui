from nicegui import ui
from ex4nicegui import rxui


class AppState(rxui.ViewModel):
    nums = [1, 2, 3, 4, 5]

    def append(self, num: int):
        self.nums.append(num)

    def pop(self):
        self.nums.pop()

    def reverse(self):
        self.nums.reverse()

    def display_nums(self):
        return ", ".join(map(str, self.nums))

    def get_new_num(self):
        return max(self.nums) + 1


def index():
    app_state = AppState()

    with ui.card(), ui.row(align_items="center"):
        ui.button(
            text="Append", on_click=lambda: app_state.append(app_state.get_new_num())
        )
        ui.button(text="Pop", on_click=app_state.pop)
        ui.button(text="Reverse", on_click=app_state.reverse)
    rxui.label(app_state.display_nums)

    @rxui.vfor(app_state.nums, key=rxui.vfor.value_key)
    def _(s: rxui.VforStore[int]):
        rxui.label(s.get())
