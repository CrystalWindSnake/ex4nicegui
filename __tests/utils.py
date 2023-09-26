from __future__ import annotations

from typing import Optional
from playwright.sync_api import Page
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
