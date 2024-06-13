from .gsap import set_defaults, from_, to, new, run_script
from .timeline import Timeline as timeline


import warnings

RED = "\033[91m"
RESET = "\033[0m"

warnings.warn(
    f"{RED}The gsap module is deprecated and will be removed in the next major version.{RESET}",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "set_defaults",
    "from_",
    "to",
    "new",
    "run_script",
    "timeline",
]
