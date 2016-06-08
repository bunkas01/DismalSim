import digraph

__author__ = "Ashleigh"

"""Placeholder Docstring"""


def wyatt_causality_reversal(aGraph, startNodeName, endNodeName):
    """Reverses causality between two nodes, and modifies graph in place"""
    emptyPath = []
    startNode = aGraph.get_node(startNodeName)
    endNode = aGraph.get_node(endNodeName)
    edgePath = brute_find_path(aGraph, startNode, endNode, emptyPath)
    nodePath = find_node_path(edgePath)
    for edge in edgePath:
        edge.reverse()
        edge.change_invert()
    adjust_converging_edges(aGraph, edgePath, nodePath)



def find_node_path(edgePath):
    """helper function for wyatt_causality_reversal()"""

    nodePath = []
    nodePath.append(edgePath[0].get_parent_node())
    for edge in edgePath:
        nodePath.append(edge.get_child_node())
    return nodePath


def adjust_converging_edges(aGraph, edgePath, nodePath):
    """Helper function for wyatt_causality_reversal()"""

    allEdges = aGraph.get_all_edges()
    for edge in allEdges:
        if edge not in edgePath and edge.get_child_node() in nodePath:
            oldChild = edge.get_child_node()
            newChildIndex = nodePath.index(oldChild) - 1
            if newChildIndex >= 0:
                edge.set_child_node(nodePath[newChildIndex])
                edge.change_negation()
                edge *= oldChild.get_edge_by_child(nodePath[newChildIndex])


def brute_find_path(aGraph, startNode, endNode, edgePath):
    """Helper function for wyatt_causality_reversal()"""

    for edge in startNode.get_all_edges():
        targetNode = edge.get_child_node()
        targetNode.set_searched_edge(edge)
        if targetNode != endNode:
            brute_find_path(aGraph, targetNode, endNode, edgePath)
        elif targetNode == endNode:
            edgePath.insert(0, edge)
            for pathEdge in reversed(edgePath):
                if pathEdge.get_parent_node().get_searched_edge() != None:
                    nextEdge = pathEdge.get_parent_node().get_searched_edge()
                    edgePath.insert(0, nextEdge)
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
