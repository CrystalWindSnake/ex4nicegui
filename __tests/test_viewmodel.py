from typing import List, Union, Dict
from ex4nicegui import rxui, on, Ref, ref
from nicegui import ui
from .screen import BrowserManager
import json


def list_dict_to_text(value: Union[List, Dict]):
    return json.dumps(str(value))[1:-1]


def test_base_type(browser: BrowserManager, page_path: str):
    """use value by base type e.g. int, str, bool"""

    class Person(rxui.ViewModel):
        name = rxui.var("")
        age = rxui.var(0.0)
        is_male = rxui.var(False)

    @ui.page(page_path)
    def _():
        person = Person()
        rxui.label(person.name).classes("label-name")
        rxui.label(person.age).classes("label-age")
        rxui.label(person.is_male).classes("label-is-male")

        rxui.input(value=person.name).classes("input-name")
        rxui.number(value=person.age).classes("input-age")
        rxui.checkbox(value=person.is_male).classes("checkbox-is-male")

    page = browser.open(page_path)
    label_name = page.Label(".label-name")
    label_age = page.Label(".label-age")
    label_is_male = page.Label(".label-is-male")

    input_name = page.Input(".input-name")
    input_age = page.Input(".input-age")
    checkbox_is_male = page.Checkbox(".checkbox-is-male")

    # test initial value
    label_name.expect_equal_text("")
    label_age.expect_equal_text("0.0")
    label_is_male.expect_equal_text("False")

    # test input value
    input_name.fill_text("Alice")
    input_age.fill_text("25")
    checkbox_is_male.click()

    label_name.expect_equal_text("Alice")
    label_age.expect_equal_text("25.0")
    label_is_male.expect_equal_text("True")


def test_list_type(browser: BrowserManager, page_path: str):
    """use value by list, dict"""

    class Person(rxui.ViewModel):
        info = rxui.var(lambda: ["", 0.0, False])

    @ui.page(page_path)
    def _():
        person = Person()
        rxui.label(person.info).classes("label-info")

        def set_name():
            person.info.value[0] = "Alice"

        def set_age():
            person.info.value[1] = 25.0

        def set_is_male():
            person.info.value[2] = True

        ui.button("set name").on_click(set_name).classes("btn-set-name")
        ui.button("set age").on_click(set_age).classes("btn-set-age")
        ui.button("set is_male").on_click(set_is_male).classes("btn-set-is-male")

    page = browser.open(page_path)
    label_info = page.Label(".label-info")

    btn_set_name = page.Button(".btn-set-name")
    btn_set_age = page.Button(".btn-set-age")
    btn_set_is_male = page.Button(".btn-set-is-male")

    # test initial value
    label_info.expect_equal_text(list_dict_to_text(["", 0.0, False]))

    # test input value
    btn_set_name.click()
    btn_set_age.click()
    btn_set_is_male.click()

    label_info.expect_equal_text(list_dict_to_text(["Alice", 25.0, True]))


def test_dict_type(browser: BrowserManager, page_path: str):
    """use value by list, dict"""

    class Person(rxui.ViewModel):
        name = rxui.var("")
        age = rxui.var(0)
        is_male = rxui.var(False)

        def __init__(self, name: str, age: int, is_male: bool):
            super().__init__()

            self.name = name
            self.age = age
            self.is_male = is_male

        def to_str(self) -> str:
            return f"{self.name} {self.age} {self.is_male}"

    class Home(rxui.ViewModel):
        persons: Ref[List[Person]] = rxui.var(lambda: [])

        def display_ref(self) -> Ref[str]:
            result = ref("")

            @on(self.persons)
            def _():
                persons = [person.to_str() for person in self.persons.value]

                result.value = ";".join(persons)

            return result

    @ui.page(page_path)
    def _():
        will_born_persons = iter(
            [
                {"name": "Alice", "age": 25, "is_male": True},
                {"name": "Bob", "age": 30, "is_male": False},
                {"name": "Charlie", "age": 35, "is_male": True},
            ]
        )

        home = Home()
        rxui.label(home.display_ref()).classes("label-info")

        def add_person():
            person = Person(**next(will_born_persons))
            home.persons.value.append(person)

        ui.button("add person").on_click(add_person).classes("btn-add-person")

    page = browser.open(page_path)
    label_info = page.Label(".label-info")

    btn_add_person = page.Button(".btn-add-person")

    btn_add_person.click(click_count=3)

    label_info.expect_equal_text("Alice 25 True;Bob 30 False;Charlie 35 True")


def test_class_var(browser: BrowserManager, page_path: str):
    class Person(rxui.ViewModel):
        name = rxui.var("")

    @ui.page(page_path)
    def _():
        rxui.label(lambda: f"Hello, {Person.name.value}!").classes("label-name")
        rxui.input(value=Person.name).classes("input-name")

    page = browser.open(page_path)
    label_name = page.Label(".label-name")
    input_name = page.Input(".input-name")

    # test initial value
    label_name.expect_equal_text("Hello, !")

    # test input value
    input_name.fill_text("Alice")

    label_name.expect_equal_text("Hello, Alice!")


def test_cached_var(browser: BrowserManager, page_path: str):
    counter = {"lower name": 0}

    class Person(rxui.ViewModel):
        name = rxui.var("")

        def upper_name(self) -> str:
            return self.name.value.upper()

        @rxui.cached_var
        def lower_name(self) -> str:
            counter["lower name"] += 1
            return self.name.value.lower()

    @ui.page(page_path)
    def _():
        p = Person()
        rxui.label(p.upper_name).classes("label-upper-name")
        rxui.label(lambda: f"Hello, {p.lower_name()}!").bind_color(
            lambda: "red" if p.lower_name() == "alice" else "black"
        ).classes("label-lower-name")
        rxui.input(value=p.name).classes("input-name")

    page = browser.open(page_path)
    label_upper_name = page.Label(".label-upper-name")
    label_lower_name = page.Label(".label-lower-name")
    input_name = page.Input(".input-name")

    # test input value
    input_name.fill_text("Alice")

    label_upper_name.expect_equal_text("ALICE")
    label_lower_name.expect_equal_text("Hello, alice!")

    assert counter["lower name"] == 2


class TestWithImplicit:
    def test_by_instance(self, browser: BrowserManager, page_path: str):
        class Countr(rxui.ViewModel):
            count = 0

            def increment(self):
                self.count += 1

            def decrement(self):
                self.count -= 1

            def plus_one(self):
                return self.count + 1

            def text(self):
                return f"Count: {self.count}, plus one: {self.plus_one()}"

        @ui.page(page_path)
        def _():
            c = Countr()
            ui.button("Decrement", on_click=c.decrement).classes("btn-decrement")
            rxui.label(c.count).classes("label-count")
            ui.button("Increment", on_click=c.increment).classes("btn-increment")
            rxui.label(c.text).classes("label-text")

        page = browser.open(page_path)
        btn_decrement = page.Button(".btn-decrement")
        label_count = page.Label(".label-count")
        btn_increment = page.Button(".btn-increment")
        label_text = page.Label(".label-text")

        # test initial value
        label_count.expect_equal_text("0")
        label_text.expect_equal_text("Count: 0, plus one: 1")

        # test increment
        btn_increment.click()
        label_count.expect_equal_text("1")
        label_text.expect_equal_text("Count: 1, plus one: 2")

        # test decrement
        btn_decrement.click()
        label_count.expect_equal_text("0")
        label_text.expect_equal_text("Count: 0, plus one: 1")

    def test_use_empty_list(self, browser: BrowserManager, page_path: str):
        class Numbers(rxui.ViewModel):
            nums = []

            def __init__(self):
                super().__init__()
                self.nums = [1, 2, 3]

            def add_number(self):
                new_value = max(self.nums) + 1
                self.nums.append(new_value)

            def pop_number(self):
                self.nums.pop()

            def reversed_with_slice(self):
                self.nums = self.nums[::-1]

            def reversed_method(self):
                self.nums.reverse()

            def reversed(self):
                self.nums = list(reversed(self.nums))

            def display_nums(self):
                return ", ".join(map(str, self.nums))

            def get_new_num(self):
                return max(self.nums) + 1

        @ui.page(page_path)
        def _():
            numbers = Numbers()
            ui.button("Add number", on_click=numbers.add_number).classes(
                "btn-add-number"
            )
            ui.button("Pop number", on_click=numbers.pop_number).classes(
                "btn-pop-number"
            )
            ui.button(
                "Reversed with slice", on_click=numbers.reversed_with_slice
            ).classes("btn-reversed-with-slice")
            ui.button("Reversed method", on_click=numbers.reversed_method).classes(
                "btn-reversed-method"
            )
            ui.button("Reversed", on_click=numbers.reversed).classes("btn-reversed")
            rxui.label(lambda: ",".join(map(str, numbers.nums))).classes(
                "label-numbers"
            )

        page = browser.open(page_path)
        btn_add_number = page.Button(".btn-add-number")
        btn_pop_number = page.Button(".btn-pop-number")
        btn_reversed_with_slice = page.Button(".btn-reversed-with-slice")
        btn_reversed_method = page.Button(".btn-reversed-method")
        btn_reversed = page.Button(".btn-reversed")
        label_numbers = page.Label(".label-numbers")

        # test initial value
        label_numbers.expect_equal_text("1,2,3")

        # test add number
        btn_add_number.click()
        label_numbers.expect_equal_text("1,2,3,4")

        # test pop number
        btn_pop_number.click()
        label_numbers.expect_equal_text("1,2,3")

        # test reversed with slice
        btn_reversed_with_slice.click()
        label_numbers.expect_equal_text("3,2,1")

        # test reversed method
        btn_reversed_method.click()
        label_numbers.expect_equal_text("1,2,3")

        # test reversed
        btn_reversed.click()
        label_numbers.expect_equal_text("3,2,1")

    def test_use_list_var(self, browser: BrowserManager, page_path: str):
        class Numbers(rxui.ViewModel):
            numbers = rxui.list_var(lambda: [1, 2, 3])

            def add_number(self):
                new_value = max(self.numbers) + 1
                self.numbers.append(new_value)

            def pop_number(self):
                self.numbers.pop()

            def reversed_with_slice(self):
                self.numbers = self.numbers[::-1]

            def reversed_method(self):
                self.numbers.reverse()

            def reversed(self):
                self.numbers = list(reversed(self.numbers))

        @ui.page(page_path)
        def _():
            numbers = Numbers()
            ui.button("Add number", on_click=numbers.add_number).classes(
                "btn-add-number"
            )
            ui.button("Pop number", on_click=numbers.pop_number).classes(
                "btn-pop-number"
            )
            ui.button(
                "Reversed with slice", on_click=numbers.reversed_with_slice
            ).classes("btn-reversed-with-slice")
            ui.button("Reversed method", on_click=numbers.reversed_method).classes(
                "btn-reversed-method"
            )
            ui.button("Reversed", on_click=numbers.reversed).classes("btn-reversed")
            rxui.label(lambda: ",".join(map(str, numbers.numbers))).classes(
                "label-numbers"
            )

        page = browser.open(page_path)
        btn_add_number = page.Button(".btn-add-number")
        btn_pop_number = page.Button(".btn-pop-number")
        btn_reversed_with_slice = page.Button(".btn-reversed-with-slice")
        btn_reversed_method = page.Button(".btn-reversed-method")
        btn_reversed = page.Button(".btn-reversed")
        label_numbers = page.Label(".label-numbers")

        # test initial value
        label_numbers.expect_equal_text("1,2,3")

        # test add number
        btn_add_number.click()
        label_numbers.expect_equal_text("1,2,3,4")

        # test pop number
        btn_pop_number.click()
        label_numbers.expect_equal_text("1,2,3")

        # test reversed with slice
        btn_reversed_with_slice.click()
        label_numbers.expect_equal_text("3,2,1")

        # test reversed method
        btn_reversed_method.click()
        label_numbers.expect_equal_text("1,2,3")

        # test reversed
        btn_reversed.click()
        label_numbers.expect_equal_text("3,2,1")

    def test_use_list_independent(self, browser: BrowserManager, page_path: str):
        class Numbers(rxui.ViewModel):
            numbers = []

            def change_values_1(self):
                self.numbers = [1, 2, 3]

            def change_values_2(self):
                self.numbers = [4, 5, 6]

        @ui.page(page_path)
        def _():
            numbers1 = Numbers()
            numbers2 = Numbers()
            ui.button("change values 1", on_click=numbers1.change_values_1).classes(
                "btn-change-values-1"
            )
            ui.button("change values 2", on_click=numbers2.change_values_2).classes(
                "btn-change-values-2"
            )
            rxui.label(lambda: ",".join(map(str, numbers1.numbers))).classes(
                "label-numbers-1"
            )
            rxui.label(lambda: ",".join(map(str, numbers2.numbers))).classes(
                "label-numbers-2"
            )

        page = browser.open(page_path)
        btn_change_values_1 = page.Button(".btn-change-values-1")
        btn_change_values_2 = page.Button(".btn-change-values-2")
        label_numbers_1 = page.Label(".label-numbers-1")
        label_numbers_2 = page.Label(".label-numbers-2")

        btn_change_values_1.click()
        btn_change_values_2.click()

        label_numbers_1.expect_equal_text("1,2,3")
        label_numbers_2.expect_equal_text("4,5,6")

    def test_str_to_none(self, browser: BrowserManager, page_path: str):
        class State(rxui.ViewModel):
            text = ""

        @ui.page(page_path)
        def _():
            state = State()

            rxui.label(text=state.text).classes("label-text")
            rxui.input(value=state.text).props("clearable").classes("input-text")

        page = browser.open(page_path)
        label_text = page.Label(".label-text")
        input_text = page.Input(".input-text")

        # test initial value
        label_text.expect_equal_text("")

        # test input value
        input_text.fill_text("hello")
        label_text.expect_equal_text("hello")

        # test clear input
        input_text.click_cancel_icon()
        label_text.expect_equal_text("None")
