from typing import Any, Awaitable, Callable, Optional, Union
from weakref import WeakValueDictionary
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    to_value,
    _TMaybeRef as TMaybeRef,
)
from ex4nicegui.utils.scheduler import next_tick
from nicegui import ui
from .base import BindableUi
from ex4nicegui.reactive.mixins.value_element import ValueElementMixin
from .tab_panel import lazy_tab_panel


class TabPanelsBindableUi(BindableUi[ui.tab_panels], ValueElementMixin[bool]):
    def __init__(
        self,
        value: Optional[TMaybeRef[str]] = None,
        *,
        on_change: Optional[Callable[..., Any]] = None,
        animated: TMaybeRef[bool] = True,
        keep_alive: TMaybeRef[bool] = True,
    ) -> None:
        """Tab Panels

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#tab_panels
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#tab_panels

        Args:
            value (TMaybeRef[str], optional): The value of the tab panel. Defaults to None.
            on_change (Callable[..., Any], optional): The callback function when the value of the tab panel changes. Defaults to None.
            animated (TMaybeRef[bool], optional): Whether to animate the tab panel. Defaults to True.
            keep_alive (TMaybeRef[bool], optional): Whether to keep the tab panel alive. Defaults to True.
        """
        pc = ParameterClassifier(
            locals(),
            maybeRefs=["value", "animated", "keep_alive"],
            v_model=("value", "on_change"),
            events=["on_change"],
        )

        element = ui.tab_panels(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if ValueElementMixin._bind_specified_props(self, prop, value):
            return self

        return super().bind_prop(prop, value)


class LazyTabPanelsBindableUi(TabPanelsBindableUi):
    def __init__(
        self,
        value: Optional[TMaybeRef[str]] = None,
        *,
        on_change: Optional[Callable[..., Any]] = None,
        animated: TMaybeRef[bool] = True,
        keep_alive: TMaybeRef[bool] = True,
    ) -> None:
        """Lazy Tab Panels

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#lazy_tab_panels
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#lazy_tab_panels

        Args:
            value (Optional[TMaybeRef[str]], optional): The value of the tab panel. Defaults to None.
            on_change (Optional[Callable[..., Any]], optional):  The callback function when the value of the tab panel changes. Defaults to None.
            animated (TMaybeRef[bool], optional):  Whether to animate the tab panel. Defaults to True.
            keep_alive (TMaybeRef[bool], optional):  Whether to keep the tab panel alive. Defaults to True.
        """
        super().__init__(
            value, on_change=on_change, animated=animated, keep_alive=keep_alive
        )

        self._panels: WeakValueDictionary[str, lazy_tab_panel] = WeakValueDictionary()

        if value:

            @self._ui_effect
            def _():
                current_value = to_value(value)
                if current_value in self._panels:
                    panel = self._panels[current_value]

                    @next_tick
                    def _():
                        panel.try_run_build_fn()

    def add_tab_panel(self, name: str):
        return TabPanelDescriptor(self, name)


class TabPanelDescriptor:
    def __init__(self, tab_panels: LazyTabPanelsBindableUi, panle_name: str):
        self.panle_name = panle_name
        self.tab_panels = tab_panels

    def __call__(self, fn: Callable[..., Union[None, Awaitable]]):
        with self.tab_panels:
            panel = lazy_tab_panel(self.panle_name)
        str_name = panel.element._props["name"]
        self.tab_panels._panels[str_name] = panel
        panel.build_fn(fn)

        if self.tab_panels.value == self.panle_name:
            panel.try_run_build_fn()

        return panel

    def props(self, **kwargs):
        pass
