from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    cast,
)
from nicegui import ui
from ex4nicegui.utils.signals import is_ref, is_setter_ref
from nicegui.events import handle_event
from ex4nicegui.reactive.systems.reactive_system import (
    convert_kws_ref2value,
    inject_method,
)
from ex4nicegui.utils.proxy import is_base_type_proxy


_EVENT_SOURCE_INTERNAL_FLAG = "__ex4ng_set_value_from_signal_"


class ParameterClassifier:
    def __init__(
        self,
        args: Dict,
        *,
        maybeRefs: Optional[Iterable[str]] = None,
        events: Optional[List[str]] = None,
        v_model: Optional[Tuple[str, str]] = None,
        v_model_arg_getter: Optional[Callable[[Any], Any]] = None,
        exclude: Optional[List[str]] = None,
        extend_kws: Optional[str] = None,
    ) -> None:
        exclude = exclude or []
        if extend_kws:
            exclude.append(extend_kws)

        self._args: Dict[str, Any] = {
            k: v._ref if is_base_type_proxy(v) else v
            for k, v in args.items()
            if k != "self" and k[0] != "_" and (k not in exclude)
        }

        self.maybeRefs = maybeRefs or []
        self.events = events or []
        self.v_model = v_model
        self.v_model_arg_getter = v_model_arg_getter or (lambda e: getattr(e, "value"))

        if extend_kws:
            extend_args = cast(Dict, args.get(extend_kws))
            self.events.extend(
                k for k, v in extend_args.items() if isinstance(v, Callable)
            )

            self._args.update(
                {k: v for k, v in extend_args.items() if not isinstance(v, Callable)}
            )

    def get_values_kws(self) -> Dict:
        value_kws = convert_kws_ref2value(
            {k: v for k, v in self._args.items() if k not in self.events}
        )

        # replace event
        value_kws.update({k: v for k, v in self._args.items() if k in self.events})

        if self.v_model:
            v_name, event_name = self.v_model
            model_value = self._args.get(v_name)
            event = self._args.get(event_name)

            if is_setter_ref(model_value):

                def inject_on_change(e):
                    change_from_inner_signal = (
                        ParameterClassifier.get_event_source_internal_flag(e.sender)
                    )

                    if not change_from_inner_signal:
                        model_value.value = self.v_model_arg_getter(e)  # type: ignore

                    ParameterClassifier.remove_event_source_internal_flag(e.sender)
                    handle_event(event, e)

                value_kws.update({event_name: inject_on_change})

        return value_kws

    def get_bindings(self) -> Dict:
        return {
            k.replace("_", "-"): v
            for k, v in self._args.items()
            if (k in self.maybeRefs and (is_ref(v) or isinstance(v, Callable)))
        }

    @staticmethod
    def mark_event_source_as_internal(element: ui.element):
        element.__dict__[_EVENT_SOURCE_INTERNAL_FLAG] = True

    @staticmethod
    def get_event_source_internal_flag(element: ui.element):
        return element.__dict__.get(_EVENT_SOURCE_INTERNAL_FLAG, False)

    @staticmethod
    def remove_event_source_internal_flag(element: ui.element):
        element.__dict__.pop(_EVENT_SOURCE_INTERNAL_FLAG, None)


def inject_handle_delete(element: ui.element, on_delete: Callable[[], None]):
    inject_method(element, "_handle_delete", on_delete)
