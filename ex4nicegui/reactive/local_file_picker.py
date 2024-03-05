from typing import Callable, Optional, List, Union
from typing_extensions import Literal
from nicegui import ui, Tailwind
from pathlib import Path

from ex4nicegui.utils.signals import (
    Ref,
    effect_refreshable,
    ReadonlyRef,
    effect,
    ref_computed as computed,
    to_ref,
)


SelectMode = Literal["dir", "file"]


class LocalFilePickerResult:
    def __init__(self, ref: ReadonlyRef[str], open_fn: Callable[..., None]) -> None:
        self.__open_fn = open_fn
        self._ref = ref

    def open(self):
        self.__open_fn()

    def bind_ref(self, ref: Ref[str]):
        @effect
        def _():
            ref.value = self._ref.value

        return self


def local_file_picker(
    title: Optional[str] = None,
    dir: Optional[Union[str, Path]] = None,
    mode: SelectMode = "file",
    ext: Optional[List[str]] = None,
):
    """本地文件目录选择框

    Args:
        title (Optional[str], optional): 标题. Defaults to None.
        dir (Optional[str], optional): 起始目录,默认为当前目录. Defaults to None.
        mode (SelectMode, optional): 选择文件或选择目录，'file' | 'dir'. Defaults to "file".
        ext (Optional[List[str]], optional): 当 `mode` 为 'file' 时,保留指定的文件后缀.例如: ```ext=['.xlsx','.csv']```. Defaults to None.

    Returns:
        _type_: open,result
            open:打开选择框函数
            result: 获取结果的信号函数。

    例子:
        ```python

        fp = local_file_picker(dir=r"D://dataset", ext=[".xlsx"])
        fp.open()

        # 获取结果
        fp.value
        ```
    """
    # data define
    title = title or "选择文件" if mode == "file" else "选择文件夹"
    dir_path = Path(dir).absolute() if dir else Path("./").absolute()

    # 当前所在目录
    cur_dir = to_ref(dir_path)
    cur_name = computed(lambda: str(cur_dir.value.absolute()))

    # 选中的路径
    selected = to_ref("")

    # 返回外部的结果路径
    result = to_ref("")

    no_ex_filter = ext is None
    ext_set = set(ext or [])

    def filter_ex(p: Path):
        if mode == "dir" or p.is_dir() or no_ex_filter:
            return True

        return p.suffix in ext_set

    # 当前目录下的文件(或目录)的列表
    @computed
    def paths():
        all_paths = sorted(cur_dir.value.glob("*"), key=lambda x: not x.is_dir())

        all_paths = (p for p in all_paths if mode == "file" or p.is_dir())
        all_paths = [p for p in all_paths if filter_ex(p)]

        return all_paths

    # ui define
    row_text_style = Tailwind().align_items("center").justify_content("center")

    dia = ui.dialog().props("persistent")

    with dia, ui.card().style("max-width:fit-content"):
        with ui.row().classes("w-full"):
            ui.label(title).classes("mr-auto")

            ui.icon("close", size="xs").classes("cursor-pointer").on(
                "click", handler=lambda: dia.close()
            )

        with ui.row().classes("w-full") as row:
            row.tailwind(row_text_style)

            # ui_cur_dir = ui.label()
            # bind_from(ui_cur_dir, cur_name)

            def onenter():
                cur_dir.value = Path(ui_cur_dir.value)

            ui_cur_dir = ui.input(
                "当前路径", validation={"无效路径": lambda value: Path(value).exists()}
            ).on("keydown.enter", handler=onenter)
            ui_cur_dir.classes("mr-auto grow")

            @effect
            def _():
                ui_cur_dir.value = cur_name()

            @effect_refreshable
            def pre_btn():
                dir = cur_dir.value
                if dir.is_dir() and dir.parent.is_dir():

                    def onclick():
                        cur_dir.value = dir.parent

                    ui.button("上一级", on_click=onclick)

        # 文件或目录的表格
        @effect_refreshable
        def paths_table():
            rowData = [
                {"名称": p.name, "类型": "文件夹" if p.is_dir() else "文件"}
                for p in paths()
            ]

            grid = ui.aggrid(
                {
                    "defaultColDef": {
                        "resizable": True,
                    },
                    "columnDefs": [
                        {
                            "field": "名称",
                        },
                        {
                            "field": "类型",
                        },
                        # {'field':'修改日期',},
                        # {'field':'大小',},
                    ],
                    "rowData": rowData,
                }
            )

            grid.style("width:50vw")
            # grid.tailwind("w-96")

            def dblClicked(e):
                path = cur_dir.value / Path(e.args["data"]["名称"])

                if path.is_dir():
                    cur_dir.value = path
                    return

                if mode == "file" and path.is_file():
                    result.value = str(path.absolute())
                    dia.close()

            def clicked(e):
                path = cur_dir.value / Path(e.args["data"]["名称"])

                if mode == "file" and path.is_dir():
                    return
                selected.value = str(path)

            grid.on("cellDoubleClicked", handler=dblClicked)
            grid.on("cellClicked", handler=clicked)

        # 页脚部分
        with ui.row():
            ui_selected_label = ui.label("当前选择:")

            @effect
            def _():
                ui_selected_label.text = f"当前选择： {Path(selected.value).name}"

        def onclick_ok():
            dia.close()
            result.value = selected.value

        ok_btn = ui.button("ok", on_click=onclick_ok)

        @effect
        def _():
            ok_btn.set_enabled(len(selected.value) > 0)

    file_picker_result = LocalFilePickerResult(result, dia.open)

    return file_picker_result
