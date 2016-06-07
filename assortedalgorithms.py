import digraph

__author__ = "Ashleigh"

"""Placeholder Docstring"""


def wyatt_causality_reversal(aGraph, startNodeName, endNodeName):
    emptyPath = []
    edgePath = brute_find_path(aGraph, startNodeName, endNodeName, emptyPath)
    for edge in edgePath:
        edge.change_invert()


def brute_find_path(aGraph, startNodeName, endNodeName, edgePath):
    startNode = aGraph.get_node(startNodeName)
    endNode = aGraph.get_node(endNodeName)

    for edge in startNode.get_all_edges():
        targetNode = edge.get_child_node()
        if targetNode != endNode:
            brute_find_path(aGraph, targetNode, endNode, edgePath)

    edgePath.insert(0, targetNode)
    return edgePath


def basic_breadth_first_search(aGraph, startNodeName, endNodeName):
    edgesOnPath = []
    searchQueue = []
    startNode = aGraph.get_node(startNodeName)
    startNode.set_distance(0)
    startNode.set_colour("grey")
    endNode = aGraph.get_node(endNodeName)
    searchQueue.append(startNode)

    for node in searchQueue:
        for edge in node.get_all_edges():
            targetNode = edge.get_child_node()
            targetNode.set_distance(node.get_distance() + 1)
            targetNode.set_colour("grey")


def basic_depth_first_search(aGraph):
    pass


def count_based_delta_application(aGraph):
    pass


def colour_based_delta_application(aGraph):
    pass


def main():
    aGraph = digraph.DiGraph()
    aGraph.add_node("A")
    aGraph.add_node("B")
    aGraph.add_node("C")
    aGraph.add_node("D")
    aGraph.add_node("E")
    aGraph.add_edge("A", "D", "proportional", ["coefficient"], [2])
    aGraph.add_edge("C", "D", "proportional", ["coefficient"], [2])
    aGraph.add_edge("D", "B", "proportional", ["coefficient"], [2])
    aGraph.add_edge("D", "E", "proportional", ["coefficient"], [2])

    print(aGraph)
    for edge in aGraph.get_all_edges():
        print(edge)
    wyatt_causality_reversal(aGraph, "A", "E")
    print(aGraph)
    for edge in aGraph.get_all_edges():
        print(edge)


if __name__ == '__main__':
    main()
