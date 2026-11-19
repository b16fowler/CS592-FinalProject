#######################################################################
# File containing gui stuff
#######################################################################

import generate
from nicegui import ui
import sympy as sp
from sympy import *

x = symbols("x")

def gui():
    def handle_enter():
        polynomial, shares = generate.generate_polynomial(int(n_input.value), int(k_input.value))

        sp.pprint(polynomial)
        sp.pprint(polynomial.coeff(x,0))
        sp.pprint(shares)
        # ui.notify("n = " + str(int(n_input.value)) + ", k = " + str(int(k_input.value)))
    
    ui.label("Shamir Secret Sharing Key Generator")

    n_input = ui.number(label="Number of keys to generate:", value="1")
    k_input = ui.number(label="Threshold to unlock secret:", value="1")

    ui.button(text="Enter", on_click=handle_enter)
    
    # Run
    ui.run()
