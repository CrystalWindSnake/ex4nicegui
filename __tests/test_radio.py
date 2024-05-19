from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager
from .utils import RadioUtils, set_test_id


def test_display(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.radio(["a", "b"]).classes("target")

    page = browser.open(page_path)

    target = page.Radio(".target")

    target.expect_to_be_visible()
    target.expect_not_to_be_checked("a")
    target.expect_not_to_be_checked("b")

    target.check_by_label("a")

    target.expect_to_be_checked("a")
    target.expect_not_to_be_checked("b")

    target.check_by_label("b")

    target.expect_not_to_be_checked("a")
    target.expect_to_be_checked("b")


def test_ref_value(browser: BrowserManager, page_path: str):
    r_value = to_ref("")

    @ui.page(page_path)
    def _():
        rxui.radio(["a", "b"], value=r_value).classes("target")
        rxui.label(r_value).classes("label")

    page = browser.open(page_path)

    target = page.Radio(".target")
    label = page.Label(".label")

    target.expect_to_be_visible()

    target.expect_not_to_be_checked("a")
    target.expect_not_to_be_checked("b")

    assert r_value.value is None

    target.check_by_label("a")

    target.expect_to_be_checked("a")
    target.expect_not_to_be_checked("b")
    label.expect_contain_text("a")

    target.check_by_label("b")

    target.expect_not_to_be_checked("a")
    target.expect_to_be_checked("b")
    label.expect_contain_text("b")


def test_ref_str_change_value(browser: BrowserManager, page_path: str):
    r_value = to_ref("")

    @ui.page(page_path)
    def _():
        rxui.radio(["a", "b"], value=r_value).classes("target")

    page = browser.open(page_path)

    target = page.Radio(".target")

    target.expect_to_be_visible()

    r_value.value = "a"

    target.expect_to_be_checked("a")
    target.expect_not_to_be_checked("b")

    r_value.value = "b"
    target.expect_not_to_be_checked("a")
    target.expect_to_be_checked("b")


def test_ref_value_dict_options(browser: BrowserManager, page_path: str):
    r_value = to_ref("")

    @ui.page(page_path)
    def _():
        opts = {
            "a": "a value",
            "b": "b value",
        }
        rxui.radio(opts, value=r_value).classes("target")
        rxui.label(r_value).classes("label")

    page = browser.open(page_path)

    target = page.Radio(".target")
    label = page.Label(".label")

    target.expect_to_be_visible()

    target.check_by_label("a value")

    target.expect_to_be_checked("a value")
    target.expect_not_to_be_checked("b value")
    label.expect_contain_text("a")

    target.check_by_label("b value")

    target.expect_not_to_be_checked("a value")
    target.expect_to_be_checked("b value")
    label.expect_contain_text("b")
