import edgenode

__author__ = "Ashleigh"

"""Placeholder Docstring"""


class DiGraph:
    def __init__(self):
        self.nodes = []

    def __contains__(self, nodeName):
        for node in self.nodes:
            if node.get_name() == nodeName:
                return True
        return False

    def __str__(self):
        graphDetails = ["This directed graph contains the following Nodes:"]
        for node in self.nodes:
            graphDetails.append(str(node))
        return "\n".join(graphDetails)

    def get_all_nodes(self):
        return self.nodes

    def get_all_edges(self):
        allEdges = []
        for node in self.nodes:
            allEdges.extend(node.get_all_edges())
        return allEdges

    def get_edge(self, parentNodeName, childNodeName):
        parentNode = self.get_node(parentNodeName)
        childNode = self.get_node(childNodeName)
        edge = parentNode.get_edge_by_child(childNode)
        return edge

    def add_edge(self, parentNodeName, childNodeName, transformType, paramNames,
                 paramVals):
        parentNode = self.get_node(parentNodeName)
        childNode = self.get_node(childNodeName)
        parentNode.add_edge(childNode, transformType, paramNames, paramVals)

    def get_node(self, nodeName):
        for node in self.nodes:
            if node.get_name() == nodeName:
                return node

    def add_node(self, name, data=None):
        newNode = edgenode.Node(name, data)
        self.nodes.append(newNode)


def main():
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
