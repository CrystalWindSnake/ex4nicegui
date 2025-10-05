from typing import Dict, List, cast
from ex4nicegui import rxui
from nicegui import ui
from ex4nicegui import to_ref, ref_computed
from ex4nicegui.utils.signals import deep_ref
from .screen import BrowserManager
from playwright.sync_api import expect


class TestExample:
    def test_todos_example(self, browser: BrowserManager, page_path: str):
        class TodoItem(rxui.ViewModel):
            done = rxui.var(False)
            title: str

            def __init__(self, title: str):
                super().__init__()
                self.title = title

        @ui.page(page_path)
        def _():
            ui.row.default_classes("flex-center")

            todos = deep_ref(cast(List[TodoItem], []))
            input = to_ref("")

            @ref_computed
            def total_done():
                return sum(todo.done.value for todo in todos.value)

            @ref_computed
            def totals():
                return len(todos.value)

            def new_todo(text: str):
                todos.value.append(TodoItem(text))

                input.value = ""

            def del_todo(todo):
                todos.value.remove(todo)

            def change_done(todo: TodoItem, done: bool):
                todo.done.value = done

            def all_done():
                for todo in todos.value:
                    todo.done.value = True

            def swap(a: int, b: int):
                todos.value[a], todos.value[b] = todos.value[b], todos.value[a]

            with ui.row():
                rxui.input(value=input).classes("input")
                rxui.button("add", on_click=lambda: new_todo(input.value)).classes(
                    "btn-add"
                )
                rxui.button("all done", on_click=lambda: all_done()).classes(
                    "btn-all-done"
                )
                rxui.button("swap", on_click=lambda: swap(0, -1)).classes("btn-swap")

                with ui.row():
                    ui.label("done count:")
                    rxui.label(total_done).classes("label-done")

                with ui.row():
                    ui.label("totals count:")
                    rxui.label(totals).classes("label-totals")

            with ui.column().classes("card_zone"):

                @rxui.vfor(todos, key="title")
                def _(store: rxui.VforStore[TodoItem]):
                    item = store.get_item()
                    with ui.card().classes("w-full row-card"), ui.row():
                        rxui.label(lambda: item.title).classes("row-title")
                        rxui.checkbox(
                            "done",
                            value=item.done,
                            on_change=lambda e: change_done(item, e.value),
                        )
                        rxui.button(
                            "del", on_click=lambda: del_todo(item)
                        ).bind_enabled(lambda: item.done.value)

        page = browser.open(page_path)

        btn_add = page.Button(".btn-add")
        btn_all_done = page.Button(".btn-all-done")
        btn_swap = page.Button(".btn-swap")
        input = page.Input(".input")

        label_done = page.Label(".label-done")
        label_totals = page.Label(".label-totals")

        locator_row_cards = page.locator(".row-card")
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
            rxui.label(total_count).classes("label-totals")

            @rxui.vfor(items, key="id")
            def _(store: rxui.VforStore[Dict]):
                item = store.get()
                with ui.card().classes("row-card"):
                    rxui.checkbox(
                        text=item.value["message"],
                        value=rxui.vmodel(item, "done"),
                    )

        page = browser.open(page_path)

        label_totals = page.Label(".label-totals")

        locator_row_cards = page.locator(".row-card")
        locator_row_checkboxs = locator_row_cards.get_by_role("checkbox")

        def get_checkbox(index: int):
            return locator_row_checkboxs.all()[index]

        label_totals.expect_contain_text("1")

        get_checkbox(0).click()

        label_totals.expect_contain_text("2")

    def test_two_way_binding_with_dataclass(
        self, browser: BrowserManager, page_path: str
    ):
        class Item(rxui.ViewModel):
            message = rxui.var("")
            done = rxui.var(False)

            def __init__(self, id: int, message: str, done: bool):
                super().__init__()
                self.id = id
                self.message.value = message
                self.done.value = done

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
                return sum(item.done.value for item in items.value)

            # ui
            rxui.label(total_count).classes("label-totals")

            @rxui.vfor(items, key="id")
            def _(store: rxui.VforStore[Item]):
                item = store.get_item()
                with ui.card().classes("row-card"):
                    rxui.checkbox(
                        text=item.message,
                        value=item.done,
                    )

        page = browser.open(page_path)

        label_totals = page.Label(".label-totals")

        locator_row_cards = page.locator(".row-card")
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
                    rxui.label(store.get_item())

        page = browser.open(page_path)

        page.should_contain("abcd")

        text.value = "abc"
        page.should_contain("abc")

    def test_deep_ref(self, browser: BrowserManager, page_path: str):
        data = deep_ref([1, 2, 3, 4])

        @ui.page(page_path)
        def _():
            with ui.column().classes("for_box"):

                @rxui.vfor(data)
                def _(store: rxui.VforStore[str]):
                    item = store.get()
                    row_num = store.row_index.value + 1

                    with ui.row().classes("flex-center"):
                        rxui.label(item).classes(f"vfor-label-{row_num}")
                        rxui.input(value=item).classes(f"vfor-input-{row_num}")

            rxui.label(data).classes("list-label")
            rxui.input(value=rxui.vmodel(data, 0)).classes("input1")

            def onclick():
                data.value[0] = 66

            ui.button("change", on_click=onclick).classes("btn")

        page = browser.open(page_path)

        list_label = page.Label(".list-label")
        input_for_1 = page.Input(".input1")
        change_btn = page.Button(".btn")

        vfor_label1 = page.Label(".vfor-label-1")
        vfor_input1 = page.Input(".vfor-input-1")

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

            rxui.label(data).classes("list-label")

            @rxui.vfor(data.value["a"])
            def _(s):
                row_num = s.row_index.value + 1
                rxui.label(s.get())
                rxui.input(value=s.get()).classes(f"vfor-input-{row_num}")

        page = browser.open(page_path)

        list_label = page.Label(".list-label")
        vfor_input1 = page.Input(".vfor-input-1")

        list_label.expect_contain_text("[1, 2]")

        vfor_input1.fill_text("x1")
        list_label.expect_contain_text("['x1', 2]")
