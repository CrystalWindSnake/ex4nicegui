from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_base(browser: BrowserManager, page_path: str):
    min = to_ref(1)
    max = to_ref(5)
    page_value = to_ref(2)
    direction_links = to_ref(True)

    @ui.page(page_path)
    def _():
        rxui.pagination(
            min, max, direction_links=direction_links, value=page_value
        ).classes("pagination")
        rxui.label(page_value).classes("label")

    page = browser.open(page_path)

    pagination = page.Base(".pagination")
    label_value = page.Label(".label")

    pagination.expect.to_contain_text("keyboard_arrow_left12345keyboard_arrow_right")
    label_value.expect_contain_text("2")

    pagination.target_locator.get_by_role("button").filter(has_text="4").click()
    label_value.expect_contain_text("4")

    min.value = 2
    pagination.expect.to_contain_text("keyboard_arrow_left2345keyboard_arrow_right")

    max.value = 4
    pagination.expect.to_contain_text("keyboard_arrow_left234keyboard_arrow_right")

    direction_links.value = False
    pagination.expect.to_contain_text("234")
