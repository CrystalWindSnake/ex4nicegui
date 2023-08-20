from typing import Any, Callable, Optional
from dataclasses import dataclass
from nicegui.helpers import KWONLY_SLOTS
from nicegui.events import handle_event, UiEventArguments
from nicegui.element import Element
from signe import createSignal, effect, batch
from ex4nicegui.utils.signals import ref_from_signal

_Update_Args = [
    "x",
    "y",
    "style",
    "isFirst",
    "isFinal",
]


@dataclass(**KWONLY_SLOTS)
class UseDraggableUpdateEventArguments(UiEventArguments):
    x: float
    y: float
    style: str
    isFirst: bool
    isFinal: bool


def use_draggable(element: Element, init_x=0.0, init_y=0.0, auto_bind_style=True):
    ud = UseDraggable(element, init_x, init_y)
    if auto_bind_style:
        element.style(add=f"position:fixed;left:{init_x}px;top:{init_y}px")
        ud.bind_style(element)

    return ud


class UseDraggable(Element, component="UseDraggable.js"):
    def __init__(self, element: Element, init_x=0.0, init_y=0.0) -> None:
        super().__init__()
        self._props["elementId"] = str(element.id)
        self._props["options"] = {"initialValue": {"x": init_x, "y": init_y}}

        self.__style_getter, self.__style_setter = createSignal("")
        self.__x_getter, self.__x_setter = createSignal(init_x)
        self.__y_getter, self.__y_setter = createSignal(init_y)
        self.__isDragging_getter, self.__isDragging_setter = createSignal(False)

        self.__isFirst_getter, self.__isFirst_setter = createSignal(True)
        self.__isFinal_getter, self.__isFinal_setter = createSignal(False)

        def update(args: UseDraggableUpdateEventArguments):
            @batch
            def _():
                self.__style_setter(args.style)
                self.__x_setter(args.x)
                self.__y_setter(args.y)
                self.__isFirst_setter(args.isFirst)
                self.__isFinal_setter(args.isFinal)

        self.on_update(update)

        def on_isDraggingUpdate(e):
            self.__isDragging_setter(e.args["isDragging"])
            # print(args['args']['isDragging'])

        self.on("isDraggingUpdate", on_isDraggingUpdate)

    @property
    def x(self):
        return ref_from_signal(self.__x_getter)

    @property
    def y(self):
        return ref_from_signal(self.__y_getter)

    @property
    def style(self):
        return ref_from_signal(self.__style_getter)

    @property
    def is_dragging(self):
        return ref_from_signal(self.__isDragging_getter)

    @property
    def isFirst(self):
        return ref_from_signal(self.__isFirst_getter)

    @property
    def isFinal(self):
        return ref_from_signal(self.__isFinal_getter)

    def bind_style(self, element: Element):
        @effect
        def _():
            element.style(self.__style_getter())
            element.update()

    def on_update(self, handler: Optional[Callable[..., Any]]):
        def inner_handler(e):
            args = e.args
            handle_event(
                handler,
                UseDraggableUpdateEventArguments(
                    sender=self,
                    client=self.client,
                    x=args["x"],
                    y=args["y"],
                    style=args["style"],
                    isFirst=args["isFirst"],
                    isFinal=args["isFinal"],
                ),
            )

        self.on("update", inner_handler, args=_Update_Args)
