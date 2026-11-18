#####################################################
## Brett Fowler                                    ##
## Final Project- CS 592                           ##
## Shamir's Secret Sharing Generator               ##
#####################################################

import sympy as sp
from sympy import *
x = symbols('x')
init_printing(use_unicode=True)

def generate_polynomial():
    # Generate polynomial using predetermined
    import random as rng
    # rng.seed(33)
    n = 6; k = 3
    # TODO: Change rng secret range
    s = rng.randint(999, 10000)

    # Generate random secret and k - 1 integers to create polynomial
    polynomial = s
    # Starting at 1 because it makes exponents easier

    for i in range(1, k):
        # TODO: Change coefficient rng range
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

    # Fix shares to match Wiki example for testing
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
    
    
def main():

    shares = generate_polynomial()
    secret = retrieve_secret(shares)
    sp.pprint(secret)


if __name__ == "__main__":
    main()