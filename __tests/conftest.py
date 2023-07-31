import importlib
import pytest
import logging
from playwright.sync_api import Browser, Playwright
from .screen import Screen, ScreenPage
from nicegui import Client, globals
from nicegui.page import page as ui_page


@pytest.fixture(autouse=True)
def reset_globals(request: pytest.FixtureRequest):
    if "noautofixt" in request.keywords:
        return

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
    globals.index_client = Client(ui_page("/"), shared=True).__enter__()
    globals.app.get("/")(globals.index_client.build_response)


@pytest.fixture(scope="module")
def screen(playwright: Playwright, request: pytest.FixtureRequest):
    if "noautofixt" in request.keywords:
        return
    browser = playwright.chromium.launch()
    screen = Screen(browser)

    yield screen

    screen.stop_server()


@pytest.fixture(scope="function")
def page(screen: Screen, request: pytest.FixtureRequest):
    if "noautofixt" in request.keywords:
        return
    test_page = screen.new_page()

    yield test_page

    test_page.close()


URL_COUNTER = 0


@pytest.fixture
def page_path(request: pytest.FixtureRequest):
    if "noautofixt" in request.keywords:
        return
    global URL_COUNTER
    URL_COUNTER += 1

    return f"/{URL_COUNTER}"
