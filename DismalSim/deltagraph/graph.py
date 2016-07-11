from DismalSim.deltagraph import transforms

"""Non-standard graph implementation, intended for use in modeling.

While initially developed with macroeconomic modeling in mind, the
graph implementation of the DismalSim package is designed to also be
useful for modeling other linked dynamic systems.

Classes:
    - Vertex
    - Graph

Exceptions:
    - GraphError
    - InitError
    - EdgeError
    - DataError
    - RetrievalError
"""


class Vertex:
    """The Vertex class, intended for use in a Graph.

    The Vertex class is designed for usage in directed graphs, and it
    maintains a system of dual references to the directed edges between
    _vertices. This is done through the usage of separate <_parents> and
    <_children> dictionaries of edges. When an edge is created between
    two _vertices, the 'parent' Vertex uses the 'child' Vertex as the
    key for an entry in its <_children> dictionary, and the 'child'
    Vertex uses the 'parent' Vertex as an entry in its <_parents>
    dictionary. A Tuple containing information about the relationship
    represented by the edge is shared by the dictionaries. This system
    of dual references, while technically unnecessary, enables the
    Graph to be used with either Generous-Parent or Greedy-Child
    Transform paradigms. This reference redundancy can also to some
    extent enable the Graph to be considered both directed and
    undirected.

    Supported Transform Types:
        - Proportional (Absolute-Edge, Percent-Edge)
        - Linear (Absolute-Edge, Percent-Edge)
        - Exponential (Absolute-Edge, Percent-Edge)
        - Polynomial (Absolute-Edge, Percent-Edge)

    Class Data:
        - self.transformKeyMap, a dictionary of integer values, indexed
          by strings corresponding to different types of predefined
          transforms. This is used when generating the relationship-
          tuple for an edge. This dictionary is shared across all
          instances of the Vertex class.
        - self.name, the name of the Vertex. It takes its value from
          the <name> argument of the __init__ method, and it must be a
          string.
        - self.data, the data contained by the Vertex. It takes its
          value from the <data> parameter, which defaults to None. It
          must be either None, an integer, or a float.
        - self._parents, the dictionary containing the parent _vertices.
          When the Vertex is instantiated, the dictionary is empty.
          When edges are added to the Vertex, the parent Vertex is used
          as the key for the dictionary; the value in the key-value
          pair is a Tuple containing a value that corresponds to a
          specific gc_transform function, as well as the parameters for
          that gc_transform function.
        - self._children, the dictionary containing the child _vertices.
          When the Vertex is instantiated, the dictionary is empty.
          When edges are added to the Vertex, the child Vertex is used
          as the key for the dictionary; the value in the key-value
          pair is a Tuple containing a value that corresponds to a
          specific gc_transform function, and the parameters for that
          gc_transform function.
        - self._absDeltaPrev, the list of previous absolute delta
          values. These are used for modeling changes to the vertex in
          a linked system--the previous absolute delta values are used
          to calculate the floating delta of the Vertex's _children.
        - self._perDeltaPrev, the list of previous percent delta values.
          These are used for modeling changes to the vertex in a
          linked system--the previous absolute delta values are used to
          calculate the floating delta of the Vertex's _children.
        - self._deltaFloat, the absolute floating delta value. This
          value is what edge and self transforms modify, and, as it
          does not modify the Vertex's data until explicitly applied,
          it is considered to 'float'.

    Public Methods:
        - get_name
        - set_name
        - get_data
        - set_data
        - get_abs_delta_prev
        - set_abs_delta_prev
        - get_per_delta_prev
        - set_per_delta_prev
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
        - gc_transform
        - gp_transform
    """

    transformKeyMap = {"aa_lin": 0, "aa_exp": 1, "aa_poly": 2, "ap_lin": 3,
                       "ap_exp": 4, "ap_poly": 5, "pa_lin": 6, "pa_exp": 7,
                       "pa_poly": 8, "pp_lin": 9, "pp_exp": 10, "pp_poly": 11}

    def __init__(self, name, data=None):
        """Initializes class data for a Vertex.

        The method initializes the Vertex to a default state; only the
        <name> parameter is required, though the <data> can also be set
        during instantiation. All other class data is set to default
        values, independent of method arguments. Additionally,
        the method raises an InitError if any of the passed arguments
        are of invalid types.

        Method Parameters:
            - name, the name for the method to give the Vertex; it is
            required.
            - data, the data for the method with which to instantiate
            the Vertex; it defaults to None.
        """

        if data is not None and not isinstance(data, (int, float)):
            raise InitError(0)

        self.name = str(name)
        self.data = data
        self._parents = {}
        self._children = {}
        self._absDeltaPrev = [0]
        self._perDeltaPrev = [0]
        self._deltaFloat = 0

    def __str__(self):
        """Returns a string describing the Vertex."""
        pList = []
        cList = []
        for vertex in self._children:
            cList.append(vertex.get_name())
        for vertex in self._parents:
            pList.append(vertex.get_name())
        vStr = ("Vertex {0} has value: {1}, is a parent of _vertices: {2}, and a"
                " child of _vertices: {3}".format(self.name, str(self.data),
                " ".join(cList), " ".join(pList)))
        return vStr

    def __contains__(self, item):
        """Checks if the Vertex is linked by any edge to <item>."""
        if item in self._parents or item in self._children:
            return True
        else:
            return False

    def get_name(self):
        """Returns the Vertex's name."""
        return self.name

    def set_name(self, newName):
        """Sets the Vertex's name to <newName>."""
        self.name = str(newName)

    def get_data(self):
        """Returns the Vertex's data."""
        if self.data is None:
            raise RetrievalError(0)
        return self.data

    def set_data(self, newData):
        """Sets the Vertex's data to <newData>."""
        try:
            self.data = float(newData)
        except ValueError:
            raise DataError(0)

    def get_abs_delta_prev(self):
        """Returns the previous absolute delta value."""
        return self._absDeltaPrev[0]

    def set_abs_delta_prev(self, newDelta):
        """Sets the previous absolute delta value to <newDelta>."""
        try:
            self._absDeltaPrev.insert(0, float(newDelta))
        except ValueError:
            raise DataError(1)

    def get_per_delta_prev(self):
        """Returns the previous percent delta value."""
        return self._perDeltaPrev[0]

    def set_per_delta_prev(self, newDelta):
        """Sets the previous percent delta value to <newDelta>."""
        try:
            self._perDeltaPrev.insert(0, float(newDelta))
        except ValueError:
            raise DataError(1)

    def get_delta_float(self):
        """Returns the Vertex's floating delta value."""
        return self._deltaFloat

    def set_delta_float(self, newDelta):
        """Sets the Vertex's previous floating delta value to <newDelta>."""
        try:
            self._deltaFloat = float(newDelta)
        except ValueError:
            raise DataError(2)
    def apply_delta_float(self):
        """Adds the current value of _deltaFloat to data."""
        newData = self.data + self._deltaFloat
        self._absDeltaPrev.insert(0, self._deltaFloat)
        self._perDeltaPrev.insert(0, (((newData / self.data) - 1) * 100))
        self.data += self._deltaFloat
        self._deltaFloat = 0

    def get_parent_vertices(self):
        """Returns a list of the Vertex's parent _vertices."""
        return list(self._parents.keys())

    def check_parent(self, aVertex):
        """Checks if <aVertex> is a parent of the Vertex."""
        if aVertex in self._parents:
            return True
        else:
            return False

    def add_parent(self, pVertex, tData):
        """Adds an edge reference with <pVertex> as the 'parent.'"""
        self._parents[pVertex] = tData

    def remove_parent(self, pVertex):
        """Removes edge reference where <pVertex> is the 'parent.'"""
        try:
            del self._parents[pVertex]
        except KeyError:
            raise EdgeError(2)

    def get_child_vertices(self):
        """Returns a list of the Vertex's child _vertices."""
        return list(self._children.keys())

    def check_child(self, aVertex):
        """Checks if <aVertex> is a child of the Vertex."""
        if aVertex in self._children:
            return True
        else:
            return False

    def add_child(self, cVertex, tData):
        """Adds an edge reference with <cVertex> as the 'child.'"""
        self._children[cVertex] = tData

    def remove_child(self, cVertex):
        """Removes edge reference where <cVertex> is the 'child.'"""
        try:
            del self._children[cVertex]
        except KeyError:
            raise EdgeError(3)

    def add_edge(self, cVertex, tName, tParameters):
        """Adds a directed edge between the Vertex and <cVertex>.

        The method serves primarily as a wrapper for the add_parent and
        add_child methods of the Vertex class, using them for the
        actual creation of the edge. It does, however, perform the
        gc_transform lookup, pulling the integer gc_transform key, used
        for cleaner gc_transform selection statements, from the
        TransformKeyMap dictionary.

        Method Parameters:
            - cVertex, the 'child' vertex of the edge.
            - tName, the name of the gc_transform that the edge
              represents.
            - tParameters, the list of parameters for the gc_transform
              function.
        """

        try:
            tKey = self.transformKeyMap[str(tName.lower())]
        except KeyError:
            raise EdgeError(0)
        tData = [tKey]
        tData.extend(tParameters)
        tDataTuple = tuple(tData)
        try:
            self.add_child(cVertex, tDataTuple)
            cVertex.add_parent(self, tDataTuple)
        except AttributeError:
            raise EdgeError(1)

    def remove_edge(self, cVertex):
        """Removes a directed edge between the Vertex and <cVertex>.

        The method function as a wrapper function for the remove_child
        and remove_parent methods of the Vertex.

        Method Parameters:
            - cVertex, the 'child' vertex of the edge to be removed.
        """

        try:
            cVertex.remove_parent(self)
            self.remove_child(cVertex)
        except AttributeError:
            raise EdgeError(3)

    def gc_transform(self):
        """Calculates '_deltaFloat' based on a greedy-child paradigm.

        When using the greedy-child transform paradigm, _deltaFloat is
        calculated by pulling relevant data from the parent nodes.
        """

        for pVertex in self._parents:
            tData = self._parents[pVertex]
            tKey = tData[0]
            tData = tData[1:]
            if tKey >= 0 and tKey <= 5:
                pDelta = pVertex.get_abs_delta_prev()
            elif tKey >= 6 and tKey <= 11:
                pDelta = pVertex.get_per_delta_prev()
            if tKey == 0:
                nDelta = transforms.AA_linear(pDelta, tData)
            elif tKey == 1:
                nDelta = transforms.AA_exponential(pDelta, tData)
            elif tKey == 2:
                nDelta = transforms.AA_polynomial(pDelta, tData)
            elif tKey == 3:
                nDelta = transforms.AP_linear(pDelta, tData)
            elif tKey == 4:
                nDelta = transforms.AP_exponential(pDelta, tData)
            elif tKey == 5:
                nDelta = transforms.AP_polynomial(pDelta, tData)
            elif tKey == 6:
                nDelta = transforms.PA_linear(pDelta, tData)
            elif tKey == 7:
                nDelta = transforms.PA_exponential(pDelta, tData)
            elif tKey == 8:
                nDelta = transforms.PA_polynomial(pDelta, tData)
            elif tKey == 9:
                nDelta = transforms.PP_linear(pDelta, tData)
            elif tKey == 10:
                nDelta = transforms.PP_exponential(pDelta, tData)
            elif tKey == 11:
                nDelta = transforms.PP_polynomial(pDelta, tData)
            if tKey in (0, 1, 2, 6, 7, 8):
                # Applies absolute changes
                self._deltaFloat += nDelta
            elif tKey in (3, 4, 5, 9, 10, 11) and pDelta != 0:
                # Applies percentage changes
                self._deltaFloat += nDelta * self.data

    def gp_transform(self):
        """Calculates '_deltaFloat' based on a generous-parent paradigm."""
        pass


class Graph:
    """The Graph class, intended to model linked systems.

    This Graph is a directed one, though the dual edge references
    maintained by the Graph's _vertices enable it be used in a fashion
    similar to an undirected one, if needed. The Graph is primarily
    implemented as a container for its _vertices, and many, but not all,
    of the Graph's methods are just wrappers for the equivalent Vertex
    methods.

    Class Data:
        - _vertices, a dictionary of the _vertices contained in the
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
        However, the method takes _vertices as optional positional
        arguments. The _vertices in the arguments have their names
        extracted and are added to the Graph's dictionary of _vertices,
        indexed by their extracted names. Additionally, if any objects
        that are not instances of the Vertex class are passed into the
        method, it raises an InitError.

        Method Parameters:
            - *vertices, the list of optional arguments--presumed to be
              vertices to be included in the Graph at instantiation.
        """

        self._vertices = {}
        if len(vertices) != 0:
            try:
                for vertex in vertices:
                    vName = vertex.get_name()
                    self._vertices[vName] = vertex
            except AttributeError:
                del self
                raise InitError(1)

    def __str__(self):
        """Returns a string describing the Graph."""
        vList = []
        for vertex in self:
            vList.append(vertex.get_name())
        gStr = "The Graph contains _vertices: {0}".format(" ".join(vList))
        return gStr

    def __contains__(self, aVertex):
        """Checks if <aVertex> is present in the Graph.

        <aVertex> may be either a reference to the Vertex itself, or a
        string. If it is a string, the string is treated as the
        Vertex's name, and the method checks if the name is present in
        the keys of the '_vertices' dictionary.

        Method Parameters:
            - aVertex, a reference to an instance of the Vertex class,
            or a string corresponding to a Vertex's name.
        """

        if isinstance(aVertex, str) and aVertex in self._vertices.keys():
            return True
        elif aVertex in self._vertices.values():
            return True
        else:
            return False

    def __len__(self):
        """Returns the number of _vertices in the Graph."""
        return len(self._vertices)

    def __iter__(self):
        """Returns an iterator over the _vertices of the Graph."""
        return iter(self._vertices.values())

    def __eq__(self, other):
        """Tests equality of two graphs based on their vertices."""
        pass

    def __add__(self, other):
        """Adds a vertex to the Graph.

        The function takes either an instance of the Vertex class, or a
        tuple containing data to instantiate a new Vertex, and adds the
        Vertex to the Graph, instantiating it if necessary.
        """

        pass

    def __getitem__(self, item):
        pass

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def get_all_vertices(self):
        """Returns a list of all _vertices in the Graph."""
        return list(self._vertices.values())

    def get_vertex(self, vName):
        """Retrieves a Vertex from the graph based on its name."""
        try:
            aVertex = self._vertices[vName]
        except KeyError:
            raise RetrievalError(1)
        return aVertex

    def add_vertex(self, name, data=None):
        """Instantiates and adds a new Vertex to the Graph.

        Method Parameters:
            - name, the name of the Vertex to be instantiated and added
              to the Graph. This parameter is required.
            - data, the data for the new Vertex to contain. It is an
              optional parameter and defaults to None.
        """
        newVertex = Vertex(name, data)
        self._vertices[name] = newVertex

    def add_existing_vertex(self, aVertex):
        """Adds an already instantiated Vertex to the Graph."""
        self._vertices[aVertex.get_name()] = aVertex

    def add_edge(self, pVertex, cVertex, tName, tParameters):
        """Adds a directed edge to the Graph.

        The function is primarily a wrapper for the Vertex add_edge
        method and creates a directed edge between <pVertex> and
        <cVertex>.

        Method Parameters:
            - pVertex, the 'parent' Vertex of the edge to be created.
            - cVertex, the 'child' Vertex of the edge to be created.
            - tName, the name of the gc_transform function to be
              associated with the new edge.
            - tParameters, the parameters for the gc_transform function
              associated with the edge.
        """
        if isinstance(pVertex, str):
            pvertex = self.get_vertex(pVertex)
        else:
            pvertex = pVertex
        if isinstance(cVertex, str):
            cvertex = self.get_vertex(cVertex)
        else:
            cvertex = cVertex
        pvertex.add_edge(cvertex, tName, tParameters)

    def remove_edge(self, pVertex, cVertex):
        """Removes a directed edge between <pVertex> and <cVertex>.

        This method is a wrapper function for the Vertex remove_edge
        class method.

        Method Parameters:
            - pVertex, the 'parent' Vertex of the edge to be removed.
            - cVertex, the 'child' Vertex of the edge to be removed.
        """

        try:
            pVertex.remove_edge(cVertex)
        except AttributeError:
            raise EdgeError(4)

    def apply_floating_deltas(self):
        for vert in self:
            vert.apply_delta_float()


class GraphError(Exception):
    """Base class for exceptions defined by this module.

    The GraphError base class defines __init__ and __str__ methods, to
    be used by the assorted exceptions that subclass it. While all
    methods are shared between exception classes in this module, the
    'messages' class data is unique to each exception class and
    dictates the messages displayed by the exception.

    Class Data:
        - self.messages, the dictionary of predefined messages for the
          exception to use.
        - self.msg, the specific message contained within a given
          instance of the exception.
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

    Superclass Differences:
        -self.messages, the contents of the dictionary are different.
    """

    messages = {0: "Invalid value for Vertex Constructor <data> parameter."
                " Parameter must be either omitted, an integer, or a float."
                " Unable to initialize Vertex.",
                1: "Invalid argument for Graph constructor arguments. All"
                   " arguments must be instances of the Vertex class. Unable to"
                   " initialize Graph."}


class EdgeError(GraphError):
    """Exception for issues with Vertex edges.

    This exception will generally be raised when passing invalid
    _vertices to a Vertex's add_edge and remove_edge methods, as well as
    if an invalid gc_transform name is passed to the add_edge method.

    Superclass Differences:
        -self.messages, the contents of the dictionary are different.
    """

    messages = {0: "Transform function name not in dictionary, unable to map"
                   " gc_transform to gc_transform key. The edge cannot be"
                   " created.",
                1: "Object passed in as <cVertex> argument invalid. Object"
                   " must be an instance of Vertex class. Unable to create"
                   " edge.",
                2: "Object passed in as <pVertex> argument not in Vertex's"
                   " '_parents' dictionary. Cannot remove non-existent"
                   " 'parent'",
                3: "Object passed in as <cVertex> argument not in Vertex's"
                   " '_children' dictionary. Cannot remove non-existent"
                   " 'child'",
                4: "object passed in as <pVertex> argument is not an instance"
                   " of the Vertex class. Unable to remove edges from fake"
                   " _vertices."}


class DataError(GraphError):
    """Exception for issues with Vertex data or delta values.

    This exception will generally be raised when an invalid value is
    passed to a Vertex set method.

    Superclass Differences:
        -self.messages, the contents of the dictionary are different.
    """

    messages = {0: "Invalid value for Vertex 'data' attribute, unable to set"
                   " 'data' to <newData>",
                1: "Invalid value for Vertex '_absDeltaPrev' attribute, unable"
                   " to set '_absDeltaPrev' to <newDelta>",
                2: "Invalid value for Vertex '_deltaFloat' attribute, unable to"
                   " set '_deltaFloat' to <newDelta>"}


class RetrievalError(GraphError):
    """Exception for attempting to retrieve non-existent data.

    This exception is raised either when a Vertex's 'data' attribute is
    None, or when attempting to retrieve a Vertex by name from a Graph,
    and the Vertex isn't present.

    Superclass Differences:
        -self.messages, the contents of the dictionary are different.
    """

    messages = {0: "Vertex data is None. Conventional operations on this data"
                   " are not recommended.",
                1: "Vertex name not present in Graph '_vertices' dictionary."
                   " Unable to retrieve vertex."}


def main():
    """Test script for the classes and exceptions in this module.

    Test Components:
        - try-except blocks that deliberately result in raising the
          exceptions included in the module, followed by catching them
          to test and demonstrate the exceptions.
        - Instantiating a Graph with _vertices as positional arguments,
          and adding further _vertices via class methods, to test and
          demonstrate the Graph's instantiation and mutation.
        - for loops iterating over the _vertices of the Graph, to test
          and demonstrate its __iter__ method.
        - Creation and deletion of edges within a graph, to test and
          demonstrate relevant methods.
        - Print the Graph, to test both Graph and Vertex __str__
          methods.
        - Forcibly set the _absDeltaPrev attribute of all _vertices in
          the test graph, and call the gc_transform method of those
          _vertices.

    """

    # Begin error demonstration
    try:
        Vertex("A", "lies")
    except InitError as error:
        print(error)
    try:
        Graph(Vertex("A"), 5)
    except InitError as error:
        print(error)
    aVertex = Vertex("A", 2)
    bVertex = Vertex("B")
    try:
        aVertex.add_edge(bVertex, "math", [42])
    except EdgeError as error:
        print(error)
    try:
        aVertex.add_edge(5, "abs_proportional", [1])
    except EdgeError as error:
        print(error)
    try:
        aVertex.remove_edge(5)
    except EdgeError as error:
        print(error)
    try:
        bVertex.remove_parent(4)
    except EdgeError as error:
        print(error)
    try:
        aVertex.set_data("A")
    except DataError as error:
        print(error)
    try:
        aVertex.set_abs_delta_prev("A")
    except DataError as error:
        print(error)
    try:
        aVertex.set_delta_float("A")
    except DataError as error:
        print(error)
    try:
        bVertex.get_data()
    except RetrievalError as error:
        print(error)
    aGraph = Graph()
    try:
        aGraph.get_vertex("C")
    except RetrievalError as error:
        print(error)
    del aVertex, bVertex, aGraph
    # End error demonstration

    # Begin Graph instantiation and iteration
    vertex1 = Vertex("A", 5)
    vertex2 = Vertex("B", 10)
    vertex3 = Vertex("C", 3)
    aGraph = Graph(vertex1, vertex2, vertex3)
    aGraph.add_vertex("D", 7)
    aSum = 0
    for vertex in aGraph:
        aSum += vertex.get_data()
    print(aSum)
    # End Graph instantiation and iteration.

    # Begin edge testing
    # Create edges, through Graph and Vertex methods
    vertex5 = Vertex("E", 5)
    aGraph.add_existing_vertex(vertex5)
    vertex1.add_edge(vertex2, "aa_lin", [1])
    aGraph.add_edge(vertex1, vertex3, "aa_lin", [3, 3])
    aGraph.add_edge(vertex2, aGraph.get_vertex("D"), "aa_lin", [2, 1])
    aGraph.add_edge(vertex2, vertex5, "pa_exp", [2, 3])
    aGraph.add_edge(vertex3, vertex1, "pa_lin", [2, 1])
    vertex3.add_edge(aGraph.get_vertex("D"), "pp_lin", [2])
    aGraph.get_vertex("D").add_edge(vertex3, "aa_lin", [1, 1])
    vertex5.add_edge(aGraph.get_vertex("D"), "aa_exp", [3])

    # Remove edges, through Graph and Vertex methods
    vertex1.remove_edge(vertex3)
    aGraph.remove_edge(vertex3, aGraph.get_vertex("D"))
    # End edge testing

    # Begin print test
    print(aGraph)
    for vert in aGraph:
        print(vert)
    # End print test

    # Begin gc_transform method test
    for vert in aGraph:
        vert.set_abs_delta_prev(10)
    for vert in aGraph:
        vert.gc_transform()
    aGraph.apply_floating_deltas()
    for vert in aGraph:
        print(vert)
    # End gc_transform method test


if __name__ == '__main__':
    main()
