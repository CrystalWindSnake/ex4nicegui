from ex4nicegui import rxui
from nicegui import ui


class State(rxui.ViewModel):
    a = 0
    sign = "+"
    b = 0
    error = ""

    _sign_options = ["+", "-", "*", "/"]

    @rxui.cached_var
    def result(self):
        self.error = ""
        try:
            return eval(f"{self.a}{self.sign}{self.b}")
        except Exception as e:
            self.error = str(e)

        return "N/A"

    def result_style(self):
        if self.error:
            return "text-red-500"

        result: float = self.result()  # type: ignore

        if result > 0:
            return "text-green-500"
        elif result < 0:
            return "text-red-500"
        else:
            return "text-gray-500"


ui.number.default_props("outlined dense")
ui.select.default_props("outlined dense")


def index():
    state = State()

    with ui.row(align_items="center"):
        rxui.number(value=state.a, label="a").element.mark("a")
        rxui.select(state._sign_options, value=state.sign, label="sign")
        rxui.number(value=state.b, label="b").element.mark("b")
        ui.label("=")
        rxui.label(text=state.result).classes("text-xl font-bold").bind_classes(
            state.result_style
        ).element.mark("result")

    rxui.label(state.error).classes("text-red-500")
