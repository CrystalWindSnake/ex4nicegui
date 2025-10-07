from ex4nicegui import rxui, to_ref, PageState
from nicegui import ui
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    class MyState(PageState):
        def __init__(self):
            self.a = to_ref(1.0)

    def sub_view():
        state = MyState.get()
        rxui.label(lambda: f"{state.a.value=}")

    @ui.page(page_path)
    def _():
        state = MyState.get()
        rxui.number(value=state.a).classes("input")

        sub_view()

    page = browser.open(page_path)

    page.should_contain("state.a.value=1.0")
    page.Number("input").fill_text("2")
    page.should_contain("state.a.value=2.0")
