from typing import List, cast
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, ref_computed
from ex4nicegui.utils.signals import deep_ref
from .screen import BrowserManager
from .utils import ButtonUtils, InputUtils, LabelUtils, set_test_id
from playwright.sync_api import expect
from dataclasses import dataclass


class TestExample:
    def test_todos_example(self, browser: BrowserManager, page_path: str):
        @dataclass
        class TodoItem:
            title: str
            done: bool = False

        @ui.page(page_path)
        def _():
            ui.row.default_classes("flex-center")

            todos = deep_ref(cast(List[TodoItem], []))
            input = to_ref("")

            @ref_computed
            def total_done():
                return sum(todo.done for todo in todos.value)

            @ref_computed
            def totals():
                return len(todos.value)

            def new_todo(text: str):
                todos.value.append(TodoItem(text))

                input.value = ""

            def del_todo(todo):
                todos.value.remove(todo)

            def change_done(todo: TodoItem, done: bool):
                todo.done = done

            def all_done():
                for todo in todos.value:
                    todo.done = True

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
                def _(store: rxui.VforStore[TodoItem]):
                    item = store.get()
                    with ui.card().classes("w-full row-card"), ui.row():
                        rxui.label(lambda: item.value.title).classes("row-title")
                        rxui.checkbox(
                            "done",
                            value=rxui.vmodel(item.value.done),
                            on_change=lambda e: change_done(item.value, e.value),
                        )
                        rxui.button(
                            "del", on_click=lambda: del_todo(item.value)
                        ).bind_enabled(lambda: item.value.done)

        page = browser.open(page_path)

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
    def test_two_way_binding_with_dict(self, browser: BrowserManager, page_path: str):
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
                item = store.get()
                with ui.card().classes("row-card"):
                    rxui.checkbox(
                        text=lambda: item.value["message"],
                        value=rxui.vmodel(item, "done"),
                    )

        page = browser.open(page_path)

        label_totals = LabelUtils(page, "label totals")

        locator_row_cards = page._page.locator(".row-card")
        locator_row_checkboxs = locator_row_cards.get_by_role("checkbox")

        def get_checkbox(index: int):
            return locator_row_checkboxs.all()[index]

        label_totals.expect_contain_text("1")

        get_checkbox(0).click()

        label_totals.expect_contain_text("2")

    def test_two_way_binding_with_dataclass(
        self, browser: BrowserManager, page_path: str
    ):
        @dataclass
        class Item:
            id: int
            message: str
            done: bool

        @ui.page(page_path)
        def _():
            # refs
            items = deep_ref(
                [
                    Item(**{"id": 1, "message": "foo", "done": False}),
                    Item(**{"id": 2, "message": "bar", "done": True}),
                ]
            )

            # ref_computeds
            @ref_computed
            def total_count():
                return sum(item.done for item in items.value)

            # ui
            set_test_id(rxui.label(total_count), "label totals")

            @rxui.vfor(items, key="id")
            def _(store: rxui.VforStore[Item]):
                item = store.get()
                with ui.card().classes("row-card"):
                    rxui.checkbox(
                        text=lambda: item.value.message,
                        value=rxui.vmodel(item.value.done),
                    )

        page = browser.open(page_path)

        label_totals = LabelUtils(page, "label totals")

        locator_row_cards = page._page.locator(".row-card")
        locator_row_checkboxs = locator_row_cards.get_by_role("checkbox")

        def get_checkbox(index: int):
            return locator_row_checkboxs.all()[index]

        label_totals.expect_contain_text("1")

        get_checkbox(0).click()

        label_totals.expect_contain_text("2")

    def test_shallow_ref(self, browser: BrowserManager, page_path: str):
        text = to_ref("abcd")

        @ui.page(page_path)
        def _():
            with ui.row():

                @rxui.vfor(text)  # type: ignore
                def _(store: rxui.VforStore[str]):
                    rxui.label(store.get())

        page = browser.open(page_path)

        page.should_contain("abcd")

        text.value = "abc"
        page.should_contain("abc")

    def test_deep_ref(self, browser: BrowserManager, page_path: str):
        data = deep_ref([1, 2, 3, 4])

        @ui.page(page_path)
        def _():
            with ui.column() as for_box:

                @rxui.vfor(data)
                def _(store: rxui.VforStore[int]):
                    item = store.get()
                    row_num = store.row_index.value + 1

                    with ui.row().classes("flex-center"):
                        label = rxui.label(item)
                        input = rxui.input(value=rxui.vmodel(item))

                        set_test_id(label, f"vfor-label-{row_num}")
                        set_test_id(input, f"vfor-input-{row_num}")

            set_test_id(for_box, "for_box")

            set_test_id(rxui.label(data), "list-label")

            set_test_id(rxui.input(value=rxui.vmodel(data, 0)), "input1")

            def onclick():
                data.value[0] = 66

            set_test_id(ui.button("change", on_click=onclick), "btn")

        page = browser.open(page_path)

        list_label = LabelUtils(page, "list-label")
        input_for_1 = InputUtils(page, "input1")
        change_btn = ButtonUtils(page, "btn")

        vfor_label1 = LabelUtils(page, "vfor-label-1")
        vfor_input1 = InputUtils(page, "vfor-input-1")

        list_label.expect_contain_text("[1, 2, 3, 4]")

        vfor_input1.fill_text("x1")
        vfor_label1.expect_contain_text("x1")
        input_for_1.expect_to_have_text("x1")
        list_label.expect_contain_text("['x1', 2, 3, 4]")

        #
        input_for_1.fill_text("z20")

        vfor_label1.expect_contain_text("z20")
        vfor_input1.expect_to_have_text("z20")
        list_label.expect_contain_text("['z20', 2, 3, 4]")

        #
        change_btn.click()

        input_for_1.expect_to_have_text("66")
        vfor_label1.expect_contain_text("66")
        vfor_input1.expect_to_have_text("66")
        list_label.expect_contain_text("[66, 2, 3, 4]")

    def test_should_with_proxy(self, browser: BrowserManager, page_path: str):
        @ui.page(page_path)
        def _():
            data = deep_ref({"a": [1, 2]})

            set_test_id(rxui.label(data), "list-label")

            @rxui.vfor(data.value["a"])
            def _(s):
                row_num = s.row_index.value + 1
                rxui.label(s.get())
                input = rxui.input(value=rxui.vmodel(s.get()))
                set_test_id(input, f"vfor-input-{row_num}")

        page = browser.open(page_path)

        list_label = LabelUtils(page, "list-label")
        vfor_input1 = InputUtils(page, "vfor-input-1")

        list_label.expect_contain_text("[1, 2]")

        vfor_input1.fill_text("x1")
        list_label.expect_contain_text("['x1', 2]")
