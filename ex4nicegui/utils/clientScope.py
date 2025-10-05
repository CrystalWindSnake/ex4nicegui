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
        """Create a scope that can collect all reactive watch functions within it, allowing for a unified destruction process.

        @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#new_scope
        @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#new_scope

        Args:
            detached (bool, optional): Whether the scope should be detached from the client. Defaults to False.

        """
        return self.get_current_scope().scope(detached=detached)

    def get_current_scope(self):
        client = ui.context.client

        if client.id not in self._client_scope_map:
            self._client_scope_map[client.id] = NgScopeSuite()

            @client.on_disconnect
            def _(e: Client):
                if e.id in self._client_scope_map:
                    self._client_scope_map[e.id]._top_scope.dispose()  # type: ignore
                    del self._client_scope_map[e.id]

        return self._client_scope_map[client.id]


_CLIENT_SCOPE_MANAGER = NgClientScopeManager()


new_scope = _CLIENT_SCOPE_MANAGER.new_scope
