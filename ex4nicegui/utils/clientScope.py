from typing import Dict, List
from signe.core.effect import Effect
from signe.core.scope import IScope
from signe.core.protocols import DisposableProtocol
from nicegui import Client, context as ng_context


_TClientID = str


class NgClientScope(IScope):
    def __init__(self) -> None:
        self._effects: List[DisposableProtocol] = []

    def add_disposable(self, disposable: DisposableProtocol):
        self._effects.append(disposable)

    def dispose(self):
        for effect in self._effects:
            effect.dispose()


class NgClientScopeManager:
    def __init__(self) -> None:
        self._client_scope_map: Dict[_TClientID, NgClientScope] = {}

    def get_scope(self):
        if len(ng_context.get_slot_stack()) <= 0:
            return

        client = ng_context.get_client()
        if client.shared:
            return

        if client.id not in self._client_scope_map:
            self._client_scope_map[client.id] = NgClientScope()

            @client.on_disconnect
            def _(e: Client):
                if e.id in self._client_scope_map:
                    self._client_scope_map[e.id].dispose()

        return self._client_scope_map[client.id]


_CLIENT_SCOPE_MANAGER = NgClientScopeManager()
