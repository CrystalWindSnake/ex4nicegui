from typing import List, Literal, Optional, Dict

from ex4nicegui.utils.signals import (
    _TMaybeRef as TMaybeRef,
)

from nicegui import ui
from nicegui.events import Handler, ValueChangeEventArguments
from .base import BindableUi
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier


class TreeBindableUi(
    BindableUi[ui.tree],
):
    def __init__(
        self,
        nodes: TMaybeRef[List[Dict]],
        *,
        selected: Optional[TMaybeRef[str]] = None,
        node_key: str = "id",
        label_key: str = "label",
        children_key: str = "children",
        on_select: Optional[Handler[ValueChangeEventArguments]] = None,
        on_expand: Optional[Handler[ValueChangeEventArguments]] = None,
        on_tick: Optional[Handler[ValueChangeEventArguments]] = None,
        tick_strategy: Optional[
            TMaybeRef[Literal["leaf", "leaf-filtered", "strict"]]
        ] = None,
    ) -> None:
        """Tree

        Display hierarchical data using Quasar's `QTree <https://quasar.dev/vue-components/tree>`_ component.

        If using IDs, make sure they are unique within the whole tree.

        To use checkboxes and ``on_tick``, set the ``tick_strategy`` parameter to "leaf", "leaf-filtered" or "strict".


        Args:
            nodes (TMaybeRef[List[Dict]]):  hierarchical list of node objects
            selected (Optional[TMaybeRef[str]], optional): Key of node currently selected. Defaults to None.
            node_key (str, optional):  property name of each node object that holds its unique id. Defaults to "id".
            label_key (str, optional): property name of each node object that holds its label. Defaults to "label".
            children_key (str, optional): property name of each node object that holds its list of children. Defaults to "children".
            on_select (Optional[Handler[ValueChangeEventArguments]], optional): callback which is invoked when the node selection changes. Defaults to None.
            on_expand (Optional[Handler[ValueChangeEventArguments]], optional): callback which is invoked when the node expansion changes. Defaults to None.
            on_tick (Optional[Handler[ValueChangeEventArguments]], optional): callback which is invoked when a node is ticked or unticked. Defaults to None.
            tick_strategy (Optional[ TMaybeRef[Literal[&quot;leaf&quot;, &quot;leaf, optional): whether and how to use checkboxes. Defaults to None.


        Example:
        .. code-block:: python
            from ex4nicegui import to_ref, rxui

            selected = to_ref("")
            nodes = to_ref(
                [
                    {"id": "numbers", "children": [{"id": "1"}, {"id": "2"}]},
                    {"id": "letters", "children": [{"id": "A"}, {"id": "B"}]},
                ]
            )

            rxui.label(lambda: f"Selected node: {selected.value}")
            rxui.tree(nodes, selected=selected, label_key="id")
        """
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "nodes",
                "node_key",
                "label_key",
                "children_key",
                "tick_strategy",
            ],
            v_model=("selected", "on_select"),
            events=["on_select", "on_expand", "on_tick"],
        )

        value_kws = pc.get_values_kws()
        value_kws.pop("selected")
        element = ui.tree(**value_kws)
        super().__init__(element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore
