__author__ = "Ashleigh"

"""Placeholder Docstring"""


class Node:
    def __init__(self, name, data=None):
        self.name = name
        self.data = data
        self.edges = []

    def __str__(self):
        nodeDetails = ["Node:", self.name, "has value:", str(self.data), "\n",
                       "and is linked to these nodes:"]
        for edge in self.edges:
            nodeDetails.append(edge.get_child_node().get_name())
        return " ".join(nodeDetails)

    def get_data(self):
        return self.data

    def set_data(self, newData):
        self.data = newData
        return None

    def get_name(self):
        return self.name

    def set_name(self, newName):
        self.name = newName
        return None

    def get_all_edges(self):
        return self.edges

    def get_edge_by_child(self, childNode):
        for edge in self.edges:
            if edge.get_child_node() == childNode:
                return edge
        return None

    def add_edge(self, childNode, transformType, paramNames, paramVals):
        newEdge = TransformEdge(self, childNode, transformType, paramNames,
                                paramVals)
        self.edges.append(newEdge)
        return None


class TransformEdge:
    def __init__(self, parentNode, childNode, transformType, paramNames,
                 paramVals):
        self.parentNode = parentNode
        self.childNode = childNode
        self.transformType = transformType
        self.transformArgNames = paramNames
        self.transformArgs = paramVals

    def __str__(self):
        edgeDetails = ["This is a directed edge between",
                       self.parentNode.get_name(), "and",
                       self.childNode.get_name(), "with transform type:",
                       self.transformType, "\n",
                       "and the following parameters:"]
        for index in range(0, len(self.transformArgNames)):
            edgeDetails.append(str(self.transformArgNames[index]))
            edgeDetails.append(str(self.transformArgs[index]))
        return " ".join(edgeDetails)

    def get_parent_node(self):
        return self.parentNode

    def set_parent_node(self, newParentNode):
        self.parentNode = newParentNode
        return None

    def get_child_node(self):
        return self.childNode

    def set_child_node(self, newChildNode):
        self.childNode = newChildNode
        return None

    def get_transform_type(self):
        return self.transformType

    # def set_transform_type(self, newTransformType, **kwargs):
    #     self.transformType = newTransformType
    #     self.transformArgs = kwargs
    #     return None
    #
    # This class method may not be used. And its class data is horribly
    # out of date.


def main():
    node1 = Node("ONE", 42)
    node2 = Node("TWO", 8)
    node3 = Node("THREE", 50)
    node4 = Node("FOUR", 9)
    node5 = Node("FIVE", 21)

    node1.add_edge(node3, "proportional", ["coefficient"], [1])
    node1.add_edge(node2, "linear", ["gradient", "intercept"], [2,5])
    node1.add_edge(node5, "proportional", ["coefficient"], [2])
    node2.add_edge(node4, "proportional", ["coefficient"], [1])
    node2.add_edge(node5, "polynomial", ["first coefficient", "first power"],
                   [3,2])
    node3.add_edge(node2, "proportional", ["coefficient"], [4])
    node4.add_edge(node1, "proportional", ["coefficient"], [1])
    node5.add_edge(node4, "proportional", ["coefficient"], [6])

    for edge in node1.get_all_edges():
        print(edge)
    for edge in node2.get_all_edges():
        print(edge)
    for edge in node3.get_all_edges():
        print(edge)
    for edge in node4.get_all_edges():
        print(edge)
    for edge in node5.get_all_edges():
        print(edge)

    print(node1) # Expected links: THREE, TWO, and FIVE
    print(node2) # Expected links: FOUR and FIVE
    print(node3) # Expected links: TWO
    print(node4) # Expected links: ONE
    print(node5) # Expected links: FOUR


if __name__ == '__main__':
    main()
