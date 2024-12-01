from typing import Callable, Optional, TypedDict
from ex4nicegui import on, ref_computed
from ex4nicegui.toolbox.core.vue_use import VueUse
from ex4nicegui.utils.signals import to_ref


class UseDarkOptions(TypedDict):
    selector: str
    attribute: str
    valueDark: str
    valueLight: str


class UseDark:
    def __init__(
        self,
        value: bool = True,
        *,
        options: Optional[UseDarkOptions] = None,
        on_value_change: Optional[Callable[[bool], None]] = None,
    ):
        """Dark mode manager

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#use_dark

        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#use_dark

        Args:
            value (bool, optional): Dark mode value. Defaults to True.
            options (Optional[UseDarkOptions], optional): Options for dark mode manager. Defaults from Quasar dark mode manager.
            on_value_change (Optional[Callable[[bool], None]], optional): Callback function when dark mode value changes. Defaults to None.
        """
        options = options or {
            "selector": "body",
            "attribute": "class",
            "valueDark": "body--dark dark",
            "valueLight": "body--light",
        }

        self.__vue_use = VueUse("useDark", args=[options, value])

        if on_value_change:
            self.on_value_change(on_value_change)

        self.__is_dark = to_ref(value)

        self.is_dark = ref_computed(lambda: self.__is_dark.value)

        @self.on_value_change
        def _(is_dark: bool):
            self.__is_dark.value = is_dark

    def on_value_change(self, callback: Callable[[bool], None]):
        """Callback function when dark mode value changes

        Args:
            callback (Callable[[bool], None]): Callback function.
        """
        self.__vue_use.on_event("isDark", callback)

    def toggle(self, value: Optional[bool] = None):
        """Toggle dark mode

        Args:
            value (Optional[bool], optional):  Dark mode value. Defaults to None.
        """
        self.__vue_use.run_method("toggleDark", value)
