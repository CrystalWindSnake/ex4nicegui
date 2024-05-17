from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager
from playwright.sync_api import expect

target_test_id = "switch"


def test_const_value(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.switch(value=False).props(f'data-testid="{target_test_id}"')

    page = browser.open(page_path)

    switch = page.get_by_test_id(target_test_id)

    expect(switch).to_be_visible()
    expect(switch).not_to_be_checked()

    page.wait()
    page._page.get_by_test_id("switch").locator("div").nth(2).click()
    page.wait()
    expect(switch).to_be_checked()


def test_ref_value(browser: BrowserManager, page_path: str):
    r_on = to_ref(False)

    @ui.page(page_path)
    def _():
        rxui.switch(value=r_on).props(f'data-testid="{target_test_id}"')

    page = browser.open(page_path)
    switch = page.get_by_test_id(target_test_id)

    expect(switch).to_be_visible()
    expect(switch).not_to_be_checked()
    assert r_on.value is False

    page.wait()
    page._page.get_by_test_id("switch").locator("div").nth(2).click()
    page.wait()
    expect(switch).to_be_checked()
    assert r_on.value is True


def test_ref_str_change_value(browser: BrowserManager, page_path: str):
    r_on = to_ref(False)

    @ui.page(page_path)
    def _():
        rxui.switch(value=r_on).props(f'data-testid="{target_test_id}"')

    page = browser.open(page_path)
    switch = page.get_by_test_id(target_test_id)

    expect(switch).to_be_visible()
    expect(switch).not_to_be_checked()

    page.wait()
    r_on.value = True

    page.wait()
    expect(switch).to_be_checked()
