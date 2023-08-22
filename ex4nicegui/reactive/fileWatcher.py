from nicegui import app
from typing import Callable, List, Set, Union
from pathlib import Path
from watchfiles import awatch
from watchfiles.main import FileChange
import asyncio


TON_FILE_CHANGE_HANDER = Callable[[Set[FileChange]], None]


class FilesWatcher:
    def __init__(self, paths: Union[Path, str], recursive=False) -> None:
        self.callbacks: List[TON_FILE_CHANGE_HANDER] = []
        self.__stop_event = asyncio.Event()

        async def watch_fn():
            async for file in awatch(
                paths, stop_event=self.__stop_event, recursive=recursive
            ):
                for fn in self.callbacks:
                    fn(file)

        if asyncio.get_event_loop().is_running():
            asyncio.get_event_loop().create_task(watch_fn())
        else:

            def on_app_startup():
                asyncio.get_event_loop().create_task(watch_fn())

            app.on_startup(on_app_startup)

    def stop(self):
        self.__stop_event.set()

    def on_FileChange(self, handler: TON_FILE_CHANGE_HANDER):
        self.callbacks.append(handler)
        return self
