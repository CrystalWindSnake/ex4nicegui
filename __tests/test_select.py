from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, ref_computed, effect, deep_ref
from .screen import BrowserManager
import pytest


def test_const_str(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.select(["a", "b"], label="test select").classes("min-w-[20ch] target")

    page = browser.open(page_path)

    target = page.Select(".target")
    target.expect_to_be_visible()


def test_ref_str(browser: BrowserManager, page_path: str):
    r_str = to_ref("")

    @ui.page(page_path)
    def _():
        rxui.select(["a", "b"], value=r_str).classes("min-w-[20ch] target")

    page = browser.open(page_path)
    target = page.Select(".target")

    target.expect_not_to_have_value("a")
    target.expect_not_to_have_value("b")

    r_str.value = "a"
    target.expect_to_have_value("a")

    r_str.value = "b"
    target.expect_to_have_value("b")

    r_str.value = ""
    target.expect_not_to_have_value("a")
    target.expect_not_to_have_value("b")


def test_clearable(browser: BrowserManager, page_path: str):
    r_str = to_ref("a")

    @ui.page(page_path)
    def _():
        rxui.select(["a", "b"], value=r_str).classes("min-w-[20ch] target").props(
            "clearable"
        )

    page = browser.open(page_path)
    target = page.Select(".target")

    target.expect_to_have_value("a")

    target.click_cancel()

    target.expect_not_to_have_value("a")
    target.expect_not_to_have_value("b")

    assert r_str.value is None


def test_option_change(browser: BrowserManager, page_path: str):
    r_str = to_ref(None)
    r_has_data = to_ref(False)

    @ref_computed
    def cp_data():
        if r_has_data.value:
            return ["a", "b"]
        return []

    @ui.page(page_path)
    def _():
        rxui.switch("has data", value=r_has_data).classes("switch")
        rxui.select(cp_data, value=r_str).classes("min-w-[20ch] target")
        rxui.label(r_str).classes("label-str")

    page = browser.open(page_path)
    target = page.Select(".target")
    switch = page.Switch(".switch")
    label = page.Label(".label-str")

    switch.click()

    target.click_and_select("a")

    label.expect_contain_text("a")


def test_multiple_list_opts(browser: BrowserManager, page_path: str):
    r_value = to_ref(["a", "b"])

    @ui.page(page_path)
    def _():
        rxui.select(["a", "b", "c", "d"], value=r_value, multiple=True).classes(
            "target"
        )
        rxui.label(r_value).classes("label-value")

    page = browser.open(page_path)
    target = page.Select(".target")
    label = page.Label(".label-value")

    target.expect_to_have_value("a, b")

    target.click_and_select("d")

    target.expect_to_have_value("a, b, d")

    label.expect_contain_text("['a', 'b', 'd']")


def test_multiple_dict_opts(browser: BrowserManager, page_path: str):
    r_value = to_ref([1, 2])

    @ui.page(page_path)
    def _():
        rxui.select(
            {1: "a", 2: "b", 3: "c", 4: "d"}, value=r_value, multiple=True
        ).classes("min-w-[20ch] target")

        rxui.label(r_value).classes("label-value")

    page = browser.open(page_path)
    target = page.Select(".target")
    label = page.Label(".label-value")

    target.expect_to_have_value("a, b")

    target.click_and_select("d")
    target.expect_to_have_value("a, b, d")

    label.expect_contain_text("[1, 2, 4]")


@pytest.mark.skip(reason="not implemented yet")
def test_new_value_mode(browser: BrowserManager, page_path: str):
    r_str = to_ref(None)
    r_opts = to_ref([])

    @ui.page(page_path)
    def _():
        rxui.select(
            r_opts, clearable=True, value=r_str, new_value_mode="add-unique"
        ).classes("min-w-[20ch] target")

        rxui.label(r_str).classes("label-str")
        rxui.label(r_opts).classes("label-opts")

    page = browser.open(page_path)
    target = page.Select(".target")
    label_str = page.Label(".label-str")
    label_opts = page.Label(".label-opts")

    target.input_and_enter("a")

    target.click_cancel()

    target.input_and_enter("other")

    label_str.expect_contain_text("other")

    target.click_cancel()

    label_str.expect_contain_text("None")

    label_opts.expect_contain_text("""["a", "other"]""")


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

        rxui.select(opts2, value=value2).classes("min-w-[20ch] target")

        def onclick():
            value1.value = "opts2"

        ui.button("change opt2", on_click=onclick).classes("btn")

    page = browser.open(page_path)

    target = page.Select(".target")
    button = page.Button(".btn")
    target.expect_to_have_value("a")

    button.click()
    target.expect_to_have_value("m")


def test_multiple_with_deep_ref(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        data = deep_ref([])

        rxui.label(data).classes("label-ref")

        s = rxui.select(
            options=["reading", "swimming", "running"],
            value=data,
            multiple=True,
        ).classes("target")

        lbl_element_value = ui.label().classes("label-value")

        ui.button(
            "display value", on_click=lambda: lbl_element_value.set_text(str(s.value))
        ).classes("btn")

    page = browser.open(page_path)

    target = page.Select(".target")
    button = page.Button(".btn")
    lbl_element_value = page.Label(".label-value")
    lbl_ref = page.Label(".label-ref")

    target.click_and_select("reading", "swimming")
    target.show_popup_click()
    button.click()
    lbl_element_value.expect_contain_text("['reading', 'swimming']")
    lbl_ref.expect_contain_text("['reading', 'swimming']")
