from nicegui import ui, app
from app.startup import startup


app.on_startup(startup)


ui.run()
