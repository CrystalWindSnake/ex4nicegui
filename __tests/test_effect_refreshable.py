import asyncio
from nicegui import ui
from ex4nicegui import to_ref, effect_refreshable, rxui
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        v1 = to_ref("v1")
        v2 = to_ref("v2")

        rxui.input(value=v1).classes("input-v1")
        rxui.input(value=v2).classes("input-v2")

        @effect_refreshable
        def _():
            ui.label(text=v1.value).classes("label-v1")
            ui.label(text=v2.value).classes("label-v2")

    page = browser.open(page_path)

    input1 = page.Input(".input-v1")
    input2 = page.Input(".input-v2")
    label1 = page.Label(".label-v1")
    label2 = page.Label(".label-v2")

    label1.expect_contain_text("v1")
    label2.expect_contain_text("v2")

    input1.fill_text("new1")
    label1.expect_contain_text("new1")

    input2.fill_text("new2")
    label2.expect_contain_text("new2")


def test_on_method_should_tracked_ref_only(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        v1 = to_ref("v1")
        v2 = to_ref("v2")

        rxui.input(value=v1).classes("input-v1")
        rxui.input(value=v2).classes("input-v2")

        @effect_refreshable.on(v1)
        def _():
            ui.label(text=v1.value).classes("label-v1")
            ui.label(text=v2.value).classes("label-v2")

    page = browser.open(page_path)

    input1 = page.Input(".input-v1")
    input2 = page.Input(".input-v2")
    label1 = page.Label(".label-v1")
    label2 = page.Label(".label-v2")

    label1.expect_contain_text("v1")
    label2.expect_contain_text("v2")

    #
    input2.fill_text("new2")
    label2.expect_not_to_contain_text("new2")

    input1.fill_text("new1")
    label1.expect_contain_text("new1")
    label2.expect_contain_text("new2")


def test_on_method_diff_type(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        v1 = to_ref("v1")
        v2 = "v2"

        def v3():
            return "v3"

        def v4():
            return f"v4+{v1.value}"

        rxui.input(value=v1).classes("input-v1")

        @effect_refreshable.on([v1, v2, v3, v4])
        def all():
            ui.label(text=v1.value).classes("label-v1")
            ui.label(text=v2).classes("label-v2")
            ui.label(text=v3()).classes("label-v3")
            ui.label(text=v4()).classes("label-v4")

        @effect_refreshable.on([v2, v3, v4])
        def exclude_v1():
            ui.label(text=v2)
            ui.label(text=v3())
            ui.label(text=v4()).classes("step-v4")

    page = browser.open(page_path)

    input1 = page.Input(".input-v1")
    label1 = page.Label(".label-v1")
    label2 = page.Label(".label-v2")
    label3 = page.Label(".label-v3")
    label4 = page.Label(".label-v4")
    label4_step = page.Label(".step-v4")

    label1.expect_contain_text("v1")
    label2.expect_contain_text("v2")
    label3.expect_contain_text("v3")
    label4.expect_contain_text("v4+v1")
    label4_step.expect_contain_text("v4+v1")

    #
    input1.fill_text("new1")

    label1.expect_contain_text("new1")
    label4.expect_contain_text("v4+new1")

    label4_step.expect_contain_text("v4+new1")


def test_async_on(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        count = rxui.var(0)

        def plus_one():
            count.value += 1

        async def long_running_zone(count: int):
            await asyncio.sleep(0.5)
            ui.label(f"count: {count}").classes("label-count")

        # ui
        ui.button(text="click me", on_click=plus_one).classes("btn-plus")

        @effect_refreshable.on(count)
        async def _():
            await long_running_zone(int(count.value))

    page = browser.open(page_path)
    button = page.Button(".btn-plus")
    label = page.Label(".label-count")

    label.expect_equal_text("count: 0")
    button.click()
    label.expect_contain_text("count: 1")
    button.click()
    label.expect_contain_text("count: 2")
