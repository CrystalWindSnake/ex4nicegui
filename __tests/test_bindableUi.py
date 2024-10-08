from pathlib import Path
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, ref_computed
from .screen import BrowserManager
from playwright.sync_api import expect
from .utils import fn


def test_bind_classes(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        # binding to dict
        # can have multiple classes toggled
        def binding_to_dict():
            bg_color = to_ref(False)
            has_error = to_ref(False)

            test_prefix = "test1"

            rxui.switch("bg_color", value=bg_color).classes(f"{test_prefix}_switch1")
            rxui.switch("has_error", value=has_error).classes(f"{test_prefix}_switch2")
            rxui.label("test").bind_classes(
                {"bg-blue": bg_color, "text-red": lambda: has_error.value}
            ).classes(f"{test_prefix}_label")

        # can also bind to a ref_computed
        def bind_to_ref_computed_or_fn():
            bg_color = to_ref(False)
            has_error = to_ref(False)

            class_obj = ref_computed(
                lambda: {"bg-blue": bg_color.value, "text-red": has_error.value}
            )

            test_prefix = "test2"

            rxui.switch("bg_color", value=bg_color).classes(f"{test_prefix}_switch1")
            rxui.switch("has_error", value=has_error).classes(f"{test_prefix}_switch2")
            rxui.label("bind to ref_computed").bind_classes(class_obj).classes(
                f"{test_prefix}_label"
            )
            rxui.label("bind to fn").bind_classes(
                lambda: {"bg-blue": bg_color.value, "text-red": has_error.value}
            ).classes(f"{test_prefix}_label_fn")

        # binding to list
        def bind_to_list():
            bg_color = to_ref("red")
            bg_color_class = ref_computed(lambda: f"bg-{bg_color.value}")

            text_color = to_ref("green")
            text_color_class = ref_computed(lambda: f"text-{text_color.value}")

            test_prefix = "test3"
            rxui.select(
                ["red", "green", "yellow"], label="bg color", value=bg_color
            ).classes(f"{test_prefix}_select1")

            rxui.select(
                ["red", "green", "yellow"], label="text color", value=text_color
            ).classes(f"{test_prefix}_select2")

            rxui.label("binding to arrays").bind_classes(
                [bg_color_class, lambda: text_color_class.value]
            ).classes(f"{test_prefix}_label")

        def bind_single_class():
            bg_color = to_ref("red")
            bg_color_class = ref_computed(lambda: f"bg-{bg_color.value}")

            test_prefix = "test4"
            rxui.select(
                ["red", "green", "yellow"], label="bg color", value=bg_color
            ).classes(f"{test_prefix}_select1")

            rxui.label("hello").bind_classes(bg_color_class).classes(
                f"{test_prefix}_label"
            )

        binding_to_dict()
        bind_to_ref_computed_or_fn()
        bind_to_list()
        bind_single_class()

    page = browser.open(page_path)

    def test1():
        test_prefix = "test1"
        switch1 = page.Switch(f".{test_prefix}_switch1")
        switch2 = page.Switch(f".{test_prefix}_switch2")
        label = page.Label(f".{test_prefix}_label")

        label.expect_not_to_contain_class("bg-red", "text-green")
        switch1.click()

        label.expect_to_contain_class("bg-blue")

        switch2.click()
        label.expect_to_contain_class("bg-blue", "text-red")

    test1()

    def test2():
        test_prefix = "test2"
        switch1 = page.Switch(f".{test_prefix}_switch1")
        switch2 = page.Switch(f".{test_prefix}_switch2")
        label = page.Label(f".{test_prefix}_label")
        label_fn = page.Label(f".{test_prefix}_label_fn")

        label.expect_not_to_contain_class("bg-red", "text-green")
        label_fn.expect_not_to_contain_class("bg-red", "text-green")
        switch1.click()

        label.expect_to_contain_class("bg-blue")
        label_fn.expect_to_contain_class("bg-blue")

        switch2.click()
        label.expect_to_contain_class("bg-blue", "text-red")
        label_fn.expect_to_contain_class("bg-blue", "text-red")

    test2()

    def test3():
        test_prefix = "test3"
        select1 = page.Select(f".{test_prefix}_select1")
        select2 = page.Select(f".{test_prefix}_select2")
        label = page.Label(f".{test_prefix}_label")

        label.expect_to_contain_class("bg-red", "text-green")

        #
        select1.click_and_select("green")

        label.expect_not_to_contain_class("bg-red")
        label.expect_to_contain_class("bg-green", "text-green")

        #
        select2.click_and_select("yellow")

        label.expect_not_to_contain_class("text-green")
        label.expect_to_contain_class("bg-green", "text-yellow")

    test3()

    def test4():
        test_prefix = "test4"
        select1 = page.Select(f".{test_prefix}_select1")
        label = page.Label(f".{test_prefix}_label")

        label.expect_to_contain_class("bg-red")

        #
        select1.click_and_select("green")

        label.expect_not_to_contain_class("bg-red")
        label.expect_to_contain_class("bg-green")

    test4()


def test_bind_style(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        # binding to dict
        def binding_to_dict():
            bg_color = to_ref("blue")
            text_color = to_ref("red")

            test_prefix = "binding_to_dict"

            rxui.select(
                ["blue", "green", "yellow"], label="bg color", value=bg_color
            ).classes(f"{test_prefix}_select1")
            rxui.select(
                ["red", "green", "yellow"], label="text color", value=text_color
            ).classes(f"{test_prefix}_select2")

            rxui.label("test").bind_style(
                {
                    "background-color": lambda: bg_color.value,
                    "color": text_color,
                }
            ).classes(f"{test_prefix}_label")

        binding_to_dict()

    page = browser.open(page_path)

    def test_binding_to_dict():
        test_prefix = "binding_to_dict"
        select1 = page.Select(f".{test_prefix}_select1")
        select2 = page.Select(f".{test_prefix}_select2")
        label = page.Label(f".{test_prefix}_label")

        label.expect_to_have_style("background-color", "rgb(0, 0, 255)")
        label.expect_to_have_style("color", "rgb(255, 0, 0)")

        #
        select1.click_and_select("green")

        label.expect_to_have_style("background-color", "rgb(0, 128, 0)")
        label.expect_to_have_style("color", "rgb(255, 0, 0)")

        #
        select2.click_and_select("yellow")
        label.expect_to_have_style("background-color", "rgb(0, 128, 0)")
        label.expect_to_have_style("color", "rgb(255, 255, 0)")

    test_binding_to_dict()


def test_bind_prop(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        label = to_ref("hello")

        rxui.element("div").props('innerText="target1"').bind_prop("prop", label)
        rxui.element("div").props('innerText="target2"').bind_prop(
            "prop", lambda: f"{label.value} world"
        )

        rxui.input(value=label)

    page = browser.open(page_path)

    pw_page = page._page

    target1 = pw_page.get_by_text("target1")
    target2 = pw_page.get_by_text("target2")
    input = pw_page.get_by_role("textbox")

    expect(target1).to_have_attribute("prop", "hello")
    expect(target2).to_have_attribute("prop", "hello world")

    input.fill("hello foo")

    expect(target1).to_have_attribute("prop", "hello foo")
    expect(target2).to_have_attribute("prop", "hello foo world")


def test_bind_props(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        label = to_ref("hello")
        bool_prop = to_ref(False)

        def get_props_str():
            return f'prop="{label.value}"'

        rxui.element("div").props('innerText="target1"').bind_props(get_props_str)
        rxui.element("div").props('innerText="target2"').bind_props(
            {
                "prop": label,
                "bool-prop": bool_prop,
            }
        )

        rxui.input(value=label).classes("input")
        rxui.checkbox(value=bool_prop).classes("checkbox")

    page = browser.open(page_path)
    pw_page = page._page

    target1 = pw_page.get_by_text("target1")
    target2 = pw_page.get_by_text("target2")
    input = page.Input(".input")
    checkbox = page.Checkbox(".checkbox")

    expect(target1).to_have_attribute("prop", "hello")
    expect(target2).to_have_attribute("prop", "hello")
    expect(target2).not_to_have_attribute("bool-prop", "")

    input.fill_text("hello foo")
    checkbox.click()

    expect(target1).to_have_attribute("prop", "hello foo")
    expect(target2).to_have_attribute("prop", "hello foo")
    expect(target2).to_have_attribute("bool-prop", "true")


def test_handle_delete(browser: BrowserManager, page_path: str):
    @fn
    def caller():
        pass

    class MyElement(rxui.element):
        def __init__(self) -> None:
            super().__init__("div")
            self.classes("w-[100px] h-[100px] bg-gray-200")

        def _on_element_delete(self):
            caller()
            return super()._on_element_delete()

    @ui.page(page_path)
    def _():
        element = MyElement()
        ui.button("delete", on_click=element.delete).classes("delete")

    page = browser.open(page_path)

    delete_btn = page.Button(".delete")
    delete_btn.click()

    assert caller.calledTimes == 1


def test_effect_dispose_after_element_delete(browser: BrowserManager, page_path: str):
    class MyElement(rxui.element):
        def __init__(self, ref, other) -> None:
            super().__init__("div")
            self.classes("w-[100px] h-[100px] bg-gray-200")

            @self._ui_effect
            def _():
                other.value = "other " + ref.value

    @ui.page(page_path)
    def _():
        org = to_ref("a")
        other = to_ref("")

        rxui.input(value=org).classes("input")
        element = MyElement(org, other)

        rxui.label(org).classes("org")
        rxui.label(other).classes("other")

        ui.button("delete", on_click=element.delete).classes("delete")

    page = browser.open(page_path)
    delete_btn = page.Button(".delete")
    input = page.Input(".input")
    org_label = page.Label(".org")
    other_label = page.Label(".other")

    input.input_text("x")
    delete_btn.click()

    input.input_text("x")

    org_label.expect_contain_text("axx")
    other_label.expect_equal_text("other ax")


class TestScopedStyle:
    async def _get_style_content(self, element: ui.element, split_lines=False):
        if split_lines:
            return await ui.run_javascript(
                rf"""
                const target = document.querySelector('style.ex4ng-scoped-style-c{element.id}');
                if (!target) return "";
                return target.innerHTML.split(/\n/);
                """
            )

        return await ui.run_javascript(
            rf"""
            const target = document.querySelector('style.ex4ng-scoped-style-c{element.id}');
            if (!target) return "";
            return target.innerHTML;
            """
        )

    def test_scoped_style(self, browser: BrowserManager, page_path: str):
        style_content = ""

        @ui.page(page_path)
        def _():
            nonlocal style_content

            style = r"background-color: red"

            with rxui.row().scoped_style("div", style) as row:
                ui.label("Hello")

            result = ui.label("").classes("result")

            async def get_style_content():
                content = await self._get_style_content(row.element)
                result.set_text(content)

            ui.button("get style content", on_click=get_style_content).classes(
                "get-style"
            )
            ui.button("del element", on_click=row.delete).classes("del-element")

            style_content = rf"#c{row.element.id} div{{{style}}}"

        page = browser.open(page_path)

        get_style_btn = page.Button(".get-style")
        del_element_btn = page.Button(".del-element")
        result_label = page.Label(".result")

        get_style_btn.click()
        result_label.expect_contain_text(style_content)

        del_element_btn.click()
        result_label.expect_contain_text("")

    def test_with_hover_selector(self, browser: BrowserManager, page_path: str):
        style_content = ""

        @ui.page(page_path)
        def _():
            nonlocal style_content

            style = r"background-color: red"

            with rxui.row().scoped_style(":hover > *", style) as row:
                ui.label("Hello")

            result = ui.label("").classes("result")

            async def get_style_content():
                content = await self._get_style_content(row.element)
                result.set_text(content)

            ui.button("get style content", on_click=get_style_content).classes(
                "get-style"
            )
            ui.button("del element", on_click=row.delete).classes("del-element")

            style_content = rf"#c{row.element.id}:hover > *{{{style}}}"

        page = browser.open(page_path)

        get_style_btn = page.Button(".get-style")
        del_element_btn = page.Button(".del-element")
        result_label = page.Label(".result")

        get_style_btn.click()
        result_label.expect_contain_text(style_content)

        del_element_btn.click()
        result_label.expect_contain_text("")

    def test_by_css_file(self, browser: BrowserManager, page_path: str):
        style_content = ""

        @ui.page(page_path)
        def _():
            nonlocal style_content

            style_file = Path(__file__).parent / "files/scoped_style.css"

            with rxui.row().scoped_style(":hover", style_file) as row:
                ui.label("Hello")

            result = ui.label("").classes("result")

            async def get_style_content():
                content = await self._get_style_content(row.element)
                result.set_text(content)

            ui.button("get style content", on_click=get_style_content).classes(
                "get-style"
            )

            style_content = rf"#c{row.element.id}:hover * {{background-color: red;}}"

        page = browser.open(page_path)

        get_style_btn = page.Button(".get-style")
        result_label = page.Label(".result")

        get_style_btn.click()
        result_label.expect_contain_text(style_content)

    def test_multiple_call(self, browser: BrowserManager, page_path: str):
        style_content = ""

        @ui.page(page_path)
        def _():
            nonlocal style_content

            style1 = r"background-color: blue;"
            style2 = r"border: 1px solid red;"

            with rxui.row().scoped_style(":hover > *", style1).scoped_style(
                ".target", style2
            ) as row:
                ui.label("Hello").classes("target")

            result = ui.label("").classes("result")

            async def get_style_content():
                content = await self._get_style_content(row.element, split_lines=True)
                result.set_text(str(content))

            ui.button("get style content", on_click=get_style_content).classes(
                "get-style"
            )

            style_content = [
                rf"#c{row.element.id}:hover > *{{{style1}}}",
                rf"#c{row.element.id} .target{{{style2}}}",
            ]

            style_content = str(style_content)

        page = browser.open(page_path)

        get_style_btn = page.Button(".get-style")
        result_label = page.Label(".result")

        get_style_btn.click()
        result_label.expect_contain_text(style_content)

    def test_with_self(self, browser: BrowserManager, page_path: str):
        style_content = ""

        @ui.page(page_path)
        def _():
            nonlocal style_content

            style = r"border: 1px solid red;"

            with rxui.row().scoped_style(":self", style) as row:
                ui.label("Hello")

            result = ui.label("").classes("result")

            async def get_style_content():
                content = await self._get_style_content(row.element)
                result.set_text(content)

            ui.button("get style content", on_click=get_style_content).classes(
                "get-style"
            )

            style_content = rf"#c{row.element.id},#c{row.element.id} {{{style}}}"

        page = browser.open(page_path)

        get_style_btn = page.Button(".get-style")
        result_label = page.Label(".result")

        get_style_btn.click()
        result_label.expect_contain_text(style_content)

    def test_with_self_and_hover(self, browser: BrowserManager, page_path: str):
        style_content = ""

        @ui.page(page_path)
        def _():
            nonlocal style_content

            style = r"outline: 1px solid red;"

            with rxui.row().scoped_style(":self:hover *", style) as row:
                ui.label("Hello")

            result = ui.label("").classes("result")

            async def get_style_content():
                content = await self._get_style_content(row.element)
                result.set_text(content)

            ui.button("get style content", on_click=get_style_content).classes(
                "get-style"
            )

            style_content = (
                rf"#c{row.element.id}:hover,#c{row.element.id}:hover *{{{style}}}"
            )

        page = browser.open(page_path)

        get_style_btn = page.Button(".get-style")
        result_label = page.Label(".result")

        get_style_btn.click()
        result_label.expect_contain_text(style_content)
