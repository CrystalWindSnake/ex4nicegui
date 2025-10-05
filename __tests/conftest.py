import pytest
from playwright.sync_api import Playwright
from .screen import ServerManager
import os
from nicegui import Client, app, core

HEADLESS = "GITHUB_ACTION" in os.environ


@pytest.fixture(autouse=True)
def reset_globals(request: pytest.FixtureRequest):
    if "noautofixt" in request.keywords:
        return

    app.openapi_schema = None
    app.middleware_stack = None
    app.user_middleware.clear()
    app.urls.clear()
    core.air = None
    Client.instances.clear()
    Client.page_routes.clear()


@pytest.fixture(scope="session")
def server(playwright: Playwright, request: pytest.FixtureRequest):
    if "noautofixt" in request.keywords:
        return
    browser = playwright.chromium.launch(headless=HEADLESS)
    server = ServerManager(browser)

    yield server

    server.stop_server()


@pytest.fixture(scope="module")
def browser(server: ServerManager, request: pytest.FixtureRequest):
    if "noautofixt" in request.keywords:
        return
    browser = server.new_page()

    yield browser

    browser.close()


URL_COUNTER = 0


@pytest.fixture
def page_path(request: pytest.FixtureRequest):
    if "noautofixt" in request.keywords:
        return
    global URL_COUNTER
    URL_COUNTER += 1

    return f"/{URL_COUNTER}"
