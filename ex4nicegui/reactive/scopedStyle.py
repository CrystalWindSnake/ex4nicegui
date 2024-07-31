from nicegui.element import Element
from ex4nicegui.helper import client_instance_locker
from nicegui import ui


class ScopedStyle(Element, component="scopedStyle.js"):
    pass

    @staticmethod
    def get():
        if not ui.context.slot_stack:
            return None
        return _scoped_style_factory.get_object(ui.context.client)

    def create_style(self, element: Element, css: str):
        element_id = f"c{element.id}"

        self.run_method("createStyle", element_id, css)

    def remove_style(self, element: Element):
        element_id = f"c{element.id}"
        self.run_method("removeStyle", element_id)


_scoped_style_factory = client_instance_locker.ClientInstanceLocker(ScopedStyle)
