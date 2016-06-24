__author__ = "Ashleigh Bunkofske"

"""Non-standard graph implementation, intended for use in simulations.

Classes:
    - Vertex
    - Graph

Exceptions:
    - GraphError
    - InitError
    - EdgeError
    - DataError
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
        - self.name, the name of the Vertex. It takes its value from
          the <name> argument of the __init__ method, and must be a
          string.
        - self.data, the data contained by the Vertex. It takes its
          value from the <data> parameter, which defaults to None. It
          must be either None, an integer, or a float.
        - self.parents, the dictionary containing the parent vertices.
          When the Vertex is instantiated, the dictionary is empty.
          When edges are added to the Vertex, the parent Vertex is used
          as the key for the dictionary; the value in the key-value
          pair is a Tuple containing a value that corresponds to a
          specific transform function, and the parameters for that
          transform function.
        - self.children, the dictionary containing the child vertices.
          When the Vertex is instantiated, the dictionary is empty.
          When edges are added to the Vertex, the child Vertex is used
          as the key for the dictionary; the value in the key-value
          pair is a Tuple containing a value that corresponds to a
          specific transform function, and the parameters for that
          transform function.
        - self.deltaPrev, the previous delta value. This is used for
          modelling changes to the vertex in a linked system--the
          previous delta value is used to calculate the floating delta
          of the Vertex's children.
        - self.deltaFloat, the floating delta value. This value is what
          edge transforms modify, and as it does not modify the
          Vertex's data until explicitly applied, is considered to
          'float'.

    Public Methods:
        - get_name
        - set_name
        - get_data
        - set_data
        - get_delta_prev
        - set_delta_prev
        - get_delta_float
        - set_delta_float
        - get_parent_vertices
        - check_parent
        - add_parent
        - remove_parent
        - get_child_vertices
        - check_child
        - add_child
        - remove_child
        - add_edge
        - remove_edge
    """

    def __init__(self, name, data=None):
        """Initializes class data for a Vertex.

        The method initializes the Vertex to a default state; Only the
        name parameter is required, though the data can also be set
        during instantiation. All other class data is set to default
        values, independent of method arguments. Additionally,
        the method raises an InitError if any of the passed arguments
        are of invalid types.

        Method Parameters:
            - name, the name for the method to give the Vertex; it is
            required.
            - data, the data for the method to instantiate the Vertex
            with; it defaults to None.
        """

        if data is not None:
            try:
                data = float(data)
            except ValueError:
                del self
                raise InitError(0)

        self.name = str(name)
        self.data = data
        self.parents = {}
        self.children = {}
        self.deltaPrev = 0
        self.deltaFloat = 0

    def __str__(self):
        """Returns a string describing the Vertex."""
        pass

    def __contains__(self, item):
        """Checks if the Vertex is linked by any edge to <item>."""
        if item in self.parents or item in self.children:
            return True
        else:
            return False

    def get_name(self):
        """Returns the Vertex's name."""
        return self.name

    def set_name(self, newName):
        """Sets the Vertex's name to <newName>."""
        self.name = newName

    def get_data(self):
        """Returns the Vertex's data."""
        return self.data

    def set_data(self, newData):
        """Sets the Vertex's data to <newData>."""
        try:
            self.data = float(newData)
        except ValueError:
            raise DataError(0)

    def get_delta_prev(self):
        """Returns the Vertex's previous delta value."""
        return self.deltaPrev

    def set_delta_prev(self, newDelta):
        """Sets the Vertex's previous delta value to <newDelta>."""
        try:
            self.deltaPrev = float(newDelta)
        except ValueError:
            raise DataError(1)

    def get_delta_float(self):
        """Returns the Vertex's floating delta value."""
        return self.deltaFloat

    def set_delta_float(self, newDelta):
        """Sets the Vertex's previous floating delta value to <newDelta>."""
        try:
            self.deltaFloat = float(newDelta)
        except ValueError:
            raise DataError(2)

    def get_parent_vertices(self):
        """Returns a list of the Vertex's parent vertices."""
        return list(self.parents.keys())

    def check_parent(self, aVertex):
        """Checks if <aVertex> is a parent of the Vertex."""
        if aVertex in self.parents:
            return True
        else:
            return False

    def add_parent(self):
        pass

    def remove_parent(self):
        pass

    def get_child_vertices(self):
        """Returns a list of the Vertex's child vertices."""
        return list(self.children.keys())

    def check_child(self, aVertex):
        """Checks if <aVertex> is a child of the Vertex."""
        if aVertex in self.children:
            return True
        else:
            return False

    def add_child(self):
        pass

    def remove_child(self):
        pass

    def add_edge(self):
        pass

    def remove_edge(self):
        pass


class Graph:
    """The Graph class, intended to model linked systems.

    This Graph is functionally a directed one, however when an edge is
    added to the Graph, two are actually created, one in each direction
    between the two vertices. This allows the Graph to function as if
    it is undirected when that would prove beneficial, while still
    allowing for operations that assume directionality of edges. The
    Graph is primarily implemented as a container for its vertices, and
    many, but not all of the Graph's methods are just wrappers for the
    equivalent Vertex methods.

    Class Data:
        - self.vertices, a dictionary of the vertices contained in the
          Graph, indexed by the name of the Vertex. They take their
          initial value, if any, from the <*vertices> argument of the
          __init__ method.

    Public Methods:
        - get_all_vertices
        - get_vertex
        - add_vertex
        - add_existing_vertex
        - apply_floating_deltas
    """

    def __init__(self, *vertices):
        """Initializes class data for the Graph.

        When the Graph is instantiated, it defaults to an empty state.
        However, the method takes vertices as optional positional
        arguments. The vertices in the arguments have their names
        extracted, and are added to the Graph's dictionary of vertices,
        indexed by their extracted name. Additionally, if any objects
        that are not instances of the Vertex class are passed in to the
        method, it raises an InitError.

        Method Parameters:
            - *vertices, the list of optional arguments--presumed to be
              vertices to be included in the Graph at instantiation.
        """

        self.vertices = {}
        if vertices is not None:
            try:
                for vertex in vertices:
                    vName = vertex.get_name()
                    self.vertices[vName] = vertex
            except AttributeError:
                del self
                raise InitError(1)

    def __str__(self):
        """Returns a string describing the Graph."""
        pass

    def __contains__(self, item):
        pass

    def __len__(self):
        """Returns the number of Vertices in the Graph."""
        return len(self.vertices)

    def __iter__(self):
        """Returns an iterator over the vertices of the Graph."""
        return iter(self.vertices.values())

    def get_all_vertices(self):
        """Returns a list of all vertices in the Graph."""
        return list(self.vertices.values())

    def get_vertex(self):
        pass

    def add_vertex(self, name, data=None):
        """Instantiates and adds a new Vertex to the Graph."""
        newVertex = Vertex(name, data)
        self.vertices[name] = newVertex

    def add_existing_vertex(self, aVertex):
        """Adds an already instantiated Vertex to the Graph."""
        self.vertices[aVertex.get_name()] = aVertex

    def apply_floating_deltas(self):
        pass


class GraphError(Exception):
    """Base class for exceptions defined by this module.

    The GraphError base class defines __init__ and __str__ methods, to
    be used by the assorted exceptions that subclass it. While all
    methods are shared between exception classes in this module, the
    'messages' class data is unique to each exception class, and
    dictates the messages displayed by the exception.
    """

    messages = {0: "GraphError is intended only to be subclassed, and should"
                   " never be raised directly."}

    def __init__(self, msgKey):
        self.msg = self.messages[msgKey]

    def __str__(self):
        return self.msg


class InitError(GraphError):
    """Exception for issues with initializing classes from this module.

    The __init__ methods of other classes will raise this exception in
    the event of an issue with initialization--usually when the
    __init__ method receives an argument of an invalid type.
    """

    messages = {0: "Invalid value for Vertex 'data' attribute. Unable to"
                " initialize Vertex.", 1: "invalid argument for Graph __init__"
                " method; arguments must be instances of the Vertex class."
                " Unable to initialize Graph."}


class EdgeError(GraphError):
    """Exception for issues with Vertex edges."""

    messages = {}


class DataError(GraphError):
    """Exception for issues with Vertex data or delta values."""

    messages = {0: "Invalid value for Vertex 'data' attribute, unable to set"
                " 'data' to <newData>", 1: "Invalid value for Vertex"
                " 'deltaPrev' attribute, unable to set 'deltaPrev' to"
                " <newDelta>", 2: "Invalid value for Vertex 'deltaFloat'"
                " attribute, unable to set 'deltaFloat' to <newDelta>"}


def main():
    """Test script for the classes and exceptions in this module.

    Test components:
        - try-except blocks that deliberately result in raising the
          exceptions included in the module, followed by catching them
          to test and demonstrate the exceptions.
        - Instantiating a Graph with vertices as positional arguments,
          and adding further vertices via class methods, to test and
          demonstrate the Graph's instantiation and mutation.
        - for loops iterating over the vertices of the Graph, to test
          and demonstrate its __iter__ method.

    """

    try:
        Vertex("A", "lies")
    except InitError as error:
        print(error)
    try:
        Graph(Vertex("A"), 5)
    except InitError as error:
        print(error)

    vertex1 = Vertex("A", 5)
    vertex2 = Vertex("B", 10)
    vertex3 = Vertex("C", 3)
    aGraph = Graph(vertex1, vertex2, vertex3)
    aGraph.add_vertex("D", 7)
    aSum = 0
    for vertex in aGraph:
        aSum += vertex.get_data()
    print(aSum)


if __name__ == '__main__':
    main()
