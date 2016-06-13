__author__ = "Linnea"


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


def main():
    """Test script for the functions in this module."""
    oldDelta = 5
    newDelta = proportional_transform(oldDelta, [3])
    print(newDelta)
    newDelta = linear_transform(oldDelta, [6, 7])
    print(newDelta)
    newDelta = polynomial_transform(4, [3, 2, 4, 1, 5, 0])
    print(newDelta)


if __name__ == '__main__':
    main()