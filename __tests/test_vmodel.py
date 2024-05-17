import warnings
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from ex4nicegui.utils.signals import deep_ref
from .screen import BrowserManager
from .utils import InputUtils, LabelUtils, set_test_id


def test_should_dict_sync(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        data = deep_ref({"a": 1, "b": [1, 2, 3, 4]})

        set_test_id(rxui.label(data), "label")
        set_test_id(rxui.input(value=rxui.vmodel(data.value["a"])), "input")

    page = browser.open(page_path)

    label = LabelUtils(page, "label")
    input = InputUtils(page, "input")

    input.expect_to_have_text("1")
    label.expect_to_have_text("{'a': 1, 'b': [1, 2, 3, 4]}")

    input.fill_text("99")

    label.expect_to_have_text("{'a': '99', 'b': [1, 2, 3, 4]}")


def test_should_dict_sync_deep_value(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        data = deep_ref({"a": 1, "b": [1, 2, 3, 4]})

        set_test_id(rxui.label(data), "label")
        set_test_id(rxui.input(value=rxui.vmodel(data.value["b"][0])), "input")

    page = browser.open(page_path)

    label = LabelUtils(page, "label")
    input = InputUtils(page, "input")

    input.expect_to_have_text("1")
    label.expect_to_have_text("{'a': 1, 'b': [1, 2, 3, 4]}")

    input.fill_text("99")

    label.expect_to_have_text("{'a': 1, 'b': ['99', 2, 3, 4]}")


def test_should_sync_shallow_ref(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        data = to_ref(1)

        set_test_id(rxui.label(data), "label")
        set_test_id(rxui.input(value=rxui.vmodel(data)), "input")

    page = browser.open(page_path)

    label = LabelUtils(page, "label")
    input = InputUtils(page, "input")

    input.expect_to_have_text("1")
    label.expect_to_have_text("1")

    input.fill_text("99")

    label.expect_to_have_text("99")


def test_should_sync_reactive_object_var(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        data = deep_ref({"a": 1})
        item = data.value

        set_test_id(rxui.label(data), "label")
        set_test_id(rxui.input(value=rxui.vmodel(item["a"])), "input")

    page = browser.open(page_path)

    label = LabelUtils(page, "label")
    input = InputUtils(page, "input")

    input.expect_to_have_text("1")
    label.expect_to_have_text("{'a': 1}")

    input.fill_text("99")

    label.expect_to_have_text("{'a': '99'}")


def test_should_warning_when_no_key_expr(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        data = deep_ref(1)
        item = data.value

        with warnings.catch_warnings(record=True) as w:
            set_test_id(rxui.input(value=rxui.vmodel(item)), "input")

            assert len(w) == 1

    page = browser.open(page_path)

    input = InputUtils(page, "input")

    input.expect_to_have_text("1")
