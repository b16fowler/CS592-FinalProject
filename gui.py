#######################################################################
# File containing gui stuff
#######################################################################

import generate
from nicegui import ui
import sympy as sp
from sympy import *

x = symbols("x")

def gui():
    def handle_generate():
        show_shares()

        reconstruct()

    def show_shares():
        polynomial, shares = generate.generate_polynomial(int(n_input.value), int(k_input.value))
        
        # Show secret in markdown
        ui.markdown(content=f"**Secret**\n\n{polynomial.coeff(x, 0)}")

        # Show shares in markdown
        for i in range(len(shares)):
            share = f"**Share #{i + 1}**\n\n({shares[i][0]}, {shares[i][1]})"
            ui.markdown(content=share)

    # ui for entering share info to reconstruct secret
    def reconstruct():
        # Create entry box for each k
        for i in range(len(k_input.value)):
            with ui.splitter() as splitter:
                with splitter.before:
                    ui.number(label=f"**Share #{i + 1}:** Enter x value")
                with splitter.after:
                    ui.number(label=f"Enter y value")

    # Heading
    ui.label("Shamir Secret Sharing Key Generator")

    # Input boxes for n and k
    with ui.splitter() as splitter:
        with splitter.before:
            n_input = ui.number(label="Number of keys to generate:", value="5")
        with splitter.after:
            k_input = ui.number(label="Threshold to unlock secret:", value="3")
    
    ui.button(text="Enter", on_click=handle_generate)
    md = ui.markdown("")

    # Run
    ui.run()
