"""Assorted Transform Functions for use in modelling.

The transform functions of this module represent a variety of
generalized, predefined transforms for the transform method of the
Vertex class to call. These transforms are what enable the graph to
model complex changes in a linked system. The leading identifier on
each transform function denotes the type of value it takes when
calculating a new delta, and whether its calculations are based upon
edge relationships.

Function Identifiers:
    - AE, Absolute Edge
    - PE, Percent Edge
    - AS, Absolute Self
    - PS, Percent Self

Functions:
    - AE_propotional
    - AE_linear
    - AE_polynomial
    - AE_exponential

Exceptions:
    - TransformError
    - ParameterError
"""


class TransformError(Exception):
    """Base class for exceptions defined by this module.

    The Transform base class defines __init__ and __str__ methods, to
    be used by the assorted exceptions that subclass it. While all
    methods are shared between exception classes in this module, the
    'messages' class data is unique to each exception class, and
    dictates the messages displayed by the exception.

    Class Data:
        - self.messages, the dictionary of predefined messages for the
          exception to use.
        - self.msg, the specific message contained within a given
          instance of the exception.
    """

    messages = {0: "TransformError is intended only to be subclassed, and"
                   "should never be raised directly."}

    def __init__(self, msgKey):
        self.msg = self.messages[msgKey]

    def __str__(self):
        return self.msg


class ParameterError(TransformError):
    """Exception for issues with gc_transform parameters."""

    messages = {0: "The value supplied for the <parameters> argument of the"
                   " gc_transform function is not a valid sequence. Unable to"
                   " extract gc_transform parameters.",
                1: "Sequence index is out of range, insufficient parameters"
                   " present in supplied sequence. Unable to extract all"
                   " necessary gc_transform parameters.",
                2: "A value in the sequence <parameters> is not an integer or a"
                   " float. Unable to use value for gc_transform."}


def AE_proportional(oDelta, parameters):
    """Calculates a new delta based on supplied arguments.

    The function extracts a value from the (theoretically) single-item
    sequence <parameters>, and multiplies this proportional constant by
    the previous absolute delta value to calculate the new delta value.

    Function Arguments:
        - oDelta, the old absolute delta value.
        - parameters, the sequence of parameters to be used for
          calculating the new delta value.
    """

    if isinstance(parameters, (tuple, list)):
        try:
            nDelta = oDelta * parameters[0]
            return float(nDelta)
        except IndexError:
            raise ParameterError(1)
        except ValueError:
            raise ParameterError(2)
    else:
        raise ParameterError(0)


def AE_linear(oDelta, parameters):
    """Calculates a new delta based on supplied arguments.

    The function extracts the gradient and intercept from the
    (hopefully) two-item sequence <parameters>, and uses them to
    calculate a new delta value based on a linear relationship between
    the old one and the new. The defined ordering in the sequence is
    [gradient, intercept].

    Function Arguments:
        - oDelta, the old absolute delta value.
        - parameters, the sequence of parameters to be used for
          calculating the new delta value.
    """

    if isinstance(parameters, (tuple, list)):
        try:
            gradient = parameters[0]
            intercept = parameters[1]
            nDelta = (oDelta * gradient) + intercept
            return float(nDelta)
        except IndexError:
            raise ParameterError(1)
        except ValueError:
            raise ParameterError(2)
    else:
        raise ParameterError(0)


def AE_polynomial(delta, parameters):
    """Calculates a new delta based on supplied arguments.

    Function Arguments:
        - oDelta, the old absolute delta value.
        - parameters, the sequence of parameters to be used for
          calculating the new delta value.
    """

    newDelta = 0
    while len(parameters) != 0:
        coefficient = parameters.pop(0)
        power = parameters.pop(0)
        newDelta += coefficient * delta ** power
    return newDelta


def AE_exponential(delta, parameters):
    """Calculates a new delta based on supplied arguments.

    Function Arguments:
        - oDelta, the old absolute delta value.
        - parameters, the sequence of parameters to be used for
          calculating the new delta value.
    """

    newDelta = 0
    base = parameters[0]
    constant = parameters[1]
    newDelta = base ** delta + constant
    return newDelta


# def foil(x, polynomialOne, polynomialTwo):
#     """Multiplies two polynomials together according to the FOIL
#     method.
#     """
#
#     subTotal = 0
#     total = 0
#     while len(polynomialOne) != 0:
#         coefficientOne = polynomialOne.pop(0)
#         powerOne = polynomialOne.pop(0)
#         termOne = coefficientOne * x ** powerOne
#         for i in range(len(polynomialTwo) // 2):
#             coefficientTwo = polynomialTwo[(2 * i)]
#             powerTwo = polynomialTwo[(2 * i + 1)]
#             termTwo = coefficientTwo * x ** powerTwo
#             newTerm = termOne * termTwo
#             subTotal += newTerm
#         total += subTotal
#         subTotal = 0
#     return total


def main():
    pass


if __name__ == '__main__':
    main()
