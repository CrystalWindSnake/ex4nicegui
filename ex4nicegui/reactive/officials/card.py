from typing import (
    Any,
    Literal,
    Optional,
)
from nicegui import ui
from .base import BindableUi
from ex4nicegui.reactive.mixins.flexLayout import FlexAlignItemsMixin
from ex4nicegui.utils.signals import TMaybeRef
from ex4nicegui.reactive.services.reactive_service import ParameterClassifier


class CardBindableUi(BindableUi[ui.card], FlexAlignItemsMixin):
    def __init__(
        self,
        align_items: Optional[
            TMaybeRef[Literal["start", "end", "center", "baseline", "stretch"]]
        ] = None,
    ) -> None:
        """Card

        This element is based on Quasar's `QCard <https://quasar.dev/vue-components/card>`_ component.
        It provides a container with a dropped shadow.

        Note:
        In contrast to this element,
        the original QCard has no padding by default and hides outer borders and shadows of nested elements.
        If you want the original behavior, use the `tight` method.

        :param align_items: alignment of the items in the card ("start", "end", "center", "baseline", or "stretch"; default: `None`)
        """
        pc = ParameterClassifier(locals(), maybeRefs=["wrap", "align_items"], events=[])
        element = ui.card(**pc.get_values_kws())

        super().__init__(element)

        for key, value in pc.get_bindings().items():
            self.bind_prop(key, value)  # type: ignore

    def bind_prop(self, prop: str, value: TMaybeRef):
        if FlexAlignItemsMixin._bind_specified_props(self, prop, value):
            return self

        return super().bind_prop(prop, value)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)

    def tight(self):
        """Removes padding and gaps between nested elements."""
        self.element._classes.clear()
        self.element._style.clear()
        return self


class CardSectionBindableUi(BindableUi[ui.card_section]):
    def __init__(
        self,
    ) -> None:
        element = ui.card_section()

        super().__init__(element)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)


class CardActionsBindableUi(BindableUi[ui.card_actions]):
    def __init__(
        self,
    ) -> None:
        element = ui.card_actions()

        super().__init__(element)

    def __enter__(self):
        self.element.__enter__()
        return self

    def __exit__(self, *_: Any):
        self.element.__exit__(*_)
