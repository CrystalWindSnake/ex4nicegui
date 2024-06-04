from typing import Any, Callable, Optional, cast
from dataclasses import dataclass
from nicegui.dataclasses import KWONLY_SLOTS
from nicegui.events import handle_event, UiEventArguments
from nicegui.element import Element

from ex4nicegui.utils.signals import TReadonlyRef, batch, to_ref

_Update_Args = [
    "x",
    "y",
    "sourceType",
]


@dataclass(**KWONLY_SLOTS)
class UseMouseUpdateEventArguments(UiEventArguments):
    x: float
    y: float
    sourceType: str


class UseMouse(Element, component="UseMouse.js"):
    def __init__(self, options: Optional[dict] = None) -> None:
        super().__init__()

        if options:
            self._props["options"] = options

        self.__x = to_ref(0.0)
        self.__y = to_ref(0.0)
        self.__sourceType = to_ref("sourceType")

        def update(args: UseMouseUpdateEventArguments):
            @batch
            def _():
                self.__x.value = args.x
                self.__y.value = args.y
                self.__sourceType.value = args.sourceType

        self.on_update(update)

    @property
    def x(self):
        return cast(TReadonlyRef[float], self.__x)

    @property
    def y(self):
        return cast(TReadonlyRef[float], self.__y)

    @property
    def sourceType(self):
        return cast(TReadonlyRef[float], self.__sourceType)

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


_Use_Mouse_Ins = None


def use_mouse(options: Optional[dict] = None):
    global _Use_Mouse_Ins
    if _Use_Mouse_Ins is None:
        _Use_Mouse_Ins = UseMouse(options)

    return cast(UseMouse, _Use_Mouse_Ins)
