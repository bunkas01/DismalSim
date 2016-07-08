"""Assorted Transform Functions for use in modelling.

The transform functions of this module represent a variety of
generalized, predefined transforms for the transform method of the
Vertex class to call. These transforms are what enable the graph to
model complex changes in a linked system. The leading identifier on the
function names is shorthand for the input and output, not in the usual
sense of a return type, but in terms of whether the transform takes an
absolute or percentage value as input, and returns an absolute or
percentage value as output. When a percentage change is returned, it is
returned as a multiplier, not a percentage proper. Additionally, a
'base' identifier is used, marking the wrapped functions containing
code shared across analogous transform types.

Function Identifiers:
    - AA, takes an absolute change, returns an absolute change.
    - AP, takes an absolute change, returns a percentage change.
    - PA, takes a percentage change, returns an absolute change.
    - PP, takes a percentage change, returns a percentage change.
    - base, a basic transform function, wrapped by the other functions
      to reduce code repetition.

Functions:
    - base_linear
    - base_exponential
    - base_polynomial
    - AA_linear
    - AA_exponential
    - AA_polynomial
    - AP_linear
    - AP_exponential
    - AP_polynomial
    - PA_linear
    - PA_exponential
    - PA_polynomial
    - PP_ linear
    - PP_exponential
    - PP_polynomial

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


def base_linear(value, parameters):
    """Basic linear transform function, intended for wrapping.

    The defined ordering for the sequence is [gradient, <intercept>],
    where the intercept is optional, and will default to 0.

    Function Arguments:
        - value, the value to be linearly transformed
        - parameters, the container sequence (Current implementation
          accepts tuples and lists) holding the parameters for the
          transform function.
    """

    if isinstance(parameters, (tuple, list)):
        try:
            gradient = parameters[0]  # Extracts the gradient
            if len(parameters) > 1:  # For expressions with an intercept
                intercept = parameters[1]  # Extracts the intercept, if present
            else:  # For expressions without a constant
                intercept = 0
            newVal = (gradient * value) + intercept
            return float(newVal)
        except IndexError:
            raise ParameterError(1)
        except ValueError:
            raise ParameterError(2)
        except TypeError:
            raise ParameterError(2)
    else:
        raise ParameterError(0)


def base_exponential(value, parameters):
    """Basic exponential transform function, intended for wrapping.

    The defined ordering for the sequence is [base, <constant>], where
    the constant is optional and will default to 0.

    Function Arguments:
        - value, the value to be exponentially transformed.
        - parameters, the container sequence (Current implementation
          accepts tuples and lists) holding the parameters for the
          transform function.
    """

    if isinstance(parameters, (tuple, list)):
        try:
            base = parameters[0]  # Extracts the base
            if len(parameters) > 1:  # For expressions with a constant
                constant = parameters[1]  # Extracts the constant, if present
            else:  # For expressions without a constant
                constant = 0
            newVal = (base ** value) + constant
            return float(newVal)
        except IndexError:
            raise ParameterError(1)
        except ValueError:
            raise ParameterError(2)
    else:
        raise ParameterError(0)


def base_polynomial(value, parameters):
    """Basic polynomial transform function, intended for wrapping.

    The defined ordering for the sequence is [coefficient 1,
    exponent 1, coefficient 2, exponent 2, . . . , coefficient n,
    exponent n], where n is an arbitrary integer, as the function
    supports polynomial expressions of arbitrary length.

    Function Arguments:
        - value, the value to be polynomially transformed
        - parameters, the container sequence (Current implementation
          accepts tuples and lists) holding the parameters for the
          transform function.
    """

    if isinstance(parameters, (tuple, list)):
        try:
            newVal = 0
            for k in range(len(parameters) // 2):
                coefficient = parameters[2 * k]  # Extracts the coefficient
                exponent = parameters[(2 * k) + 1]  # Extracts the exponent
                newVal += coefficient * (value ** exponent)
            if len(parameters) % 2 != 0:  # For polynomials with constants
                constant = parameters[len(parameters) - 1]
                newVal += constant
            return float(newVal)
        except IndexError:
            raise ParameterError(1)
        except ValueError:
            raise ParameterError(2)
        except TypeError:
            raise ParameterError(2)
    else:
        raise ParameterError(0)


def AA_linear(value, parameters):
    """Returns an absolute change based on an absolute change.

    This function is a wrapper function for base_linear, and is
    intended to simplify computation of linearly related changes, as
    well as simplify the usage of transform functions in Vertex
    transform methods.

    Function Arguments:
        - value, the value to be linearly transformed.
        - parameters, the container sequence (Current implementation
          accepts tuples and lists) holding the parameters for the
          transform function.
    """

    newVal = base_linear(value, parameters)
    return newVal


def AA_exponential(value, parameters):
    """Returns an absolute change based on an absolute change.

    This function is a wrapper function for base_exponential, and is
    intended to simplify computation of exponentially related changes,
    as well as simplify the usage of transform functions in Vertex
    transform methods.

    Function Arguments:
        - value, the value to be exponentially transformed.
        - parameters, the container sequence (Current implementation
          accepts tuples and lists) holding the parameters for the
          transform function.
    """

    newVal = base_exponential(value, parameters)
    return newVal


def AA_polynomial(value, parameters):
    """Returns an absolute change based on an absolute change.

    This function is a wrapper function for base_polynomial, and is
    intended to simplify computation of polynomially related changes,
    as well as simplify the usage of transform functions in Vertex
    transform methods.

    Function Arguments:
        - value, the value to be polynomially transformed.
        - parameters, the container sequence (Current implementation
          accepts tuples and lists) holding the parameters for the
          transform function.
    """

    newVal = base_polynomial(value, parameters)
    return newVal


def AP_linear(value, parameters):
    """Returns a percentage change based on an absolute change.

    This function is a wrapper function for base_linear, and is
    intended to simplify computation of linearly related changes, as
    well as simplify the usage of transform functions in Vertex
    transform methods.

    Function Arguments:
        - value, the value to be linearly transformed.
        - parameters, the container sequence (Current implementation
          accepts tuples and lists) holding the parameters for the
          transform function.
    """

    percentage = base_linear(value, parameters)
    multiplier = (percentage / 100)
    return multiplier


def AP_exponential(value, parameters):
    """Returns a percentage change based on an absolute change.

    This function is a wrapper function for base_exponential, and is
    intended to simplify computation of exponentially related changes,
    as well as simplify the usage of transform functions in Vertex
    transform methods.

    Function Arguments:
        - value, the value to be exponentially transformed.
        - parameters, the container sequence (Current implementation
          accepts tuples and lists) holding the parameters for the
          transform function.
    """

    percentage = base_exponential(value, parameters)
    multiplier = (percentage / 100)
    return multiplier


def AP_polynomial(value, parameters):
    """Returns a percentage change based on an absolute change.

    This function is a wrapper function for base_polynomial, and is
    intended to simplify computation of polynomially related changes,
    as well as simplify the usage of transform functions in Vertex
    transform methods.

    Function Arguments:
        - value, the value to be polynomially transformed.
        - parameters, the container sequence (Current implementation
          accepts tuples and lists) holding the parameters for the
          transform function.
    """

    percentage = base_polynomial(value, parameters)
    multiplier = (percentage / 100)
    return multiplier


def PA_linear(value, parameters):
    """Returns an absolute change based on a percentage change.

    This function is a wrapper function for base_linear, and is
    intended to simplify computation of linearly related changes, as
    well as simplify the usage of transform functions in Vertex
    transform methods.

    Function Arguments:
        - value, the value to be linearly transformed.
        - parameters, the container sequence (Current implementation
          accepts tuples and lists) holding the parameters for the
          transform function.
    """

    newVal = base_linear(value, parameters)
    return newVal


def PA_exponential(value, parameters):
    """Returns an absolute change based on a percentage change.

    This function is a wrapper function for base_exponential, and is
    intended to simplify computation of exponentially related changes,
    as well as simplify the usage of transform functions in Vertex
    transform methods.

    This function is a wrapper function for base_linear, and is
    intended to simplify computation of linearly related changes, as
    well as simplify the usage of transform functions in Vertex
    transform methods.

    Function Arguments:
        - value, the value to be exponentially transformed.
        - parameters, the container sequence (Current implementation
          accepts tuples and lists) holding the parameters for the
          transform function.
    """

    newVal = base_exponential(value, parameters)
    return newVal


def PA_polynomial(value, parameters):
    """Returns an absolute change based on a percentage change.

    This function is a wrapper function for base_polynomial, and is
    intended to simplify computation of polynomially related changes,
    as well as simplify the usage of transform functions in Vertex
    transform methods.

    Function Arguments:
        - value, the value to be polynomially transformed.
        - parameters, the container sequence (Current implementation
          accepts tuples and lists) holding the parameters for the
          transform function.
    """

    newVal = base_polynomial(value, parameters)
    return newVal


def PP_linear(value, parameters):
    """Returns a percentage change based on a percentage change.

    This function is a wrapper function for base_linear, and is
    intended to simplify computation of linearly related changes, as
    well as simplify the usage of transform functions in Vertex
    transform methods.

    Function Arguments:
        - value, the value to be linearly transformed.
        - parameters, the container sequence (Current implementation
          accepts tuples and lists) holding the parameters for the
          transform function.
    """

    percentage = base_linear(value, parameters)
    multiplier = (percentage / 100)
    return multiplier


def PP_exponential(value, parameters):
    """Returns a percentage change based on a percentage change.

    This function is a wrapper function for base_exponential, and is
    intended to simplify computation of exponentially related changes,
    as well as simplify the usage of transform functions in Vertex
    transform methods.

    Function Arguments:
        - value, the value to be exponentially transformed.
        - parameters, the container sequence (Current implementation
          accepts tuples and lists) holding the parameters for the
          transform function.
    """

    percentage = base_exponential(value, parameters)
    multiplier = (percentage / 100)
    return multiplier


def PP_polynomial(value, parameters):
    """Returns a percentage change based on a percentage change.

    This function is a wrapper function for base_polynomial, and is
    intended to simplify computation of polynomially related changes,
    as well as simplify the usage of transform functions in Vertex
    transform methods.

    Function Arguments:
        - value, the value to be polynomially transformed.
        - parameters, the container sequence (Current implementation
          accepts tuples and lists) holding the parameters for the
          transform function.
    """

    percentage = base_polynomial(value, parameters)
    multiplier = (percentage / 100)
    return multiplier


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
        base_linear(5, "a")
    except ParameterError as error:
        print(error)
    try:
        base_linear(5, [5])
    except ParameterError as error:
        print(error)
    try:
        base_linear(5, [5, "a"])
    except ParameterError as error:
        print(error)
    # End Error Test

    # Begin Computation Test
    # base transforms
    print("Testing base transform functions.")
    aVal = base_linear(5, [2, 5])  # Should return 15
    print(aVal)
    aVal = base_exponential(5, [2, 32])  # Should return 64
    print(aVal)
    aVal = base_polynomial(5, [2, 2, 3, 3])  # Should return 425
    print(aVal)

    # AA transforms
    print("Testing absolute-absolute transform functions.")
    aVal = AA_linear(3, [3, 2])  # Should return 11
    print(aVal)
    aVal = AA_exponential(2, [2, 4])  # Should return 8
    print(aVal)
    aVal = AA_polynomial(3, [1, 2, 2, 3, 9])  # Should return 72
    print(aVal)

    # AP transforms
    print("Testing absolute-percentage transform functions.")
    aVal = AP_linear(10, [3, 5])  # Should return .35
    print(aVal)
    print(aVal * 100)  # Should print 35
    aVal = AP_exponential(7, [2])  # Should return 1.28
    print(aVal)
    print(aVal * 100)  # Should print 128
    aVal = AP_polynomial(5, [1, 2])  # Should return .25
    print(aVal)
    print(aVal * 100)  # Should print 25

    # PA transforms
    print("Testing percentage-absolute transform functions.")
    aVal = PA_linear(30, [2])  # Should return 60
    print(aVal)
    aVal = PA_exponential(2, [4, 16])  # Should return 32
    print(aVal)
    aVal = PA_polynomial(6, [1, 2, 12])  # Should return 48
    print(aVal)

    # PP transforms
    print("testing percentage-percentage transform functions.")
    aVal = PP_linear(20, [2.5, 6])  # Should return .56
    print(aVal)
    print(aVal * 100)  # Should print 56
    aVal = PP_exponential(3, [3, 13])  # Should return .4
    print(aVal)
    print(aVal * 100)  # Should print 40
    aVal = PP_polynomial(4, [1, 3, 1, 2])  # Should return .8
    print(aVal)
    print(aVal * 100)  # Should print 80

    # End Computation Test


if __name__ == '__main__':
    main()
