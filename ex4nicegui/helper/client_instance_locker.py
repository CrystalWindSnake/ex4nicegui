from typing import Callable, Optional, TypeVar, Generic
from nicegui import ui, Client
from weakref import WeakKeyDictionary


_T = TypeVar("_T")


class ClientInstanceLocker(Generic[_T]):
    def __init__(self, factory: Callable[[], _T]):
        """Creates a new instance locker that creates a new instance for each client.

        Args:
            factory (Callable[[], _T]):  A factory function that creates a new instance.
        """
        self._client_instances: WeakKeyDictionary[Client, _T] = WeakKeyDictionary()
        self._factory = factory

    def get_object(self, client: Optional[Client] = None):
        if not ui.context.slot_stack:
            return None

        if client is not None and (client not in self._client_instances):
            return None

        client = client or ui.context.client
        if client not in self._client_instances:
            self._client_instances[client] = self._factory()

            @client.on_disconnect
            def _():
                self._client_instances.pop(client, None)

        return self._client_instances[client]
