from typing import Callable, Optional
from ex4nicegui.toolbox.core.vue_use import VueUse
from ex4nicegui.utils.signals import (
    to_value,
    TMaybeRef,
    is_ref,
    on,
    to_ref,
    ref_computed,
)


class UseQRCode:
    def __init__(
        self,
        text: TMaybeRef[str],
        *,
        on_data_change: Optional[Callable[[str], None]] = None,
    ):
        """Create a QR code.

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#use_qr_code

        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#use_qr_code

        Args:
            text (TMaybeRef[str]): The text to be encoded in the QR code.
            on_data_change (Optional[Callable[[str], None]], optional): Callback function when qr code changes. Defaults to None.

        Example:
        .. code-block:: python
            from ex4nicegui import rxui, to_ref, toolbox as tb
            from nicegui import ui

            text = to_ref("ex4nicegui")
            qr_code = tb.use_qr_code(text)

            rxui.input(value=text)
            rxui.image(qr_code.code).classes("w-20 h-20").props("no-transition")
        """

        self.__vue_use = VueUse("useQRCode", args=[to_value(text)])

        if on_data_change:
            self.on_data_change(on_data_change)

        self.__text = text
        self.__qr_code = to_ref("")
        self.code = ref_computed(lambda: self.__qr_code.value)

        if is_ref(self.__text):

            @on(self.__text, onchanges=True)
            def _():
                self.update_text(to_value(self.__text))

            @self.on_data_change
            def _on_data_change(data: str):
                self.__qr_code.value = data

    async def get_qr_code(self) -> str:
        """Get the QR code data.

        Returns:
            str: The QR code data.
        """
        return await self.__vue_use.run_method("getQRCode")

    def update_text(self, text: str):
        """Update the text to be encoded in the QR code.

        Args:
            text (str): The new text to be encoded in the QR code.
        """
        self.__vue_use.run_method("updateText", text)

    def on_data_change(self, callback: Callable[[str], None]):
        """Callback function when qr code changes.

        Args:
            callback (Callable[[bool], None]): Callback function.
        """
        self.__vue_use.on_event("qrcode", callback)
