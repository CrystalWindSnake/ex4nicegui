import os
from pathlib import Path
from typing import Dict, Optional, Union
from nicegui.element import Element
from nicegui import context as ng_context


class Timeline(
    Element,
    component="timeline.js",
    exposed_libraries=["../libs/gsap/gsap.mjs"],
    extra_libraries=["../libs/gsap/*.js", "../libs/gsap/utils/*.js"],
):
    def __init__(
        self,
        defaults: Optional[Dict] = None,
    ) -> None:
        super().__init__()
        self._props["defaults"] = defaults or {}
        self._props["tasks"] = []
        self._props["scriptTasks"] = []

    def from_(self, targets: str, vars: Dict, position: Optional[str] = None):
        self.__try_run_task("from", targets, vars, position)
        return self

    def to(self, targets: str, vars: Dict, position: Optional[str] = None):
        self.__try_run_task("to", targets, vars, position)
        return self

    def run_script(self, script: Union[str, Path]):
        if isinstance(script, Path):
            script = script.read_text("utf8")

        script = os.linesep.join([s for s in script.splitlines() if s])
        self.__try_run_script_task(script)
        return self

    def __try_run_script_task(self, script: str):
        def fn():
            self.run_method("runScript", script)

        if ng_context.get_client().has_socket_connection:
            fn()
        else:
            tasks = self._props["scriptTasks"]
            tasks.append(script)

    def __try_run_task(
        self, name: str, targets: str, vars: Dict, position: Optional[str] = None
    ):
        def fn():
            self.run_method(name, targets, vars)

        if ng_context.get_client().has_socket_connection:
            fn()
        else:
            tasks = self._props["tasks"]
            tasks.append(
                {"method": name, "targets": targets, "vars": vars, "position": position}
            )

    def pause(self):
        self.run_method("callTimeline", "pause")

    def play(self):
        self.run_method("callTimeline", "play")

    def resume(
        self,
    ):
        self.run_method("callTimeline", "resume")

    def seek(self, position: Optional[str] = None, suppressEvents=True):
        self.run_method("callTimeline", "seek", position, suppressEvents)

    def reverse(self):
        self.run_method("callTimeline", "reverse")
