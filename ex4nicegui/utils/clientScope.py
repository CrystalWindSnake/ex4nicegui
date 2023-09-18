from typing import Dict, List
from signe.core.effect import Effect
from signe.core.scope import IScope
from nicegui import globals as ng_globals, Client


_TClientID = str


class NgClientScope(IScope):
    def __init__(self) -> None:
        self._effects: List[Effect] = []

    def add_effect(self, effect: Effect):
        self._effects.append(effect)

    def dispose(self):
        for effect in self._effects:
            effect.dispose()


class NgClientScopeManager:
    def __init__(self) -> None:
        self._client_scope_map: Dict[_TClientID, NgClientScope] = {}

    def get_scope(self):
        if len(ng_globals.get_slot_stack()) <= 0:
            return

        client = ng_globals.get_client()
        if client.shared:
            return

        if client.id not in self._client_scope_map:
            self._client_scope_map[client.id] = NgClientScope()

            @client.on_disconnect
            def _(e: Client):
                if e.id in self._client_scope_map:
                    self._client_scope_map[e.id].dispose()

        return self._client_scope_map[client.id]
