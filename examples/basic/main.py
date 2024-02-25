from nicegui import ui

from lazy_tab_panel import lazy_tab_panels
from importlib import import_module

topics = ["use_ref"]

with ui.tabs() as tabs:
    for name in topics:
        ui.tab(name).props("no-caps")


with lazy_tab_panels(tabs).classes("w-full h-full") as panels:
    for name in topics:
        panel = panels.tab_panel(name)

        @panel.build_fn
        def _(name: str):
            import_module(name)


ui.run()
