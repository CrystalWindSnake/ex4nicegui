from typing import Any, Callable, Optional, Union
from nicegui import ui
from nicegui.elements.tabs import Tab, TabPanel, Tabs
from nicegui.events import handle_event
from weakref import WeakValueDictionary


class lazy_tab_panels(ui.tab_panels):
    def __init__(
        self,
        tabs: Optional[Tabs] = None,
        *,
        value: Union[Tab, TabPanel, str, None] = None,
        on_change: Union[Callable[..., Any], None] = None,
        animated: bool = True,
        keep_alive: bool = True,
    ) -> None:
        self.__panels: WeakValueDictionary[str, lazy_tab_panel] = WeakValueDictionary()

        def inject_onchange(e):
            panel = self.__panels.get(self.value)
            if panel:
                panel.try_run_build_fn()
            if on_change:
                handle_event(on_change, e)

        super().__init__(
            tabs,
            value=value,
            on_change=inject_onchange,
            animated=animated,
            keep_alive=keep_alive,
        )

    def tab_panel(self, name: Union[ui.tab, str]):
        panel = lazy_tab_panel(name)
        str_name = panel._props["name"]
        self.__panels[str_name] = panel
        return panel


class lazy_tab_panel(ui.tab_panel):
    def __init__(self, name: Union[Tab, str]) -> None:
        super().__init__(name)
        self._build_fn = None

    def try_run_build_fn(self):
        if self._build_fn:
            with self:
                self._build_fn(self._props["name"])
            self._build_fn = None

    def build_fn(self, fn: Callable[[str], None]):
        self._build_fn = fn
        return fn
