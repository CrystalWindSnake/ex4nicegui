from typing import Dict
from signe.core.scope import ScopeSuite
from nicegui import Client, ui


_TClientID = str


class NgScopeSuite(ScopeSuite):
    def __init__(self) -> None:
        super().__init__()
        self._top_scope = self.scope()
        self._top_scope.on()


class NgClientScopeManager:
    def __init__(self) -> None:
        self._client_scope_map: Dict[_TClientID, NgScopeSuite] = {}

    def new_scope(self, detached: bool = False):
        return self.get_current_scope().scope(detached)

    def get_current_scope(self):
        # if len(ng_context.get_slot_stack()) <= 0:
        #     return

        client = ui.context.client

        if client.id not in self._client_scope_map:
            self._client_scope_map[client.id] = NgScopeSuite()

            # shared clients always not dispose their scope
            if not client.shared:

                @client.on_disconnect
                def _(e: Client):
                    if e.id in self._client_scope_map:
                        self._client_scope_map[e.id]._top_scope.dispose()
                        del self._client_scope_map[e.id]

        return self._client_scope_map[client.id]


_CLIENT_SCOPE_MANAGER = NgClientScopeManager()


def new_scope():
    pass
