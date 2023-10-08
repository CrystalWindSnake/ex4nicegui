from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import RadioUtils, set_test_id


def test_const_value(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        set_test_id(rxui.radio(["a", "b"]), "target")

    page.open(page_path)

    target = RadioUtils(page, "target")

    target.expect_to_be_visible()

    assert not target.is_checked_by_label("a")
    assert not target.is_checked_by_label("b")

    page.wait()
    target.check_by_label("a")
    assert target.is_checked_by_label("a")
    assert not target.is_checked_by_label("b")

    page.wait()
    target.check_by_label("b")
    assert not target.is_checked_by_label("a")
    assert target.is_checked_by_label("b")


def test_ref_value(page: ScreenPage, page_path: str):
    r_value = to_ref("")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.radio(["a", "b"], value=r_value), "target")

    page.open(page_path)

    target = RadioUtils(page, "target")

    target.expect_to_be_visible()

    assert not target.is_checked_by_label("a")
    assert not target.is_checked_by_label("b")
    assert r_value.value == ""

    page.wait()
    target.check_by_label("a")
    assert target.is_checked_by_label("a")
    assert not target.is_checked_by_label("b")
    assert r_value.value == "a"

    page.wait()
    target.check_by_label("b")
    assert not target.is_checked_by_label("a")
    assert target.is_checked_by_label("b")
    assert r_value.value == "b"


def test_ref_str_change_value(page: ScreenPage, page_path: str):
    r_value = to_ref("")

    @ui.page(page_path)
    def _():
        set_test_id(rxui.radio(["a", "b"], value=r_value), "target")

    page.open(page_path)

    target = RadioUtils(page, "target")

    target.expect_to_be_visible()

    page.wait()
    r_value.value = "a"

    assert target.is_checked_by_label("a")
    assert not target.is_checked_by_label("b")

    page.wait()
    r_value.value = "b"
    assert not target.is_checked_by_label("a")
    assert target.is_checked_by_label("b")


def test_ref_value_dict_options(page: ScreenPage, page_path: str):
    r_value = to_ref("")

    @ui.page(page_path)
    def _():
        opts = {
            "a": "a value",
            "b": "b value",
        }
        set_test_id(rxui.radio(opts, value=r_value), "target")

    page.open(page_path)

    target = RadioUtils(page, "target")

    target.expect_to_be_visible()

    assert not target.is_checked_by_label("a value")
    assert not target.is_checked_by_label("b value")
    assert r_value.value == ""

    page.wait()
    target.check_by_label("a value")
    assert target.is_checked_by_label("a value")
    assert not target.is_checked_by_label("b value")
    assert r_value.value == "a"

    page.wait()
    target.check_by_label("b value")
    assert not target.is_checked_by_label("a value")
    assert target.is_checked_by_label("b value")
    assert r_value.value == "b"
