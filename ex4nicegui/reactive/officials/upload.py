from typing import (
    Any,
    Callable,
    Optional,
)
from nicegui import events as ng_events
from ex4nicegui.utils.signals import (
    is_ref,
    _TMaybeRef as TMaybeRef,
)
from nicegui import ui
from .base import SingleValueBindableUi
from .utils import _convert_kws_ref2value


class UploadResult:
    def __init__(self, content: bytes = bytes(), name="", type=""):
        self.content = content
        self.name = name
        self.type = type

    def get_bytes(self):
        return self.content

    @property
    def ready(self):
        return len(self.content) > 0


class UploadBindableUi(SingleValueBindableUi[UploadResult, ui.upload]):
    @staticmethod
    def _setup_(binder: "UploadBindableUi"):
        def on_upload(e: ng_events.UploadEventArguments):
            binder._ref.value = UploadResult(e.content.read(), e.name, e.type)

        binder._on_upload_callbacks.append(on_upload)

    def __init__(
        self,
        multiple: TMaybeRef[bool] = False,
        max_file_size: Optional[TMaybeRef[int]] = None,
        max_total_size: Optional[TMaybeRef[int]] = None,
        max_files: Optional[TMaybeRef[int]] = None,
        on_upload: Optional[Callable[..., Any]] = None,
        on_rejected: Optional[Callable[..., Any]] = None,
        label: TMaybeRef[str] = "",
        auto_upload: TMaybeRef[bool] = False,
    ) -> None:
        kws = {
            "multiple": multiple,
            "max_file_size": max_file_size,
            "max_total_size": max_total_size,
            "max_files": max_files,
            "on_rejected": on_rejected,
            "label": label,
            "auto_upload": auto_upload,
        }

        value_kws = _convert_kws_ref2value(kws)

        self._on_upload_callbacks = []

        def _on_upload(e: ng_events.UploadEventArguments):
            for fn in self._on_upload_callbacks:
                fn(e)

        if on_upload:
            self._on_upload_callbacks.append(on_upload)

        element = ui.upload(**value_kws, on_upload=_on_upload)

        super().__init__(UploadResult(), element)  # type: ignore

        for key, value in kws.items():
            if is_ref(value):
                self.bind_prop(key, value)  # type: ignore

        UploadBindableUi._setup_(self)
