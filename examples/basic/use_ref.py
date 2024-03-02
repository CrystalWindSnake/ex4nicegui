from nicegui import ui
from ex4nicegui import rxui, deep_ref

ui.button.default_props("no-caps")

data = deep_ref([1, 2, 3])
show = deep_ref(True)  # or to_ref(True)


def toggle():
    show.value = not show.value


with ui.row():
    ui.button("toggle list", on_click=toggle)
    ui.button("push number", on_click=lambda: data.value.append(len(data.value) + 1))
    ui.button("pop number", on_click=lambda: len(data.value) and data.value.pop())
    ui.button("reverse list", on_click=lambda: data.value.reverse())

# must be a function to be triggered
rxui.label(lambda: f"{len(data.value)=}")
rxui.label(lambda: f"{show.value=!s}")

# show is a ref, it can be triggered by passing it directly.
rxui.label(show)

# can't be triggered because it's equivalent to `rxui.label(True)`
rxui.label(str(show.value))

with rxui.column().bind_visible(show):

    @rxui.vfor(data)
    def _(store: rxui.VforStore[int]):
        item = store.get()
        rxui.label(item)
