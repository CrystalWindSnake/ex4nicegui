from typing import List, Optional
from nicegui.elements.mixins.content_element import ContentElement
from pathlib import Path
import nicegui

NG_ROOT = Path(nicegui.__file__).parent / "elements"


exposed_libraries = [
    NG_ROOT / "lib/mermaid/mermaid.esm.min.mjs",
    "../libs/d3/*.js",
]
extra_libraries = [
    NG_ROOT / "lib/mermaid/*.js",
]


class Mermaid(
    ContentElement,
    component="mermaid.js",
    exposed_libraries=exposed_libraries,  # type: ignore
    extra_libraries=extra_libraries,  # type: ignore
):
    CONTENT_PROP = "content"

    def __init__(
        self, content: str, clickable_nodes: Optional[List[str]] = None
    ) -> None:
        """Mermaid Diagrams

        Renders diagrams and charts written in the Markdown-inspired `Mermaid <https://mermaid.js.org/>`_ language.
        The mermaid syntax can also be used inside Markdown elements by providing the extension string 'mermaid' to the ``ui.markdown`` element.

        :param content: the Mermaid content to be displayed
        """
        super().__init__(content=content)
        self._props["currentId"] = str(self.id)
        self._props["clickableNodes"] = clickable_nodes or []

    def on_content_change(self, content: str) -> None:
        self._props[self.CONTENT_PROP] = content.strip()
        self.run_method("update", content.strip())
