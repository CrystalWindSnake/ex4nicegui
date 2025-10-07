from nicegui import ui
from ex4nicegui import rxui


class PaginationTable(rxui.ViewModel):
    page_size = 10

    def __init__(self):
        super().__init__()

        self.columns = [
            {
                "name": "name",
                "label": "Name",
                "field": "name",
                "required": True,
                "align": "left",
            },
            {"name": "age", "label": "Age", "field": "age", "sortable": True},
        ]

        self.rows = [{"name": f"n{idx}", "age": idx} for idx in range(100)]

        self.pagination = rxui.use_pagination(self.rows, self.page_size)

    @property
    def data(self):
        return self.pagination.current_source

    def create(self):
        with (
            rxui.table(self.columns, self.data).props("hide-pagination").add_slot("top")
        ):
            with ui.row().classes("flex-center"):
                rxui.select(
                    [10, 15, 20, 30],
                    label="number of rows per page",
                    value=self.page_size,
                ).classes("min-w-[8em]").props("dense outlined")
                self.pagination.create_q_pagination().props(
                    ' outline  color="orange" active-design="unelevated"  active-color="brown"  active-text-color="orange"'
                )


def index():
    ptable = PaginationTable()
    ptable.create()
