from nicegui import ui

from ex4nicegui import rxui, to_ref
from ex4nicegui.layout import grid_box
from viewModel import State, TodoItem


# ui
def page_init():
    ui.query("body").classes("bg-[#f5f5f5]")

    # ui.query("main.q-page").classes("flex justify-stretch items-stretch")
    # ui.query(".nicegui-content").classes("w-full")
    ui.row.default_classes("w-full items-center")
    ui.column.default_classes("w-full items-center")
    ui.input.default_classes("min-w-[20ch]").default_props("outlined dense")
    ui.card.default_classes("flex flex-col no-wrap")
    ui.grid.default_classes("w-full")
    ui.button.default_classes("w-fit")


page_init()


# main ui
state = State()


def job_panel():
    with ui.element("div").classes(" w-full job-panel"), ui.card().classes(
        "flex-center py-10"
    ):
        input_content = to_ref("")

        def add_todo():
            state.add_todo(input_content.value)
            input_content.value = ""

        with ui.row().classes("gap-0 flex-center"):
            rxui.input(
                value=input_content, placeholder="What would you like to do?"
            ).classes("w-[80%]").on(
                "keyup.enter",
                add_todo,
            )
            rxui.button(icon="add", on_click=add_todo).classes(
                "text-white self-stretch"
            ).props("square").bind_enabled(lambda: len(input_content.value) > 0)


def todo_list_panel():
    with ui.element("div").classes(
        " w-full grow overflow-hidden"
    ) as outter, ui.card().tight().classes(" py-4 h-full overflow-hidden"):
        # header
        with ui.row():
            with ui.element("q-chip").props(
                'class="glossy" square color="teal" text-color="white" icon="bookmark"'
            ):
                ui.label("todo list").classes("text-h5")

        with grid_box(template_columns="1fr auto 1fr", vertical="center"):
            rxui.label(lambda: f"{state.active_count.value} items left").bind_visible(
                lambda: state.total_count.value > 0
            )

            rxui.radio(["all", "active", "completed"], value=state.filter_do).classes(
                "row"
            ).bind_visible(lambda: state.total_count.value > 0)

            rxui.button("clear completed", on_click=state.remove_completed_todos).props(
                "desen  flat"
            ).bind_visible(lambda: state.completed_count.value > 0)

        # table
        with grid_box(template_columns="5fr 1fr auto", vertical="center").classes(
            "px-10 overflow-y-auto"
        ):
            ui.label("List").classes("pl-2").on("dblclick", state.all_unchecks).tooltip(
                "double click all uncheck"
            ).tailwind.cursor("pointer").user_select("none")
            ui.label("Status").classes("place-self-center px-20")
            ui.label("Close").classes("place-self-center  px-10")

            @rxui.vfor(state.filtered_todos, key="id")
            def _(store: rxui.VforStore[TodoItem]):
                todo = store.get()

                rxui.checkbox(
                    lambda: todo.value.title, value=rxui.vmodel(todo, "completed")
                )

                with ui.element("q-chip").classes("w-fit place-self-center").props(
                    "square clickable color=primary text-color=white"
                ) as chip:
                    rxui.label(
                        lambda: "completed" if todo.value.completed else "pending"
                    )

                def switch_todo_state():
                    todo.value.completed = not todo.value.completed

                chip.on("click", switch_todo_state)

                rxui.button(
                    icon="delete",
                    color=lambda: "negative" if todo.value.completed else "grey-4",
                    on_click=lambda: state.remove_todo(todo.value),
                ).classes("place-self-center").props(
                    "round desen push flat "
                ).bind_enabled(lambda: todo.value.completed)

    return outter


with ui.card().classes("w-[50vw] self-center  overflow-hidden").style(
    "height:calc(100vh - calc(var(--nicegui-default-padding) * 2));"
):
    ui.label("todo list").classes("text-h3 self-center bg-primary px-6 text-white")
    rxui.linear_progress(state.completion_ratio)
    job_panel()

    todo_list_panel()


ui.run()
