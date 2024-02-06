from signe import utils as signe_utils
import asyncio
from typing import Literal


class PostEventExecutionScheduler(signe_utils.BatchExecutionScheduler):
    def __init__(self) -> None:
        super().__init__()
        self.__has_callback = False

    def run(self):
        if not self.__has_callback:
            try:
                asyncio.get_running_loop().call_soon(self.real_run)
            except RuntimeError:
                super().run_batch()
            self.__has_callback = True

    def real_run(
        self,
    ):
        super().run_batch()
        self.__has_callback = False


_T_Scheduler = Literal["sync", "post-event"]


def reset_execution_scheduler(type: _T_Scheduler):
    """Reset responsive scheduler type

    Args:
        type (Literal["sync", "post-event"]):
            `sync`: triggers the relevant computation as soon as the ref is assigned.
            `post-event`: performs other trigger calculations after the event loop in which the ref is assigned.
    """
    if type == "post-event":
        signe_utils.get_current_executor().set_default_execution_scheduler(
            PostEventExecutionScheduler()
        )
    elif type == "sync":
        signe_utils.get_current_executor().set_default_execution_scheduler(
            signe_utils.ExecutionScheduler()
        )
