from DismalSim.deltagraph import transforms
import random

"""Non-standard graph implementation, intended for use in modeling.

While initially developed with macroeconomic modeling in mind, the
graph implementation of the DismalSim package is designed to also be
useful for modeling other linked dynamic systems.

Classes:
    - Vertex
    - DiGraph

Exceptions:
    - GraphError
    - InitError
    - EdgeError
    - DataError
    - RetrievalError
"""


class Vertex:
    """The Vertex class, intended for use in a DiGraph.

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
    DiGraph to be used with either Generous-Parent or Greedy-Child
    Transform paradigms. This reference redundancy can also to some
    extent enable the DiGraph to be considered both directed and
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
          specific transform function, as well as the parameters for
          that transform function.
        - self._children, the dictionary containing the child _vertices.
          When the Vertex is instantiated, the dictionary is empty.
          When edges are added to the Vertex, the child Vertex is used
          as the key for the dictionary; the value in the key-value
          pair is a Tuple containing a value that corresponds to a
          specific transform function, and the parameters for that
          transform function.
        - self._deltaPrevAbs, the list of previous absolute delta
          values. These are used for modeling changes to the vertex in
          a linked system--the previous absolute delta values are used
          to calculate the floating delta of the Vertex's _children.
        - self._deltaPrevPer, the list of previous percent delta values.
          These are used for modeling changes to the vertex in a
          linked system--the previous absolute delta values are used to
          calculate the floating delta of the Vertex's _children.
        - self.deltaFloat, the absolute floating delta value. This
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
        - transform
        - gp_transform
    """

    transformKeyMap = {"aa_lin": 0, "aa_exp": 1, "aa_poly": 2, "ap_lin": 3,
                       "ap_exp": 4, "ap_poly": 5, "pa_lin": 6, "pa_exp": 7,
                       "pa_poly": 8, "pp_lin": 9, "pp_exp": 10, "pp_poly": 11}

    def __init__(self, name, data=None, **kwargs):
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
        self._deltaPrevAbs = [0]
        self._deltaPrevPer = [0]
        self.deltaFloat = 0

        if kwargs is not None:
            if "deltaInherent" in kwargs.keys():
                self._deltaInherent = kwargs["deltaInherent"]
            else:
                self._deltaInherent = 0
            if "percentFlag" in kwargs.keys():
                self._percentFlag = kwargs["percentFlag"]
            else:
                self._percentFlag = False
            if "randomDeltaFlag" in kwargs.keys():
                self._randomDeltaFlag = kwargs["randomDeltaFlag"]
            else:
                self._randomDeltaFlag = False
            if "randomValFlag" in kwargs.keys():
                self._randomValFlag = kwargs["randomValFlag"]
            else:
                self._randomValFlag = False
            if "randomInfo" in kwargs.keys():
                self._randomInfo = kwargs["randomInfo"]
            else:
                self._randomInfo = None

    def __str__(self):
        """Returns a string describing the Vertex."""
        pList = []
        for vertex in self._parents:
            pList.append(vertex.name)
        vStr = ("Vertex {0} has value: {1} and is a child of vertices:"
                " {2}".format(self.name, str(self.data), " ".join(pList)))
        return vStr

    def __contains__(self, item):
        """Checks if the Vertex is linked by any edge to <item>."""
        if item in self._parents:
            return True
        else:
            return False

    def apply_delta_inherent(self):
        """Placeholder."""
        if self._percentFlag:
            multiplier = self._deltaInherent / 100
            self.deltaFloat += multiplier * self.data
            if self._randomDeltaFlag:
                a = self._randomInfo[0]
                b = self._randomInfo[1]
                multiplier = random.uniform(a, b)
                self.deltaFloat += multiplier * self.data
        else:
            self.deltaFloat += self._deltaInherent
            if self._randomDeltaFlag:
                a = self._randomInfo[0]
                b = self._randomInfo[1]
                self.deltaFloat = random.uniform(a, b)

    def apply_delta_float(self):
        """Adds the current value of deltaFloat to data."""

        if not self._randomValFlag:
            newData = self.data + self.deltaFloat
            self._deltaPrevAbs.insert(0, self.deltaFloat)
            self._deltaPrevPer.insert(0, (((newData / self.data) - 1) * 100))
            self.data += self.deltaFloat
            self.deltaFloat = 0
        else:
            a = self._randomInfo[0]
            b = self._randomInfo[1]
            newData = random.uniform(a, b)
            delta = self.data - newData
            self._deltaPrevAbs.insert(0, delta)
            self._deltaPrevPer.insert(0, (((delta / self.data) - 1) * 100))
            self.deltaFloat = 0
            self.data = newData

    def add_edge(self, pVertex, tName, tParameters):
        """Adds a directed edge between the Vertex and <cVertex>.

        The method serves primarily as a wrapper for the add_parent and
        add_child methods of the Vertex class, using them for the
        actual creation of the edge. It does, however, perform the
        transform lookup, pulling the integer transform key, used
        for cleaner transform selection statements, from the
        TransformKeyMap dictionary.

        Method Parameters:
            - cVertex, the 'child' vertex of the edge.
            - tName, the name of the transform that the edge
              represents.
            - tParameters, the list of parameters for the transform
              function.
        """

        try:
            tKey = self.transformKeyMap[str(tName.lower())]
        except KeyError:
            raise EdgeError(0)
        tData = [tKey]
        tData.extend(tParameters)
        tDataTuple = tuple(tData)
        self._parents[pVertex] = tDataTuple


    def remove_edge(self, pVertex):
        """Removes a directed edge between the Vertex and <cVertex>.

        The method function as a wrapper function for the remove_child
        and remove_parent methods of the Vertex.

        Method Parameters:
            - cVertex, the 'child' vertex of the edge to be removed.
        """

        try:
            del self._parents[pVertex]
        except AttributeError:
            raise EdgeError(3)

    def transform(self):
        """Calculates 'deltaFloat' based on a greedy-child paradigm.

        When using the greedy-child transform paradigm, deltaFloat is
        calculated by pulling relevant data from the parent nodes.
        """

        for pVertex in self._parents:
            tData = self._parents[pVertex]
            tKey = tData[0]
            tData = tData[1:]
            if tKey >= 0 and tKey <= 5:
                pDelta = pVertex._deltaPrevAbs[0]
            elif tKey >= 6 and tKey <= 11:
                pDelta = pVertex._deltaPrevAbs[0]
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
                self.deltaFloat += nDelta
            elif tKey in (3, 4, 5, 9, 10, 11):
                # Applies percentage changes
                self.deltaFloat += nDelta * self.data


class DiGraph:
    """The DiGraph class, intended to model linked systems.

    This DiGraph is a directed one, though the dual edge references
    maintained by the DiGraph's _vertices enable it be used in a fashion
    similar to an undirected one, if needed. The DiGraph is primarily
    implemented as a container for its _vertices, and many, but not all,
    of the DiGraph's methods are just wrappers for the equivalent Vertex
    methods.

    Class Data:
        - _vertices, a dictionary of the _vertices contained in the
          DiGraph, indexed by the name of the Vertex. They take their
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
        """Initializes class data for the DiGraph.

        When the DiGraph is instantiated, it defaults to an empty state.
        However, the method takes _vertices as optional positional
        arguments. The _vertices in the arguments have their names
        extracted and are added to the DiGraph's dictionary of _vertices,
        indexed by their extracted names. Additionally, if any objects
        that are not instances of the Vertex class are passed into the
        method, it raises an InitError.

        Method Parameters:
            - *vertices, the list of optional arguments--presumed to be
              vertices to be included in the DiGraph at instantiation.
        """

        self._vertices = {}
        if len(vertices) != 0:
            try:
                for vertex in vertices:
                    vName = vertex.name
                    self._vertices[vName] = vertex
            except AttributeError:
                del self
                raise InitError(1)

    def __str__(self):
        """Returns a string describing the DiGraph."""
        vList = []
        for vertex in self:
            vList.append(vertex.name)
        gStr = "The DiGraph contains _vertices: {0}".format(" ".join(vList))
        return gStr

    def __contains__(self, aVertex):
        """Checks if <aVertex> is present in the DiGraph.

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
        """Returns the number of _vertices in the DiGraph."""
        return len(self._vertices)

    def __iter__(self):
        """Returns an iterator over the _vertices of the DiGraph."""
        return iter(self._vertices.values())

    def __eq__(self, other):
        """Tests equality of two graphs based on their vertices.

        The method iterates over the vertices of the first graph, and
        checks to see if the second graph contains those vertices. If
        the second graph contains all the same vertices, and has an
        equal length, they evaluate as equal. The DiGraph never evaluates
        as equal to anything other than another graph.
        """

        for vert in self:
            if vert not in other:
                return False
        if len(self) == len(other):
            return True

    def __add__(self, vertex):
        """Adds a vertex to the DiGraph.

        The method takes an instance of the Vertex class, and adds it
        to the DiGraph.
        """

        if isinstance(vertex, Vertex):
            vName = vertex.name
            self._vertices[vName] = vertex

    def __getitem__(self, key):
        """Retrieves a vertex from the graph, using its name as a key.

        The relevant Vertex is looked up in the graph's _vertices
        dictionary, with the supplied string as a key. If the key isn't
        present, a KeyError is raised.
        """

        aVertex = self._vertices[key]
        return aVertex

    def __setitem__(self, key, vertex):
        """Adds a vertex to the graph, indexed by <key>."""

        self._vertices[key] = vertex

    def __delitem__(self, key):
        """Removes the vertex indexed by <key> from the DiGraph.

        If the key is not present in the DiGraph's _vertices dictionary,
        then a KeyError is raised.
        """

        del self._vertices[key]

    def add_edge(self, pVertex, cVertex, tName, tParameters):
        """Adds a directed edge to the DiGraph.

        The function is primarily a wrapper for the Vertex add_edge
        method and creates a directed edge between <pVertex> and
        <cVertex>.

        Method Parameters:
            - pVertex, the 'parent' Vertex of the edge to be created.
            - cVertex, the 'child' Vertex of the edge to be created.
            - tName, the name of the transform function to be
              associated with the new edge.
            - tParameters, the parameters for the transform function
              associated with the edge.
        """
        if isinstance(pVertex, str):
            pvertex = self[pVertex]
        else:
            pvertex = pVertex
        if isinstance(cVertex, str):
            cvertex = self[cVertex]
        else:
            cvertex = cVertex
        cvertex.add_edge(pvertex, tName, tParameters)

    def remove_edge(self, pVertex, cVertex):
        """Removes a directed edge between <pVertex> and <cVertex>.

        This method is a wrapper function for the Vertex remove_edge
        class method.

        Method Parameters:
            - pVertex, the 'parent' Vertex of the edge to be removed.
            - cVertex, the 'child' Vertex of the edge to be removed.
        """

        try:
            cVertex.remove_edge(pVertex)
        except AttributeError:
            raise EdgeError(4)

    def apply_floating_deltas(self):
        for vert in self:
            vert.apply_delta_float()

    def apply_inherent_deltas(self):
        for vert in self:
            vert.apply_delta_inherent()


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
                1: "Invalid argument for DiGraph constructor arguments. All"
                   " arguments must be instances of the Vertex class. Unable to"
                   " initialize DiGraph."}


class EdgeError(GraphError):
    """Exception for issues with Vertex edges.

    This exception will generally be raised when passing invalid
    _vertices to a Vertex's add_edge and remove_edge methods, as well as
    if an invalid transform name is passed to the add_edge method.

    Superclass Differences:
        -self.messages, the contents of the dictionary are different.
    """

    messages = {0: "Transform function name not in dictionary, unable to map"
                   " transform to transform key. The edge cannot be"
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
                1: "Invalid value for Vertex '_deltaPrevAbs' attribute, unable"
                   " to set '_deltaPrevAbs' to <newDelta>",
                2: "Invalid value for Vertex 'deltaFloat' attribute, unable to"
                   " set 'deltaFloat' to <newDelta>"}


class RetrievalError(GraphError):
    """Exception for attempting to retrieve non-existent data.

    This exception is raised either when a Vertex's 'data' attribute is
    None, or when attempting to retrieve a Vertex by name from a DiGraph,
    and the Vertex isn't present.

    Superclass Differences:
        -self.messages, the contents of the dictionary are different.
    """

    messages = {0: "Vertex data is None. Conventional operations on this data"
                   " are not recommended.",
                1: "Vertex name not present in DiGraph '_vertices' dictionary."
                   " Unable to retrieve vertex."}


def main():
    """Test script for the classes and exceptions in this module.


    """

    bGraph = DiGraph()
    bGraph + Vertex("alpha", 20, deltaInherent=5)
    bGraph["beta"] = Vertex("beta", 13)
    bGraph.add_edge(bGraph["alpha"], bGraph["beta"], "aa_lin", [1])
    print(bGraph["alpha"])
    print(bGraph)
    bGraph + Vertex("gamma", 4, randomFlag=True, randomInfo=(0, 10))
    bGraph.apply_floating_deltas()
    for vert in bGraph:
        print(vert)


if __name__ == '__main__':
    main()
