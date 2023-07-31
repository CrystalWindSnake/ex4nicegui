from typing import (
    Dict,
)
from signe import effect
from ex4nicegui.utils.signals import (
    ReadonlyRef,
    is_ref,
    ref_computed,
    _TMaybeRef as TMaybeRef,
)
from .base import BindableUi
from .utils import _convert_kws_ref2value
from ex4nicegui.reactive.EChartsComponent.ECharts import echarts


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
