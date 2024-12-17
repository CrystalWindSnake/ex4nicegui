import asyncio
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, async_computed, effect_refreshable
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        async def long_time_query(input: str):
            await asyncio.sleep(1)
            return f"task done {input}"

        search = to_ref("")
        evaluating = to_ref(False)

        @async_computed(search, evaluating=evaluating, init="")
        async def search_result():
            return await long_time_query(search.value)

        rxui.input(value=search).classes("input")

        rxui.label(
            lambda: "loading" if evaluating.value else "plase enter something"
        ).classes("loading")
        rxui.label(search_result).classes("result")

    page = browser.open(page_path)

    input = page.Input(".input")
    loading = page.Label(".loading")
    result = page.Label(".result")

    loading.expect_to_have_text("plase enter something")
    input.fill_text("hello")

    loading.expect_to_have_text("loading")
    result.expect_to_have_text("task done hello")
    loading.expect_to_have_text("plase enter something")


def test_with_refreshable(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        async def long_time_query(input: str):
            await asyncio.sleep(1)
            return f"task done {input}"

        search = to_ref("init")
        evaluating = to_ref(False)

        @async_computed(search, evaluating=evaluating, init="", onchanges=False)
        async def search_result():
            return await long_time_query(search.value)

        rxui.input(value=search).classes("input")

        @effect_refreshable.on([search_result, evaluating])
        def _():
            if evaluating.value:
                ui.label("loading")
                return
            ui.label(search_result.value)

    page = browser.open(page_path)

    input = page.Input(".input")

    page.should_contain("loading")

    page.should_contain("task done init")

    input.fill_text("hello")

    page.should_contain("task done hello")
