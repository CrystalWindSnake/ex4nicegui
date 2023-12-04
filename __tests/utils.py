from __future__ import annotations

from typing import List, Optional, Any, Callable
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


class fn:
    def __init__(self, fn: Optional[Callable] = None) -> None:
        self._fn = fn
        self._called_count = 0

    def mockClear(self):
        self._called_count = 0
        return self

    @property
    def calledTimes(self):
        return self._called_count

    def toHaveBeenCalled(self):
        return self.calledTimes > 0

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self._fn is None:
            pass
            self._called_count += 1
            return

        assert self._fn is not None
        result = self._fn(*args, **kwds)
        self._called_count += 1

        return result


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
        self.click()
        self.page.get_by_role("option", name=value).click()

    def get_input_value(self):
        return self.target_locator.input_value()


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

    def get_all_labels(self):
        return self.target_locator.locator(".q-radio__label").all_inner_texts()


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


class TableUtils:
    def __init__(self, screen_page: ScreenPage, test_id: str) -> None:
        self.page = screen_page._page
        self.test_id = test_id
        self.target_locator = self.page.get_by_test_id(test_id)

    def expect_cell_to_be_visible(self, cell_values: List):
        for cell_value in cell_values:
            expect(
                self.target_locator.get_by_role("cell", name=cell_value, exact=True)
            ).to_be_visible()

    def expect_cell_not_to_be_visible(self, cell_values: List):
        for cell_value in cell_values:
            expect(
                self.target_locator.get_by_role("cell", name=cell_value, exact=True)
            ).not_to_be_visible()

    def click_checkbox(self, row_values: List):
        name = " ".join((str(d) for d in row_values))
        self.target_locator.get_by_role("row", name=name).get_by_role(
            "checkbox"
        ).click()

    def get_cell_style(self, cell_value: str):
        return self.target_locator.get_by_role(
            "cell", name=cell_value, exact=True
        ).get_attribute("style")


class MermaidUtils:
    def __init__(self, screen_page: ScreenPage, test_id: str) -> None:
        self.page = screen_page._page
        self.test_id = test_id
        self.target_locator = self.page.get_by_test_id(test_id)

    def click_node(self, nodeId: str):
        self.target_locator.get_by_text(nodeId, exact=True).click()


class AggridUtils:
    def __init__(self, screen_page: ScreenPage, test_id: str) -> None:
        self.page = screen_page._page
        self.test_id = test_id
        self.target_locator = self.page.get_by_test_id(test_id)

    def expect_cell_to_be_visible(self, cell_values: List):
        for cell_value in cell_values:
            expect(
                self.target_locator.get_by_role("gridcell", name=cell_value, exact=True)
            ).to_be_visible()

    def expect_selection_cell_to_be_visible(self, cell_values: List):
        for cell_value in cell_values:
            expect(
                self.target_locator.get_by_role("gridcell")
                .locator("div")
                .filter(has_text="a")
            ).to_be_visible()

    def expect_cell_not_to_be_visible(self, cell_values: List):
        for cell_value in cell_values:
            expect(
                self.target_locator.get_by_role("gridcell", name=cell_value, exact=True)
            ).not_to_be_visible()

    def get_rows(
        self,
    ):
        return self.target_locator.locator(".ag-body-viewport").get_by_role("row").all()


class ButtonUtils:
    def __init__(self, screen_page: ScreenPage, test_id: str) -> None:
        self.page = screen_page._page
        self.test_id = test_id
        self.target_locator = self.page.get_by_test_id(test_id)

    def click(self):
        self.target_locator.click()
