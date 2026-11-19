#######################################################################
# File containing gui stuff
#######################################################################

from nicegui import ui

def gui():
    # GUI
    ui.label("Hello world")
    ui.button("CLICK ME RIGHT NOW", on_click=lambda: ui.notify("I'VE BEEN CLICKED"))
    ui.run()