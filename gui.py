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
        # Display generated shares and true_secret in markdown
        shares, true_secret = display_shares()

        # Number input boxes to enter share info to reconstruct secret
        share_inputs(shares, true_secret)

    # Called when 'Submit' button is clicked after user has entered information of k-shares
    def handle_reconstruct(true_secret):
        # Keep all inputs in list of tuples
        inputs = []
        for i in range(len(x_inputs)):
            inputs.append((x_inputs[i].value, y_inputs[i].value))

        # Reconstruct Lagrange polynomials
        ### This nested for loop was borrowed from ai ###
        secret = 0
        for i, (xi, yi) in enumerate(inputs):
            numerator = sp.Rational(1)
            denominator = sp.Rational(1)

            for j, (xj, yj) in enumerate(inputs):
                if i != j:
                    numerator *= -xj
                    denominator *= (xi - xj)
            lagrange = numerator / denominator
            secret += yi * lagrange
        
        found_secret = sp.simplify(secret)

        if found_secret == true_secret:
            ui.markdown(content="Secret successfully reconstructed")

    def display_shares():
        polynomial, shares = generate.generate_polynomial(int(n_input.value), int(k_input.value))
        
        # Show secret in markdown
        true_secret = polynomial.coeff(x, 0)
        ui.markdown(content=f"**Secret**\n\n{true_secret}")

        # Show shares in markdown
        for i in range(len(shares)):
            share = f"**Share #{i + 1}**\n\n({shares[i][0]}, {shares[i][1]})"
            ui.markdown(content=share)

        return shares, true_secret

    # ui for entering share info to reconstruct secret
    x_inputs = {}
    y_inputs = {}
    def share_inputs(shares, true_secret):
        # Create entry box for each share, k
        for i in range(int(k_input.value)):
            ui.markdown(f"Share #{i + 1}:")
            with ui.splitter() as splitter:
                with splitter.before:
                    x_inputs[i] = ui.number(label=f"x value", value=shares[i][0])
                with splitter.after:
                    y_inputs[i] = ui.number(label=f"y value", value=shares[i][1])
        ui.button(text="Submit", on_click=lambda: handle_reconstruct(true_secret))


    # Heading
    ui.label("Shamir Secret Sharing Key Generator")

    # Input boxes for n and k
    with ui.splitter() as splitter:
        with splitter.before:
            n_input = ui.number(label="Keys to generate:", value="5")
        with splitter.after:
            k_input = ui.number(label="Threshold to unlock secret:", value="3")
    
    ui.button(text="Enter", on_click=handle_generate)

    # Run
    ui.run(dark=True)
