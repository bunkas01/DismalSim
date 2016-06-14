import sys

import edgenode

__author__ = "Ashleigh"

"""Contains the implementation of a directed graph.

Classes:
    - DiGraph: a basic directed graph.
"""


class DiGraph:
    """The DiGraph class, a directed graph intended for ecconomic sims.

    The DiGraph class functions primarily as a container for Nodes.
    Most of the class methods for the DiGraph are just wrappers around
    the equivalent methods of the Node or TransformEdge classes.
    Additionally, the DiGraph usually takes the name of any relevant
    Nodes, and looks up the Nodes in its list of Nodes, rather than
    take direct references to Nodes.

    The instance variables for the DiGraph class are as follows:
        - nodes, a list of nodes within the graph.
        - maxDistance, the maximum distance reached in a breadth-first
          traversal of the graph.

    The public methods for the DiGraph Class are as follows:
        - get_all_nodes(self)
        - get_all_edges(self)
        - get_edge(self, parentNodeName, childNodeName)
        - add_edge(self, parentNodeName, childNodeName, transformType,
                   paramNames, paramVals)
        - get_node(self, nodeName)
        - add_node(self, name, data=None)
        - get_max_distance(self)
        - set_max_distance(self, newDistance)
        - apply_all_new_deltas(self)
    """

    def __init__(self):
        """Initializes an empty DiGraph."""
        self.nodes = []
        self.maxDistance = sys.maxsize

    def __contains__(self, nodeName):
        """Determines if the graph contains a given named Node."""
        for node in self.nodes:
            if node.get_name() == nodeName:
                return True
        return False

    def __str__(self):
        """Returns a formatted string containing the Node strings.

        Effectively, the DiGraph's string method just packages the
        strings for all of its Nodes together.
        """

        graphDetails = ["This directed graph contains the following Nodes:"]
        for node in self.nodes:
            graphDetails.append(str(node))
        return "\n".join(graphDetails)

    def get_all_nodes(self):
        """Returns the DiGraph's Node list."""
        return self.nodes

    def get_all_edges(self):
        """Returns all TransformEdges possessed by all Nodes.

        Every Node in the graph is searched for TransformEdges, and
        those are then added to the list of all TransformEdges that the
        DiGraph possesses. That list is then returned.
        """

        allEdges = []
        for node in self.nodes:
            allEdges.extend(node.get_all_edges())
        return allEdges

    def get_edge(self, parentNodeName, childNodeName):
        """Returns a TransformEdge based on its parent and child Nodes."""
        parentNode = self.get_node(parentNodeName)
        childNode = self.get_node(childNodeName)
        edge = parentNode.get_edge_by_child(childNode)
        return edge

    def add_edge(self, parentNodeName, childNodeName, transformType, paramNames,
                 paramVals):
        """Initializes a TransformEdge between two Nodes."""
        parentNode = self.get_node(parentNodeName)
        childNode = self.get_node(childNodeName)
        parentNode.add_edge(childNode, transformType, paramNames, paramVals)

    def get_node(self, nodeName):
        """Returns a Node in the graph, based on its name."""
        for node in self.nodes:
            if node.get_name() == nodeName:
                return node

    def add_node(self, name, data=None):
        """Initializes a Node, and adds it to the graph."""
        newNode = edgenode.Node(name, data)
        self.nodes.append(newNode)

    def get_max_distance(self):
        """Returns the maximum distance of the graph.

        The maximum distance is the maximum number of connections
        taken to reach all Nodes in the DiGraph from a given start Node
        during a breadth-first traversal.
        """

        return self.maxDistance

    def set_max_distance(self, newDistance):
        """Changes the graph's maxDistance to newDistance."""
        self.maxDistance = newDistance

    def apply_all_new_deltas(self):
        """Applies the deltaNew of every Node in the graph to itself."""
        for node in self.nodes:
            node.apply_new_delta()


def main():
    """Test Script for the DiGraph class.

    A DiGraph is instantiated, and five nodes, creatively named by the
    order of their creation, are added to the graph. Each node contains
    an integer as data. Eight TransformEdges are added between Nodes,
    with an assortment of transformative functions assigned to them. To
    complete the test, the DiGraph is printed to the screen.
    """

    aGraph = DiGraph()
    aGraph.add_node("ONE", 42)
    aGraph.add_node("TWO", 8)
    aGraph.add_node("THREE", 50)
    aGraph.add_node("FOUR", 9)
    aGraph.add_node("FIVE", 21)

    aGraph.add_edge("ONE", "THREE", "proportional", ["coefficient"], [1])
    aGraph.add_edge("ONE", "TWO", "linear", ["gradient", "intercept"], [2,5])
    aGraph.add_edge("ONE", "FIVE", "proportional", ["coefficient"], [2])
    aGraph.add_edge("TWO", "FOUR", "proportional", ["coefficient"], [1])
    aGraph.add_edge("TWO", "FIVE", "polynomial", ["first coefficient",
                    "first power"], [3, 2])
    aGraph.add_edge("THREE", "TWO", "proportional", ["coefficient"], [4])
    aGraph.add_edge("FOUR", "ONE", "proportional", ["coefficient"], [1])
    aGraph.add_edge("FIVE", "FOUR", "proportional", ["coefficient"], [6])

    print(aGraph)


if __name__ == '__main__':
    main()
