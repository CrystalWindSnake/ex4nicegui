from nicegui import ui, app

from ex4nicegui import rxui, to_ref, ref_computed, gsap, deep_ref, Ref
from ex4nicegui.layout import grid_box
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
