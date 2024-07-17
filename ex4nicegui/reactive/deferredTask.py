from typing import Callable
from nicegui import ui, Client as ng_client


class DeferredTask:
    def __init__(self):
        self._tasks = []

        async def on_client_connect(
            client: ng_client,
        ):
            await client.connected()

            for task in self._tasks:
                task()

            # Avoid events becoming ineffective due to page refresh when sharing the client.
            if not client.shared:
                # In a shared page, execution is required with every refresh.
                # note:https://github.com/CrystalWindSnake/ex4nicegui/issues/227
                self._tasks.clear()
                client.connect_handlers.remove(on_client_connect)  # type: ignore

        ui.context.client.on_connect(on_client_connect)

    def register(self, task: Callable[..., None]):
        if ui.context.client.has_socket_connection:
            task()
        else:
            self._tasks.append(task)
