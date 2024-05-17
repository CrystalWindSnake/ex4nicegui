from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager
from .utils import LabelUtils, set_test_id


def test_display(browser: BrowserManager, page_path: str):
    r_str = to_ref("ref label")
    r_bool = to_ref("init")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.label("test label"), "target")
        set_test_id(rxui.label(r_str), "ref target")

        r_bool.value = True  # type: ignore
        set_test_id(rxui.label(r_bool), "bool ref target")

    page = browser.open(page_path)

    target_const = LabelUtils(page, "target")
    target_const.expect_to_have_text("test label")

    target_ref = LabelUtils(page, "ref target")
    target_ref.expect_to_have_text("ref label")

    target_bool_ref = LabelUtils(page, "bool ref target")
    target_bool_ref.expect_to_have_text("True")


def test_ref_str_change_value(browser: BrowserManager, page_path: str):
    r_str = to_ref("old")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.label(r_str), "target")

    page = browser.open(page_path)

    target = LabelUtils(page, "target")
    target.expect_to_have_text("old")

    r_str.value = "new"

    target.expect_to_have_text("new")


def test_bind_color(browser: BrowserManager, page_path: str):
    r_color = to_ref("red")

    @ui.page(page_path)
    def _():
        label = rxui.label("label")
        label.bind_color(r_color)
        set_test_id(label, "target")

    page = browser.open(page_path)
    target = LabelUtils(page, "target")

    assert target.get_style("color") == "red"

    r_color.value = "green"
    page.wait()
    assert target.get_style("color") == "green"
