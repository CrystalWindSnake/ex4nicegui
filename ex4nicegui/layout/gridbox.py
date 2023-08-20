from typing import List, Optional, Union, cast
from nicegui.client import Client
from nicegui.element import Element
from ex4nicegui.reactive.officials.base import BindableUi


def _areas_str2array(areas: str) -> List[List[str]]:
    """
    >>> input='''
        sc1 sc2
        sc3
        table table table table
    '''
    >>> areas_str2array(input)
    >>> [
        ["sc1", "sc2"],
        ["sc3"],
        ["table", "table", "table", "table"]
    ]
    """
    pass

    lines = (line.strip() for line in areas.splitlines())
    remove_empty_rows = (line for line in lines if len(line) > 0)
    splie_space = (line.split() for line in remove_empty_rows)
    return list(splie_space)


def _areas_array2str(areas_array: List[List[str]]):
    """
    >>> input = [
        ["sc1", "sc2"],
        ["sc3"],
        ["table"] * 4
    ]
    >>> areas_array2str(input)
    >>> '"sc1 sc2 . ." "sc3 . . ." "table table table table"'
    """
    max_len = max(map(len, areas_array))

    fix_empty = (
        [*line, *(["."] * (max_len - len(line)))] if len(line) < max_len else line
        for line in areas_array
    )

    line2str = (f'"{" ".join(line)}"' for line in fix_empty)
    return " ".join(line2str)


class grid_box(Element):
    def __init__(
        self,
        areas_text: str,
        template_columns: Optional[str] = None,
        template_rows: Optional[str] = None,
        *,
        _client: Client | None = None,
    ) -> None:
        super().__init__("div", _client=_client)

        areas_list = _areas_str2array(areas_text)

        areas = _areas_array2str(areas_list)

        areas_cols_len = max(map(len, areas_list))
        areas_rows_len = len(areas_list)

        template_columns = template_columns or f"repeat({areas_cols_len}, 1fr)"
        template_rows = template_rows or f"repeat({areas_rows_len}, 1fr)"

        self.style(
            f"""
width: 100%;
grid-template-areas: {areas};
display: grid;
grid-template-columns: {template_columns};
grid-template-rows:{template_rows};"""
        )

    def areas_mark(self, element: Union[Element, BindableUi], mark: str):
        if isinstance(element, BindableUi):
            element = element.element
        element = cast(Element, element)
        element.style(f"grid-area:{mark}")
        return element
