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
    overload,
)

from typing_extensions import Self
from ex4nicegui.utils.apiEffect import ui_effect
import signe
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    effect,
    to_value,
    is_ref,
    WatchedState,
    on,
)
from ex4nicegui.utils.clientScope import new_scope
from nicegui import Tailwind, ui
from nicegui.elements.mixins.text_element import TextElement
from nicegui.elements.mixins.disableable_element import DisableableElement
from ex4nicegui.reactive.services.reactive_service import inject_handle_delete
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
]


class BindableUi(Generic[TWidget]):
    def __init__(self, element: TWidget) -> None:
        self._element = element
        inject_handle_delete(self.element, self._on_element_delete)
        self.tailwind = Tailwind(cast(ui.element, self._element))
        self._effect_scope = new_scope()

    def _on_element_delete(self):
        self._effect_scope.dispose()

    @property
    def _ui_effect(self):
        return partial(ui_effect, scope=self._effect_scope)

    @property
    def _ui_signal_on(self):
        return partial(on, scope=self._effect_scope)

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

    def bind_prop(self, prop: str, ref_ui: TGetterOrReadonlyRef[Any]):
        """data binding is manipulating an element's property

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#bind_prop
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#bind_prop

        Args:
            prop (str): property name
            ref_ui (TGetterOrReadonlyRef[Any]): a reference to the value to bind to

        """
        if prop == "visible":
            return self.bind_visible(ref_ui)

        if prop == "text" and isinstance(self.element, TextElement):

            @self._ui_effect
            def _():
                cast(TextElement, self.element).set_text(to_value(ref_ui))
                self.element.update()

        @self._ui_effect
        def _():
            element = cast(ui.element, self.element)
            element._props[prop] = to_value(ref_ui)
            element.update()

        return self

    def bind_visible(self, ref_ui: TGetterOrReadonlyRef[bool]):
        @self._ui_effect
        def _():
            element = cast(ui.element, self.element)
            element.set_visibility(to_value(ref_ui))

        return self

    def bind_not_visible(self, ref_ui: TGetterOrReadonlyRef[bool]):
        return self.bind_visible(lambda: not to_value(ref_ui))

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
    def bind_classes(self, classes: Dict[str, TGetterOrReadonlyRef[bool]]):
        ...

    @overload
    def bind_classes(self, classes: TGetterOrReadonlyRef[Dict[str, bool]]):
        ...

    @overload
    def bind_classes(self, classes: List[TGetterOrReadonlyRef[str]]):
        ...

    @overload
    def bind_classes(self, classes: TGetterOrReadonlyRef[str]):
        ...

    def bind_classes(self, classes: _T_bind_classes_type):
        """data binding is manipulating an element's class list

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#bind-class-names
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#%E7%BB%91%E5%AE%9A%E7%B1%BB%E5%90%8D

        Args:
            classes (_T_bind_classes_type): dict of refs | ref to dict | str ref | list of refs

        ## usage

        bind class names with dict,value is bool ref, for example:

            ```python
            bg_color = to_ref(True)
            has_error = to_ref(False)

            rxui.label('Hello').bind_classes({'bg-blue':bg_color, 'text-red':has_error})
            ```

        bind list of class names with ref

            ```python
            color = to_ref('red')
            bg_color = lambda: f"bg-{color.value}"

            rxui.label('Hello').bind_classes([bg_color])
            ```

        bind single class name with ref

            ```python
            color = to_ref('red')
            bg_color = lambda: f"bg-{color.value}"

            rxui.label('Hello').bind_classes(bg_color)
            ```

        """
        if isinstance(classes, dict):
            for name, ref_obj in classes.items():

                @self._ui_effect
                def _(name=name, ref_obj=ref_obj):
                    if to_value(ref_obj):
                        self.classes(add=name)
                    else:
                        self.classes(remove=name)

        elif is_ref(classes) or isinstance(classes, Callable):
            ref_obj = to_value(classes)  # type: ignore

            if isinstance(ref_obj, dict):

                @self._ui_effect
                def _():
                    for name, value in cast(Dict, to_value(classes)).items():  # type: ignore
                        if value:
                            self.classes(add=name)
                        else:
                            self.classes(remove=name)
            else:
                self._bind_single_class(cast(_T_bind_classes_type_single, classes))

        elif isinstance(classes, list):
            for ref_name in classes:
                self._bind_single_class(ref_name)

        return self

    def _bind_single_class(self, class_name: _T_bind_classes_type_single):
        if is_ref(class_name) or isinstance(class_name, Callable):

            @on(class_name)
            def _(state: WatchedState):
                self.classes(add=state.current, remove=state.previous)
        else:
            self.classes(class_name)  # type: ignore

        return self

    def bind_style(self, style: Dict[str, TGetterOrReadonlyRef[Any]]):
        """data binding is manipulating an element's style

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#bind-style
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#bind-style

        Args:
            style (Dict[str, Union[ReadonlyRef[str], Ref[str]]]): dict of style name and ref value


        ## usage
        ```python
        bg_color = to_ref("blue")
        text_color = to_ref("red")

        rxui.label("test").bind_style(
            {
                "background-color": bg_color,
                "color": text_color,
            }
        )
        ```
        """
        if isinstance(style, dict):
            for name, ref_obj in style.items():
                if is_ref(ref_obj) or isinstance(ref_obj, Callable):

                    @self._ui_effect
                    def _(name=name, ref_obj=ref_obj):
                        self.element._style[name] = str(to_value(ref_obj))
                        self.element.update()

        return self

    def update(self):
        """Update the element on the client side."""
        self.element.update()


_T_DisableableBinder = TypeVar("_T_DisableableBinder", bound=DisableableElement)


class DisableableMixin(Protocol):
    _ui_effect: Callable[[Callable[..., Any]], signe.Effect[None]]

    @property
    def element(self) -> DisableableElement:
        ...

    def bind_enabled(self, ref_ui: TGetterOrReadonlyRef[bool]):
        @self._ui_effect
        def _():
            value = to_value(ref_ui)
            self.element.set_enabled(value)
            self.element._handle_enabled_change(value)

        return self

    def bind_disable(self, ref_ui: TGetterOrReadonlyRef[bool]):
        @self._ui_effect
        def _():
            value = not to_value(ref_ui)
            self.element.set_enabled(value)
            self.element._handle_enabled_change(value)

        return self


DisableableBindableUi = DisableableMixin
