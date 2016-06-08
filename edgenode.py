import sys

__author__ = "Ashleigh"

"""Placeholder Docstring"""


class Node:
    def __init__(self, name, data=None):
        self.name = name
        self.data = data
        self.edges = []
        self.colour = "white"
        self.distance = sys.maxsize
        self.searchedEdge = None

    def __str__(self):
        nodeDetails = ["Node:", self.name, "has value:", str(self.data), "\n",
                       "and is linked to these nodes:"]
        for edge in self.edges:
            nodeDetails.append(edge.get_child_node().get_name())
        return " ".join(nodeDetails)

    def __contains__(self, item):
        pass

    def __eq__(self, other):
        if self.name == other.get_name():
            return True
        else:
            return False

    def get_data(self):
        return self.data

    def set_data(self, newData):
        self.data = newData

    def get_name(self):
        return self.name

    def set_name(self, newName):
        self.name = newName

    def get_all_edges(self):
        return self.edges

    def get_edge_by_child(self, childNode):
        for edge in self.edges:
            if edge.get_child_node() == childNode:
                return edge

    def add_edge(self, childNode, transformType, paramNames, paramVals):
        newEdge = TransformEdge(self, childNode, transformType, paramNames,
                                paramVals)
        self.edges.append(newEdge)

    def add_existing_edge(self, edge):
        self.edges.append(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)

    def get_colour(self):
        return self.colour

    def set_colour(self, newColour):
        self.colour = newColour

    def get_distance(self):
        return self.distance

    def set_distance(self, newDistance):
        self.distance = newDistance

    def get_searched_edge(self):
        return self.searchedEdge

    def set_searched_edge(self, searchedEdge):
        self.searchedEdge = searchedEdge


class TransformEdge:
    """Edges with support for transformative functions.

    Currently, linear, proportional, and polynomial transformation
    functions are supported, as well as combinations of any two of
    these functions. Transformative functions are called as part of the
    graph's role as a basis for an economic simulation.
    """

    def __init__(self, parentNode, childNode, transformType, paramNames,
                 paramVals):
        self.parentNode = parentNode
        self.childNode = childNode
        self.transformType = transformType
        self.transformArgNames = paramNames
        self.transformArgs = paramVals
        self.invertedFlag = False
        self.negatedFlag = False

    def __str__(self):
        edgeDetails = ["This is a directed edge between",
                       self.parentNode.get_name(), "and",
                       self.childNode.get_name(), "with transform type:",
                       self.transformType, "\n",
                       "and the following parameters:"]
        for index in range(0, len(self.transformArgNames)):
            edgeDetails.append(str(self.transformArgNames[index]))
            edgeDetails.append(str(self.transformArgs[index]))
        if self.invertedFlag:
            edgeDetails.extend(["\n", "The edge transform function has been "
                                      "inverted as part of causality reversal"])
        return " ".join(edgeDetails)

    def __eq__(self, other):
        if other is None:
            return False
        elif (self.parentNode == other.get_parent_node() and self.childNode ==
              other.get_child_node()):
            return True
        else:
            return False

    def __mul__(self, other):
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
                self.transformType = "fuckifiknow"
                # figure it out on a whiteboard
            elif other.get_transform_type() == "polynomial":
                self.transformType = "fuckifiknow"
                # figure it out on a whiteboard
        elif self.transformType == "polynomial":
            if other.get_transform_type() == "proportional":
                self.transformType = "polynomial"
                # multiply all coefficients by proportional coefficient
            elif other.get_transform_type() == "linear":
                self.transformType = "fuckifiknow"
                # figure it out on a whiteboard
            elif other.get_transform_type() == "polynomial":
                self.transformType = "polynomial"  # implement FOIL
        return self

    # def __imul__(self, other):
    #     self.transformType = self * other
    #     return self

    def reverse(self):
        tempParent = self.parentNode
        tempChild = self.childNode
        self.parentNode = tempChild
        self.childNode = tempParent
        self.childNode.remove_edge(self)
        self.parentNode.add_existing_edge(self)

    def get_parent_node(self):
        return self.parentNode

    def set_parent_node(self, newParentNode):
        self.parentNode = newParentNode

    def get_child_node(self):
        return self.childNode

    def set_child_node(self, newChildNode):
        self.childNode = newChildNode

    def get_transform_type(self):
        return self.transformType

    def check_invert(self):
        return self.invertedFlag

    def change_invert(self):
        self.invertedFlag = not self.invertedFlag

    def check_negation(self):
        return self.negatedFlag

    def change_negation(self):
        self.negatedFlag = not self.negatedFlag


def main():
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
