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
                   " float. Unable to use value for computation."}


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
            nDelta = oDelta * gradient + intercept
            return float(nDelta)
        except IndexError:
            raise ParameterError(1)
        except ValueError:
            raise ParameterError(2)
    else:
        raise ParameterError(0)


def AE_polynomial(oDelta, parameters):
    """Calculates a new delta based on supplied arguments.

    The function supports a polynomial of arbitrary length, and if the
    polynomial includes a constant, does not require an exponent of
    zero in the sequence for that term of the expression. The exponent
    and coefficient of each term are extracted in turn from the
    sequence <parameters>. The defined order of the sequence is
    [coefficient_1, exponent_1, ... , coefficient_n, exponent_n].

    Function Arguments:
        - oDelta, the old absolute delta value.
        - parameters, the sequence of parameters to be used for
          calculating the new delta value.
    """

    if isinstance(parameters, (tuple, list)):
        try:
            nDelta = 0
            for k in range(len(parameters) // 2):
                coefficient = parameters[2 * k]
                exponent = parameters[(2 * k) + 1]
                nDelta += coefficient * (oDelta ** exponent)
            if len(parameters) % 2 != 0:
                nDelta += parameters[len(parameters) - 1]
            return float(nDelta)
        except IndexError:
            raise ParameterError(1)
        except ValueError:
            raise ParameterError(2)
    else:
        raise ParameterError(0)


def AE_exponential(oDelta, parameters):
    """Calculates a new delta based on supplied arguments.

    The function extracts the base and constant from the (hopefully)
    two-item sequence <parameters>, and uses them to calculate a new
    delta value based on an exponential relationship between the old
    one and the new. The defined ordering in the sequence is [base,
    constant].

    Function Arguments:
        - oDelta, the old absolute delta value.
        - parameters, the sequence of parameters to be used for
          calculating the new delta value.
    """

    if isinstance(parameters, (tuple, list)):
        try:
            base = parameters[0]
            if len(parameters) == 1:
                constant = 0
            else:
                constant = parameters[1]
            nDelta = (base ** oDelta) + constant
            return float(nDelta)
        except IndexError:
            raise ParameterError(1)
        except ValueError:
            raise ParameterError(2)
    else:
        raise ParameterError(0)


def main():
    """Test script for the functions and exceptions in this module.

    Test Components:
        - try-except blocks that deliberately result in raising the
          exceptions defined in this module, following by catching the
          exceptions to test and demonstrate them.
        - Performing computations with each transform, to test the
          accuracy of each functions computations.
    """

    # Begin Error Test
    try:
        AE_proportional(5, "A")
    except ParameterError as error:
        print(error)
    try:
        AE_linear(5, [5])
    except ParameterError as error:
        print(error)
    try:
        AE_proportional(5, ("a",))
    except ParameterError as error:
        print(error)
    # End Error Test

    # Begin Computation Test
    delta = AE_proportional(5, [5])  # Should return 25
    print(delta)
    delta = AE_linear(5, [2, 10])  # Should return 20
    print(delta)
    delta = AE_polynomial(5, (2, 2, 2, 2))  # Should return 100
    print(delta)
    delta = AE_polynomial(5, [2, 2, 10])  # Should return 60
    print(delta)
    delta = AE_exponential(5, [2, 32])  # Should return 64
    print(delta)
    # End Computation Test


if __name__ == '__main__':
    main()
