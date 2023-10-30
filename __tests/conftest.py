import importlib
import pytest
from playwright.sync_api import Playwright
from .screen import Screen
from nicegui.page import page as ui_page
from nicegui import Client, binding, app, core
from nicegui.elements import plotly, pyplot
import os

HEADLESS = "GITHUB_ACTION" in os.environ


@pytest.fixture(autouse=True)
def reset_globals(request: pytest.FixtureRequest):
    if "noautofixt" in request.keywords:
        return

    for path in {"/"}.union(Client.page_routes.values()):
        app.remove_route(path)
    app.openapi_schema = None
    app.middleware_stack = None
    app.user_middleware.clear()
    # NOTE favicon routes must be removed separately because they are not "pages"
    for route in app.routes:
        if route.path.endswith("/favicon.ico"):
            app.routes.remove(route)
    # importlib.reload(globals)
    # # repopulate globals.optional_features
    importlib.reload(plotly)
    importlib.reload(pyplot)
    app.storage.clear()
    index_client = Client(ui_page("/"), shared=True).__enter__()
    app.get("/")(index_client.build_response)
    binding.reset()


@pytest.fixture(scope="session")
def screen(playwright: Playwright, request: pytest.FixtureRequest):
    if "noautofixt" in request.keywords:
        return
    browser = playwright.chromium.launch(headless=HEADLESS)
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
