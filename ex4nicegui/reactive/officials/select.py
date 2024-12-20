from typing import (
    Any,
    Callable,
    List,
    Optional,
    TypeVar,
    Dict,
    Union,
)
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    _TMaybeRef as TMaybeRef,
    to_value,
    to_raw,
)
from nicegui import ui
from .base import BindableUi

T = TypeVar("T")


class SelectBindableUi(BindableUi[ui.select]):
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
        **kwargs,
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
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "options",
                "label",
                "value",
                "with_input",
                "multiple",
                "clearable",
            ],
            v_model=("value", "on_change"),
            events=["on_change"],
            extend_kws="kwargs",
        )

        value_kws = pc.get_values_kws()

        element = ui.select(**value_kws)
        super().__init__(element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if prop == "value":
            return self.bind_value(value)

        if prop == "options":
            return self.bind_options(value)

        return super().bind_prop(prop, value)

    def bind_options(self, options: TGetterOrReadonlyRef):
        @self._ui_signal_on(options, deep=True)
        def _():
            self.element.set_options(to_value(options))

        return self

    def bind_value(self, value: TGetterOrReadonlyRef):
        @self._ui_signal_on(value, deep=True)
        def _():
            ParameterClassifier.mark_event_source_as_internal(self.element)
            self.element.set_value(to_raw(to_value(value)) or None)

        return self
