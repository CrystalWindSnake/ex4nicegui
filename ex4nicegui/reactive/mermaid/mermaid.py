from typing import Callable, List, Optional
from nicegui.elements.mixins.content_element import ContentElement
from pathlib import Path
import nicegui
from dataclasses import dataclass
from nicegui.events import UiEventArguments
from nicegui.dataclasses import KWONLY_SLOTS

NG_ROOT = Path(nicegui.__file__).parent / "elements"

EX4_LIBS_ROOT = Path(__file__).parent.parent.parent / "libs"

dependencies = [
    NG_ROOT / "lib/mermaid/mermaid.esm.min.mjs",
    EX4_LIBS_ROOT / "d3/*.js",
    NG_ROOT / "lib/mermaid/*.js",
]


@dataclass(**KWONLY_SLOTS)
class NodeClickEventArguments(UiEventArguments):
    nodeId: str


class Mermaid(  # type: ignore
    ContentElement,
    component="mermaid.js",
    dependencies=dependencies,  # type: ignore
):
    CONTENT_PROP = "content"

    def __init__(
        self, content: str, clickable_nodes: Optional[List[str]] = None, zoom_mode=False
    ) -> None:
        """Mermaid Diagrams

        Renders diagrams and charts written in the Markdown-inspired `Mermaid <https://mermaid.js.org/>`_ language.
        The mermaid syntax can also be used inside Markdown elements by providing the extension string 'mermaid' to the ``ui.markdown`` element.

        :param content: the Mermaid content to be displayed
        """
        super().__init__(content=content)
        self._props["currentId"] = str(self.id)
        self._props["clickableNodes"] = clickable_nodes or []
        self._props["zoomMode"] = zoom_mode

    def on_content_change(self, content: str) -> None:
        self._props[self.CONTENT_PROP] = content.strip()
        self.run_method("update", content.strip())

    def on_node_click(
        self,
        handler: Callable[[NodeClickEventArguments], None],
    ):
        def inner_handler(e):
            handler(
                NodeClickEventArguments(
                    sender=self, client=self.client, nodeId=e.args["nodeId"]
                )
            )

        self.on("onNodeClick", inner_handler, ["nodeId"])
