from pathlib import Path
import re
import shutil
from typing import List

FILE_MAPPING = {
    "ECharts": "reactive/EChartsComponent/ECharts.js",
    "UseDraggable": "reactive/UseDraggable/UseDraggable.js",
    "UseMouse": "reactive/UseMouse/UseMouse.js",
    "DropZone": "reactive/DropZone/DropZone.js",
    "GridFlex": "layout/gridFlex/GridFlex.js",
    "VueUse": "toolbox/core/VueUse.js",
}

EX_REACTIVE_DIR_ROOT = Path(__file__).parent.parent.parent / "ex4nicegui"

DIST_ROOT = Path(__file__).parent.parent / "dist"


RE_import_stm = re.compile(r"""import(.+)from\s+["|']vue["|']""")


def tran_vue_imports(js_file_name_without_ex: str):
    """把vite生成的js组件文件中的 improt {getCurrentScope as kL,..} from 'vue'
    转换成
    const kL = Vue.getCurrentScope
    ...
    """
    js_file_name = f"{js_file_name_without_ex}.js"

    file = DIST_ROOT / js_file_name
    lines = file.read_text(encoding="utf8").splitlines()
    to_file = EX_REACTIVE_DIR_ROOT / FILE_MAPPING[js_file_name_without_ex]

    i, const_stms = extract_vue_imports(lines)

    if i is not None:
        assert const_stms is not None

        with open(to_file, mode="w", encoding="utf8") as f:
            new_lines = lines[:i] + [const_stms] + lines[i + 1 :]
            f.write("\n".join(new_lines))

    else:
        with open(to_file, mode="w", encoding="utf8") as f:
            f.write(file.read_text(encoding="utf8"))

    print(f"create file[{str(to_file)}]")


def extract_vue_imports(lines: List[str]):
    for i, line in enumerate(lines):
        import_stm = line
        match = RE_import_stm.match(import_stm)
        if match:
            target = match.group(1).replace("{", "").replace("}", "").strip()

            each_as_stms = target.split(",")

            each_const_stms = (as_stem.split(" as ") for as_stem in each_as_stms)

            each_const_stms = [
                f"const {as_stem[1].strip()} = Vue.{as_stem[0].strip()};"
                for as_stem in each_const_stms
            ]

            const_stms = "\n".join(each_const_stms) + "\n"

            return i, const_stms

    return None, None


def copy2styls(src, to_file):
    src = Path(src)
    to_file = Path(to_file)

    file_name = src.name  # noqa: F841

    shutil.copy(src, to_file)


tran_vue_imports("VueUse")
