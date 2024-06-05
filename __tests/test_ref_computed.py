import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, ref_computed
from ex4nicegui import effect
from ex4nicegui.utils.signals import deep_ref
from .screen import BrowserManager


def test_method_decorator(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        class MyState:
            def __init__(self) -> None:
                self.r_text = to_ref("")

            @ref_computed
            def post_text(self):
                return self.r_text.value + " post"

        state = MyState()

        rxui.input(value=state.r_text).classes("input")
        rxui.label(state.post_text).classes("label")

    page = browser.open(page_path)

    input = page.Input(".input")
    label = page.Label(".label")

    label.expect_to_have_text("post")
    input.fill_text("new text")
    label.expect_to_have_text("new text post")


@pytest.mark.noautofixt
def test_should_not_destroyed():
    dummy = []

    class State:
        def __init__(self) -> None:
            self.todos = deep_ref([])

        @ref_computed
        def total_count(self):
            return len(self.todos.value)

        def add_data(self):
            self.todos.value.append(1)

    s = State()

    @effect
    def _():
        # computed is created in this effect,
        # causing it to be destroyed before each execution of this function.
        # The correct approach is that it should not be destroyed
        dummy.append(s.total_count.value)

    assert dummy == [0]

    s.add_data()
    s.add_data()
    assert dummy == [0, 1, 2]


def test_should_work_with_private_page(browser: BrowserManager, page_path: str):
    class MyState:
        def __init__(self):
            self.count = to_ref(0)

        @ref_computed
        def color(self):
            return "green" if self.count.value % 2 == 0 else "red"

    state = MyState()

    @ui.page(page_path)
    def _():
        rxui.label(state.color)
        ui.button("reload", on_click=ui.navigate.reload).classes("button")

    page = browser.open(page_path)

    button = page.Button(".button")

    button.click(click_count=6, delay=500)
