from __future__ import annotations

from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    TypeVar,
    Generic,
    Union,
    cast,
    overload,
)

from typing_extensions import Self
from ex4nicegui.utils.apiEffect import ui_effect
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    to_value,
    is_ref,
    WatchedState,
    on,
)
from ex4nicegui.utils.clientScope import new_scope
from ex4nicegui.utils.types import _TMaybeRef as TMaybeRef
from nicegui import Tailwind, ui
from nicegui.elements.mixins.text_element import TextElement
from ex4nicegui.reactive.services.reactive_service import inject_handle_delete
from ex4nicegui.reactive.scopedStyle import ScopedStyle
from ex4nicegui.reactive.mixins.disableable import DisableableMixin
from functools import partial

T = TypeVar("T")


TWidget = TypeVar("TWidget", bound=ui.element)

_T_bind_classes_type_dict = Dict[str, TGetterOrReadonlyRef[bool]]
_T_bind_classes_type_ref_dict = TGetterOrReadonlyRef[Dict[str, bool]]
_T_bind_classes_type_single = TGetterOrReadonlyRef[str]
_T_bind_classes_type_array = List[_T_bind_classes_type_single]


_T_bind_classes_type = Union[
    _T_bind_classes_type_dict,
    _T_bind_classes_type_ref_dict,
    _T_bind_classes_type_single,
    _T_bind_classes_type_array,
    Dict[str, bool],
    List[str],
]


class BindableUi(Generic[TWidget]):
    def __init__(self, element: TWidget) -> None:
        self._element = element
        inject_handle_delete(self.element, self._on_element_delete)
        self.tailwind = Tailwind(cast(ui.element, self._element))
        self._effect_scope = new_scope()
        self.__used_scope_style = False

    def _on_element_delete(self):
        self._effect_scope.dispose()

        if self.__used_scope_style:
            scope_style = ScopedStyle.get()
            if scope_style:
                scope_style.remove_style(self.element)

    @property
    def _ui_effect(self):
        return partial(ui_effect, scope=self._effect_scope)

    @property
    def _ui_signal_on(self):
        """equivalent to `on`, but with the effect scope,and with `onchanges`=True and `deep` = False"""

        return partial(on, scope=self._effect_scope, onchanges=True, deep=False)

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

    def tooltip(self, text: TMaybeRef[str]) -> Self:
        from ex4nicegui.reactive.officials.tooltip import TooltipBindableUi

        with self:
            TooltipBindableUi(text)

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
        return self._element

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

    @overload
    def bind_props(self, props: Dict[str, TMaybeRef[Any]]) -> Self: ...

    @overload
    def bind_props(self, props: TMaybeRef[str]) -> Self: ...

    def bind_props(self, props: Union[Dict[str, TMaybeRef[Any]], TMaybeRef[str]]):
        """data binding is manipulating an element's props

        Args:
            props (TMaybeRef[str]):  a reference to the props to bind to

        ## usage

        .. code-block:: python
            outlined = to_ref(True)
            size = to_ref("xs")

            def props_str():
                return f'{"flat" if flat.value else ""} {"size=" + size.value}'

            rxui.button("click me").bind_props(props_str)

        """
        if isinstance(props, dict):

            def props_str():
                props_dict = (
                    f"""{name if isinstance(raw_value,bool) else f"{name}='{raw_value}'"}"""
                    for name, value in props.items()
                    if (raw_value := to_value(value))
                )

                return " ".join(props_dict)

            self._bind_props_for_str_fn(props_str)
        else:
            self._bind_props_for_str_fn(props)

        return self

    def _bind_props_for_str_fn(self, props_str: TMaybeRef[str]):
        @self._ui_signal_on(props_str, onchanges=False, deep=False)
        def _(state: WatchedState):
            self.props(add=state.current, remove=state.previous)

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef[Any]):
        """data binding is manipulating an element's property

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#bind_prop
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#bind_prop

        Args:
            prop (str): property name
            value (TGetterOrReadonlyRef[Any]): a reference to the value to bind to

        """
        if prop == "visible":
            return self.bind_visible(value)

        if prop == "text" and isinstance(self.element, TextElement):

            @self._ui_effect
            def _():
                cast(TextElement, self.element).set_text(to_value(value))
                self.element.update()

        @self._ui_effect
        def _():
            element = cast(ui.element, self.element)
            element._props[prop] = to_value(value)
            element.update()

        return self

    def bind_visible(self, value: TMaybeRef[bool]):
        @self._ui_effect
        def _():
            element = cast(ui.element, self.element)
            element.set_visibility(to_value(value))

        return self

    def bind_not_visible(self, value: TMaybeRef[bool]):
        return self.bind_visible(lambda: not to_value(value))

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

    @overload
    def bind_classes(self, classes: Dict[str, TGetterOrReadonlyRef[bool]]) -> Self: ...

    @overload
    def bind_classes(self, classes: Dict[str, bool]) -> Self: ...

    @overload
    def bind_classes(self, classes: TGetterOrReadonlyRef[Dict[str, bool]]) -> Self: ...

    @overload
    def bind_classes(self, classes: List[TGetterOrReadonlyRef[str]]) -> Self: ...

    @overload
    def bind_classes(self, classes: List[str]) -> Self: ...

    @overload
    def bind_classes(self, classes: TGetterOrReadonlyRef[str]) -> Self: ...

    def bind_classes(self, classes: _T_bind_classes_type) -> Self:
        """data binding is manipulating an element's class list

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#bind_classes
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#bind_classes

        Args:
            classes (_T_bind_classes_type): dict of refs | ref to dict | str ref | list of refs

        ## usage

        bind class names with dict,value is bool ref, for example:

        .. code-block:: python
            bg_color = to_ref(True)
            has_error = to_ref(False)

            rxui.label('Hello').bind_classes({'bg-blue':bg_color, 'text-red':has_error})


        bind list of class names with ref

        .. code-block:: python
            color = to_ref('red')
            bg_color = lambda: f"bg-{color.value}"

            rxui.label('Hello').bind_classes([bg_color])


        bind single class name with ref

        .. code-block:: python
            color = to_ref('red')
            bg_color = lambda: f"bg-{color.value}"

            rxui.label('Hello').bind_classes(bg_color)


        """
        if isinstance(classes, dict):
            self._bind_classes_for_str_fn(
                lambda: " ".join(
                    name for name, value in classes.items() if to_value(value)
                )
            )

        elif isinstance(classes, list):
            self._bind_classes_for_str_fn(
                lambda: " ".join(to_value(c) for c in classes)
            )
        elif is_ref(classes) or isinstance(classes, Callable):
            ref_obj = to_value(classes)  # type: ignore

            if isinstance(ref_obj, dict):

                def classes_str():
                    return " ".join(
                        name
                        for name, value in to_value(classes).items()  # type: ignore
                        if to_value(value)
                    )

                self._bind_classes_for_str_fn(classes_str)

            else:
                self._bind_classes_for_str_fn(classes)  # type: ignore

        return self

    def _bind_classes_for_str_fn(self, classes_str: TGetterOrReadonlyRef[str]):
        @self._ui_signal_on(classes_str, onchanges=False, deep=False)
        def _(state: WatchedState):
            self.classes(add=state.current, remove=state.previous)

    @overload
    def bind_style(self, style: TMaybeRef[str]) -> Self: ...

    @overload
    def bind_style(self, style: Dict[str, TMaybeRef[Any]]) -> Self: ...

    def bind_style(self, style: Union[TMaybeRef[str], Dict[str, TMaybeRef[Any]]]):
        """data binding is manipulating an element's style

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#bind_style
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#bind_style

        Args:
            style (Dict[str, Union[ReadonlyRef[str], Ref[str]]]): dict of style name and ref value


        ## usage

        .. code-block:: python
            bg_color = to_ref("blue")
            text_color = to_ref("red")

            rxui.label("test").bind_style(
                {
                    "background-color": bg_color,
                    "color": text_color,
                }
            )

        """
        if isinstance(style, dict):
            self._bind_style_for_str_fn(
                lambda: ";".join(
                    f"{name}:{to_value(value)}" for name, value in style.items()
                )
            )
        else:
            self._bind_style_for_str_fn(style)

        return self

    def _bind_style_for_str_fn(self, style_str: TMaybeRef[str]):
        @self._ui_signal_on(style_str, onchanges=False, deep=False)
        def _(state: WatchedState):
            self.style(add=state.current, remove=state.previous)

    def scoped_style(self, selector: str, style: Union[str, Path]):
        """add scoped style to the element

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#scoped_style
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#scoped_style

        Args:
            selector (str): css selector
            style (Union[str, Path]): path to css file or inline style string

        ## usage

        .. code-block:: python
            # all children of the element will have red outline, excluding itself
            with rxui.row().scoped_style("*", "outline: 1px solid red;") as row:
                ui.label("Hello")
                ui.label("World")

            # all children of the element will have red outline, including the element itself
            with rxui.row().scoped_style(":self *", "outline: 1px solid red;") as row:
                ui.label("Hello")
                ui.label("World")

            # all children of the element will have red outline when element is hovered
            with rxui.row().scoped_style(":hover *", "outline: 1px solid red;") as row:
                ui.label("Hello")
                ui.label("World")

            # all children of the element and itself will have red outline when element is hovered
            with rxui.row().scoped_style(":self:hover *", "outline: 1px solid red;") as row:
                ui.label("Hello")
                ui.label("World")

        """

        is_css_file = isinstance(style, Path)

        if is_css_file:
            style = style.read_text(encoding="utf-8")

        id = f"c{self.element.id}"
        selector_with_self = _utils._parent_id_with_selector(id, selector, is_css_file)
        css = ""
        if is_css_file:
            css = f"{selector_with_self} {style}"
        else:
            css = f"{selector_with_self}{{{style}}}"

        scope_style = ScopedStyle.get()
        assert scope_style, "can not find scope style"
        scope_style.create_style(self.element, css)
        self.__used_scope_style = True
        return self

    def update(self):
        """Update the element on the client side."""
        self.element.update()


class _utils:
    @staticmethod
    def _parent_id_with_selector(
        parent_id: str, selector: str, is_css_file=False
    ) -> str:
        selector_with_self = f"#{parent_id}"

        selector = selector.strip()
        if (not selector) and (not is_css_file):
            selector = "* "

        if selector.startswith(":self"):
            selector = selector[5:].lstrip()
            parent_selector = f"#{parent_id}"
            if selector.startswith(":"):
                parent_selector = f"{parent_selector}{selector.split()[0]}"

            selector_with_self = f"{parent_selector},{selector_with_self}"

        if not selector.startswith(":"):
            selector_with_self = selector_with_self + " "

        selector_with_self = selector_with_self + selector
        return selector_with_self


DisableableBindableUi = DisableableMixin
