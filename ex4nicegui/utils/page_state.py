from typing import ClassVar
from typing_extensions import Self
from contextvars import ContextVar


class PageState:
    """
    A base class for defining per-page reactive state containers.

    Each subclass of `PageState` provides an isolated state context that is automatically
    managed through a `ContextVar`. When used inside different `ui.page` definitions,
    each page will maintain its own independent instance of the subclass, ensuring
    states do not interfere across pages.

    Subclasses should define reactive variables (e.g., created via `to_ref`) within
    their `__init__` method. The instance can then be accessed anywhere in the same
    page context using `MyState.get()` — without needing to pass it through function parameters.

    Typical use cases include sharing state across multiple components or functions
    within the same page.

    @see - https://github.com/CrystalWindSnake/ex4nicegui/blob/main/README.en.md#PageState
    @中文文档 - https://gitee.com/carson_add/ex4nicegui/tree/main/#PageState

    # Example:
    .. code-block:: python
        from ex4nicegui import rxui, to_ref, PageState
        from nicegui import ui

        class MyState(PageState):
            def __init__(self):
                self.a = to_ref(1.0)

        def sub_view():
            state = MyState.get()
            rxui.label(lambda: f"{state.a.value=}")

        @ui.page('/')
        def _():
            state = MyState.get()
            rxui.number(value=state.a)
            sub_view()
    """

    _ctx: ClassVar[ContextVar["PageState"]]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._ctx = ContextVar(f"{cls.__name__}_ctx")

    @classmethod
    def get(cls) -> Self:
        """
        Retrieves the current instance of the page state for this subclass.

        If no instance exists yet in the current context, a new one is created
        and stored. Subsequent calls within the same page will return the same instance.

        This method allows components and functions within the same page
        to share reactive state seamlessly without passing references explicitly.

        Returns:
            Self: The current `PageState` subclass instance associated with this page.
        """
        inst = cls._ctx.get(None)

        if inst is None:
            inst = cls()
            cls._ctx.set(inst)
        return inst  # type: ignore
