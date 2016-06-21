__author__ = "Ashleigh"

"""Placeholder Docstring."""


def proportional_count(delta, parameters, count):
    """placeholder."""
    cGradient = parameters[0]
    cConst = parameters[1]
    coefficient = ((cGradient * count) + cConst)
    newDelta = coefficient * delta
    return newDelta



def main():
    oldDelta = 5
    newDelta = proportional_count(oldDelta, [3, 2], 4)
    print(newDelta)


if __name__ == '__main__':
    main()