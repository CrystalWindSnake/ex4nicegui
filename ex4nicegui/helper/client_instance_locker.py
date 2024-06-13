from typing import Callable, TypeVar, Generic
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

    def get_object(self):
        if not ui.context.slot_stack:
            return None

        client = ui.context.client
        if client not in self._client_instances:
            self._client_instances[client] = self._factory()

            @client.on_disconnect
            def _():
                del self._client_instances[client]

        return self._client_instances[client]
