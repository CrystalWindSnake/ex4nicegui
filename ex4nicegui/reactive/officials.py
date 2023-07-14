from __future__ import annotations
import asyncio

from typing import (
    Any,
    Callable,
    List,
    Optional,
    TypeVar,
    Generic,
    cast,
    Dict,
    Union,
    overload,
)
from typing_extensions import Literal, Self
from signe import effect
from ex4nicegui.utils.signals import (
    ReadonlyRef,
    Ref,
    ref_computed,
    to_ref,
    to_value,
    is_ref,
    _TMaybeRef as TMaybeRef,
)
import ex4nicegui.utils.common as utils_common
from nicegui import ui
from nicegui.elements.mixins.text_element import TextElement
from nicegui.elements.mixins.value_element import ValueElement
from nicegui.elements.mixins.color_elements import (
    TextColorElement,
    QUASAR_COLORS,
    TAILWIND_COLORS,
)
from nicegui.page_layout import Drawer
from ex4nicegui.reactive.echarts.ECharts import echarts

T = TypeVar("T")

TWidget = TypeVar("TWidget")


class BindableUi(Generic[TWidget]):
    def __init__(self, element: TWidget) -> None:
        self.__element = element

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


class SingleValueBindableUi(BindableUi[TWidget], Generic[T, TWidget]):
    def __init__(self, value: TMaybeRef[T], element: TWidget) -> None:
        super().__init__(element)
        self._ref = to_ref(value)

    @property
    def value(self) -> T:
        return self._ref.value

    def bind_ref(self, ref: Ref[T]):
        @effect
        def _():
            ref.value = self._ref.value

        return self


def _bind_color(bindable_ui: SingleValueBindableUi, ref_ui: ReadonlyRef):
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


class TextColorElementBindableUi(SingleValueBindableUi[T, TWidget]):
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


def _convert_kws_ref2value(kws: Dict):
    return {key: to_value(value) for key, value in kws.items()}


class SelectBindableUi(SingleValueBindableUi[T, ui.select]):
    @staticmethod
    def _setup_(binder: "SelectBindableUi"):
        def onValueChanged(args):
            binder._ref.value = args["args"]["label"]  # type: ignore

        @effect
        def _():
            binder.element.value = binder.value

        binder.element.on("update:modelValue", handler=onValueChanged)

    def __init__(
        self,
        options: Union[TMaybeRef[List], TMaybeRef[Dict]],
        *,
        label: Optional[TMaybeRef[str]] = None,
        value: TMaybeRef[Any] = None,
        on_change: Optional[Callable[..., Any]] = None,
        with_input: TMaybeRef[bool] = False,
        multiple: TMaybeRef[bool] = False,
        clearable: TMaybeRef[bool] = False,
    ) -> None:
        kws = {
            "options": options,
            "label": label,
            "value": value,
            "on_change": on_change,
            "with_input": with_input,
            "multiple": multiple,
            "clearable": clearable,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.select(**value_kws)
        element.classes("min-w-[10rem]")

        super().__init__(value, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)

        SelectBindableUi._setup_(self)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_text(ref_ui)

        if prop == "options":
            return self.bind_options(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_options(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            self.element.options = ref_ui.value
            self.element.update()

        return self

    def bind_text(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            cast(ValueElement, self.element).on_value_change(ref_ui.value)

        return self


class RadioBindableUi(SingleValueBindableUi[bool, ui.radio]):
    @staticmethod
    def _setup_(binder: "RadioBindableUi"):
        def onValueChanged(args):
            binder._ref.value = binder.element.options[args["args"]]  # type: ignore

        @effect
        def _():
            binder.element.value = binder.value

        binder.element.on("update:modelValue", handler=onValueChanged)

    def __init__(
        self,
        options: Union[TMaybeRef[List], TMaybeRef[Dict]],
        *,
        value: TMaybeRef[Any] = None,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        kws = {"options": options, "value": value, "on_change": on_change}

        value_kws = _convert_kws_ref2value(kws)

        element = ui.radio(**value_kws)

        super().__init__(value, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)

        RadioBindableUi._setup_(self)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        if prop == "options":
            return self.bind_options(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_options(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            self.element.options = ref_ui.value
            self.element.update()

        return self

    def bind_value(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            cast(ValueElement, self.element).on_value_change(ref_ui.value)

        return self


class SwitchBindableUi(SingleValueBindableUi[bool, ui.switch]):
    @staticmethod
    def _setup_(binder: "SwitchBindableUi"):
        def onValueChanged(args):
            binder._ref.value = args["args"]  # type: ignore

        ele = cast(ValueElement, binder.element)

        @effect
        def _():
            ele.value = binder.value

        ele.on("update:modelValue", handler=onValueChanged)

    def __init__(
        self,
        text: TMaybeRef[str] = "",
        *,
        value: TMaybeRef[bool] = False,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        kws = {"text": text, "value": value, "on_change": on_change}

        value_kws = _convert_kws_ref2value(kws)

        element = ui.switch(**value_kws)

        super().__init__(value, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

        SwitchBindableUi._setup_(self)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: ReadonlyRef[bool]):
        @effect
        def _():
            self.element.on_value_change(ref_ui.value)

        return self


class CheckboxBindableUi(SingleValueBindableUi[bool, ui.checkbox]):
    @staticmethod
    def _setup_(binder: "CheckboxBindableUi"):
        def onValueChanged(args):
            binder._ref.value = args["args"]  # type: ignore

        ele = cast(ValueElement, binder.element)

        @effect
        def _():
            ele.value = binder.value

        ele.on("update:modelValue", handler=onValueChanged)

    def __init__(
        self,
        text: str = "",
        *,
        value: bool = False,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        kws = {"text": text, "value": value, "on_change": on_change}

        value_kws = _convert_kws_ref2value(kws)

        element = ui.checkbox(**value_kws)

        super().__init__(value, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

        CheckboxBindableUi._setup_(self)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: ReadonlyRef[bool]):
        @effect
        def _():
            self.element.on_value_change(ref_ui.value)

        return self


class InputBindableUi(SingleValueBindableUi[str, ui.input]):
    def __init__(
        self,
        label: Optional[TMaybeRef[str]] = None,
        *,
        placeholder: Optional[TMaybeRef[str]] = None,
        value: TMaybeRef[str] = "",
        password: TMaybeRef[bool] = False,
        password_toggle_button: TMaybeRef[bool] = False,
        on_change: Optional[Callable[..., Any]] = None,
        autocomplete: Optional[TMaybeRef[List[str]]] = None,
        validation: Dict[str, Callable[..., bool]] = {},
    ) -> None:
        kws = {
            "label": label,
            "placeholder": placeholder,
            "value": value,
            "password": password,
            "password_toggle_button": password_toggle_button,
            "autocomplete": autocomplete,
            "validation": validation,
            "on_change": on_change,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.input(**value_kws)

        super().__init__(value, element)

        for key, value in kws.items():
            if is_ref(value) and key != "value":
                self.bind_prop(key, value)  # type: ignore

        self._ex_setup()

    def _ex_setup(self):
        ele = self.element

        @effect
        def _():
            ele.value = self.value

        def onModelValueChanged(args):
            self._ref.value = args["args"] or ""  # type: ignore

        ele.on("update:modelValue", handler=onModelValueChanged)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: ReadonlyRef[bool]):
        @effect
        def _():
            self.element.on_value_change(ref_ui.value)

        return self


class LazyInputBindableUi(InputBindableUi):
    def __init__(
        self,
        label: Optional[TMaybeRef[str]] = None,
        *,
        placeholder: Optional[TMaybeRef[str]] = None,
        value: TMaybeRef[str] = "",
        password: TMaybeRef[bool] = False,
        password_toggle_button: TMaybeRef[bool] = False,
        on_change: Optional[Callable[..., Any]] = None,
        autocomplete: Optional[TMaybeRef[List[str]]] = None,
        validation: Dict[str, Callable[..., bool]] = {},
    ) -> None:
        super().__init__(
            label,
            placeholder=placeholder,
            value=value,
            password=password,
            password_toggle_button=password_toggle_button,
            on_change=on_change,
            autocomplete=autocomplete,
            validation=validation,
        )

    def _ex_setup(self):
        ele = self.element

        @effect
        def _():
            ele.value = self.value

        def onValueChanged():
            self._ref.value = ele.value or ""

        ele.on("blur", onValueChanged)
        ele.on("keyup.enter", onValueChanged)


_TSliderValue = TypeVar("_TSliderValue", float, int)


class SliderBindableUi(SingleValueBindableUi[Optional[_TSliderValue], ui.slider]):
    def __init__(
        self,
        min: TMaybeRef[_TSliderValue],
        max: TMaybeRef[_TSliderValue],
        step: TMaybeRef[_TSliderValue] = 1.0,
        value: Optional[TMaybeRef[_TSliderValue]] = None,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        kws = {
            "min": min,
            "max": max,
            "step": step,
            "value": value,
            "on_change": on_change,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.slider(**value_kws).props("label label-always switch-label-side")

        super().__init__(value, element)  # type: ignore

        for key, value in kws.items():
            if is_ref(value) and key != "value":
                self.bind_prop(key, value)  # type: ignore

        self._ex_setup()

    def _ex_setup(self):
        ele = self.element

        @effect
        def _():
            ele.value = self.value

        def onModelValueChanged(args):
            self._ref.value = args["args"]  # type: ignore

        ele.on("update:modelValue", handler=onModelValueChanged)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: ReadonlyRef[float]):
        @effect
        def _():
            self.element.on_value_change(ref_ui.value)

        return self


class LazySliderBindableUi(SliderBindableUi):
    def __init__(
        self,
        min: TMaybeRef[float],
        max: TMaybeRef[float],
        step: TMaybeRef[float] = 1,
        value: TMaybeRef[float | None] = None,
        on_change: Callable[..., Any] | None = None,
    ) -> None:
        super().__init__(min, max, step, value, on_change)

    def _ex_setup(self):
        ele = self.element

        @effect
        def _():
            ele.value = self.value

        def onValueChanged():
            self._ref.value = ele.value

        ele.on("change ", onValueChanged)


class TextareaBindableUi(SingleValueBindableUi[str, ui.textarea]):
    def __init__(
        self,
        label: Optional[TMaybeRef[str]] = None,
        *,
        placeholder: Optional[TMaybeRef[str]] = None,
        value: TMaybeRef[str] = "",
        on_change: Optional[Callable[..., Any]] = None,
        validation: Dict[str, Callable[..., bool]] = {},
    ) -> None:
        kws = {
            "label": label,
            "placeholder": placeholder,
            "value": value,
            "validation": validation,
            "on_change": on_change,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.textarea(**value_kws)

        super().__init__(value, element)

        for key, value in kws.items():
            if is_ref(value) and key != "value":
                self.bind_prop(key, value)  # type: ignore

        self._ex_setup()

    def _ex_setup(self):
        ele = self.element

        @effect
        def _():
            ele.value = self.value

        def onModelValueChanged(args):
            self._ref.value = args["args"]  # type: ignore

        ele.on("update:modelValue", handler=onModelValueChanged)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: ReadonlyRef[bool]):
        @effect
        def _():
            self.element.on_value_change(ref_ui.value)

        return self


class LazyTextareaBindableUi(TextareaBindableUi):
    def __init__(
        self,
        label: Optional[TMaybeRef[str]] = None,
        *,
        placeholder: Optional[TMaybeRef[str]] = None,
        value: TMaybeRef[str] = "",
        on_change: Optional[Callable[..., Any]] = None,
        validation: Dict[str, Callable[..., bool]] = {},
    ) -> None:
        super().__init__(
            label,
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            validation=validation,
        )

    def _ex_setup(self):
        ele = self.element

        @effect
        def _():
            ele.value = self.value

        def onValueChanged():
            self._ref.value = ele.value

        ele.on("blur", onValueChanged)
        ele.on("keyup.enter", onValueChanged)


class LabelBindableUi(SingleValueBindableUi[str, ui.label]):
    @staticmethod
    def _setup_(binder: "LabelBindableUi"):
        def onValueChanged(args):
            binder._ref.value = args["args"]["label"]  # type: ignore

        @effect
        def _():
            binder.element.text = binder.value

        binder.element.on("update:modelValue", handler=onValueChanged)

    def __init__(
        self,
        text: TMaybeRef[str] = "",
    ) -> None:
        kws = {
            "text": text,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.label(**value_kws)

        super().__init__(text, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

        LabelBindableUi._setup_(self)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "text":
            return self.bind_text(ref_ui)

        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            ele = self.element
            color = ref_ui.value
            ele._style["color"] = color
            ele.update()

    def bind_text(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            self.element.on_text_change(str(ref_ui.value))
            # self.element.update()

        return self


class IconBindableUi(SingleValueBindableUi[str, ui.icon]):
    def __init__(
        self,
        name: TMaybeRef[str],
        *,
        size: Optional[TMaybeRef[str]] = None,
        color: Optional[TMaybeRef[str]] = None,
    ) -> None:
        kws = {
            "name": name,
            "size": size,
            "color": color,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.icon(**value_kws)

        super().__init__(name, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

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


class ButtonBindableUi(SingleValueBindableUi[str, ui.button]):
    def __init__(
        self,
        text: TMaybeRef[str] = "",
        *,
        on_click: Optional[Callable[..., Any]] = None,
        color: Optional[TMaybeRef[str]] = "primary",
        icon: Optional[TMaybeRef[str]] = None,
    ) -> None:
        kws = {
            "text": text,
            "color": color,
            "icon": icon,
            "on_click": on_click,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.button(**value_kws)

        super().__init__(text, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "text":
            return self.bind_text(ref_ui)
        if prop == "icon":
            return self.bind_icon(ref_ui)
        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: ReadonlyRef):
        return _bind_color(self, ref_ui)

    def bind_text(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            ele = self.element
            ele._props["text"] = ref_ui.value
            ele.update()

        return self

    def bind_icon(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            ele = self.element
            ele._props["icon"] = ref_ui.value
            ele.update()

        return self


class ColorPickerBindableUi(SingleValueBindableUi[str, ui.color_picker]):
    def __init__(
        self,
        color: TMaybeRef[str] = "",
        *,
        on_pick: Optional[Callable[..., Any]] = None,
        value: TMaybeRef[bool] = False,
    ) -> None:
        kws = {
            "value": value,
            "on_pick": on_pick,
        }

        value_kws = _convert_kws_ref2value(kws)

        with ui.card().tight():
            element_menu = ui.color_picker(**value_kws)
            self._element_picker = element_menu.default_slot.children[0]
            self._element_picker.props(f'format-model="rgba"')

            ui.button(on_click=element_menu.open, icon="colorize")

        super().__init__(color, element_menu)

        for key, value in kws.items():
            if is_ref(value) and key != "color":
                self.bind_prop(key, value)  # type: ignore

        self._ex_setup()

    def _ex_setup(self):
        ele = self._element_picker

        @effect
        def _():
            ele._props["modelValue"] = self.value

        def onModelValueChanged(args):
            self._ref.value = args["args"]  # type: ignore

        ele.on("update:modelValue", handler=onModelValueChanged)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: ReadonlyRef[str]):
        @effect
        def _():
            self._element_picker._props["modelValue"] = ref_ui.value

        return self

    def bind_value(self, ref_ui: ReadonlyRef[bool]):
        @effect
        def _():
            self._element_picker._props["value"] = ref_ui.value

        return self


class ColorPickerLazyBindableUi(ColorPickerBindableUi):
    def __init__(
        self,
        color: TMaybeRef[str] = "",
        *,
        on_pick: Callable[..., Any] | None = None,
        value: TMaybeRef[bool] = False,
    ) -> None:
        super().__init__(color, on_pick=on_pick, value=value)

    def _ex_setup(self):
        ele = self._element_picker

        # @effect
        # def _():
        #     ele._props["modelValue"] = self.value

        def onModelValueChanged(args):
            self._ref.value = args["args"]  # type: ignore

        ele.on("change", handler=onModelValueChanged)


_TAggridValue = Dict


class AggridBindableUi(BindableUi[ui.aggrid]):
    def __init__(
        self,
        options: TMaybeRef[Dict],
        *,
        html_columns: TMaybeRef[List[int]] = [],
        theme: TMaybeRef[str] = "balham",
    ) -> None:
        kws = {
            "options": options,
            "html_columns": html_columns,
            "theme": theme,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.aggrid(**value_kws)

        super().__init__(element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    @staticmethod
    def from_pandas(df: TMaybeRef):
        if is_ref(df):

            @ref_computed
            def cp_convert_df():
                return utils_common.convert_dataframe(df.value)

            @ref_computed
            def cp_options():
                columnDefs = [
                    {"headerName": col, "field": col}
                    for col in cp_convert_df.value.columns
                ]
                rowData = cp_convert_df.value.to_dict("records")
                data = {"columnDefs": columnDefs, "rowData": rowData}
                return data

            return AggridBindableUi(cp_options)

        columnDefs = [{"headerName": col, "field": col} for col in df.columns]  # type: ignore
        rowData = df.to_dict("records")  # type: ignore
        options = {"columnDefs": columnDefs, "rowData": rowData}
        return AggridBindableUi(options)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "options":
            return self.bind_options(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_options(self, ref_ui: ReadonlyRef[List[Dict]]):
        @effect
        def _():
            ele = self.element
            data = ref_ui.value
            ele._props["options"].update(data)
            ele.update()

        return self


class TableBindableUi(BindableUi[ui.table]):
    def __init__(
        self,
        columns: TMaybeRef[List[Dict]],
        rows: TMaybeRef[List[Dict]],
        row_key: TMaybeRef[str] = "id",
        title: Optional[TMaybeRef[str]] = None,
        selection: Optional[TMaybeRef[Literal["single", "multiple"]]] = None,
        pagination: Optional[TMaybeRef[int]] = 15,
        on_select: Optional[Callable[..., Any]] = None,
    ) -> None:
        kws = {
            "columns": columns,
            "rows": rows,
            "row_key": row_key,
            "title": title,
            "selection": selection,
            "pagination": pagination,
            "on_select": on_select,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.table(**value_kws)

        super().__init__(element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    @staticmethod
    def from_pandas(df: TMaybeRef):
        if is_ref(df):

            @ref_computed
            def cp_convert_df():
                return utils_common.convert_dataframe(df.value)

            @ref_computed
            def cp_rows():
                return cp_convert_df.value.to_dict("records")

            @ref_computed
            def cp_cols():
                return [
                    {
                        "name": col,
                        "label": col,
                        "field": col,
                    }
                    for col in cp_convert_df.value.columns
                ]

            return TableBindableUi(cp_cols, cp_rows)

        df = utils_common.convert_dataframe(df)
        rows = df.to_dict("records")

        cols = [
            {
                "name": col,
                "label": col,
                "field": col,
            }
            for col in df.columns
        ]
        return TableBindableUi(cols, rows)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "dataframe":
            return self.bind_dataframe(ref_ui)

        if prop == "rows":
            return self.bind_rows(ref_ui)

        if prop == "columns":
            return self.bind_columns(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_dataframe(self, ref_df: ReadonlyRef):
        @ref_computed
        def cp_converted_df():
            df = ref_df.value
            return utils_common.convert_dataframe(df)

        @ref_computed
        def cp_rows():
            return cp_converted_df.value.to_dict("records")

        @ref_computed
        def cp_cols():
            return [
                {
                    "name": col,
                    "label": col,
                    "field": col,
                }
                for col in cp_converted_df.value.columns
            ]

        self.bind_rows(cp_rows).bind_columns(cp_cols)

        return self

    def bind_rows(self, ref_ui: ReadonlyRef[List[Dict]]):
        @effect
        def _():
            ele = self.element
            ele._props["rows"] = ref_ui.value
            ele.update()

        return self

    def bind_columns(self, ref_ui: ReadonlyRef[List[Dict]]):
        @effect
        def _():
            ele = self.element
            ele._props["columns"] = ref_ui.value
            ele.update()

        return self


class DrawerBindableUi(SingleValueBindableUi[bool, Drawer]):
    def __init__(self, value: bool, element: Drawer) -> None:
        super().__init__(value, element)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)


class EChartsBindableUi(BindableUi[echarts]):
    def __init__(
        self,
        options: TMaybeRef[Dict],
    ) -> None:
        kws = {
            "options": options,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = echarts(**value_kws)

        super().__init__(element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    @staticmethod
    def _pyecharts2opts(chart):
        import simplejson as json
        from pyecharts.charts.chart import Base

        if isinstance(chart, Base):
            return json.loads(chart.dump_options())

        return {}

    @staticmethod
    def from_pyecharts(chart: TMaybeRef):
        if is_ref(chart):

            @ref_computed
            def chart_opt():
                return EChartsBindableUi._pyecharts2opts(chart.value)

            return EChartsBindableUi(chart_opt)

        return EChartsBindableUi(EChartsBindableUi._pyecharts2opts(chart))

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "options":
            return self.bind_options(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_options(self, ref_ui: ReadonlyRef[Dict]):
        @effect
        def _():
            ele = self.element
            ele.update_options(ref_ui.value)
            ele.update()

        return self


class RowBindableUi(BindableUi[ui.row]):
    def __init__(
        self,
    ) -> None:
        element = ui.row()

        super().__init__(element)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)


class CardBindableUi(BindableUi[ui.card]):
    def __init__(
        self,
    ) -> None:
        element = ui.card()

        super().__init__(element)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)

    def tight(self):
        """Removes padding and gaps between nested elements."""
        self.element._classes.clear()
        self.element._style.clear()
        return self


class CardSectionBindableUi(BindableUi[ui.card_section]):
    def __init__(
        self,
    ) -> None:
        element = ui.card_section()

        super().__init__(element)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)


class CardActionsBindableUi(BindableUi[ui.card_actions]):
    def __init__(
        self,
    ) -> None:
        element = ui.card_actions()

        super().__init__(element)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)


class HtmlBindableUi(SingleValueBindableUi[str, ui.html]):
    @staticmethod
    def _setup_(binder: "HtmlBindableUi"):
        first = True

        @effect
        def _():
            nonlocal first

            async def task():
                pass
                await ui.run_javascript(
                    f"getElement({binder.element.id}).innerText= '{binder.value}' ",
                    respond=False,
                )

            if not first:
                asyncio.run(task())
            else:
                first = False

    def __init__(
        self,
        content: TMaybeRef[str] = "",
    ) -> None:
        kws = {
            "content": content,
        }

        value_kws = _convert_kws_ref2value(kws)

        element = ui.html(**value_kws)

        super().__init__(content, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

        HtmlBindableUi._setup_(self)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            ele = self.element
            color = ref_ui.value
            ele._style["color"] = color
            ele.update()
