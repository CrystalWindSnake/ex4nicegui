from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import ScreenPage
from playwright.sync_api import expect


def test_const_value(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.date("2023-01-01")

    page.open(page_path)

    page.should_contain("2023")
    page.should_contain("Sun, Jan 1")


def test_const_range_value(page: ScreenPage, page_path: str):
    @ui.page(page_path)
    def _():
        rxui.date([{"from": "2023-01-01", "to": "2023-01-06"}, "2023-01-10"])  # type: ignore

    page.open(page_path)

    page.should_contain("Jan 2023")
    page.should_contain("7 days")


def test_ref_value(page: ScreenPage, page_path: str):
    r_value = to_ref("2023-01-01")

    @ui.page(page_path)
    def _():
        rxui.date(r_value)

    page.open(page_path)

    page.should_contain("2023")
    page.should_contain("Sun, Jan 1")


def test_ref_range_value(page: ScreenPage, page_path: str):
    r_value = to_ref([{"from": "2023-01-01", "to": "2023-01-06"}, "2023-01-10"])

    @ui.page(page_path)
    def _():
        rxui.date(r_value)  # type: ignore

    page.open(page_path)

    page.should_contain("Jan 2023")
    page.should_contain("7 days")


def test_ref_change_value(page: ScreenPage, page_path: str):
    single_date_id = "single"
    range_date_id = "range"

    r_single_value = to_ref("2023-01-01")
    r_range_value = to_ref([{"from": "2023-01-01", "to": "2023-01-06"}])

    @ui.page(page_path)
    def _():
        rxui.date(r_single_value).props(f'data-testid="{single_date_id}"')
        rxui.date(r_range_value).props(f'data-testid="{range_date_id}" multiple range')  # type: ignore

    page.open(page_path)

    single_date = page.get_by_test_id(single_date_id)
    range_date = page.get_by_test_id(range_date_id)

    expect(single_date.get_by_text("Sun, Jan 1").first).to_be_visible()
    page.wait()
    r_single_value.value = "2023-01-02"
    expect(single_date.get_by_text("Mon, Jan 2").first).to_be_visible()

    expect(range_date.get_by_text("6 days").first).to_be_visible()
    page.wait()
    r_range_value.value = [
        {"from": "2023-01-06", "to": "2023-01-10"},
        {"from": "2023-01-15", "to": "2023-01-16"},
        "2023-01-12",  # type: ignore
    ]
    expect(range_date.get_by_text("8 days").first).to_be_visible()
