import importlib
from typing import Generator
import pytest
import logging
from playwright.sync_api import Page
from .screen import Screen
from nicegui import Client, globals
from nicegui.page import page


@pytest.fixture(autouse=True)
def reset_globals():
    for path in {"/"}.union(globals.page_routes.values()):
        globals.app.remove_route(path)
    globals.app.middleware_stack = None
    globals.app.user_middleware.clear()
    # NOTE favicon routes must be removed separately because they are not "pages"
    [
        globals.app.routes.remove(r)
        for r in globals.app.routes
        if r.path.endswith("/favicon.ico")  # type: ignore
    ]
    importlib.reload(globals)
    globals.app.storage.clear()
    globals.index_client = Client(page("/"), shared=True).__enter__()
    globals.app.get("/")(globals.index_client.build_response)


@pytest.fixture
def screen(page: Page):
    print("beforeEach")

    screen = Screen(page)

    yield screen

    screen.stop_server()
