from typing import Any, Callable, Dict, List, Optional
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

        # self._tasks: List[Callable] = []

        # async def on_client_connect(
        #     client: nicegui.Client,
        # ) -> Any:
        #     await client.connected()

        #     for func in self._tasks:
        #         func()

        # ng_context.get_client().on_connect(on_client_connect)

    def set_defaults(
        self,
        defaults: Optional[Dict] = None,
    ):
        self._props["defaults"] = defaults or {}
        return self

    def from_(self, target: str, options: Dict):
        self.__try_run_task("from", target, options)
        return self

    def to(self, target: str, options: Dict):
        self.__try_run_task("to", target, options)
        return self

    def __try_run_task(self, name: str, target: str, options: Dict):
        def fn():
            self.run_method(name, target, options)

        if ng_context.get_client().has_socket_connection:
            fn()
        else:
            tasks = self._props["tasks"]
            tasks.append({"method": name, "target": target, "options": options})


__instance_map: WeakKeyDictionary[nicegui.Client, Gsap] = WeakKeyDictionary()


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


def from_(target: str, options: Dict):
    return _get_instance().from_(target, options)


def to(target: str, options: Dict):
    return _get_instance().to(target, options)
