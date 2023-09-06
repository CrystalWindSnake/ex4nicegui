from typing import List


def areas_str2array(areas: str) -> List[List[str]]:
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


def areas_array2str(areas_array: List[List[str]]):
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


def best_grid_template_columns(min_column_size: str):
    return f"repeat(auto-fit,minmax(min({min_column_size},100%),1fr))"
