from typing import Any, TypeVar, Generic, cast, Dict, Union, overload
from typing_extensions import Self
from signe import createSignal, effect
from ex4nicegui.utils.signals import ReadonlyRef, Ref
from nicegui import ui
from nicegui.elements.mixins.text_element import TextElement
from nicegui.elements.mixins.value_element import ValueElement
from nicegui.elements.mixins.color_elements import (
    TextColorElement,
    QUASAR_COLORS,
    TAILWIND_COLORS,
)
from nicegui.page_layout import Drawer

T = TypeVar("T")

TWidget = TypeVar("TWidget")


class RefUi(Ref[T], Generic[T, TWidget]):
    def __init__(self, value: T, element: TWidget) -> None:
        getter, setter = createSignal(value)
        super().__init__(getter, setter)
        self.__element = element

    @property
    def element(self):
        return self.__element


class BindableUi(RefUi[T, TWidget]):
    def __init__(self, value: T, element: TWidget) -> None:
        super().__init__(value, element)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "visible":
            return self.bind_visible(ref_ui)

        @effect
        def _():
            element = cast(ui.element, self.element)
            element._props[prop] = ref_ui.value
            element.update()

        return self

    def bind_visible(self, ref_ui: ReadonlyRef[bool]):
        @effect
        def _():
            element = cast(ui.element, self.element)
            element.set_visibility(ref_ui.value)

        return self


def _bind_color(bindable_ui: BindableUi, ref_ui: ReadonlyRef):
    @effect
    def _():
        ele = cast(TextColorElement, bindable_ui.element)
        color = ref_ui.value

        if color in QUASAR_COLORS:
            ele._props[ele.TEXT_COLOR_PROP] = color
        elif color in TAILWIND_COLORS:
            ele.classes(replace=f"text-{color}")
        elif color is not None:
            ele._style["color"] = color
        ele.update()

    return bindable_ui


class TextColorElementBindableUi(BindableUi[T, TWidget]):
    def __init__(self, value: T, element: TWidget) -> None:
        super().__init__(value, element)

        ele = cast(TextColorElement, element)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "name":
            return self.bind_name(ref_ui)

        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: ReadonlyRef):
        return _bind_color(self, ref_ui)

    def bind_name(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            ele = cast(TextColorElement, self.element)
            ele._props["name"] = ref_ui.value
            ele.update()

        return self


class ValueElementBindableUi(BindableUi[T, TWidget]):
    @staticmethod
    def _setup_normal(bui: "ValueElementBindableUi"):
        def onValueChanged(args):
            bui.value = args["args"]

        ele = cast(ValueElement, bui.element)

        @effect
        def _():
            ele.value = bui.value

        ele.on("update:modelValue", handler=onValueChanged)

    @staticmethod
    def _setup_select(bui: "ValueElementBindableUi"):
        def onValueChanged(args):
            bui.value = args["args"]["label"]

        @effect
        def _():
            bui.element.value = bui.value

        bui.element.on("update:modelValue", handler=onValueChanged)

    @staticmethod
    def _setup_radio(bui: "ValueElementBindableUi"):
        def onValueChanged(args):
            bui.value = bui.element.options[args["args"]]

        @effect
        def _():
            bui.element.value = bui.value

        bui.element.on("update:modelValue", handler=onValueChanged)

    def __init__(self, value: T, element: TWidget) -> None:
        super().__init__(value, element)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_text(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_text(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            cast(ValueElement, self.element).on_value_change(ref_ui.value)

        return self


class TextElementBindableUi(BindableUi[str, TWidget]):
    def __init__(self, value: str, element: TWidget) -> None:
        super().__init__(value, element)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "text":
            return self.bind_text(ref_ui)

        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            ele = cast(ui.label, self.element)
            color = ref_ui.value
            ele._style["color"] = color
            ele.update()

    def bind_text(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            cast(TextElement, self.element).on_text_change(str(ref_ui.value))

        return self


_TAggridValue = Dict


class AggridBindableUi(BindableUi[_TAggridValue, ui.aggrid]):
    def __init__(self, value: _TAggridValue, element: ui.aggrid) -> None:
        super().__init__(value, element)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "options":
            return self.bind_options(ref_ui)

        return super().bind_prop(prop, ref_ui)

    @overload
    def bind_options(self, ref_ui: ReadonlyRef[Dict]) -> Self:
        ...

    @overload
    def bind_options(self, ref_ui: ReadonlyRef) -> Self:
        ...

    def bind_options(self, ref_ui: ReadonlyRef):
        import pandas as pd

        @effect
        def _():
            ele = self.element

            data = ref_ui.value
            if isinstance(data, pd.DataFrame):
                columnDefs = [{"headerName": col, "field": col} for col in data.columns]

                for col in data.select_dtypes(["datetime"]).columns:
                    data[col] = data[col].dt.strftime("%Y-%m-%d")

                rowData = data.to_dict("records")

                data = {"columnDefs": columnDefs, "rowData": rowData}

            ele._props["options"].update(data)

            ele.update()

        return self


class DrawerBindableUi(BindableUi[bool, Drawer]):
    def __init__(self, value: bool, element: Drawer) -> None:
        super().__init__(value, element)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)
