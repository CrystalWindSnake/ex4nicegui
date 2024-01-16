from typing import Any, Callable, List, Optional, TypeVar, cast
from typing_extensions import TypedDict

from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    _TMaybeRef as TMaybeRef,
    effect,
    to_ref,
)
from nicegui import ui
from .base import SingleValueBindableUi
from .utils import _convert_kws_ref2value


_TDateRange = TypedDict("_TDateRange", {"from": str, "to": str})

_TDateValue = TypeVar(
    "_TDateValue", str, List[str], _TDateRange, List[_TDateRange], None
)


class DateBindableUi(SingleValueBindableUi[_TDateValue, ui.date]):
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
        value_ref = to_ref(value)
        kws = {
            "value": value_ref,
            "mask": mask,
            "on_change": on_change,
        }

        value_kws = _convert_kws_ref2value(kws)

        def inject_on_change(e):
            value_ref.value = e.value
            if on_change:
                on_change(e)

        value_kws.update({"on_change": inject_on_change})

        element = ui.date(**value_kws)

        super().__init__(value_ref, element)  # type: ignore

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_value(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_value(self, ref_ui: ReadonlyRef[bool]):
        @effect
        def _():
            self.element.set_value(ref_ui.value)
            self.element.update()

        return self
