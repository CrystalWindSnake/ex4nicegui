from typing import Optional
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, ref_computed, effect, Ref
from .screen import BrowserManager


def test_const_str(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.toggle(["a", "b"], value="a").classes("min-w-[20ch] target")

    page = browser.open(page_path)

    target = page.Toggle(".target")
    target.expect_to_be_visible()


def test_ref_str(browser: BrowserManager, page_path: str):
    r_str: Ref[Optional[str]] = to_ref(None)

    @ui.page(page_path)
    def _():
        rxui.toggle(["a", "b"], value=r_str).classes("min-w-[20ch] target")

    page = browser.open(page_path)
    target = page.Toggle(".target")

    target.expect_not_selected("a")
    target.expect_not_selected("b")

    r_str.value = "a"
    target.expect_selected("a")

    r_str.value = "b"
    target.expect_selected("b")

    r_str.value = None
    target.expect_not_selected("a")
    target.expect_not_selected("b")


def test_clearable(browser: BrowserManager, page_path: str):
    r_str = to_ref("a")

    @ui.page(page_path)
    def _():
        rxui.toggle(["a", "b"], value=r_str, clearable=True).classes(
            "min-w-[20ch] target"
        )
        rxui.label(r_str).classes("label-str")

    page = browser.open(page_path)
    target = page.Toggle(".target")
    label = page.Label(".label-str")

    target.expect_selected("a")

    target.click_select("a")

    target.expect_not_selected("a")
    target.expect_not_selected("b")

    label.expect_equal_text("None")


def test_option_change(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_value = to_ref(None)
        r_has_data = to_ref(False)

        @ref_computed
        def cp_data():
            if r_has_data.value:
                return ["a", "b"]
            return []

        rxui.switch("has data", value=r_has_data).classes("switch")
        rxui.toggle(cp_data, value=r_value).classes("min-w-[20ch] target")
        rxui.label(r_value).classes("label-str")

    page = browser.open(page_path)
    target = page.Toggle(".target")
    switch = page.Switch(".switch")
    label = page.Label(".label-str")

    switch.click()

    target.click_select("a")

    label.expect_contain_text("a")


def test_opts_value_change_same_time(browser: BrowserManager, page_path: str):
    data = {
        "opts1": list("abcd"),
        "opts2": list("mnxy"),
    }

    value1 = to_ref("opts1")
    value2 = to_ref("")

    @ui.page(page_path)
    def _():
        @ref_computed
        def opts2():
            return data[value1.value]

        @effect
        def _():
            value2.value = opts2.value[0]

        rxui.toggle(opts2, value=value2).classes("min-w-[20ch] target")

        def onclick():
            value1.value = "opts2"

        ui.button("change opt2", on_click=onclick).classes("btn")

    page = browser.open(page_path)

    target = page.Toggle(".target")
    button = page.Button(".btn")
    target.expect_selected("a")

    button.click()
    target.expect_selected("m")


def test_value_not_in_options(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        name: Ref[Optional[str]] = to_ref(None)
        options = ["a", "b"]

        rxui.toggle(options, value=name)
        rxui.label(text=name).classes("label")
        ui.button("change", on_click=lambda: name.set_value("other")).classes("btn")

    page = browser.open(page_path)

    label = page.Label(".label")
    button = page.Button(".btn")

    button.click()
    label.expect_equal_text("other")


def test_false_value(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        value = to_ref(True)

        rxui.toggle({True: "dark", False: "light", None: "auto"}, value=value).classes(
            "target"
        )
        ui.button("set to False", on_click=lambda: value.set_value(False)).classes(
            "btn"
        )

    page = browser.open(page_path)

    button = page.Button(".btn")
    target = page.Toggle(".target")

    button.click()
    target.expect_selected("light")
