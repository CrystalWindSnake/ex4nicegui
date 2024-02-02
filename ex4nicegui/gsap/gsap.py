from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union
from nicegui.element import Element
from nicegui import context as ng_context
import nicegui
from weakref import WeakKeyDictionary


class Gsap(
    Element,
    component="wrapGsap.js",
    exposed_libraries=["libs/gsap.mjs"],
    extra_libraries=["libs/*.js", "libs/utils/*.js"],
):
    def __init__(
        self,
        defaults: Optional[Dict] = None,
    ) -> None:
        super().__init__()
        self._props["defaults"] = defaults or {}
        self._props["tasks"] = []
        self._props["scriptTasks"] = []

    def set_defaults(
        self,
        defaults: Optional[Dict] = None,
    ):
        self._props["defaults"] = defaults or {}
        return self

    def from_(self, targets: str, vars: Dict):
        self.__try_run_task("from", targets, vars)
        return self

    def to(self, targets: str, vars: Dict):
        self.__try_run_task("to", targets, vars)
        return self

    def run_script(self, script: str):
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

    def __try_run_task(self, name: str, targets: str, vars: Dict):
        def fn():
            self.run_method(name, targets, vars)

        if ng_context.get_client().has_socket_connection:
            fn()
        else:
            tasks = self._props["tasks"]
            tasks.append({"method": name, "targets": targets, "vars": vars})


__instance_map = WeakKeyDictionary()


def _get_instance():
    current_client = ng_context.get_client()
    ins = __instance_map.get(current_client)

    if not ins:
        ins = Gsap()
        __instance_map[current_client] = ins

    return ins


def set_defaults(options: Dict):
    ins = _get_instance()
    ins.set_defaults(options)
    return ins


def new(
    defaults: Optional[Dict] = None,
):
    return Gsap(defaults)


def from_(targets: str, vars: Dict):
    """define where the values should START, and then it animates to the current state which is perfect for animating objects onto the screen because you can set them up the way you want them to look at the end and then animate in from elsewhere

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#gsapfrom_
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#gsapfrom_


    Args:
        targets (str): The object(s) whose properties you want to animate. This can be selector text like ".class", "#id", etc. (GSAP uses document.querySelectorAll() internally)
        vars (Dict): An object containing all the properties/values you want to animate, along with any special properties like ease, duration, delay, or onComplete (listed below)

    """
    return _get_instance().from_(targets, vars)


def to(targets: str, vars: Dict):
    """define the destination values (and most people think in terms of animating to certain values)

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#gsapto
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#gsapto


    Args:
        targets (str): The object(s) whose properties you want to animate. This can be selector text like ".class", "#id", etc. (GSAP uses document.querySelectorAll() internally)
        vars (Dict): An object containing all the properties/values you want to animate, along with any special properties like ease, duration, delay, or onComplete (listed below)
    """

    return _get_instance().to(targets, vars)


def run_script(script: Union[str, Path]):
    """Allows you to write animated js code directly

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#gsaprun_script
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#gsaprun_script


    Args:
        script (Union[str, Path]): Text of the js code. If it is of type `Path` reads the text of the file.


    """

    if isinstance(script, Path):
        script = script.read_text("utf8")
    return _get_instance().run_script(script)
