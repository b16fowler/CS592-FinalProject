#####################################################
## Brett Fowler                                    ##
## Final Project- CS 592                           ##
## Shamir's Secret Sharing Generator               ##
#####################################################

import sympy as sp
import gui
from sympy import *
from nicegui import ui

x = symbols('x')
init_printing(use_unicode=True)

def generate_polynomial():
    import random as rng
    # Number of shares being generated
    n = 6
    # Minimum number of shares needed to reconstruct secret
    k = 3

    # Generate 128 bit random secret
    s_binary = f"{rng.getrandbits(128):0{128}b}"
    s = int(s_binary, 2)

    # Generate random secret and k - 1 integers to create polynomial
    polynomial = s
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

def retrieve_secret(shares):
    # Reconstruct secret using k shares

    # TODO: Fix shares to match Wiki example for testing
    (x1, y1) = (2, 1942); (x2, y2) = (4, 3402); (x3, y3) = (5, 4414)

    # Using (x1, y1), (x2, y2) and (x3, y3) for Lagrange basis polynomials
    l1 = expand((x - x2)/(x1 - x2)*(x - x3)/(x1 - x3))    
    l2 = expand((x - x1)/(x2 - x1)*(x - x3)/(x2 - x3))
    l3 = expand((x - x1)/(x3 - x1)*(x - x2)/(x3 - x2))

    # Use formulafor polynomial interpolation
    # f(x) = y1*l1(x) + y2*l2(x) + y2*l2(x)
    fx = simplify(y1 * (l1) + y2 * (l2) + y3 * (l3))

    # x^0 coefficient is the secret
    return fx.coeff(x, 0)

def encrypt():
    pass

def decrypt():
    pass
    
def main():

    # GUI
    gui.gui()

    # shares = generate_polynomial()
    # secret = retrieve_secret(shares)
    # sp.pprint(secret)


main()