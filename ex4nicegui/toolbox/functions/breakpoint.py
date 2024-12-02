from __future__ import annotations
from typing import Callable, Dict, List, Optional
from ex4nicegui.utils.signals import to_ref, ref_computed
from ex4nicegui.utils.types import ReadonlyRef
from ex4nicegui.toolbox.core.vue_use import VueUse


_QUASAR_BREAKPOINTS = {"xs": 0, "sm": 600, "md": 1024, "lg": 1440, "xl": 1920}


class UseBreakpoints:
    def __init__(
        self,
        options: Optional[Dict] = None,
        *,
        on_active_change: Optional[Callable[[str], None]] = None,
    ):
        """monitor viewport breakpoints.

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#use_breakpoints

        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#use_breakpoints

        Args:
            options (Optional[Dict], optional): the configuration for each breakpoint. The default is the configuration from Quasar v3. Defaults to None.
            on_active_change (Optional[Callable[[str], None]], optional): callback function to be called when the breakpoint changes. Defaults to None.

        Example:
        .. code-block:: python
            from ex4nicegui import toolbox as tb

            options = {"mobile": 0, "tablet": 640, "laptop": 1024, "desktop": 1280}
            tb.use_breakpoints(options, on_active_change=lambda breakpoint: print(breakpoint))

        """
        self.__options = (options or _QUASAR_BREAKPOINTS).copy()

        self._vue_use = VueUse("useBreakpoints", args=[self.__options])

        self.__active_value = ""

        def mouted(value: str):
            self.__active_value = value

        self.__active_ref: Optional[ReadonlyRef[str]] = None
        self.__on_active_change_with_mounted(mouted)

        if on_active_change:
            self.on_active_change(on_active_change)

    @property
    def active_value(self) -> str:
        """the current breakpoint value."""
        return self.__active_value

    @property
    def active(self):
        """the current breakpoint value as a ref."""
        if self.__active_ref is None:
            active = to_ref(self.__active_value)

            self.__on_active_change_with_mounted(lambda value: active.set_value(value))
            self.__active_ref = ref_computed(lambda: active.value)

        return self.__active_ref

    def between(self, start: str, end: str) -> ReadonlyRef[bool]:
        """whether the current breakpoint is between the start and end values."""

        @ref_computed
        def between_result():
            return _Utils.is_between(
                list(self.__options.keys()), self.active.value, start, end
            )

        return between_result

    def is_between(self, start: str, end: str) -> bool:
        """whether the current breakpoint is between the start and end values.

        Args:
            start (str): Detect the start value of the range.
            end (str): Detect the end value of the range. not including.

        Returns:
            bool: True or False
        """
        return _Utils.is_between(
            list(self.__options.keys()), self.active_value, start, end
        )

    def on_active_change(self, callback: Callable[[str], None]):
        """register a callback function to be called when the breakpoint changes.

        Args:
            callback (Callable[[str], None]): the callback function to be called.
        """
        self._vue_use.on_event("active", callback)

    def __on_active_change_with_mounted(self, callback: Callable[[str], None]):
        self._vue_use.on_event("activeWithMounted", callback)


class _Utils:
    @staticmethod
    def is_between(ranges: List[str], current: str, start: str, end: str) -> bool:
        try:
            current_index = ranges.index(current)
            start_index = ranges.index(start)
            end_index = ranges.index(end)

            return start_index <= current_index < end_index
        except ValueError:
            return False
