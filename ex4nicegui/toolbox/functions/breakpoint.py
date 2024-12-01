from __future__ import annotations
from typing import Callable, Dict, Optional
from ex4nicegui import to_ref, ref_computed
from ex4nicegui.toolbox.core.vue_use import VueUse
from nicegui import app


class UseBreakpoints:
    def __init__(
        self,
        options: Optional[Dict] = None,
        *,
        immediate_trigger: bool = True,
        on_value_change: Optional[Callable[[str], None]] = None,
    ):
        """monitor viewport breakpoints.

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#use_breakpoints

        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#use_breakpoints

        Args:
            options (Optional[Dict], optional): the configuration for each breakpoint. The default is the configuration from Quasar v3. Defaults to None.
            immediate_trigger (bool, optional): whether to trigger the breakpoint change immediately. Defaults to True.
            on_value_change (Optional[Callable[[str], None]], optional): callback function to be called when the breakpoint changes. Defaults to None.

        Example:
        .. code-block:: python
            from ex4nicegui import toolbox as tb

            options = {"mobile": 0, "tablet": 640, "laptop": 1024, "desktop": 1280}
            tb.use_breakpoints(options, on_value_change=lambda breakpoint: print(breakpoint))

        """
        options = options or {"xs": 0, "sm": 600, "md": 1024, "lg": 1440, "xl": 1920}

        self._vue_use = VueUse("useBreakpoints", args=[options])

        if on_value_change:
            self.on_value_change(on_value_change)

        if immediate_trigger:

            @app.on_connect
            async def on_connect():
                value = await self.get_active()
                self._vue_use.trigger_event("active", value)

    @property
    def reactivity(self) -> BreakpointReactivity:
        """reactive breakpoint properties."""
        return BreakpointReactivity(self)

    async def get_active(self):
        """the current breakpoint value."""
        return await self._vue_use.run_method("active")

    async def get_between(self, start: str, end: str):
        """whether the current breakpoint is between the start and end values.

        Args:
            start (str): Detect the start value of the range.
            end (str): Detect the end value of the range. not including.

        Returns:
            bool: True or False
        """
        return await self._vue_use.run_method("between", start, end)

    def on_value_change(self, callback: Callable[[str], None]):
        """register a callback function to be called when the breakpoint changes.

        Args:
            callback (Callable[[str], None]): the callback function to be called.
        """
        self._vue_use.on_event("active", callback)


class BreakpointReactivity:
    _BETWEEN_NUM = 0

    def __init__(self, use_breakpoints: UseBreakpoints):
        self.__use_breakpoints = use_breakpoints

    def active(self):
        """the current breakpoint value."""
        result = to_ref("")

        self.__use_breakpoints.on_value_change(lambda value: result.set_value(value))
        return result

    def __create_between_event_name(self):
        self._BETWEEN_NUM += 1
        return "between_" + str(self._BETWEEN_NUM)

    def between(self, start: str, end: str):
        """whether the current breakpoint is between the start and end values.

        Args:
            start (str): the start value.
            end (str): the end value. not including.

        Example:
        .. code-block:: python
            options = {"mobile": 0, "tablet": 640, "laptop": 1024, "desktop": 1280}
            bp = tb.use_breakpoints(options)

            # Not included "laptop"
            is_between = bp.reactivity.between("mobile", "laptop")

            # True or False
            is_between.value

        """
        result = to_ref(False)

        event_name = self.__create_between_event_name()

        self.__use_breakpoints._vue_use.run_method(
            "betweenReactively", start, end, event_name
        )
        self.__use_breakpoints._vue_use.on_event(
            event_name, lambda value: result.set_value(value)
        )

        return ref_computed(lambda: result.value)
