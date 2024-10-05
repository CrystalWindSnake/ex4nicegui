import inspect
from typing import Awaitable, Callable, Union
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier
from ex4nicegui.utils.signals import (
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui, background_tasks, core
from .base import BindableUi


class TabPanelBindableUi(BindableUi[ui.tab_panel]):
    def __init__(
        self,
        name: TMaybeRef[str],
    ) -> None:
        pc = ParameterClassifier(
            locals(),
            maybeRefs=["name"],
        )

        element = ui.tab_panel(**pc.get_values_kws())
        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore


class lazy_tab_panel(TabPanelBindableUi):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._build_fn = None

    def try_run_build_fn(self):
        if self._build_fn:
            _helper.run_build_fn(self, self.element._props["name"])
            self._build_fn = None

    def build_fn(self, fn: Callable[..., Union[None, Awaitable]]):
        self._build_fn = fn
        return fn


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
