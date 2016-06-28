import sys

import timetransforms
import transformfunctions

__author__ = "Ashleigh"

"""Contains the Node and TransformEdge classes for a graph.

Classes:
    - Node: serves as a vertex within a directed graph.
    - TransformEdge: represents the directed edges within the graph.
      Additionally, the edges also contain references to assorted types
      of transformative functions, used when the graph is part of an
      economic simulation.
"""


class Node:
    """The Node class, intended to be used as a vertex in a graph.

    The instance variables for the Node class are as follows:
        - name, the Node's name.
        - data, the data contained within the Node.
        - edges, a list of edges that have the Node as a parent.
        - colour, the colour of the Node, to be used by traversal
          algorithms.
        - distance, the distance from a start Node, referenced in
          some traversals.
        - searchedEdge, the edge that linked to this Node from a
          predecessor in a traversal or pathfinding operation.
        - discoveredTime, used in depth-first traversals.
        - finishedTime, used in depth-first traversals.
        - deltaPrev, used as part of economic simulations.
        - deltaNew, used as part of economic simulations.

    The public methods for the Node class are as follows:
        - apply_new_delta(self)
        - reset_traversal_data(self)
        - get_data(self)
        - set_data(self, newData)
        - get_name(self)
        - set_name(self, newName)
        - get_all_edges(self)
        - get_edge_by_child(self, childNode)
        - add_edge(self, childNode, transformType, paramNames, paramVals)
        - add_existing_edge(self, edge)
        - remove_edge(self, edge)
        - get_colour(self)
        - set_colour(self, newColour)
        - get_distance(self)
        - set_distance(self, newDistance)
        - get_searched_edge(self)
        - set_searched_edge(self, searchedEdge)
        - get_discovered_time(self)
        - set_discovered_time(self, newTime)
        - get_finished_time(self)
        - set_finished_time(self, newTime)
        - get_delta_prev(self)
        - set_delta_prev(self, newDelta)
        - get_delta_new(self)
        - set_delta_new(self, newDelta)
    """

    def __init__(self, name, data=None):
        """Initializes Node class based on name and optional data."""
        self.name = name
        self.data = data
        self.edges = []
        self.colour = "white"
        self.distance = sys.maxsize
        self.searchedEdge = None
        self.discoveredTime = 0
        self.finishedTime = 0
        self.deltaPrev = 0
        self.deltaNew = 0

    def __str__(self):
        """Returns a formatted string summarizing the Node.

        The summary always has the Node's name, the data it contains,
        its colour, and the names of all of its child Nodes. When
        relevant, the string will also contain the name of the parent
        Node that linked to it in a traversal, the distance from a
        starting Node in a traversal, and/or the time counts on which
        the Node was discovered and fully explored as part of a depth-
        first traversal.
        """

        nodeDetails = ["Node:", self.name, "has value:", str(self.data),
                       "has colour:", self.colour]
        if self.searchedEdge is not None:
            nodeDetails.extend(["was linked to by: \n",
                                self.searchedEdge.get_parent_node().get_name()])
        if self.colour != "white":
            nodeDetails.extend(["and distance:", str(self.distance)])
        if self.discoveredTime != 0 or self.finishedTime != 0:
            nodeDetails.extend(["\n", "node discovered on:",
                                str(self.discoveredTime),
                                "and fully explored on:",
                                str(self.finishedTime)])
        nodeDetails.extend(["\n", "and is linked to these nodes:"])
        for edge in self.edges:
            nodeDetails.append(edge.get_child_node().get_name())
        return " ".join(nodeDetails)

    def __eq__(self, other):
        """Tests equality based on the name of the Nodes."""
        if self.name == other.get_name():
            return True
        else:
            return False

    def apply_new_delta(self):
        """Adds the value of delta to the Node's data."""
        self.data += self.deltaNew
        self.deltaPrev = self.deltaNew
        self.deltaNew = 0

    def reset_traversal_data(self):
        """Resets traversal data to default values.

        These default data values are the same as the initial values
        that the class data is set to when a Node is instantiated.
        """

        self.colour = "white"
        self.distance = sys.maxsize
        self.searchedEdge = None
        self.discoveredTime = 0
        self.finishedTime = 0

    def get_data(self):
        """Returns the Node's data."""
        return self.data

    def set_data(self, newData):
        """Changes the Node's data to newData."""
        self.data = newData

    def get_name(self):
        """Returns the Node's name."""
        return self.name

    def set_name(self, newName):
        """Changes the Node's name to newName."""
        self.name = newName

    def get_all_edges(self):
        """Returns all TransformEdges parented by the Node.

        Parenting of an edge is defined as being listed as the
        parentNode of a given TransformEdge in its class data.
        """

        return self.edges

    def get_edge_by_child(self, childNode):
        """Returns a parented TransformEdge based on its child.

        All TransformEdge instances of which the Node is a parent are
        checked against the childNode passed in. If the TransformEdge
        has that Node as a child, it is returned.
        """

        for edge in self.edges:
            if edge.get_child_node() == childNode:
                return edge

    def add_edge(self, childNode, transformType, paramNames, paramVals):
        """Adds and initializes a new TransformEdge between two Nodes."""
        newEdge = TransformEdge(self, childNode, transformType, paramNames,
                                paramVals)
        self.edges.append(newEdge)

    def add_existing_edge(self, edge):
        """Changes the parent of a TransformEdge to the current Node.

        This does not also remove the TransformEdge from the previous
        parent's edge list. The remove_edge(edge) method must also be
        called on the previous parent.
        """

        self.edges.append(edge)

    def remove_edge(self, edge):
        """Removes instance of TransformEdge from edge list."""
        self.edges.remove(edge)
        del edge

    def get_colour(self):
        """Returns the Node's colour."""
        return self.colour

    def set_colour(self, newColour):
        """Changes the Node's colour to newColour"""
        self.colour = newColour

    def get_distance(self):
        """Returns the Node's distance from a start Node in a graph.

        This distance is set as part of a breadth-first traversal, when
        the Node is first discovered.
        """

        return self.distance

    def set_distance(self, newDistance):
        """Changes the Node's distance to newDistance.

        This is used in breadth-first traversals, and is based on the
        Node's distance from a start Node in the graph being traversed.
        """

        self.distance = newDistance

    def get_searched_edge(self):
        """Returns the edge searched to reach the Node."""
        return self.searchedEdge

    def set_searched_edge(self, newSearchedEdge):
        """Changes the Node's searchedEdge to newSearchedEdge."""
        self.searchedEdge = newSearchedEdge

    def get_discovered_time(self):
        """Returns the time at which the Node was discovered."""
        return self.discoveredTime

    def set_discovered_time(self, newTime):
        """Changes the Node's discoveredTime to newTime."""
        self.discoveredTime = newTime

    def get_finished_time(self):
        """Returns the Node's finishedTime.

        The finishedTime is the time at which the node was returned to
        during a depth-first traversal, indicating that it was fully
        explored.
        """

        return self.finishedTime

    def set_finished_time(self, newTime):
        """Changes finishedTime to newTime."""

        self.finishedTime = newTime

    def get_delta_prev(self):
        """Returns the value of deltaPrev."""
        return self.deltaPrev

    def set_delta_prev(self, newDelta):
        """Sets the value of deltaPrev to newDelta."""
        self.deltaPrev = newDelta

    def get_delta_new(self):
        """Returns the value of deltaNew."""
        return self.deltaNew

    def set_delta_new(self, newDelta):
        """Sets the value of deltaNew to newDelta."""
        self.deltaNew = newDelta

    def add_to_delta_new(self, moreDelta):
        """Adds moreDelta to deltaNew."""
        self.deltaNew += moreDelta


class TransformEdge:
    """Edges with support for transformative functions.

    Currently, linear, proportional, and polynomial transformation
    functions are supported, as well as combinations of any two of
    these functions. Transformative functions are called as part of the
    graph's role as a basis for an economic simulation.

    The instance variables for the TransformEdge class are as follows:
        - parentNode, the Node that is the source of the directed edge.
        - childNode, the Node that is the target of the directed edge.
        - transformType, a string describing the transformative
          function that the TransformEdge instance helps represent.
        - targNames, the names of the parameters for the
          TransformEdge's transformative function.
        - targs, the parameters of the transformative function
          linked to the TransformEdge instance.
        - invertedFlag, a flag indicating that the output from the
          TransformEdge's transformative function should be inverted
        - negatedFlag, a flag indicating that the output from the
          TransformEdge's transformative function should be negated.

    The public methods for the TransformEdge class are as follows:
        - reverse(self)
        - transform(self)
        - get_parent_node(self)
        - set_parent_node(self, newParentNode)
        - get_child_node(self)
        - set_child_node(self, newChildNode)
        - get_transform_type(self)
        - check_invert(self)
        - change_invert(self)
        - check_negation(self)
        - change_negation(self)
    """

    def __init__(self, parentNode, childNode, transformType, paramNames,
                 paramVals):
        """Initializes TransformEdge class based on required variables."""
        self.parentNode = parentNode
        self.childNode = childNode
        self.transformType = transformType
        self.targNames = paramNames
        self.targs = paramVals
        self.invertedFlag = False
        self.negatedFlag = False

    def __str__(self):
        """Returns a formatted string summarizing the TransformEdge.

        The string references the parent and child Nodes of the
        TransformEdge, the type of transformative function associated
        with the TransformEdge, the parameters of the transformative
        function, and, if relevant, whether the function has been
        inverted during a causality reversal operation.
        """

        edgeDetails = ["This is a directed edge between",
                       self.parentNode.get_name(), "and",
                       self.childNode.get_name(), "with transform type:",
                       self.transformType, "\n",
                       "and the following parameters:"]
        for index in range(0, len(self.targNames)):
            edgeDetails.append(str(self.targNames[index]))
            edgeDetails.append(str(self.targs[index]))
        if self.invertedFlag:
            edgeDetails.extend(["\n", "The edge transform function has been "
                                      "inverted as part of causality reversal"])
        return " ".join(edgeDetails)

    def __eq__(self, other):
        """Tests equality based on parent and child Nodes.

        The equality test verifies that the parent and child Nodes of
        two TransformEdges are identical.
        """

        if other is None:
            return False
        elif (self.parentNode == other.get_parent_node() and self.childNode ==
              other.get_child_node()):
            return True
        else:
            return False

    def __mul__(self, other):
        """Combines the transformative functions of two TransformEdges.

        The function type is changed to whatever the combination of the
        transformative functions of the two TransformEdges would be.
        Additionally, a new parameter list is calculated and applied.
        """

        if self.transformType == "proportional":
            if other.get_transform_type() == "proportional":
                self.transformType = "proportional"  # coefficients multiply
            elif other.get_transform_type() == "linear":
                self.transformType = "linear"
                # multiply gradient and intercept by coefficient
            elif other.get_transform_type() == "polynomial":
                self.transformType = "polynomial"
                # multiply all coefficients by proportional coefficient
        elif self.transformType == "linear":
            if other.get_transform_type() == "proportional":
                self.transformType = "linear"
                # multiply gradient and intercept by coefficient
            elif other.get_transform_type() == "linear":
                self.transformType = "polynomial"
                # figure it out on a whiteboard
            elif other.get_transform_type() == "polynomial":
                self.transformType = "polynomial"
                # figure it out on a whiteboard
        elif self.transformType == "polynomial":
            if other.get_transform_type() == "proportional":
                self.transformType = "polynomial"
                # multiply all coefficients by proportional coefficient
            elif other.get_transform_type() == "linear":
                self.transformType = "polynomial"
                # figure it out on a whiteboard
            elif other.get_transform_type() == "polynomial":
                self.transformType = "polynomial"  # implement FOIL
        return self

    def reverse(self):
        """Reverses the direction of a TransformEdge.

        The parent and child Nodes of the TransformEdge are switched,
        and then the edge is removed from the edge list of the previous
        parent Node, and added to the edge list of the new parent Node.
        """

        tempParent = self.parentNode
        tempChild = self.childNode
        self.parentNode = tempChild
        self.childNode = tempParent
        self.childNode.remove_edge(self)
        self.parentNode.add_existing_edge(self)

    def transform(self, currentCount=None):
        """Selects and applies a transformative function.

        The selection of the transformative functions is based on
        matching the transformType to a set of predefined functions
        and then passing in the arguments that are part of the
        TransformEdge's class data.
        """

        if self.transformType == "proportional":
            prevDelta = self.parentNode.get_delta_prev()
            calcDelta = transformfunctions.proportional_transform(prevDelta,
                                                                  self.targs)
            self.childNode.add_to_delta_new(calcDelta)
        elif self.transformType == "linear":
            prevDelta = self.parentNode.get_delta_prev()
            calcDelta = transformfunctions.linear_transform(prevDelta,
                                                            self.targs)
            self.childNode.add_to_delta_new(calcDelta)
        elif self.transformType == "polynomial":
            prevDelta = self.parentNode.get_delta_prev()
            calcDelta = transformfunctions.polynomial_transform(prevDelta,
                                                                self.targs)
            self.childNode.add_to_delta_new(calcDelta)
        elif self.transformType == "propcount":
            prevDelta = self.parentNode.get_delta_prev()
            calcDelta = timetransforms.proportional_count_linear(prevDelta,
                                                                 self.targs,
                                                                 currentCount)
            self.childNode.add_to_delta_new(calcDelta)

    def get_parent_node(self):
        """Returns a reference to the parent Node."""
        return self.parentNode

    def set_parent_node(self, newParentNode):
        """Sets the parent Node to newParentNode."""
        self.parentNode = newParentNode

    def get_child_node(self):
        """Returns a reference to the child Node."""
        return self.childNode

    def set_child_node(self, newChildNode):
        """Sets the child Node to newChildNode."""
        self.childNode = newChildNode

    def get_transform_type(self):
        """Returns a reference to the name of the transform type."""
        return self.transformType

    def check_invert(self):
        """Returns the Boolean value associated with the invertedFlag.

        If the transformative function has been inverted, invertedFlag
        will be true, and the method will return True. If the function
        has not been inverted, the function will return False.
        """

        return self.invertedFlag

    def change_invert(self):
        """Switches the Boolean value of invertedFlag."""
        self.invertedFlag = not self.invertedFlag

    def check_negation(self):
        """Returns the Boolean value associated with the negatedFlag."""
        return self.negatedFlag

    def change_negation(self):
        """Switches the Boolean value of negatedFlag."""
        self.negatedFlag = not self.negatedFlag


def main():
    """Test script for the Node and TransformEdge classes.

    Five Nodes are instantiated, and TransformEdges between them are
    generated, with an assortment of transformative functions assigned
    to the TransformEdges. After this, all TransformEdges and all Nodes
    are printed to the screen, completing the test script.
    """

    node1 = Node("ONE", 42)
    node2 = Node("TWO", 8)
    node3 = Node("THREE", 50)
    node4 = Node("FOUR", 9)
    node5 = Node("FIVE", 21)

    node1.add_edge(node3, "proportional", ["coefficient"], [1])
    node1.add_edge(node2, "linear", ["gradient", "intercept"], [2, 5])
    node1.add_edge(node5, "proportional", ["coefficient"], [2])
    node2.add_edge(node4, "proportional", ["coefficient"], [1])
    node2.add_edge(node5, "polynomial", ["first coefficient", "first power"],
                   [3, 2])
    node3.add_edge(node2, "proportional", ["coefficient"], [4])
    node4.add_edge(node1, "proportional", ["coefficient"], [1])
    node5.add_edge(node4, "proportional", ["coefficient"], [6])

    print(type(node1))
    print(type(node2))
    print(type(node3))
    print(type(node4))
    print(type(node5))

    for edge in node1.get_all_edges():
        print(edge)
        print(edge.check_invert())
        print(edge.check_negation())
        edge.change_invert()
        edge.change_negation()
        print(edge.check_invert())
        print(edge.check_negation())
    for edge in node2.get_all_edges():
        print(edge)
        print(edge.check_invert())
        print(edge.check_negation())
        edge.change_invert()
        edge.change_negation()
        print(edge.check_invert())
        print(edge.check_negation())
    for edge in node3.get_all_edges():
        print(edge)
        print(edge.check_invert())
        print(edge.check_negation())
        edge.change_invert()
        edge.change_negation()
        print(edge.check_invert())
        print(edge.check_negation())
    for edge in node4.get_all_edges():
        print(edge)
        print(edge.check_invert())
        print(edge.check_negation())
        edge.change_invert()
        edge.change_negation()
        print(edge.check_invert())
        print(edge.check_negation())
    for edge in node5.get_all_edges():
        print(edge)
        print(edge.check_invert())
        print(edge.check_negation())
        edge.change_invert()
        edge.change_negation()
        print(edge.check_invert())
        print(edge.check_negation())

    print(node1)  # Expected links: THREE, TWO, and FIVE
    print(node2)  # Expected links: FOUR and FIVE
    print(node3)  # Expected links: TWO
    print(node4)  # Expected links: ONE
    print(node5)  # Expected links: FOUR


if __name__ == '__main__':
    main()
