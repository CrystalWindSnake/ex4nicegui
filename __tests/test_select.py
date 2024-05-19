from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, ref_computed, effect
from .screen import BrowserManager
from .utils import SelectUtils, set_test_id, ButtonUtils, SwitchUtils


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
        set_test_id(
            rxui.select(["a", "b"], value=r_str).classes("min-w-[20ch]"), "target"
        )

    page = browser.open(page_path)
    target = SelectUtils(page, "target")

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
        set_test_id(
            rxui.select(["a", "b"], value=r_str).classes("min-w-[20ch]"), "target"
        ).props("clearable")

    page = browser.open(page_path)
    target = SelectUtils(page, "target")

    target.expect_to_have_value("a")

    target.click_cancel()

    target.expect_not_to_have_value("a")
    target.expect_not_to_have_value("b")

    assert r_str.value is None


def test_option_change(browser: BrowserManager, page_path: str):
    r_str = to_ref("")
    r_has_data = to_ref(False)

    @ref_computed
    def cp_data():
        if r_has_data.value:
            return ["a", "b"]
        return []

    @ui.page(page_path)
    def _():
        set_test_id(rxui.switch("has data", value=r_has_data), "switch")
        set_test_id(rxui.select(cp_data, value=r_str).classes("min-w-[20ch]"), "target")

    page = browser.open(page_path)
    target = SelectUtils(page, "target")
    switch = SwitchUtils(page, "switch")

    page.wait()
    switch.click()

    target.click_and_select("a")

    page.wait()
    assert r_str.value == "a"


def test_multiple_list_opts(browser: BrowserManager, page_path: str):
    r_value = to_ref(["a", "b"])

    @ui.page(page_path)
    def _():
        set_test_id(
            rxui.select(["a", "b", "c", "d"], value=r_value, multiple=True), "target"
        )

    page = browser.open(page_path)
    target = SelectUtils(page, "target")

    target.expect_to_have_value("a, b")

    target.click_and_select("d")

    target.expect_to_have_value("a, b, d")

    assert r_value.value == ["a", "b", "d"]


def test_multiple_dict_opts(browser: BrowserManager, page_path: str):
    r_value = to_ref([1, 2])

    @ui.page(page_path)
    def _():
        set_test_id(
            rxui.select(
                {1: "a", 2: "b", 3: "c", 4: "d"}, value=r_value, multiple=True
            ).classes("min-w-[20ch]"),
            "target",
        )

    page = browser.open(page_path)
    target = SelectUtils(page, "target")

    target.expect_to_have_value("a, b")

    target.click_and_select("d")
    target.expect_to_have_value("a, b, d")
    assert r_value.value == [1, 2, 4]


def test_new_value_mode(browser: BrowserManager, page_path: str):
    r_str = to_ref(None)
    r_opts = to_ref([])

    @ui.page(page_path)
    def _():
        set_test_id(
            rxui.select(
                r_opts, clearable=True, value=r_str, new_value_mode="add-unique"
            ).classes("min-w-[20ch]"),
            "target",
        )

    page = browser.open(page_path)
    target = SelectUtils(page, "target")

    target.input_and_enter("a")

    target.click_cancel()

    target.input_and_enter("other")

    page.wait()
    assert r_str.value == "other"

    target.click_cancel()

    page.wait()
    assert r_str.value is None

    assert r_opts.value == ["a", "other"]


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

        select = rxui.select(opts2, value=value2).classes("min-w-[20ch]")

        def onclick():
            value1.value = "opts2"

        btn = ui.button("change opt2", on_click=onclick)

        set_test_id(
            select,
            "target",
        )

        set_test_id(
            btn,
            "button",
        )

    page = browser.open(page_path)

    target = SelectUtils(page, "target")
    button = ButtonUtils(page, "button")
    target.expect_to_have_value("a")

    button.click()
    page.wait()
    target.expect_to_have_value("m")
