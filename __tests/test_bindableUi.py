import pytest
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, ref_computed
from .screen import ScreenPage
from playwright.sync_api import expect
from .utils import SelectUtils, set_test_id


def test_bind_classes(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        # binding to dict
        # can have multiple classes toggled
        def binding_to_dict():
            bg_color = to_ref(False)
            has_error = to_ref(False)

            rxui.label("test").bind_classes(
                {"bg-blue": bg_color, "text-red": has_error}
            )

            rxui.switch("bg_color", value=bg_color)
            rxui.switch("has_error", value=has_error)

        # can also bind to a ref_computed
        def bind_to_ref_computed():
            bg_color = to_ref(False)
            has_error = to_ref(False)

            class_obj = ref_computed(
                lambda: {"bg-blue": bg_color.value, "text-red": has_error.value}
            )

            rxui.switch("bg_color", value=bg_color)
            rxui.switch("has_error", value=has_error)
            rxui.label("bind to ref_computed").bind_classes(class_obj)

        # binding to list
        def bind_to_list():
            bg_color = to_ref("red")
            bg_color_class = ref_computed(lambda: f"bg-{bg_color.value}")

            text_color = to_ref("green")
            text_color_class = ref_computed(lambda: f"text-{text_color.value}")

            rxui.select(["red", "green", "yellow"], label="bg color", value=bg_color)
            rxui.select(
                ["red", "green", "yellow"], label="text color", value=text_color
            )

            rxui.label("binding to arrays").bind_classes(
                [bg_color_class, text_color_class]
            )

        binding_to_dict()
        bind_to_ref_computed()
        bind_to_list()

    page.open(page_path)

    target = SelectUtils(page, "target")

    expect(target.page.get_by_text("test select", exact=True)).to_be_visible()
