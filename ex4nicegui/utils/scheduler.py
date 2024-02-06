from signe import utils as signe_utils
import asyncio


class EventDelayExecutionScheduler(signe_utils.ExecutionScheduler):
    def __init__(self) -> None:
        super().__init__()
        self.__has_callback = False

    def run(self):
        if not self.__has_callback:
            asyncio.get_running_loop().call_soon(self.real_run)
            self.__has_callback = True

    def real_run(
        self,
    ):
        super().run()
        self.__has_callback = False
