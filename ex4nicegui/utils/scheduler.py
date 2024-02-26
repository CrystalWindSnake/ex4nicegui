from collections import deque
import signe
from typing import (
    TypeVar,
    Callable,
)
from functools import lru_cache


T = TypeVar("T")

T_JOB_FN = Callable[[], None]


class UiScheduler(signe.ExecutionScheduler):
    def __init__(self) -> None:
        super().__init__()

        self._pre_deque: deque[T_JOB_FN] = deque()
        self._post_deque: deque[T_JOB_FN] = deque()

    def pre_job(self, job: T_JOB_FN):
        self._pre_deque.appendleft(job)

    def post_job(self, job: T_JOB_FN):
        self._post_deque.appendleft(job)

    def run(self):
        while self._scheduler_fns:
            super().run()

            self.pause_scheduling()
            try:
                self.run_pre_deque()
                self.run_post_deque()
                pass
            except Exception as e:
                raise e
            finally:
                self.reset_scheduling()

    def run_pre_deque(self):
        while self._pre_deque:
            self._pre_deque.pop()()

    def run_post_deque(self):
        while self._post_deque:
            self._post_deque.pop()()


@lru_cache(maxsize=1)
def get_uiScheduler():
    return UiScheduler()
