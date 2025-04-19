from ex4nicegui.reactive import rxui
from nicegui import ui
from ex4nicegui import to_ref
from .screen import BrowserManager


def test_nodes(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        nodes = to_ref(
            [
                {"id": "numbers", "children": [{"id": "1"}, {"id": "2"}]},
                {"id": "letters", "children": [{"id": "A"}, {"id": "B"}]},
            ]
        )

        def change_nodes():
            nodes.value = [
                {"id": "new numbers", "children": [{"id": "new 1"}, {"id": "new 2"}]},
                {"id": "new letters", "children": [{"id": "new A"}, {"id": "new B"}]},
            ]

        rxui.tree(nodes, label_key="id")
        ui.button("Change nodes", on_click=change_nodes).classes("btn-change")

    page = browser.open(page_path)
    btn = page.Button(".btn-change")

    page.should_contain("numbers")
    btn.click()
    page.should_contain("new numbers")


def test_selected(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        selected = to_ref("")
        nodes = to_ref(
            [
                {"id": "numbers", "children": [{"id": "1"}, {"id": "2"}]},
                {"id": "letters", "children": [{"id": "A"}, {"id": "B"}]},
            ]
        )

        rxui.label(lambda: f"currently selected {selected.value}").classes(
            "selected-label"
        )
        rxui.tree(nodes, selected=selected, label_key="id")

    page = browser.open(page_path)

    page.get_by_text("numbers").click()
    page.should_contain("currently selected numbers")
