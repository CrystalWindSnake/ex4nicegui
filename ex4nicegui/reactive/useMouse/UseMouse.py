from typing import Any, Callable, Optional
from dataclasses import dataclass
from nicegui.helpers import KWONLY_SLOTS
from nicegui.events import handle_event, EventArguments
from nicegui.element import Element
from signe import createSignal, effect, batch


_Update_Args = [
    "x",
    "y",
    "sourceType",
]


@dataclass(**KWONLY_SLOTS)
class UseMouseUpdateEventArguments(EventArguments):
    x: float
    y: float
    sourceType: str


class UseMouse(Element, component="UseMouse.js"):
    def __init__(self, options: Optional[dict] = None) -> None:
        super().__init__("UseMouse")

        if options:
            self._props["options"] = options

        self.__x_getter, self.__x_setter = createSignal(0.0)
        self.__y_getter, self.__y_setter = createSignal(0.0)
        self.__sourceType_getter, self.__sourceType_setter = createSignal("sourceType")

        def update(args: UseMouseUpdateEventArguments):
            @batch
            def _():
                self.__x_setter(args.x)
                self.__y_setter(args.y)
                self.__sourceType_setter(args.sourceType)

        self.on_update(update)

    @property
    def x(self):
        return self.__x_getter()

    @property
    def y(self):
        return self.__y_getter()

    @property
    def sourceType(self):
        return self.__sourceType_getter()

    def on_update(self, handler: Optional[Callable[..., Any]]):
        def inner_handler(e):
            args = e.args
            handle_event(
                handler,
                UseMouseUpdateEventArguments(
                    sender=self,
                    client=self.client,
                    x=args["x"],
                    y=args["y"],
                    sourceType=args["sourceType"],
                ),
            )

        self.on("update", inner_handler, args=_Update_Args)


_Use_Mouse_Ins = UseMouse()


def use_mouse(options: Optional[dict] = None):
    global _Use_Mouse_Ins
    # if _Use_Mouse_Ins is None:
    #     _Use_Mouse_Ins = UseMouse(options)

    return _Use_Mouse_Ins
