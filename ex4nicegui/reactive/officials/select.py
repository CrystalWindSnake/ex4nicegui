from typing import (
    Any,
    Callable,
    List,
    Optional,
    TypeVar,
    cast,
    Dict,
    Union,
)

from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    _TMaybeRef as TMaybeRef,
    effect,
)
from nicegui import ui
from nicegui.elements.mixins.value_element import ValueElement
from .base import SingleValueBindableUi
from .utils import _convert_kws_ref2value

T = TypeVar("T")


class SelectBindableUi(SingleValueBindableUi[T, ui.select]):
    @staticmethod
    def _setup_(binder: "SelectBindableUi"):
        def onValueChanged(e):
            binder._ref.value = binder.element._event_args_to_value(e)  # type: ignore

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
        **kwargs
    ) -> None:
        """Dropdown Selection

        The options can be specified as a list of values, or as a dictionary mapping values to labels.
        After manipulating the options, call `update()` to update the options in the UI.

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        :param with_input: whether to show an input field to filter the options
        :param multiple: whether to allow multiple selections
        :param clearable: whether to add a button to clear the selection
        """
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

        value_kws.update(kwargs)

        element = ui.select(**value_kws)
        element.classes("min-w-[10rem]")

        super().__init__(value, element)

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)

        SelectBindableUi._setup_(self)

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
            cast(ValueElement, self.element).set_value(ref_ui.value)
            self.element.update()

        return self
