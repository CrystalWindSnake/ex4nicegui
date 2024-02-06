from typing import List
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, ref_computed
from .screen import ScreenPage
from .utils import ButtonUtils, InputUtils, LabelUtils, set_test_id
from playwright.sync_api import expect



def _todo_with_dict():
    pass

def test_todos_example(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        ui.row.default_classes("flex-center")

        todos = to_ref([])
        input = to_ref("")

        @ref_computed
        def total_done():
            return sum(todo["done"] for todo in todos.value)

        @ref_computed
        def totals():
            return len(todos.value)

        @ref_computed
        def btn_enabled():
            todos_text = set(todo["title"] for todo in todos.value)
            return len(input.value) > 0 and (input.value not in todos_text)

        def new_todo(text: str):
            todos.value.append({"title": text, "done": False})
            todos.value = todos.value
            input.value = ""

        def del_todo(task_index: int):
            target = [
                todo for idx, todo in enumerate(todos.value) if idx == task_index
            ][0]
            todos.value.remove(target)
            todos.value = todos.value

        def all_done():
            for todo in todos.value:
                todo["done"] = True

            todos.value = todos.value

        with ui.row():
            set_test_id(rxui.input(value=input), "input")
            set_test_id(
                rxui.button("add", on_click=lambda: new_todo(input.value)).bind_enabled(
                    btn_enabled
                ),
                "btn add",
            )
            set_test_id(
                rxui.button("all done", on_click=lambda: all_done()), "btn all done"
            )

            with ui.row():
                ui.label("done count:")
                set_test_id(rxui.label(total_done), "label done")

            with ui.row():
                ui.label("totals count:")
                set_test_id(rxui.label(totals), "label totals")

        with ui.column().classes("card_zone"):

            @rxui.vfor(todos)
            def _(r: rxui.VforStore):
                with ui.card().classes("w-full row-card") as box, ui.row():
                    rxui.label(r.get("title")).classes("row-title")
                    rxui.checkbox("done", value=r.get("done"))
                    rxui.button(
                        "del", on_click=lambda: del_todo(r.row_index)
                    ).bind_enabled(r.get("done"))
                return box

    page.open(page_path)

    btn_add = ButtonUtils(page, "btn add")
    btn_all_done = ButtonUtils(page, "btn all done")
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
    get_checkbox(0).set_checked(True)
    label_done.expect_to_have_text("1")

    # more todos
    input.fill_text("test2")
    btn_add.click()

    input.fill_text("test3")
    btn_add.click()

    label_done.expect_to_have_text("1")
    label_totals.expect_to_have_text("3")

    #
    get_checkbox(2).set_checked(True)
    get_del_btn(0).click()

    label_done.expect_to_have_text("1")
    label_totals.expect_to_have_text("2")

    #
    btn_all_done.click()
    label_done.expect_to_have_text("2")
    label_totals.expect_to_have_text("2")

    # del all
    get_del_btn(0).click()
    get_del_btn(0).click()
    label_done.expect_to_have_text("0")
    label_totals.expect_to_have_text("0")
