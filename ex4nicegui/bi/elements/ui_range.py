from __future__ import annotations
from nicegui import ui
from ex4nicegui import to_ref
from ex4nicegui.utils.signals import Ref
from ex4nicegui.bi.dataSource import Filter
from .models import UiResult
from typing import Any, Callable, Dict, Optional, TYPE_CHECKING, cast
from typing_extensions import TypedDict


from nicegui.elements.mixins.disableable_element import DisableableElement
from nicegui.elements.mixins.value_element import ValueElement


if TYPE_CHECKING:
    from ex4nicegui.bi.dataSourceFacade import DataSourceFacade, DataSource


class QRangeValue(TypedDict):
    min: float
    max: float


TQRangeValue = Optional[QRangeValue]


class QRange(ValueElement, DisableableElement):
    def __init__(
        self,
        *,
        min: float,  # pylint: disable=redefined-builtin
        max: float,  # pylint: disable=redefined-builtin
        step: float = 1.0,
        value: TQRangeValue = None,
        on_change: Optional[Callable[..., Any]] = None,
    ) -> None:
        """Slider

        :param min: lower bound of the slider
        :param max: upper bound of the slider
        :param step: step size
        :param value: initial value to set position of the slider
        :param on_change: callback which is invoked when the user releases the slider
        """
        super().__init__(
            tag="q-range", value=value, on_value_change=on_change, throttle=0.05
        )
        self._props["min"] = min
        self._props["max"] = max
        self._props["step"] = step


class RangeResult(UiResult[QRange]):
    def __init__(
        self,
        element: QRange,
        dataSource: DataSource,
        ref_value: Ref,
        init_data: Dict,
    ) -> None:
        super().__init__(element, dataSource)
        self._ref_value = ref_value
        self._init_data = init_data

    @property
    def value(self):
        return cast(TQRangeValue, self._ref_value.value)

    def drag_range(self):
        self.element.props("drag-range")
        return self

    def _reset_state(self):
        self._ref_value.value = self._init_data
        self.element.set_value(self._init_data)
        # self.element.update()


def ui_range(self: DataSourceFacade, column: str, **kwargs):
    self._dataSource._idataSource.slider_check(self.data, column)

    min, max = self._dataSource._idataSource.range_min_max(self.data, column)
    kwargs.update({"min": min, "max": max, "value": {"min": min, "max": max}})

    with ui.element("q-item").classes("w-full"):
        with ui.element("q-item-section").props("avatar"):
            ui.label(column)
        with ui.element("q-item-section"):
            cp = QRange(**kwargs).props("label")

    ref_value = to_ref(cast(TQRangeValue, cp.value))

    def onchange():
        self._dataSource.notify_update([result])

    cp.on("change", onchange)

    def on_source_update():
        pass
        # data = self._dataSource.get_filtered_data(cp)
        # min, max = self._dataSource._idataSource.range_min_max(data, column)
        # if min is None or max is None:
        #     cp.value = None
        # else:
        #     new_value = cast(TQRangeValue, cp.value)
        #     if new_value is not None:
        #         new_value = new_value.copy()

        #         if new_value["min"] < min:
        #             new_value["min"] = min
        #         if new_value["max"] > max:
        #             new_value["max"] = max

        #         cp.value = new_value
        #         cp.update()

    result = RangeResult(
        cp, self._dataSource, ref_value, init_data={"min": min, "max": max}
    )
    self._dataSource._register_component(cp.id, on_source_update, result)

    def data_filter(data):
        cp_value = cast(TQRangeValue, cp.value)

        if cp_value is None:
            return data
        cond = (data[column] >= cp_value["min"]) & (data[column] <= cp_value["max"])
        return data[cond]

    self._dataSource.send_filter(cp.id, Filter(data_filter))

    return result
