import inspect
from typing import Any, Awaitable, Callable, Optional, Union
from weakref import WeakValueDictionary
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    TGetterOrReadonlyRef,
    to_value,
    _TMaybeRef as TMaybeRef,
)
from ex4nicegui.utils.scheduler import next_tick
from nicegui import ui, background_tasks, core
from .base import BindableUi
from ex4nicegui.reactive.mixins.value_element import ValueElementMixin


class TabPanelsBindableUi(BindableUi[ui.tab_panels], ValueElementMixin[bool]):
    def __init__(
        self,
        value: Optional[TMaybeRef[str]] = None,
        *,
        on_change: Optional[Callable[..., Any]] = None,
        animated: TMaybeRef[bool] = True,
        keep_alive: TMaybeRef[bool] = True,
    ) -> None:
        """Tab Panels

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#tab_panels
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#tab_panels

        Args:
            value (TMaybeRef[str], optional): The value of the tab panel. Defaults to None.
            on_change (Callable[..., Any], optional): The callback function when the value of the tab panel changes. Defaults to None.
            animated (TMaybeRef[bool], optional): Whether to animate the tab panel. Defaults to True.
            keep_alive (TMaybeRef[bool], optional): Whether to keep the tab panel alive. Defaults to True.
        """
        pc = ParameterClassifier(
            locals(),
            maybeRefs=["value", "animated", "keep_alive"],
            v_model=("value", "on_change"),
            events=["on_change"],
        )

        element = ui.tab_panels(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    @property
    def value(self):
        return self.element.value

    def bind_prop(self, prop: str, value: TGetterOrReadonlyRef):
        if ValueElementMixin._bind_specified_props(self, prop, value):
            return self

        return super().bind_prop(prop, value)


class lazy_tab_panel(ui.tab_panel):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._build_fn = None

    def try_run_build_fn(self):
        if self._build_fn:
            _helper.run_build_fn(self, self._props["name"])
            self._build_fn = None

    def build_fn(self, fn: Callable[..., Union[None, Awaitable]]):
        self._build_fn = fn
        return fn


class LazyTabPanelsBindableUi(TabPanelsBindableUi):
    def __init__(
        self,
        value: Optional[TMaybeRef[str]] = None,
        *,
        on_change: Optional[Callable[..., Any]] = None,
        animated: TMaybeRef[bool] = True,
        keep_alive: TMaybeRef[bool] = True,
    ) -> None:
        """Lazy Tab Panels

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#lazy_tab_panels
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#lazy_tab_panels

        Args:
            value (Optional[TMaybeRef[str]], optional): The value of the tab panel. Defaults to None.
            on_change (Optional[Callable[..., Any]], optional):  The callback function when the value of the tab panel changes. Defaults to None.
            animated (TMaybeRef[bool], optional):  Whether to animate the tab panel. Defaults to True.
            keep_alive (TMaybeRef[bool], optional):  Whether to keep the tab panel alive. Defaults to True.
        """
        super().__init__(
            value, on_change=on_change, animated=animated, keep_alive=keep_alive
        )

        self.__panels: WeakValueDictionary[str, lazy_tab_panel] = WeakValueDictionary()

        if value:

            @self._ui_effect
            def _():
                current_value = to_value(value)
                if current_value in self.__panels:
                    panel = self.__panels[current_value]

                    @next_tick
                    def _():
                        panel.try_run_build_fn()

    def add_tab_panel(self, name: str):
        def decorator(fn: Callable[..., Union[None, Awaitable]]):
            with self:
                panel = lazy_tab_panel(name)
            str_name = panel._props["name"]
            self.__panels[str_name] = panel
            panel.build_fn(fn)

            if self.value == name:
                panel.try_run_build_fn()

            return panel

        return decorator


class _helper:
    @staticmethod
    def run_build_fn(panel: lazy_tab_panel, name: str) -> None:
        """ """
        fn = panel._build_fn
        if fn is None:
            return
        try:
            expects_arguments = any(
                p.default is inspect.Parameter.empty
                and p.kind is not inspect.Parameter.VAR_POSITIONAL
                and p.kind is not inspect.Parameter.VAR_KEYWORD
                for p in inspect.signature(fn).parameters.values()
            )

            with panel:
                result = fn(name) if expects_arguments else fn()
            if isinstance(result, Awaitable):
                # NOTE: await an awaitable result even if the handler is not a coroutine (like a lambda statement)
                async def wait_for_result():
                    with panel:
                        try:
                            await result
                        except Exception as e:
                            core.app.handle_exception(e)

                if core.loop and core.loop.is_running():
                    background_tasks.create(wait_for_result(), name=str(fn))
                else:
                    core.app.on_startup(wait_for_result())
        except Exception as e:
            core.app.handle_exception(e)
