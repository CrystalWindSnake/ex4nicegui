from nicegui import app
from typing import Callable, List, Set, Union
from pathlib import Path
from watchfiles import awatch
from watchfiles.main import FileChange
import asyncio


TON_FILE_CHANGE_HANDER = Callable[[Set[FileChange]], None]


class FilesWatcher:
    r"""
    watchfiles component

    ### use
    ```python
    fw = rxui.FilesWatcher(r'E:\test')

    @g_fw.on_FileChange
    def _(e):
        print(e)
    ```
    """

    def __init__(self, paths: Union[Path, str], recursive=False) -> None:
        self.callbacks: List[TON_FILE_CHANGE_HANDER] = []
        self.__stop_event = asyncio.Event()

        async def watch_fn():
            try:
                async for file in awatch(
                    paths, stop_event=self.__stop_event, recursive=recursive
                ):
                    for fn in self.callbacks:
                        fn(file)
            except RuntimeError:
                return

        if asyncio.get_event_loop().is_running():
            asyncio.get_event_loop().create_task(watch_fn())
        else:

            @app.on_startup
            def _():
                asyncio.get_event_loop().create_task(watch_fn())

        @app.on_shutdown
        def _():
            self.stop()

    def stop(self):
        self.__stop_event.set()

    def on_FileChange(self, handler: TON_FILE_CHANGE_HANDER):
        self.callbacks.append(handler)
        return self
