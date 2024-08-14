from typing import List, Union, Dict
from ex4nicegui import rxui, on, Ref, ref, ref_computed as computed
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
    class Person(rxui.ViewModel):
        name = rxui.var("")

        def upper_name(self) -> str:
            return self.name.value.upper()

        @rxui.cached_var
        def lower_name(self) -> str:
            return self.name.value.lower()

    @ui.page(page_path)
    def _():
        p = Person()
        rxui.label(p.upper_name).classes("label-upper-name")
        rxui.label(lambda: f"Hello, {p.lower_name()}!").classes("label-lower-name")
        rxui.input(value=p.name).classes("input-name")

    page = browser.open(page_path)
    label_upper_name = page.Label(".label-upper-name")
    label_lower_name = page.Label(".label-lower-name")
    input_name = page.Input(".input-name")

    # test input value
    input_name.fill_text("Alice")

    label_upper_name.expect_equal_text("ALICE")
    label_lower_name.expect_equal_text("Hello, alice!")
