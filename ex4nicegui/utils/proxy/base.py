from typing import Any, Protocol


class ProxyProtocol(Protocol):
    _ref: Any


class Proxy(ProxyProtocol):
    pass
