from typing import Any, List, Protocol
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, ref_computed
from ex4nicegui.utils.signals import deep_ref
from .screen import ScreenPage
from .utils import ButtonUtils, InputUtils, LabelUtils, set_test_id
from playwright.sync_api import expect
import pytest
from dataclasses import dataclass


@dataclass
class TodoItem:
    title: str
    done: bool


class TodoProto(Protocol):
    def get(self, obj, attr: str) -> Any:
        ...

    def new(self, title: str, done: bool) -> Any:
        ...

    def set(self, obj: Any, attr: str, value: Any):
        ...


class DictTodo(TodoProto):
    def get(self, obj, attr: str) -> Any:
        return obj[attr]

    def set(self, obj: Any, attr: str, value: Any):
        obj[attr] = value

    def new(self, title: str, done: bool) -> Any:
        return {"title": title, "done": done}


class DataclassTodo(TodoProto):
    def get(self, obj, attr: str) -> Any:
        return getattr(obj, attr)

    def set(self, obj: Any, attr: str, value: Any):
        setattr(obj, attr, value)

    def new(self, title: str, done: bool) -> Any:
        return TodoItem(title, done)


class TestTodosExample:
    @pytest.mark.parametrize("todo_proto", [DictTodo(), DataclassTodo()])
    def test_todos_example(
        self, page: ScreenPage, page_path: str, todo_proto: TodoProto
    ):
        @ui.page(page_path)
        def _():
            ui.row.default_classes("flex-center")

            todos = deep_ref([])
            input = to_ref("")

            @ref_computed
            def total_done():
                return sum(todo_proto.get(todo, "done") for todo in todos.value)

            @ref_computed
            def totals():
                return len(todos.value)

            def new_todo(text: str):
                todos.value.append(todo_proto.new(**{"title": text, "done": False}))

                input.value = ""

            def del_todo(todo):
                todos.value.remove(todo)

            def change_done(todo, done: bool):
                todo_proto.set(todo, "done", done)

            def all_done():
                for todo in todos.value:
                    todo_proto.set(todo, "done", True)

            def swap(a: int, b: int):
                todos.value[a], todos.value[b] = todos.value[b], todos.value[a]

            with ui.row():
                set_test_id(rxui.input(value=input), "input")
                set_test_id(
                    rxui.button("add", on_click=lambda: new_todo(input.value)),
                    "btn add",
                )
                set_test_id(
                    rxui.button("all done", on_click=lambda: all_done()), "btn all done"
                )
                set_test_id(
                    rxui.button("swap", on_click=lambda: swap(0, -1)), "btn swap"
                )

                with ui.row():
                    ui.label("done count:")
                    set_test_id(rxui.label(total_done), "label done")

                with ui.row():
                    ui.label("totals count:")
                    set_test_id(rxui.label(totals), "label totals")

            with ui.column().classes("card_zone"):

                @rxui.vfor(todos, key="title")
                def _(store: rxui.VforStore):
                    with ui.card().classes("w-full row-card"), ui.row():
                        rxui.label(store.get("title")).classes("row-title")
                        rxui.checkbox(
                            "done",
                            value=store.get("done"),
                            on_change=lambda e: change_done(store.get(), e.value),
                        )
                        rxui.button(
                            "del", on_click=lambda: del_todo(store.get())
                        ).bind_enabled(store.get("done"))

        page.open(page_path)

        btn_add = ButtonUtils(page, "btn add")
        btn_all_done = ButtonUtils(page, "btn all done")
        btn_swap = ButtonUtils(page, "btn swap")
        input = InputUtils(page, "input")

        label_done = LabelUtils(page, "label done")
        label_totals = LabelUtils(page, "label totals")

        locator_row_cards = page._page.locator(".row-card")
        locator_row_titles = locator_row_cards.locator(".row-title")
        locator_row_checkboxs = locator_row_cards.get_by_role("checkbox")
        locator_row_btns = locator_row_cards.get_by_role("button")

        def expect_titles(titles: List[str]):
            for title, element in zip(titles, locator_row_titles.all()):
                expect(element).to_have_text(title)

        def expect_checkboxs(values: List[bool]):
            for value, element in zip(values, locator_row_checkboxs.all()):
                expect(element).to_be_checked(checked=value)

        def get_checkbox(index: int):
            return locator_row_checkboxs.all()[index]

        def get_del_btn(index: int):
            return locator_row_btns.all()[index]

        # first input
        input.fill_text("test1")
        btn_add.click()

        expect(locator_row_cards).to_have_count(1)
        expect_titles(["test1"])
        expect_checkboxs([False])

        label_done.expect_to_have_text("0")
        label_totals.expect_to_have_text("1")

        # click check box
        get_checkbox(0).click()
        label_done.expect_to_have_text("1")

        # more todos
        input.fill_text("test2")
        btn_add.click()

        input.fill_text("test3")
        btn_add.click()

        label_done.expect_to_have_text("1")
        label_totals.expect_to_have_text("3")

        #
        get_checkbox(2).click()
        get_del_btn(0).click()

        label_done.expect_to_have_text("1")
        label_totals.expect_to_have_text("2")

        # swap
        btn_swap.click()

        expect_titles(["test3", "test2"])
        expect_checkboxs([True, False])

        #
        btn_all_done.click()
        label_done.expect_to_have_text("2")
        label_totals.expect_to_have_text("2")

        # del all
        get_del_btn(0).click()
        get_del_btn(0).click()
        label_done.expect_to_have_text("0")
        label_totals.expect_to_have_text("0")


class TestBase:
    def test_two_way_binding(self, page: ScreenPage, page_path: str):
        @ui.page(page_path)
        def _():
            # refs
            items = deep_ref(
                [
                    {"id": 1, "message": "foo", "done": False},
                    {"id": 2, "message": "bar", "done": True},
                ]
            )

            # ref_computeds
            @ref_computed
            def total_count():
                return sum(item["done"] for item in items.value)

            # ui
            set_test_id(rxui.label(total_count), "label totals")

            @rxui.vfor(items, key="id")
            def _(store: rxui.VforStore):
                with ui.card().classes("row-card"):
                    rxui.checkbox(text=store.get("message"), value=store.get("done"))

        page.open(page_path)

        label_totals = LabelUtils(page, "label totals")

        locator_row_cards = page._page.locator(".row-card")
        locator_row_checkboxs = locator_row_cards.get_by_role("checkbox")

        def get_checkbox(index: int):
            return locator_row_checkboxs.all()[index]

        label_totals.expect_contain_text("1")

        get_checkbox(0).click()

        label_totals.expect_contain_text("2")
