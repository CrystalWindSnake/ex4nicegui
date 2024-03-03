from nicegui import ui
from ex4nicegui import rxui, to_ref


columns = [
    {
        "name": "name",
        "label": "Name",
        "field": "name",
        "required": True,
        "align": "left",
    },
    {"name": "age", "label": "Age", "field": "age", "sortable": True},
]

rows = [{"name": f"n{idx}", "age": idx} for idx in range(100)]

page_size = to_ref(10)
pagination = rxui.use_pagination(rows, page_size)

with rxui.table(columns, pagination.current_source).props("hide-pagination").add_slot(
    "top"
):
    with ui.row().classes("flex-center"):
        rxui.select([10, 15, 20, 30], label="每页数量", value=page_size).classes(
            "min-w-[8em]"
        ).props("dense outlined")
        pagination.create_q_pagination().props(
            ' outline  color="orange" active-design="unelevated"  active-color="brown"  active-text-color="orange"'
        )
