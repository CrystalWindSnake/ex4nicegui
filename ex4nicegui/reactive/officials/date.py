from typing import Any, Callable, List, Optional, TypeVar
from typing_extensions import TypedDict
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.reactive.mixins.value_element import ValueElementMixin

from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import BindableUi


_TDateRange = TypedDict("_TDateRange", {"from": str, "to": str})

_TDateValue = TypeVar(
    "_TDateValue", str, List[str], _TDateRange, List[_TDateRange], None
)


class DateBindableUi(BindableUi[ui.date], ValueElementMixin[_TDateValue]):
    def __init__(
        self,
        value: Optional[TMaybeRef[_TDateValue]] = None,
        *,
        mask: TMaybeRef[str] = "YYYY-MM-DD",
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        """Date Input

        This element is based on Quasar's `QDate <https://quasar.dev/vue-components/date>`_ component.
        The date is a string in the format defined by the `mask` parameter.

        You can also use the `range` or `multiple` props to select a range of dates or multiple dates::

            ui.date({'from': '2023-01-01', 'to': '2023-01-05'}).props('range')
            ui.date(['2023-01-01', '2023-01-02', '2023-01-03']).props('multiple')
            ui.date([{'from': '2023-01-01', 'to': '2023-01-05'}, '2023-01-07']).props('multiple range')

        :param value: the initial date
        :param mask: the format of the date string (default: 'YYYY-MM-DD')
        :param on_change: callback to execute when changing the date
        """
        pc = ParameterClassifier(
            locals(),
            maybeRefs=[
                "value",
                "mask",
            ],
            v_model=("value", "on_change"),
            events=["on_change"],
        )

        value_kws = pc.get_values_kws()
        element = ui.date(**value_kws)
        super().__init__(element)  # type: ignore

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if ValueElementMixin._bind_specified_props(self, prop, value):
            return self

        return super().bind_prop(prop, value)
