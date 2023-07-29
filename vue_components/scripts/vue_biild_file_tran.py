from pathlib import Path
import re
import shutil

EX_REACTIVE_DIR_ROOT = Path(__file__).parent.parent.parent / 'ex4nicegui'/'reactive'

DIST_ROOT = Path(__file__).parent.parent / 'dist'


RE_import_stm = re.compile(r"""import(.+)from\s+["|']vue["|']""")


def tran_vue_imports(js_file_name_without_ex:str):
    """把vite生成的js组件文件中的 improt {getCurrentScope as kL,..} from 'vue'
    转换成
    const kL = Vue.getCurrentScope
    ...
    """

    js_file_name = f'{js_file_name_without_ex}.js'

    file = DIST_ROOT / js_file_name
    lines = file.read_text(encoding="utf8").splitlines()
    import_stm = lines[0]
    match = RE_import_stm.match(import_stm)

    if match:
        target = match.group(1).replace("{", "").replace("}", "").strip()

        each_as_stms = target.split(",")

        each_const_stms = (as_stem.split("as") for as_stem in each_as_stms)

        each_const_stms = [
            f"const {as_stem[1].strip()} = Vue.{as_stem[0].strip()}"
            for as_stem in each_const_stms
        ]

        # each_const_stms.append('const defineExpose = Vue.defineExpose')

        const_stms = "\n".join(each_const_stms) + "\n"
        # print(const_stms)

        to_file = EX_REACTIVE_DIR_ROOT/ js_file_name_without_ex / js_file_name

        with open(to_file, mode="w", encoding="utf8") as f:
            f.write(const_stms)
            f.write("\n".join(lines[1:]))

    # print(RE_import_stm.match(import_stm))


def copy2styls(src, to_file):
    src = Path(src)
    to_file = Path(to_file)

    file_name = src.name

    shutil.copy(src, to_file)




tran_vue_imports('dropZone')


