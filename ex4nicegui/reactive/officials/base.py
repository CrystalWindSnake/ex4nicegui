from __future__ import annotations

from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Protocol,
    TypeVar,
    Generic,
    Union,
    cast,
    Literal,
)
from typing_extensions import Self
from ex4nicegui.utils.signals import (
    to_ref,
    ref_computed,
    _TMaybeRef as TMaybeRef,
    TRef,
    TReadonlyRef,
    effect,
    to_value,
    is_ref,
    WatchedState,
    on,
)
from nicegui import Tailwind, ui
from nicegui.elements.mixins.color_elements import (
    TextColorElement,
    QUASAR_COLORS,
    TAILWIND_COLORS,
)
from nicegui.elements.mixins.text_element import TextElement
from nicegui.elements.mixins.disableable_element import DisableableElement


T = TypeVar("T")


TWidget = TypeVar("TWidget", bound=ui.element)

_T_bind_classes_type_dict = Dict[str, TMaybeRef[bool]]
_T_bind_classes_type_ref_dict = TRef[Dict[str, bool]]
_T_bind_classes_type_array = List[TRef[str]]


_T_bind_classes_type = Union[
    _T_bind_classes_type_dict, _T_bind_classes_type_ref_dict, _T_bind_classes_type_array
]


class BindableUi(Generic[TWidget]):
    def __init__(self, element: TWidget) -> None:
        self.__element = element
        self.tailwind = Tailwind(cast(ui.element, self.__element))

    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None):
        cast(ui.element, self.element).props(add, remove=remove)
        return self

    def classes(
        self,
        add: Optional[str] = None,
        *,
        remove: Optional[str] = None,
        replace: Optional[str] = None,
    ):
        cast(ui.element, self.element).classes(add, remove=remove, replace=replace)
        return self

    def style(
        self,
        add: Optional[str] = None,
        *,
        remove: Optional[str] = None,
        replace: Optional[str] = None,
    ):
        cast(ui.element, self.element).style(add, remove=remove, replace=replace)
        return self

    def __enter__(self) -> Self:
        self.element.__enter__()
        return self

    def __exit__(self, *_):
        self.element.default_slot.__exit__(*_)

    def tooltip(self, text: str) -> Self:
        cast(ui.element, self.element).tooltip(text)
        return self

    def add_slot(self, name: str, template: Optional[str] = None):
        """Add a slot to the element.

        :param name: name of the slot
        :param template: Vue template of the slot
        :return: the slot
        """
        return cast(ui.element, self.element).add_slot(name, template)

    @property
    def element(self):
        return self.__element

    def delete(self) -> None:
        """Delete the element."""
        self.element.delete()

    def move(
        self, target_container: Optional[ui.element] = None, target_index: int = -1
    ):
        """Move the element to another container.

        :param target_container: container to move the element to (default: the parent container)
        :param target_index: index within the target slot (default: append to the end)
        """
        return self.element.move(target_container, target_index)

    def remove(self, element: Union[ui.element, int]) -> None:
        """Remove a child element.

        :param element: either the element instance or its ID
        """
        return self.element.remove(element)

    def bind_prop(self, prop: str, ref_ui: TReadonlyRef[Any]):
        if prop == "visible":
            return self.bind_visible(ref_ui)

        if prop == "text" and isinstance(self.element, TextElement):

            @effect
            def _():
                cast(TextElement, self.element).set_text(ref_ui.value)
                self.element.update()

        @effect
        def _():
            element = cast(ui.element, self.element)
            element._props[prop] = ref_ui.value
            element.update()

        return self

    def bind_visible(self, ref_ui: TReadonlyRef[bool]):
        @effect
        def _():
            element = cast(ui.element, self.element)
            element.set_visibility(ref_ui.value)

        return self

    def bind_not_visible(self, ref_ui: TRef[bool]):
        return self.bind_visible(ref_computed(lambda: not ref_ui.value))

    def on(
        self,
        type: str,
        handler: Optional[Callable[..., Any]] = None,
        args: Optional[List[str]] = None,
        *,
        throttle: float = 0.0,
        leading_events: bool = True,
        trailing_events: bool = True,
    ):
        ele = cast(ui.element, self.element)
        ele.on(
            type,
            handler,
            args,
            throttle=throttle,
            leading_events=leading_events,
            trailing_events=trailing_events,
        )

        return self

    def clear(self) -> None:
        cast(ui.element, self.element).clear()

    def bind_classes(self, classes: _T_bind_classes_type):
        """data binding is manipulating an element's class list

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#bind-class-names
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#%E7%BB%91%E5%AE%9A%E7%B1%BB%E5%90%8D

        Args:
            classes (_T_bind_classes_type):
        """
        if isinstance(classes, dict):
            for name, ref_obj in classes.items():

                @effect
                def _(name=name, ref_obj=ref_obj):
                    if to_value(ref_obj):
                        self.classes(add=name)
                    else:
                        self.classes(remove=name)

        elif is_ref(classes):
            ref_obj = to_value(classes)
            assert isinstance(ref_obj, dict)

            @effect
            def _():
                for name, value in cast(Dict, to_value(classes)).items():
                    if value:
                        self.classes(add=name)
                    else:
                        self.classes(remove=name)
        elif isinstance(classes, list):
            for ref_name in classes:
                if is_ref(ref_name):

                    @on(ref_name)
                    def _(state: WatchedState):
                        self.classes(add=state.current, remove=state.previous)
                else:
                    self.classes(ref_name)  # type: ignore

        return self

    def bind_style(self, style: Dict[str, TRef[str]]):
        """data binding is manipulating an element's style

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#bind-style
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#bind-style

        Args:
            style (Dict[str, Union[ReadonlyRef[str], Ref[str]]]): _description_
        """
        if isinstance(style, dict):
            for name, ref_obj in style.items():
                if is_ref(ref_obj):

                    @effect
                    def _(name=name, ref_obj=ref_obj):
                        self.element._style[name] = ref_obj.value
                        self.element.update()

        return self


class SingleValueBindableUi(BindableUi[TWidget], Generic[T, TWidget]):
    def __init__(self, value: TMaybeRef[T], element: TWidget) -> None:
        super().__init__(element)
        self._ref = to_ref(value)

    @property
    def value(self) -> T:
        return self._ref.value  # type: ignore

    def bind_ref(self, ref: TRef[T]):
        @effect
        def _():
            ref.value = self._ref.value  # type: ignore

        return self


_T_DisableableBinder = TypeVar("_T_DisableableBinder", bound=DisableableElement)


class DisableableMixin(Protocol):
    @property
    def element(self) -> DisableableElement:
        ...

    def bind_enabled(self, ref_ui: TReadonlyRef[bool]):
        @effect
        def _():
            value = ref_ui.value
            self.element.set_enabled(value)
            self.element._handle_enabled_change(value)

        return self

    def bind_disable(self, ref_ui: TReadonlyRef[bool]):
        @effect
        def _():
            value = not ref_ui.value
            self.element.set_enabled(value)
            self.element._handle_enabled_change(value)

        return self


DisableableBindableUi = DisableableMixin


_color_sys_type = Literal["QUASAR", "TAILWIND", "STYLE"]
_color_attr_name = "data-ex4ng-color"


def _bind_color(bindable_ui: SingleValueBindableUi, ref_ui: TReadonlyRef):
    @effect
    def _():
        ele = cast(TextColorElement, bindable_ui.element)
        color = ref_ui.value

        # get exists color
        # e.g 'QUASAR:red'
        pre_color = ele._props.get(_color_attr_name)  # type: str | None
        if pre_color:
            color_sys, value = pre_color.split(":")  # type: ignore
            color_sys: _color_sys_type

            if color_sys == "QUASAR":
                del ele._props[ele.TEXT_COLOR_PROP]
            elif color_sys == "TAILWIND":
                ele.classes(remove=value)
            else:
                del ele._style["color"]

        cur_sys: _color_sys_type = "STYLE"
        cur_color = color

        if color in QUASAR_COLORS:
            ele._props[ele.TEXT_COLOR_PROP] = color
            cur_sys = "QUASAR"
        elif color in TAILWIND_COLORS:
            cur_color = f"text-{color}"
            ele.classes(replace=cur_color)
            cur_sys = "TAILWIND"
        elif color is not None:
            ele._style["color"] = color

        ele._props[_color_attr_name] = f"{cur_sys}:{color}"

        ele.update()

    return bindable_ui
