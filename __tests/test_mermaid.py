from ex4nicegui.reactive import rxui
from nicegui import ui
from .screen import ScreenPage
from .utils import MermaidUtils, set_test_id, fn


def test_node_click(page: ScreenPage, page_path: str):
    event_spy: fn = None  # type: ignore

    @ui.page(page_path)
    def _():
        nonlocal event_spy

        code = """
flowchart TD
    A --> B
    B --> C
        """

        @fn
        def node_click(e):
            pass

        event_spy = node_click

        mm = rxui.mermaid(code, ["A", "B"], zoom_mode=True)
        mm.on_node_click(node_click)
        set_test_id(mm, "target")

    page.open(page_path)

    target = MermaidUtils(page, "target")

    target.assert_svg_exists()
    target.click_node("A")

    assert event_spy.calledTimes == 1
