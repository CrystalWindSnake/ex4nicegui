from ex4nicegui.reactive import rxui
from nicegui import ui
from .screen import BrowserManager


def test_node_click(browser: BrowserManager, page_path: str):
    @ui.page(page_path)
    def _():
        code = """
flowchart TD
    A --> B
    B --> C
        """

        def node_click(e):
            lbl.set_text("clicked")

        lbl = ui.label("").classes("result")

        rxui.mermaid(code, ["A", "B"], zoom_mode=True).classes("target").on_node_click(
            node_click
        )

    page = browser.open(page_path)

    target = page.Mermaid(".target")
    label = page.Label(".result")

    target.assert_svg_exists()
    target.click_node("A")

    label.expect_contain_text("clicked")
