from __future__ import annotations

from typing import Optional
from playwright.sync_api import expect
from .screen import ScreenPage
from nicegui import ui
from typing_extensions import Protocol, Self

ui.element().props


class IPropsAble(Protocol):
    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None) -> Self:
        ...


def set_test_id(element: IPropsAble, id: str):
    return element.props(f'data-testid="{id}"')


class SelectUtils:
    def __init__(self, screen_page: ScreenPage, test_id: str) -> None:
        self.page = screen_page._page
        self.test_id = test_id
        self.target_locator = self.page.get_by_test_id(test_id)

    def click(self):
        self.target_locator.click()

    def get_selection_values(self):
        return self.page.locator(
            "css= .q-menu.q-position-engine.scroll > .q-virtual-scroll__content > * "
        ).all_inner_texts()

    def click_cancel(self):
        self.page.get_by_role("button", name="cancel").click()

    def click_and_select(self, value: str):
        # .locator("div").nth(2)
        self.click()
        self.page.get_by_role("option", name=value).click()


class RadioUtils:
    def __init__(self, screen_page: ScreenPage, test_id: str) -> None:
        self.page = screen_page._page
        self.test_id = test_id
        self.target_locator = self.page.get_by_test_id(test_id)

    def expect_to_be_visible(self):
        expect(self.target_locator).to_be_visible()

    def is_checked_by_label(self, label: str):
        return self.target_locator.get_by_label(label).is_checked()

    def check_by_label(self, label: str):
        # self.target_locator.click(f"text={label}")

        self.target_locator.get_by_label(label).click()
        return


class EChartsUtils:
    def __init__(self, screen_page: ScreenPage, test_id: str) -> None:
        self.page = screen_page._page
        self.test_id = test_id
        self.target_locator = self.page.get_by_test_id(test_id)

    def assert_chart_exists(self):
        attr = self.target_locator.get_attribute("_echarts_instance_")
        assert attr is not None

    def get_options(self):
        opts = self.target_locator.evaluate(
            f"node => echarts.getInstanceByDom(node).getOption()"
        )

        return opts
