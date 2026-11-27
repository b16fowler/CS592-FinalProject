####################################################
# generation.py
####################################################

import sympy as sp
from sympy import *

x = symbols("x")
init_printing(use_unicode=True)

# n is number of shares being generated, k is key threshold
def generate_polynomial(n, k):
    import random as rng

    # Generate 128 bit random secret
    s_binary = f"{rng.getrandbits(128):0{128}b}"
    s = int(s_binary, 2)

    # Generate random secret and k - 1 integers to create polynomial
    polynomial = simplify(s)
    # Starting at 1 because it makes exponents easier
    for i in range(1, k):
        # TODO: Change coefficient rng range ?
        # Generate random number r as coefficient
        r = rng.randint(85, 200)
        # Append to polynomial
        polynomial += simplify(r * x**(i))

    # Calculate n shares
    shares = []
    # Starting at 1 again because it makes exponents easier
    for i in range(1, n + 1):
        # Substitute 'x' variable for 'i' value
        y = polynomial.subs(x, i)
        # Append to shares list
        shares.append((i, y))

    return polynomial, shares
