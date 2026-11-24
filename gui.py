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

    def handle_reconstruct():
        for i in x_inputs:
            print(x_inputs[i].value)

    def show_shares():
        polynomial, shares = generate.generate_polynomial(int(n_input.value), int(k_input.value))
        
        # Show secret in markdown
        ui.markdown(content=f"**Secret**\n\n{polynomial.coeff(x, 0)}")

        # Show shares in markdown
        for i in range(len(shares)):
            share = f"**Share #{i + 1}**\n\n({shares[i][0]}, {shares[i][1]})"
            ui.markdown(content=share)

    # ui for entering share info to reconstruct secret
    x_inputs = {}
    y_inputs = {}
    def reconstruct():
        # Create entry box for each share, k
        for i in range(int(k_input.value)):
            ui.markdown(f"Share #{i + 1}:")
            with ui.splitter() as splitter:
                with splitter.before:
                    x_inputs[i] = ui.number(label=f"x value", value=i)
                with splitter.after:
                    y_inputs[i] = ui.number(label=f"y value")
        ui.button(text="Submit", on_click=handle_reconstruct)


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
