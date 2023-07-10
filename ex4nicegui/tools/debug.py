from signe.core.effect import Effect
import ex4nicegui.reactive as rxui
from ex4nicegui.utils.signals import ReadonlyRef, DescReadonlyRef, Ref, ref_computed
from nicegui import ui
from typing import Callable, Dict, TypeVar, Generic

T = TypeVar("T")


def display_ref_vars_ui(vars_dict: Dict):
    cols = [
        {"name": "var", "label": "变量名", "field": "var"},
        {"name": "type", "label": "类型", "field": "type"},
        {"name": "desc", "label": "描述", "field": "desc", "style": "min-width:10rem"},
        {"name": "deps", "label": "依赖", "field": "deps"},
        {
            "name": "value",
            "label": "值",
            "field": "value",
            "align": "left",
        },
    ]

    need_vars_dict = {
        var: value
        for var, value in vars_dict.items()
        if isinstance(value, (ReadonlyRef, Effect))
    }

    all_ref_var_map = {
        getattr(value, "_Ref___signal"): var
        for var, value in need_vars_dict.items()
        if isinstance(value, Ref) and getattr(value, "_Ref___signal") is not None
    }

    all_computed_var_map = {
        getattr(value, "_ReadonlyRef___getter"): var
        for var, value in need_vars_dict.items()
        if isinstance(value, DescReadonlyRef)
    }

    @ref_computed(priority_level=9999)
    def cp_rows():
        rows = []

        for var, value in need_vars_dict.items():
            if isinstance(value, Effect):
                row = _handler_Effect_rows(
                    var, value, all_ref_var_map, all_computed_var_map
                )
                rows.append(row)

            if isinstance(value, ReadonlyRef):
                row = _handler_ReadonlyRef_rows(
                    var, value, all_ref_var_map, all_computed_var_map
                )
                rows.append(row)

        return rows

    table = rxui.table(cols, cp_rows, pagination=None)
    table.element.classes("w-full").props('separator="cell" wrap-cells=true')

    # _with_slit(table.element)


def _with_slit(table: ui.table):
    table.add_slot(
        "body",
        r"""
 <q-tr :props="props">
        <q-td key="var" :props="props">
            {{ props.row.var }}  
        </q-td>
        <q-td key="type" :props="props">
            {{ props.row.type }}  
        </q-td>
        <q-td key="desc" :props="props">
            {{ props.row.desc }}  
        </q-td>

        <q-td key="deps" :props="props">
            <div v-if="props.row.deps" class="flex flex-col gap-2 items-start">

                <p  v-for="d in props.row.deps.split(',')">
                    {{ d }}
                </p>   

            </div>
        </q-td>

        <q-td key="value" :props="props">
            {{ props.row.value }}  
        </q-td>
    </q-tr>
""",
    )


def _handler_ReadonlyRef_rows(
    var: str, ref: ReadonlyRef, all_ref_var_map, all_computed_var_map
):
    row = {
        "var": var,
        "type": ref.__class__.__name__.replace("DescReadonlyRef", "ReadonlyRef"),
    }

    if isinstance(ref, DescReadonlyRef):
        desc_computed = ref
        row["desc"] = desc_computed.desc

        cp_deps_str = _ReadonlyRef_deps_str(
            desc_computed, all_ref_var_map, all_computed_var_map
        )

        row["deps"] = cp_deps_str

    row["value"] = str(ref.value)
    return row


def _ReadonlyRef_deps_str(desc_computed, all_ref_var_map, all_computed_var_map):
    desc_computed.value

    computed_obj = getattr(desc_computed, "_ReadonlyRef___getter")
    if not isinstance(computed_obj.getter, Effect):
        return ""

    effect_obj = computed_obj.getter

    dep_signals = getattr(effect_obj, "_Effect__dep_signals")

    s_vars = [var for s, var in all_ref_var_map.items() if s in dep_signals]

    dep_effects = set(effect_obj._get_pre_dep_effects())

    c_vars = [var for s, var in all_computed_var_map.items() if s.getter in dep_effects]

    return ",".join([*s_vars, *c_vars])


def _handler_Effect_rows(
    var: str, effect_obj: Effect, all_ref_var_map, all_computed_var_map
):
    row = {
        "var": var,
        "type": "Effect",
    }

    cp_deps_str = _Effect_deps_str(effect_obj, all_ref_var_map, all_computed_var_map)

    row["deps"] = cp_deps_str

    return row


def _Effect_deps_str(effect_obj: Effect, all_ref_var_map, all_computed_var_map):
    dep_signals = getattr(effect_obj, "_Effect__dep_signals")

    s_vars = [var for s, var in all_ref_var_map.items() if s in dep_signals]

    dep_effects = set(effect_obj._get_pre_dep_effects())

    all_effect_var_map = {s.getter: var for s, var in all_computed_var_map.items()}

    c_vars = [var for e, var in all_effect_var_map.items() if e in dep_effects]

    return ",".join([*s_vars, *c_vars])
