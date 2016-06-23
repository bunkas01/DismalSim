__author__ = "Ashleigh"

"""Assorted time-dependent transform functions.

More specifically, these are transform functions where some parameter
of the overall transform function is dependent on the count of the
algorithm calling for the transform.

Functions:
    - proportional_count_linear, determines a coefficient for a
      proportional transform.
"""


def proportional_count_linear(delta, parameters, count):
    """Proportional transform with linearly determined coefficient.

    The function arguments are as follows:
        - delta, the previous delta value, to be transformed into a new
          delta value.
        - parameters, the list of parameters for the transform
          function. List order is extremely important.
        - count, the current count of the function calling this
          function.
    """

    cGradient = parameters[0]
    cConst = parameters[1]
    coefficient = ((cGradient * count) + cConst)
    newDelta = coefficient * delta
    return newDelta



def main():
    """Testing script for the functions time-dependent transforms."""
    oldDelta = 5
    newDelta = proportional_count_linear(oldDelta, [3, 2], 4)
    print(newDelta)


if __name__ == '__main__':
    main()