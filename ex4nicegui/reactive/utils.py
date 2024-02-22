from typing import Callable, Dict, Iterable, Optional

from ex4nicegui.utils.signals import is_ref, to_value


def _convert_kws_ref2value(kws: Dict) -> Dict:
    return {key: to_value(value) for key, value in kws.items()}


class ParameterClassifier:
    def __init__(
        self,
        args: Dict,
        *,
        maybeRefs: Optional[Iterable[str]] = None,
        events: Optional[Iterable[str]] = None,
    ) -> None:
        self._args = {k: v for k, v in args.items() if k != "self" and k[0] != "_"}
        self.maybeRefs = maybeRefs or []
        self.events = events or []

    def get_values_kws(self) -> Dict:
        return _convert_kws_ref2value(
            {k: v for k, v in self._args.items() if k not in self.events}
        )

    def get_bindings(self) -> Dict:
        return {
            k: v
            for k, v in self._args.items()
            if (k in self.maybeRefs and (is_ref(v) or isinstance(v, Callable)))
        }
