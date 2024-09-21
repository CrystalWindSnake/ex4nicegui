from pathlib import Path
import importlib.util
from nicegui import ui

PAGES_PATH = Path(__file__).parent / "pages"


def startup():
    infos = get_module_info(PAGES_PATH)

    @ui.page("/")
    def index():
        for _, name in infos:
            ui.link(name, f"/{name}")

    for file, name in infos:
        index_fn = import_index_functions(file)
        ui.page(f"/{name}")(index_fn)


def get_module_info(folder_path: Path):
    return [
        (file, file.stem)
        for file in folder_path.glob("*.py")
        if not file.name.startswith("_")
    ]


def import_index_functions(file_path: Path):
    # 创建模块规格
    spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
    assert spec is not None, f"Failed to load module {file_path}"
    # 创建模块
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore

    # 检查模块中是否存在 index 函数
    if not hasattr(module, "index"):
        raise ValueError(f"Module {file_path} does not have an index function")

    return getattr(module, "index")
