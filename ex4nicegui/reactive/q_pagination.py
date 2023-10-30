from typing import cast
from nicegui.element import Element
from ex4nicegui.utils.signals import (
    Ref,
    effect,
    to_value,
    _TMaybeRef as TMaybeRef,
)


class QPagination(Element):
    VALUE_PROP: str = "model-value"
    LOOPBACK = False

    def __init__(
        self,
        value: TMaybeRef[int] = 1,
        min: TMaybeRef[int] = 1,
        max: TMaybeRef[int] = 5,
    ) -> None:
        super().__init__(tag="q-pagination")

        self.__value = value
        self.__min = min
        self.__max = max

        def onchange(e):
            arg_value = cast(int, e.args)

            self._props["model-value"] = arg_value
            if isinstance(self.__value, Ref):
                self.__value.value = arg_value
            self.update()

        self.on("update:model-value", onchange)

        @effect
        def _():
            self._props["model-value"] = to_value(value)
            self._props["min"] = to_value(min)

            if self.__max is not None:
                self._props["max"] = to_value(self.__max)

            self.update()
