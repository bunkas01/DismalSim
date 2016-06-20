__author__ = "Linnea"

"""Assorted transformative functions for TransformEdges to call.

Functions:
    - proportional_transform
    - linear_transform
    - polynomial_transform
    - exponential_transform
    - foil
"""


def proportional_transform(delta, parameters):
    """Multiplies a delta by a proportional coefficient."""
    newDelta = delta * parameters[0]
    return newDelta


def linear_transform(delta, parameters):
    """Transforms a delta according to a linear relationship."""
    newDelta = delta * parameters[0] + parameters[1]
    return newDelta


def polynomial_transform(delta, parameters):
    """Transforms a delta by some polynomial."""
    newDelta = 0
    while len(parameters) != 0:
        coefficient = parameters.pop(0)
        power = parameters.pop(0)
        newDelta += coefficient * delta ** power
    return newDelta


def exponential_transform(delta, parameters):
    """Transforms a delta according to an exponential relationship."""
    newDelta = 0
    base = parameters[0]
    constant = parameters[1]
    newDelta = base ** delta + constant
    return newDelta


def foil(x, polynomialOne, polynomialTwo):
    """Attempts to FOIL things"""
    subTotal = 0
    total = 0
    while len(polynomialOne) != 0:
        coefficientOne = polynomialOne.pop(0)
        powerOne = polynomialOne.pop(0)
        termOne = coefficientOne * x ** powerOne
        for i in range(len(polynomialTwo) // 2):
            coefficientTwo = polynomialTwo[(2 * i)]
            powerTwo = polynomialTwo[(2 * i + 1)]
            termTwo = coefficientTwo * x ** powerTwo
            newTerm = termOne * termTwo
            subTotal += newTerm
        total += subTotal
        subTotal = 0
    return total


def main():
    """Test script for the functions in this module."""
    oldDelta = 5
    newDelta = proportional_transform(oldDelta, [3])
    print(newDelta)
    newDelta = linear_transform(oldDelta, [6, 7])
    print(newDelta)
    newDelta = polynomial_transform(4, [3, 2, 4, 1, 5, 0])
    print(newDelta)
    total = foil(2, [1, 2, 3, 1, 5, 0], [3, 2, 4, 1, 1, 0])
    print(total)
    newDelta = exponential_transform(3, [6, 13])
    print(newDelta)


if __name__ == '__main__':
    main()