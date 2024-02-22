from typing import Any, Callable, Dict, Iterable, Optional, Tuple

from ex4nicegui.utils.signals import is_ref, to_value, is_setter_ref
from nicegui.events import handle_event


def _convert_kws_ref2value(kws: Dict) -> Dict:
    return {key: to_value(value) for key, value in kws.items()}


class ParameterClassifier:
    def __init__(
        self,
        args: Dict,
        *,
        maybeRefs: Optional[Iterable[str]] = None,
        events: Optional[Iterable[str]] = None,
        v_model: Optional[Tuple[str, str]] = None,
        v_model_arg_getter: Optional[Callable[[Any], Any]] = None,
        exclude: Optional[Iterable[str]] = None,
    ) -> None:
        exclude = exclude or []
        self._args = {
            k: v
            for k, v in args.items()
            if k != "self" and k[0] != "_" and (k not in exclude)
        }
        self.maybeRefs = maybeRefs or []
        self.events = events or []
        self.v_model = v_model
        self.v_model_arg_getter = v_model_arg_getter or (lambda e: getattr(e, "value"))

    def get_values_kws(self) -> Dict:
        value_kws = _convert_kws_ref2value(
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
                    model_value.value = self.v_model_arg_getter(e)  # type: ignore
                    handle_event(event, e)

                value_kws.update({event_name: inject_on_change})

        return value_kws

    def get_bindings(self) -> Dict:
        return {
            k: v
            for k, v in self._args.items()
            if (k in self.maybeRefs and (is_ref(v) or isinstance(v, Callable)))
        }
