from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_const_data(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        page_size = 10
        data = list(range(105))
        pagination = rxui.use_pagination(data, page_size)
        rxui.label(pagination.current_source).classes("result")
        rxui.button("next", on_click=pagination.next).classes("btn-next")

    page = browser.open(page_path)
    lbl_result = page.Label(".result")
    btn_next = page.Button(".btn-next")

    lbl_result.expect_contain_text("[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]")

    btn_next.click(click_count=9)

    lbl_result.expect_contain_text("[90, 91, 92, 93, 94, 95, 96, 97, 98, 99]")

    btn_next.click()
    lbl_result.expect_contain_text("[100, 101, 102, 103, 104]")


def test_set_current_page(browser: BrowserManager, page_path: str):
    values = iter([1, 10, 11])

    @ui.page(page_path)
    def _():
        r_cur_page = to_ref(2)
        page_size = 10
        data = list(range(105))

        pagination = rxui.use_pagination(data, page_size, r_cur_page)
        rxui.label(pagination.current_source).classes("result")
        ui.button("change current page").on_click(
            lambda: r_cur_page.set_value(next(values))
        ).classes("btn-change-page")

    page = browser.open(page_path)
    lbl_result = page.Label(".result")
    btn_change_page = page.Button(".btn-change-page")

    lbl_result.expect_contain_text("[10, 11, 12, 13, 14, 15, 16, 17, 18, 19]")

    btn_change_page.click()
    lbl_result.expect_contain_text("[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]")

    btn_change_page.click()
    lbl_result.expect_contain_text("[90, 91, 92, 93, 94, 95, 96, 97, 98, 99]")

    btn_change_page.click()
    lbl_result.expect_contain_text("[100, 101, 102, 103, 104]")


def test_set_current_page_over_max_size(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_cur_page = to_ref(12)
        page_size = 10
        data = list(range(105))

        pagination = rxui.use_pagination(data, page_size, r_cur_page)
        rxui.label(pagination.current_source).classes("result")
        ui.button("change current page").on_click(
            lambda: r_cur_page.set_value(0)
        ).classes("btn-change-page")

    page = browser.open(page_path)
    lbl_result = page.Label(".result")
    btn_change_page = page.Button(".btn-change-page")

    lbl_result.expect_contain_text("[100, 101, 102, 103, 104]")

    btn_change_page.click()
    lbl_result.expect_contain_text("[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]")


def test_first_last_page(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        r_cur_page = to_ref(12)
        page_size = 10
        data = list(range(105))

        pagination = rxui.use_pagination(data, page_size, r_cur_page)
        rxui.label(pagination.is_first_page).classes("is-first-page")
        rxui.label(pagination.is_last_page).classes("is-last-page")
        ui.button("change current page").on_click(
            lambda: r_cur_page.set_value(0)
        ).classes("btn-change-page")

    page = browser.open(page_path)
    lbl_is_first_page = page.Label(".is-first-page")
    lbl_is_last_page = page.Label(".is-last-page")
    btn_change_page = page.Button(".btn-change-page")

    lbl_is_first_page.expect_contain_text("False")
    lbl_is_last_page.expect_contain_text("True")

    btn_change_page.click()
    lbl_is_first_page.expect_contain_text("True")
    lbl_is_last_page.expect_contain_text("False")
