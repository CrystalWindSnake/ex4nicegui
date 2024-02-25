from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, ref_computed
from .screen import ScreenPage
from .utils import SelectUtils, SwitchUtils, LabelUtils, set_test_id


def test_bind_classes(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        # binding to dict
        # can have multiple classes toggled
        def binding_to_dict():
            bg_color = to_ref(False)
            has_error = to_ref(False)

            test_prefix = "test1"

            set_test_id(
                rxui.switch("bg_color", value=bg_color),
                f"{test_prefix}_switch1",
            )
            set_test_id(
                rxui.switch("has_error", value=has_error),
                f"{test_prefix}_switch2",
            )

            set_test_id(
                rxui.label("test").bind_classes(
                    {"bg-blue": bg_color, "text-red": lambda: has_error.value}
                ),
                f"{test_prefix}_label",
            )

        # can also bind to a ref_computed
        def bind_to_ref_computed_or_fn():
            bg_color = to_ref(False)
            has_error = to_ref(False)

            class_obj = ref_computed(
                lambda: {"bg-blue": bg_color.value, "text-red": has_error.value}
            )

            test_prefix = "test2"

            set_test_id(
                rxui.switch("bg_color", value=bg_color),
                f"{test_prefix}_switch1",
            )
            set_test_id(
                rxui.switch("has_error", value=has_error),
                f"{test_prefix}_switch2",
            )

            set_test_id(
                rxui.label("bind to ref_computed").bind_classes(class_obj),
                f"{test_prefix}_label",
            )

            set_test_id(
                rxui.label("bind to fn").bind_classes(
                    lambda: {"bg-blue": bg_color.value, "text-red": has_error.value}
                ),
                f"{test_prefix}_label_fn",
            )

        # binding to list
        def bind_to_list():
            bg_color = to_ref("red")
            bg_color_class = ref_computed(lambda: f"bg-{bg_color.value}")

            text_color = to_ref("green")
            text_color_class = ref_computed(lambda: f"text-{text_color.value}")

            test_prefix = "test3"

            set_test_id(
                rxui.select(
                    ["red", "green", "yellow"], label="bg color", value=bg_color
                ),
                f"{test_prefix}_select1",
            )

            set_test_id(
                rxui.select(
                    ["red", "green", "yellow"], label="text color", value=text_color
                ),
                f"{test_prefix}_select2",
            )

            set_test_id(
                rxui.label("binding to arrays").bind_classes(
                    [bg_color_class, lambda: text_color_class.value]
                ),
                f"{test_prefix}_label",
            )

        binding_to_dict()
        bind_to_ref_computed_or_fn()
        bind_to_list()

    page.open(page_path)
    page.wait()

    def test1():
        test_prefix = "test1"
        switch1 = SwitchUtils(page, f"{test_prefix}_switch1")
        switch2 = SwitchUtils(page, f"{test_prefix}_switch2")
        label = LabelUtils(page, f"{test_prefix}_label")

        label.expect_not_to_have_class("bg-red text-green")
        switch1.click()

        label.expect_to_have_class(["bg-blue"])

        switch2.click()
        label.expect_to_have_class("bg-blue text-red")

    test1()

    def test2():
        test_prefix = "test2"
        switch1 = SwitchUtils(page, f"{test_prefix}_switch1")
        switch2 = SwitchUtils(page, f"{test_prefix}_switch2")
        label = LabelUtils(page, f"{test_prefix}_label")
        label_fn = LabelUtils(page, f"{test_prefix}_label_fn")

        label.expect_not_to_have_class("bg-red text-green")
        label_fn.expect_not_to_have_class("bg-red text-green")
        switch1.click()

        label.expect_to_have_class("bg-blue")
        label_fn.expect_to_have_class("bg-blue")

        switch2.click()
        label.expect_to_have_class("bg-blue text-red")
        label_fn.expect_to_have_class("bg-blue text-red")

    test2()

    def test3():
        test_prefix = "test3"
        select1 = SelectUtils(page, f"{test_prefix}_select1")
        select2 = SelectUtils(page, f"{test_prefix}_select2")
        label = LabelUtils(page, f"{test_prefix}_label")

        label.expect_to_have_class("bg-red text-green")

        #
        select1.click_and_select("green")

        label.expect_not_to_have_class("bg-red")
        label.expect_to_have_class("text-green bg-green")

        #
        select2.click_and_select("yellow")

        label.expect_not_to_have_class("text-green")
        label.expect_to_have_class("bg-green text-yellow")

    test3()


def test_bind_style(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        # binding to dict
        def binding_to_dict():
            bg_color = to_ref("blue")
            text_color = to_ref("red")

            test_prefix = "binding_to_dict"

            set_test_id(
                rxui.select(
                    ["blue", "green", "yellow"], label="bg color", value=bg_color
                ),
                f"{test_prefix}_select1",
            )

            set_test_id(
                rxui.select(
                    ["red", "green", "yellow"], label="text color", value=text_color
                ),
                f"{test_prefix}_select2",
            )
            set_test_id(
                rxui.label("test").bind_style(
                    {
                        "background-color": lambda: bg_color.value,
                        "color": text_color,
                    }
                ),
                f"{test_prefix}_label",
            )

        binding_to_dict()

    page.open(page_path)
    page.wait()

    def test_binding_to_dict():
        test_prefix = "binding_to_dict"
        select1 = SelectUtils(page, f"{test_prefix}_select1")
        select2 = SelectUtils(page, f"{test_prefix}_select2")
        label = LabelUtils(page, f"{test_prefix}_label")

        assert label.get_style_attr_value() == "background-color: blue; color: red;"

        #
        select1.click_and_select("green")
        page.wait()

        assert label.get_style_attr_value() == "background-color: green; color: red;"

        #
        select2.click_and_select("yellow")
        page.wait()

        assert label.get_style_attr_value() == "background-color: green; color: yellow;"

    test_binding_to_dict()
