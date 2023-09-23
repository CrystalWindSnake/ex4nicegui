from typing import TypeVar, Generic

_T_ELEMENT = TypeVar("_T_ELEMENT")


class UiResult(Generic[_T_ELEMENT]):
    def __init__(self, element: _T_ELEMENT) -> None:
        self.__element = element

    @property
    def element(self):
        return self.__element
