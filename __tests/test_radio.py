from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from .utils import RadioUtils, set_test_id


def test_display(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        set_test_id(rxui.radio(["a", "b"]), "target const")

    page.open(page_path)

    def normal_check(radio_utils: RadioUtils):
        radio_utils.expect_to_be_visible()

        assert not radio_utils.is_checked_by_label("a")
        assert not radio_utils.is_checked_by_label("b")

        radio_utils.check_by_label("a")
        page.wait()
        assert radio_utils.is_checked_by_label("a")
        assert not radio_utils.is_checked_by_label("b")

        radio_utils.check_by_label("b")
        page.wait()
        assert not radio_utils.is_checked_by_label("a")
        assert radio_utils.is_checked_by_label("b")

    target_const = RadioUtils(page, "target const")
    normal_check(target_const)


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
    page.wait()
    assert target.is_checked_by_label("a")
    assert not target.is_checked_by_label("b")
    assert r_value.value == "a"

    page.wait()
    target.check_by_label("b")
    page.wait()
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
    page.wait()
    assert target.is_checked_by_label("a")
    assert not target.is_checked_by_label("b")

    page.wait()
    r_value.value = "b"
    page.wait()
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
    page.wait()
    assert target.is_checked_by_label("a value")
    assert not target.is_checked_by_label("b value")
    assert r_value.value == "a"

    page.wait()
    target.check_by_label("b value")
    page.wait()
    assert not target.is_checked_by_label("a value")
    assert target.is_checked_by_label("b value")
    assert r_value.value == "b"
