__author__ = "Ashleigh Bunkofske"

"""Non-standard graph implementation, intended for use in simulations.

Classes:
    - Vertex
    - Graph

Exceptions:
    - GraphError
    - InitError
"""


class Vertex:
    """The Vertex class, intended for use in a graph.

    The Vertex class can be used in directed or undirected graphs, and
    is designed with linked system modelling in mind. Vertices keeps
    track of their parent and child vertices in separate dictionaries;
    this enables the graph to be either directed or undirected, as well
    as enable the usage of Generous-Parent or Greedy-Child transform
    paradigms.

    Class Data:
        - self.name, the name of the vertex. It takes its value from
          the <name> argument of the constructor, and must be a string.
        - self.data, the data contained by the vertex. It takes its
          value from the <data> parameter, which defaults to None. It
          must be either None, an integer, or a float.
        - self.parents, the dictionary containing the parent vertices.
          When the vertex is instantiated, the dictionary is empty.
          When edges are added to the vertex, the parent vertex is used
          as the key for the dictionary; the value in the key-value
          pair is a Tuple containing a value that corresponds to a
          specific transform function, and the parameters for that
          transform function.
        - self.children, the dictionary containing the child vertices.
          When the vertex is instantiated, the dictionary is empty.
          When edges are added to the vertex, the child vertex is used
          as the key for the dictionary; the value in the key-value
          pair is a Tuple containing a value that corresponds to a
          specific transform function, and the parameters for that
          transform function.
        - self.deltaPrev, the previous delta value. This is used for
          modelling changes to the vertex in a linked system -- the
          previous delta value is used to calculate the floating delta
          of the vertex's children.
        - self.deltaFloat, the floating delta value. This value is what
          edge transforms modify, and as it does not modify the
          vertex's data until explicitly applied, is considered to
          'float'.

    Public Methods:
    """

    def __init__(self, name, data=None):
        """Constructor for the Vertex class.

        The method initializes the vertex to a default state; Only the
        name parameter is required, though the data can also be set
        during instantiation. All other class data is set to default
        values, independent of method arguments. Additionally,
        the constructor raises an InitError if any of the constructor
        arguments are of invalid types.
        """

        if str(type(name)) != "<class 'str'>":
            raise InitError("Invalid name for a Vertex. The name should be a"
                            " string.")
        if data is not None and (str(type(data)) != "<class 'int'>" or
                                 str(type(data)) != "<class 'float'>"):
            raise InitError("invalid data for a Vertex. The data should be an"
                            " integer or float.")

        self.name = name
        self.data = data
        self.parents = {}
        self.children = {}
        self.deltaPrev = 0
        self.deltaFloat = 0

    def __str__(self):
        pass


class Graph:
    """The Graph class, intended to model linked systems.

    Class Data:

    Public Methods:
    """

    def __init__(self):
        pass

    def __str__(self):
        pass

    def __contains__(self, item):
        pass


class GraphError(Exception):
    """Base class for exceptions exported by this module."""
    pass


class InitError(GraphError):
    """Exception for issues with initializing classes from this module.

    The __init__ methods of other classes will raise this exception in
    the event of an issue with initialization. Additionally, class
    methods that add or modify edges may also raise this exception.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def main():
    """Test script for the classes and exceptions in this module."""

    try:
        print("hello world")
    except InitError as error:
        print("There was an error with instantiation.")
        print(error)


if __name__ == '__main__':
    main()
