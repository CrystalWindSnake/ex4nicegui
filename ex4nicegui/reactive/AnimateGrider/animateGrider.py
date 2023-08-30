from typing import Any, Callable, Dict, List, Optional, Union
from nicegui import ui, app
from nicegui.element import Element
from collections import defaultdict
from dataclasses import dataclass, field
from nicegui.helpers import KWONLY_SLOTS
from nicegui.events import handle_event, UiEventArguments


@dataclass
class PropsInfo:
    start_row: int
    start_col: int
    end_row: str = field(default="auto")
    end_col: str = field(default="auto")
    opacity: float = field(default=1.0)
    duration: float = field(default=0.3)
    ease: str = field(default="power1.inOut")


@dataclass
class StepInfo:
    target: Element
    propsInfos: List[PropsInfo] = field(default_factory=list)
    current_index: int = -1

    def add_step(self, props: PropsInfo):
        self.propsInfos.append(props)

    def get_current_props(self):
        return self.propsInfos[self.current_index]


_onAnimationFinish_Args = ["id", "style", "resultProps"]


@dataclass(**KWONLY_SLOTS)
class ResultProps:
    opacity: float


@dataclass(**KWONLY_SLOTS)
class AnimationFinishEventArguments(UiEventArguments):
    id: int
    style: str
    resultProps: ResultProps


def _to_template_area(
    start_row: int,
    start_col: int,
    end_row: Union[int, str],
    end_col: Union[int, str],
):
    return f"{start_row}/{start_col}/{end_row}/{end_col}"


class AnimateGrider(Element, component="AnimateGrider.js"):
    def __init__(
        self, rowsTemplate: str, columnsTemplate: str, auto_set_pointer_events=True
    ) -> None:
        super().__init__()
        self._props["rowsTemplate"] = rowsTemplate
        self._props["columnsTemplate"] = columnsTemplate

        self._steps_map: Dict[int, StepInfo] = {}
        self._auto_set_pointer_events = auto_set_pointer_events

        @self.on_animation_finish
        def _(e: AnimationFinishEventArguments):
            if (e.id not in self._steps_map) or (not e.style):
                return

            element = self._steps_map[e.id].target
            element.style(replace=e.style)
            if self._auto_set_pointer_events and e.resultProps.opacity <= 0:
                element.style("pointer-events: auto;")
            # print(e.style)

    def changePosition(
        self,
        element: Element,
        start_row: int,
        start_col: int,
        end_row="auto",
        end_col="auto",
        opacity=1.0,
        *,
        duration: float = 0.3,
        ease="power1.inOut",
    ):
        id = element.id

        gridTemplateStyle = _to_template_area(start_row, start_col, end_row, end_col)
        animateOption = {
            "duration": duration,
            "ease": ease,
        }
        self.run_method(
            "changePosition",
            id,
            type(element).__name__,
            gridTemplateStyle,
            opacity,
            animateOption,
        )
        return gridTemplateStyle

    def add_step(
        self,
        element: Element,
        start_row: int,
        start_col: int,
        end_row="auto",
        end_col="auto",
        opacity=1.0,
        *,
        duration: float = 0.3,
        ease="power1.inOut",
    ):
        is_first_init = element.id not in self._steps_map

        if is_first_init:
            self._steps_map[element.id] = StepInfo(element, current_index=0)

            element.style(
                f"grid-area:{_to_template_area(start_row,start_col,end_row,end_col)};opacity:{opacity}"
            )

            if self._auto_set_pointer_events and opacity <= 0:
                element.style("pointer-events: none !important;")

        props = PropsInfo(
            start_row,
            start_col,
            end_row,
            end_col,
            opacity,
            duration,
            ease,
        )

        self._steps_map[element.id].add_step(props)

        return self

    def next_step(self, element: Element, step_index=-1, ignore_index_error=True):
        step_info = self._steps_map[element.id]

        if step_index < 0:
            step_info.current_index += 1
        else:
            step_info.current_index = step_index

        if step_info.current_index >= len(step_info.propsInfos):
            if ignore_index_error:
                return
            raise ValueError(f"Step index exceeds valid range")

        props = step_info.get_current_props()
        return self.changePosition(element, **props.__dict__)

    def on_animation_finish(
        self, handler: Optional[Callable[[AnimationFinishEventArguments], Any]]
    ):
        def inner_handler(e):
            args = e.args
            handle_event(
                handler,
                AnimationFinishEventArguments(
                    sender=self,
                    client=self.client,
                    id=args["id"],
                    style=args["style"],
                    resultProps=ResultProps(**args["resultProps"]),
                ),
            )

        self.on("onAnimationFinish", inner_handler, _onAnimationFinish_Args)

    def target(self, element: Element):
        pass


class Target:
    def __init__(self, element: Element, grider: AnimateGrider) -> None:
        self._element = element
        self._grider = grider

    def add_step(
        self,
        start_row: Optional[int] = None,
        start_col: Optional[int] = None,
        end_row: Optional[str] = None,
        end_col: Optional[str] = None,
        opacity=1.0,
        *,
        duration: float = 0.3,
        ease="power1.inOut",
    ):
        pass


def animate_grider(
    rowsTemplate="repeat(50,calc(100%/50))",
    columnsTemplate="repeat(50,calc(100%/50))",
):
    return AnimateGrider(rowsTemplate, columnsTemplate)
