from typing import Any, Callable, Optional
from dataclasses import dataclass
from nicegui.dataclasses import KWONLY_SLOTS
from nicegui.events import handle_event, UiEventArguments
from nicegui.element import Element
from signe import effect, batch
from ex4nicegui.utils.signals import _TMaybeRef, to_ref, to_value


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


def use_draggable(
    element: Element,
    init_x: _TMaybeRef[float] = 0.0,
    init_y: _TMaybeRef[float] = 0.0,
    auto_bind_style=True,
):
    ud = UseDraggable(element, init_x, init_y)
    if auto_bind_style:
        element.style(
            add=f"position:fixed;left:{to_value(init_x)}px;top:{to_value(init_y)}px"
        )
        ud.bind_style(element)

    return ud


class UseDraggable(Element, component="UseDraggable.js"):
    def __init__(
        self,
        element: Element,
        init_x: _TMaybeRef[float] = 0.0,
        init_y: _TMaybeRef[float] = 0.0,
    ) -> None:
        super().__init__()
        self._props["elementId"] = str(element.id)
        self._props["options"] = {
            "initialValue": {"x": to_value(init_x), "y": to_value(init_y)}
        }

        self.__style_ref = to_ref("")
        self.__x_ref = to_ref(init_x)
        self.__y_ref = to_ref(init_y)

        self.__isDragging_ref = to_ref(False)

        self.__isFirst_ref = to_ref(True)
        self.__isFinal_ref = to_ref(False)

        def update(args: UseDraggableUpdateEventArguments):
            @batch
            def _():
                self.__style_ref.value = args.style
                self.__x_ref.value = args.x
                self.__y_ref.value = args.y
                self.__isFirst_ref.value = args.isFirst
                self.__isFinal_ref.value = args.isFinal

        self.on_update(update)

        def on_isDraggingUpdate(e):
            self.__isDragging_ref.value = e.args["isDragging"]

        self.on("isDraggingUpdate", on_isDraggingUpdate)

    @property
    def x(self):
        return self.__x_ref

    @property
    def y(self):
        return self.__y_ref

    @property
    def style(self):
        return self.__style_ref

    @property
    def is_dragging(self):
        return self.__isDragging_ref

    @property
    def isFirst(self):
        return self.__isFirst_ref

    @property
    def isFinal(self):
        return self.__isFinal_ref.value

    def bind_style(self, element: Element):
        @effect
        def _():
            element.style(self.__style_ref.value)
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
