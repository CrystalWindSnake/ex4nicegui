from typing import Dict
from ex4nicegui.utils.signals import to_value


def convert_kws_ref2value(kws: Dict) -> Dict:
    return {key: to_value(value) for key, value in kws.items()}
