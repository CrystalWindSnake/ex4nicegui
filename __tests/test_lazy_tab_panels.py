import asyncio
from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref, deep_ref
from .screen import BrowserManager, PageUtils


def click_tab(page: PageUtils, tab_name: str):
    page.get_by_role("tab", name=tab_name).locator("div").nth(1).click()


def test_base(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        texts = deep_ref([])

        current_tab = to_ref("t1")
        tabs = ["t1", "t2", "t3"]

        rxui.label(texts).classes("result")

        with rxui.tabs(current_tab):
            for tab in tabs:
                ui.tab(tab)

        with rxui.lazy_tab_panels(current_tab) as panels:
            for tab in tabs:

                @panels.add_tab_panel(tab)
                def _(tab=tab):
                    ui.label(f"panels.{tab}")
                    texts.value.append(f"panels.{tab}")

    page = browser.open(page_path)
    reslut_label = page.Label(".result")

    reslut_label.expect_contain_text("['panels.t1']")

    click_tab(page, "t2")
    reslut_label.expect_contain_text("['panels.t1', 'panels.t2']")

    click_tab(page, "t3")
    reslut_label.expect_contain_text("['panels.t1', 'panels.t2', 'panels.t3']")

    # make sure that content will not be duplicated.
    click_tab(page, "t2")
    reslut_label.expect_contain_text("['panels.t1', 'panels.t2', 'panels.t3']")

    click_tab(page, "t1")
    reslut_label.expect_contain_text("['panels.t1', 'panels.t2', 'panels.t3']")


def test_async(browser: BrowserManager, page_path: str):
    async def long_running_task():
        await asyncio.sleep(0.5)

    @ui.page(page_path)
    def _():
        texts = deep_ref([])

        current_tab = to_ref("t1")
        tabs = ["t1", "t2", "t3"]

        rxui.label(texts).classes("result")

        with rxui.tabs(current_tab):
            for tab in tabs:
                ui.tab(tab)

        with rxui.lazy_tab_panels(current_tab) as panels:
            for tab in tabs:

                @panels.add_tab_panel(tab)
                async def _(tab=tab):
                    ui.label(f"panels.{tab}")
                    await long_running_task()
                    texts.value.append(f"panels.{tab}")

    page = browser.open(page_path)
    reslut_label = page.Label(".result")

    reslut_label.expect_contain_text("['panels.t1']")

    click_tab(page, "t2")
    reslut_label.expect_contain_text("['panels.t1', 'panels.t2']")

    click_tab(page, "t3")
    reslut_label.expect_contain_text("['panels.t1', 'panels.t2', 'panels.t3']")

    # make sure that content will not be duplicated.
    click_tab(page, "t2")
    reslut_label.expect_contain_text("['panels.t1', 'panels.t2', 'panels.t3']")

    click_tab(page, "t1")
    reslut_label.expect_contain_text("['panels.t1', 'panels.t2', 'panels.t3']")


def test_nesting(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        texts = deep_ref([])

        current_tab = to_ref("t1")
        level1_tabs = ["t1", "t2", "t3"]
        level2_tabs = ["x1", "x2", "x3"]

        rxui.label(texts).classes("result")

        with rxui.tabs(current_tab):
            for tab in level1_tabs:
                ui.tab(tab)

        with rxui.lazy_tab_panels(current_tab) as panels:
            for level1_name in level1_tabs:

                @panels.add_tab_panel(level1_name)
                def _(level_name=level1_name):
                    ui.label(f"panels.{level_name}")

                    if level_name == "t2":
                        level2_tab = to_ref("x1")

                        with rxui.tabs(level2_tab):
                            for tab in level2_tabs:
                                ui.tab(tab)

                        with rxui.lazy_tab_panels(level2_tab) as level2_panels:
                            for tab in level2_tabs:

                                @level2_panels.add_tab_panel(tab)
                                def _(tab=tab):
                                    ui.label(f"panels.{level1_name}.{tab}")
                                    texts.value.append(f"panels.{level1_name}.{tab}")

    page = browser.open(page_path)
    reslut_label = page.Label(".result")

    reslut_label.expect_contain_text("[]")

    click_tab(page, "t2")
    reslut_label.expect_contain_text("['panels.t3.x1']")

    click_tab(page, "x2")
    reslut_label.expect_contain_text("['panels.t3.x1', 'panels.t3.x2']")

    click_tab(page, "x3")
    reslut_label.expect_contain_text("['panels.t3.x1', 'panels.t3.x2', 'panels.t3.x3']")

    # make sure that content will not be duplicated.
    click_tab(page, "t3")
    click_tab(page, "t2")
    reslut_label.expect_contain_text("['panels.t3.x1', 'panels.t3.x2', 'panels.t3.x3']")

    click_tab(page, "x2")
    reslut_label.expect_contain_text("['panels.t3.x1', 'panels.t3.x2', 'panels.t3.x3']")

    click_tab(page, "t1")
    reslut_label.expect_contain_text("['panels.t3.x1', 'panels.t3.x2', 'panels.t3.x3']")
